import logging
import os

import requests
import datetime
from connector.utils import ConnectorWrapper
from lead.models import Lead
from unified_connector.sources.base import Source

from deep import settings
from io import BytesIO
from django.template.loader import render_to_string
from weasyprint import HTML

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)


@ConnectorWrapper
class Kobo(Source):

    URL = 'https://kf.kobotoolbox.org/api/v2/assets/'
    title = 'KoboToolbox Reports'
    key = 'kobo-toolbox'

    options = [
        {
            'key': 'project_id',
            'field_type': 'text',
            'title': 'Project ID',
        },
        {
            'key': 'token',
            'field_type': 'text',
            'title': 'Kobo API Token',
        }
    ]

    def get_content(self, project_id, token):
        api_url = f"{self.URL}{project_id}/data/?format=json"
        headers = {"Authorization": f"Token {token}"}

        try:
            with requests.get(api_url, headers=headers, stream=True) as response:
                if response.status_code == 200:
                    return response.json().get('results', [])
                else:
                    logger.error("Failed to fetch data from API, Status code: %d", response.status_code)
        except requests.RequestException as e:
            logger.critical("A critical error occurred while fetching data: %s", e)
        return []

    def fetch(self, params):
        logger.info(f'fetching for kobo commenced with params {params}')
        result = []
        project_id = params.get('project_id')
        if not project_id:
            return [], 0

        token = params.get('token')
        if not token:
            return [], 0


        try:
            records = self.get_content(project_id, token)
            if records:

                qualitative_columns, rows = accumulate_columns_and_rows(records)
                context = {
                    'columns': qualitative_columns,
                    'rows': rows,
                }

                html_string = render_to_string('connector/pdf.html', context)

                html = HTML(string=html_string)
                pdf_file = html.write_pdf()

                pdf_stream = BytesIO(pdf_file)

                file_path = pdf_save_path_and_url(project_id, context, pdf_file=pdf_stream)
                print(f'the media url is {settings.MEDIA_URL} and the media files location is {settings.MEDIAFILES_LOCATION}')
                file_url = os.path.join(settings.MEDIA_URL, file_path)

                date = datetime.now()
                result = [{
                     'title': project_id,
                     'url': file_url,
                     'source': 'KoboToolbox',
                     'author': 'KoboToolbox',
                     'published_on': date.date(),
                     'source_type': Lead.SourceType.WEBSITE}
                ]

                logger.info(f'the resulted data of kobo is: {result}')
            return result, len(result)
        except Exception as e:
            logger.error("An error occurred: %s", e)
            return [], 0



def pdf_save_path_and_url(project_id, context, pdf_file):
    project_id = project_id
    timestamp = datetime.now().strftime('%Y%m%dT%H%M%S')
    import uuid, csv
    directory_path = os.path.join(
        str(project_id),
        str(timestamp),
    )
    pdf_directory_path = os.path.join("pdf", directory_path)
    os.makedirs(directory_path, exist_ok=True)
    file_id = uuid.uuid4()
    pdf_file_path = os.path.join(pdf_directory_path, f"{file_id}.pdf")
    def save_pdf():
        file_path = os.path.join(settings.MEDIAFILES_LOCATION, pdf_directory_path, f"{file_id}.pdf")
        default_storage.save(file_path, ContentFile(pdf_file.getvalue()))
    save_pdf()

    csv_directory_path = os.path.join(settings.MEDIAFILES_LOCATION, "csv", directory_path)
    csv_file_path = os.path.join(csv_directory_path, f"{file_id}.csv")

    def save_csv():
        import io
        csv_buffer = io.StringIO()

        writer = csv.writer(csv_buffer)
        writer.writerow(context['columns'])
        for row in context['rows']:
            writer.writerow(row)

        csv_content = ContentFile(csv_buffer.getvalue().encode('utf-8'))
        default_storage.save(csv_file_path, csv_content)

    save_csv()

    return pdf_file_path


def accumulate_columns_and_rows(records):
    """Accumulate all columns from the records and filter qualitative columns."""
    all_columns_set = set()
    rows = []

    # Accumulate all unique columns across all records
    for record in records:
        all_columns_set.update(record.keys())

    all_columns = sorted(all_columns_set)

    # Filter qualitative columns based on values across all records
    qualitative_columns = []
    for col in all_columns:
        if all(is_qualitative(col, record.get(col, "N/A")) for record in records):
            qualitative_columns.append(col)

    # Build rows with qualitative data
    for record in records:
        row = [record.get(column, "N/A") for column in qualitative_columns]
        rows.append(row)

    return qualitative_columns, rows


import re
from datetime import datetime

BOOLEAN_TRUE_VALUES = {'true', 'yes', '1', 'on'}
BOOLEAN_FALSE_VALUES = {'false', 'no', '0', 'off'}


def is_uuid(value):
    """Check if a string is a valid UUID."""
    uuid_pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$', re.IGNORECASE)
    return bool(uuid_pattern.match(value))


def is_id_field(key, value):
    """Check if a field is likely to be an ID field."""
    if isinstance(key, str):
        # Check if the key contains 'id' or 'uuid'
        if 'id' in key.lower() or 'uuid' in key.lower():
            return True

    # Check if the value is a UUID
    if isinstance(value, str) and is_uuid(value):
        return True

    # Check if it's a numeric ID
    if isinstance(value, (int, str)):
        try:
            int(value)
            return len(str(value)) > 5  # Assume IDs are typically longer than 5 digits
        except ValueError:
            pass

    return False


def is_date(value):
    """Check if a string is a valid date."""
    try:
        datetime.fromisoformat(value.replace('Z', '+00:00'))
        return True
    except (ValueError, AttributeError):
        return False


def is_boolean(value):
    """Check if the value represents a boolean."""
    if isinstance(value, bool):
        return True  # Already a boolean

    if isinstance(value, str):
        normalized_value = value.strip().lower()
        if normalized_value in BOOLEAN_TRUE_VALUES or normalized_value in BOOLEAN_FALSE_VALUES:
            return True

    return False


def is_qualitative(key, value):
    """
    Helper function to determine if a value is qualitative based on its key, type, and content.
    """

    # Check if it's an ID field
    if isinstance(value, (dict, list)):
        return True

    if is_id_field(key, value):
        return False

    # Check if it's a boolean
    if is_boolean(value):
        return False

    if isinstance(value, str):
        # Check if it's a number or date disguised as a string
        try:
            float(value)
            return False  # It's a number
        except ValueError:
            if is_date(value):
                return False  # It's a date
            return True  # It's a regular string, consider it qualitative

    if isinstance(value, (int, float)):
        return False  # Numbers are quantitative

    # Consider everything else as qualitative
    return True