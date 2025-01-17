"""deep URL Configuration
"""
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic.base import RedirectView
from django.conf.urls import include, static
from django.views.static import serve
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf import settings
from django.urls import path, register_converter, re_path
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django_otp.admin import OTPAdminSite

from . import converters


from user.views import (
    UserViewSet,
    PasswordResetView,
    user_activate_confirm,
    unsubscribe_email,
)
from gallery.views import (
    PrivateAttachmentFileView,
    FileView,
    FileViewSet,
    GoogleDriveFileViewSet,
    DropboxFileViewSet,
    FilePreviewViewSet,
    FileExtractionTriggerView,
    MetaExtractionView,
    PrivateFileView,
    DeprecatedPrivateFileView,
    PublicFileView,
)
from tabular.views import (
    BookViewSet,
    SheetViewSet,
    FieldViewSet,
    GeodataViewSet,
    TabularExtractionTriggerView,
    TabularGeoProcessTriggerView,
)
from user_group.views import (
    GroupMembershipViewSet,
    UserGroupViewSet,
)
from project.views import (
    ProjectMembershipViewSet,
    ProjectUserGroupViewSet,
    ProjectOptionsView,
    ProjectRoleViewSet,
    ProjectViewSet,
    ProjectStatViewSet,
    accept_project_confirm,
)
from geo.views import (
    AdminLevelViewSet,
    RegionCloneView,
    RegionViewSet,
    GeoAreasLoadTriggerView,
    GeoJsonView,
    GeoBoundsView,
    GeoOptionsView,
    GeoAreaView
)
from questionnaire.views import (
    QuestionnaireViewSet,
    QuestionViewSet,
    FrameworkQuestionViewSet,
    XFormView,
    KoboToolboxExport,
)
from lead.views import (
    LeadGroupViewSet,
    LeadViewSet,
    LeadBulkDeleteViewSet,
    LeadPreviewViewSet,
    LeadOptionsView,
    LeadExtractionTriggerView,
    LeadWebsiteFetch,
    LeadCopyView,

    WebInfoExtractView,
    WebInfoDataView,
)
from entry.views import (
    EntryViewSet,
    AttributeViewSet,
    FilterDataViewSet,
    EntryFilterView,
    ExportDataViewSet,
    EntryOptionsView,
    EditEntriesDataViewSet,
    EntryCommentViewSet,
    # Entry Grouping
    ProjectEntryLabelViewSet,
    LeadEntryGroupViewSet,
)
from analysis.views import (
    AnalysisViewSet,
    AnalysisPillarViewSet,
    AnalyticalStatementViewSet,
    AnalysisPillarDiscardedEntryViewSet,
    AnalysisPillarEntryViewSet,
    DiscardedEntryOptionsView
)
from quality_assurance.views import (
    EntryReviewCommentViewSet,
)
from analysis_framework.views import (
    AnalysisFrameworkCloneView,
    AnalysisFrameworkViewSet,
    PrivateAnalysisFrameworkRoleViewSet,
    PublicAnalysisFrameworkRoleViewSet,
    AnalysisFrameworkMembershipViewSet,
    ExportableViewSet,
    FilterViewSet,
    WidgetViewSet,
)
from ary.views import (
    AssessmentViewSet,
    PlannedAssessmentViewSet,
    AssessmentOptionsView,
    AssessmentTemplateViewSet,
    LeadAssessmentViewSet,
    LeadGroupAssessmentViewSet,
    AssessmentCopyView,
)
from category_editor.views import (
    CategoryEditorViewSet,
    CategoryEditorCloneView,
    CategoryEditorClassifyView,
)
from connector.views import (
    SourceViewSet,
    SourceQueryView,
    ConnectorViewSet,
    ConnectorUserViewSet,
    ConnectorProjectViewSet,
)
from export.views import (
    ExportTriggerView,
    ExportViewSet,
)
from deepl_integration.views import (
    AssistedTaggingDraftEntryPredictionCallbackView,
    AutoTaggingDraftEntryPredictionCallbackView,
    LeadExtractCallbackView,
    UnifiedConnectorLeadExtractCallbackView,
    AnalysisTopicModelCallbackView,
    AnalysisAutomaticSummaryCallbackView,
    AnalyticalStatementNGramCallbackView,
    AnalyticalStatementGeoCallbackView,
)

from deep.ses import ses_bounce_handler_view
from deep.views import (
    AccountActivate,
    Api_404View,
    CombinedView,
    CustomGraphQLView,
    EntryCommentEmail,
    EntryReviewCommentEmail,
    FrontendView,
    PasswordReset,
    ProjectJoinRequest,
    ProjectPublicVizView,
    PasswordChanged,
    get_frontend_url,
    graphql_docs
)
from organization.views import (
    OrganizationViewSet,
    OrganizationTypeViewSet,
)
from lang.views import (
    LanguageViewSet,
)
from client_page_meta.views import (
    PageViewSet,
)

from notification.views import (
    NotificationViewSet,
    AssignmentViewSet
)

from jwt_auth.views import (
    HIDTokenObtainPairView,
    TokenObtainPairView,
    TokenRefreshView,
)
from commons.views import (
    RenderChart,
)

from django.conf.urls import (
    handler404
    # handler403, handler400, handler500
)


register_converter(converters.FileNameRegex, 'filename')


handler404 = Api_404View  # noqa

router = routers.DefaultRouter()

api_schema_view = get_schema_view(
    openapi.Info(
        title="DEEP API",
        default_version='v1',
        description="DEEP API",
        contact=openapi.Contact(email="admin@thedeep.io"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


# User routers
router.register(r'users', UserViewSet,
                basename='user')

# File routers
router.register(r'files', FileViewSet,
                basename='file')
router.register(r'files-google-drive', GoogleDriveFileViewSet,
                basename='file_google_drive')
router.register(r'files-dropbox', DropboxFileViewSet,
                basename='file_dropbox')
router.register(r'file-previews', FilePreviewViewSet,
                basename='file_preview')

# Tabular routers
router.register(r'tabular-books', BookViewSet,
                basename='tabular_book')
router.register(r'tabular-sheets', SheetViewSet,
                basename='tabular_sheet')
router.register(r'tabular-fields', FieldViewSet,
                basename='tabular_field')
router.register(r'tabular-geodatas', GeodataViewSet,
                basename='tabular_geodata')

# User group registers
router.register(r'user-groups', UserGroupViewSet,
                basename='user_group')
router.register(r'group-memberships', GroupMembershipViewSet,
                basename='group_membership')

# Project routers
router.register(r'projects', ProjectViewSet,
                basename='project')
router.register(r'projects-stat', ProjectStatViewSet,
                basename='project-stat')
router.register(r'project-roles', ProjectRoleViewSet,
                basename='project_role')
router.register(r'projects/(?P<project_id>\d+)/project-memberships', ProjectMembershipViewSet,
                basename='project_membership')
router.register(r'projects/(?P<project_id>\d+)/project-usergroups', ProjectUserGroupViewSet,
                basename='project_usergroup')

# Geo routers
router.register(r'regions', RegionViewSet,
                basename='region')
router.register(r'admin-levels', AdminLevelViewSet,
                basename='admin_level')
router.register(r'projects/(?P<project_id>\d+)/geo-area', GeoAreaView,
                basename='geo_area')

# Lead routers
router.register(r'lead-groups', LeadGroupViewSet,
                basename='lead_group')
router.register(r'leads', LeadViewSet,
                basename='lead')
router.register(r'project/(?P<project_id>\d+)/leads', LeadBulkDeleteViewSet,
                basename='leads-bulk')
router.register(r'lead-previews', LeadPreviewViewSet,
                basename='lead_preview')

# Questionnaire routers
router.register(r'questionnaires/(?P<questionnaire_id>\d+)/questions',
                QuestionViewSet, basename='question')
router.register(r'questionnaires', QuestionnaireViewSet,
                basename='questionnaire')

# Entry routers
router.register(r'entries', EntryViewSet,
                basename='entry_lead')
router.register(r'entry-attributes', AttributeViewSet,
                basename='entry_attribute')
router.register(r'entry-filter-data', FilterDataViewSet,
                basename='entry_filter_data')
router.register(r'entry-export-data', ExportDataViewSet,
                basename='entry_export_data')
router.register(r'edit-entries-data', EditEntriesDataViewSet,
                basename='edit_entries_data')

router.register(r'entries/(?P<entry_id>\d+)/entry-comments', EntryCommentViewSet, basename='entry-comment')
router.register(r'projects/(?P<project_id>\d+)/entry-labels', ProjectEntryLabelViewSet, basename='entry-labels')
router.register(r'leads/(?P<lead_id>\d+)/entry-groups', LeadEntryGroupViewSet, basename='entry-groups')

# Analysis routers
router.register(r'projects/(?P<project_id>\d+)/analysis', AnalysisViewSet,
                basename='analysis')
router.register(r'projects/(?P<project_id>\d+)/analysis/(?P<analysis_id>\d+)/pillars',
                AnalysisPillarViewSet, basename='analysis_analysis_pillar')
router.register(
    r'projects/(?P<project_id>\d+)/analysis/(?P<analysis_id>\d+)/pillars/(?P<analysis_pillar_id>\d+)/analytical-statement',
    AnalyticalStatementViewSet, basename='analytical_statement')
router.register(
    r'analysis-pillar/(?P<analysis_pillar_id>\d+)/discarded-entries',
    AnalysisPillarDiscardedEntryViewSet, basename='analysis_pillar_discarded_entries'
)

# QA routers
router.register(
    r'entries/(?P<entry_id>\d+)/review-comments', EntryReviewCommentViewSet, basename='entry-review-comment')

# Analysis framework routers
router.register(r'analysis-frameworks/(?P<af_id>\d+)/questions',
                FrameworkQuestionViewSet, basename='framework-question')
router.register(r'analysis-frameworks', AnalysisFrameworkViewSet,
                basename='analysis_framework')
router.register(r'analysis-framework-widgets', WidgetViewSet,
                basename='analysis_framework_widget')
router.register(r'analysis-framework-filters', FilterViewSet,
                basename='analysis_framework_filter')
router.register(r'analysis-framework-exportables', ExportableViewSet,
                basename='analysis_framework_exportable')
router.register(r'framework-memberships', AnalysisFrameworkMembershipViewSet,
                basename='framework_memberships')
router.register(r'private-framework-roles', PrivateAnalysisFrameworkRoleViewSet,
                basename='framework_roles')
router.register(r'public-framework-roles', PublicAnalysisFrameworkRoleViewSet,
                basename='framework_roles')

# Assessment registry
router.register(r'assessments', AssessmentViewSet,
                basename='assessment')
router.register(r'planned-assessments', PlannedAssessmentViewSet,
                basename='planned-assessment')

router.register(r'lead-assessments', LeadAssessmentViewSet,
                basename='lead_assessment')
router.register(r'lead-group-assessments', LeadGroupAssessmentViewSet,
                basename='lead_group_assessment')
router.register(r'assessment-templates', AssessmentTemplateViewSet,
                basename='assessment_template')

# Category editor routers
router.register(r'category-editors', CategoryEditorViewSet,
                basename='category_editor')

# Connector routers
router.register(r'connector-sources', SourceViewSet,
                basename='connector_source')
router.register(r'connectors', ConnectorViewSet,
                basename='connector')
router.register(r'connector-users', ConnectorUserViewSet,
                basename='connector_users')
router.register(r'connector-projects', ConnectorProjectViewSet,
                basename='connector_projects')

# Organization routers
router.register(r'organizations', OrganizationViewSet, basename='organization')
router.register(r'organization-types', OrganizationTypeViewSet, basename='organization-type')

# Export routers
router.register(r'exports', ExportViewSet, basename='export')

# Notification routers
router.register(r'notifications',
                NotificationViewSet, basename='notification')
router.register(r'assignments',
                AssignmentViewSet, basename='assignments')

# Language routers
router.register(r'languages', LanguageViewSet, basename='language')

# Page routers
router.register(r'pages', PageViewSet, basename='page')

# Versioning : (v1|v2|v3)

API_PREFIX = r'^api/(?P<version>(v1|v2))/'


def get_api_path(path):
    return '{}{}'.format(API_PREFIX, path)


CustomGraphQLView.graphiql_template = "graphene_graphiql_explorer/graphiql.html"

# Enable OTP in Production
if not settings.DEBUG:
    admin.site.__class__ = OTPAdminSite

urlpatterns = [
    re_path(r'^$', FrontendView.as_view(), name='server-frontend'),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^graphql-docs/$', graphql_docs, name='graphql_docs'),
    re_path(r'^api-docs(?P<format>\.json|\.yaml)$',
            api_schema_view.without_ui(cache_timeout=settings.OPEN_API_DOCS_TIMEOUT), name='schema-json'),
    re_path(r'^api-docs/$', api_schema_view.with_ui('swagger', cache_timeout=settings.OPEN_API_DOCS_TIMEOUT),
            name='schema-swagger-ui'),
    re_path(r'^redoc/$', api_schema_view.with_ui('redoc', cache_timeout=settings.OPEN_API_DOCS_TIMEOUT),
            name='schema-redoc'),

    # JWT Authentication
    re_path(get_api_path(r'token/$'),
            TokenObtainPairView.as_view()),

    re_path(get_api_path(r'token/hid/$'),
            HIDTokenObtainPairView.as_view()),

    re_path(get_api_path(r'token/refresh/$'),
            TokenRefreshView.as_view()),

    # Gallery
    re_path(r'^file/(?P<file_id>\d+)/$', FileView.as_view(), name='file'),
    path(
        'private-file/<uuid:uuid>/<filename:filename>',
        PrivateFileView.as_view(),
        name='gallery_private_url',
    ),
    path(
        'deprecated-private-file/<uuid:uuid>/<filename:filename>',
        DeprecatedPrivateFileView.as_view(),
        name='deprecated_gallery_private_url',
    ),
    path(
        'external/private-file/<str:module>/<str:identifier>/<filename:filename>',
        PrivateAttachmentFileView.as_view(),
        name='external_private_url',
    ),
    re_path(
        r'^public-file/(?P<fidb64>[0-9A-Za-z]+)/(?P<token>.+)/(?P<filename>.*)$',
        PublicFileView.as_view(),
        name='gallery_public_url',
    ),

    # Activate User
    re_path(r'^user/activate/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
            user_activate_confirm,
            name='user_activate_confirm'),

    # Unsubscribe User Email
    re_path(r'^user/unsubscribe/email/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/'
            '(?P<email_type>[A-Za-z_]+)/$',
            unsubscribe_email,
            name='unsubscribe_email'),
    # Project Request Accept
    re_path(r'^project/join-request/'
            '(?P<uidb64>[0-9A-Za-z]+)-(?P<pidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
            accept_project_confirm,
            name='accept_project_confirm'),

    # password reset API
    re_path(get_api_path(r'password/reset/$'),
            PasswordResetView.as_view()),

    # Password Reset
    re_path(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
            auth_views.PasswordResetConfirmView.as_view(
                success_url='{}://{}/login/'.format(
                    settings.HTTP_PROTOCOL, settings.DEEPER_FRONTEND_HOST,
                )
            ),
            name='password_reset_confirm'),

    # Attribute options for various models
    re_path(get_api_path(r'lead-options/$'),
            LeadOptionsView.as_view()),
    re_path(get_api_path(r'assessment-options/$'),
            AssessmentOptionsView.as_view()),
    re_path(get_api_path(r'entry-options/$'),
            EntryOptionsView.as_view()),
    re_path(get_api_path(r'project-options/$'),
            ProjectOptionsView.as_view()),
    re_path(get_api_path(r'discarded-entry-options/$'),
            DiscardedEntryOptionsView.as_view()),

    # Triggering api
    re_path(get_api_path(r'lead-extraction-trigger/(?P<lead_id>\d+)/$'),
            LeadExtractionTriggerView.as_view()),

    re_path(get_api_path(r'file-extraction-trigger/$'),
            FileExtractionTriggerView.as_view()),

    re_path(get_api_path(r'meta-extraction/(?P<file_id>\d+)/$'),
            MetaExtractionView.as_view()),

    re_path(get_api_path(r'geo-areas-load-trigger/(?P<region_id>\d+)/$'),
            GeoAreasLoadTriggerView.as_view()),

    re_path(get_api_path(r'export-trigger/$'),
            ExportTriggerView.as_view()),

    re_path(get_api_path(r'tabular-extraction-trigger/(?P<book_id>\d+)/$'),
            TabularExtractionTriggerView.as_view()),

    re_path(get_api_path(r'tabular-geo-extraction-trigger/(?P<field_id>\d+)/$'),
            TabularGeoProcessTriggerView.as_view()),

    # Website fetch api
    re_path(get_api_path(r'lead-website-fetch/$'), LeadWebsiteFetch.as_view()),

    re_path(get_api_path(r'web-info-data/$'), WebInfoDataView.as_view()),
    re_path(get_api_path(r'web-info-extract/$'), WebInfoExtractView.as_view()),

    # Questionnaire utils api
    re_path(get_api_path(r'xlsform-to-xform/$'), XFormView.as_view()),
    re_path(get_api_path(r'import-to-kobotoolbox/$'), KoboToolboxExport.as_view()),

    # Lead copy
    re_path(get_api_path(r'lead-copy/$'), LeadCopyView.as_view()),
    # Assessment copy
    re_path(get_api_path(r'assessment-copy/$'), AssessmentCopyView.as_view()),

    # Filter apis
    re_path(get_api_path(r'entries/filter/'), EntryFilterView.as_view()),
    re_path(
        get_api_path(r'analysis-pillar/(?P<analysis_pillar_id>\d+)/entries'),
        AnalysisPillarEntryViewSet.as_view(),
        name='analysis_pillar_entries',
    ),

    re_path(get_api_path(
        r'projects/(?P<project_id>\d+)/category-editor/classify/'
    ), CategoryEditorClassifyView.as_view()),

    # Source query api
    re_path(get_api_path(
        r'connector-sources/(?P<source_type>[-\w]+)/(?P<query>[-\w]+)/',
    ), SourceQueryView.as_view()),

    # Geojson api
    re_path(get_api_path(r'admin-levels/(?P<admin_level_id>\d+)/geojson/$'),
            GeoJsonView.as_view()),
    re_path(get_api_path(r'admin-levels/(?P<admin_level_id>\d+)/geojson/bounds/$'),
            GeoBoundsView.as_view()),
    re_path(get_api_path(r'geo-options/$'),
            GeoOptionsView.as_view()),

    # Clone apis
    re_path(get_api_path(r'clone-region/(?P<region_id>\d+)/$'),
            RegionCloneView.as_view()),
    re_path(get_api_path(r'clone-analysis-framework/(?P<af_id>\d+)/$'),
            AnalysisFrameworkCloneView.as_view()),
    re_path(get_api_path(r'clone-category-editor/(?P<ce_id>\d+)/$'),
            CategoryEditorCloneView.as_view()),

    # NLP Callback endpoints
    re_path(
        get_api_path(r'callback/lead-extract/$'),
        LeadExtractCallbackView.as_view(),
        name='lead_extract_callback',
    ),
    re_path(
        get_api_path(r'callback/unified-connector-lead-extract/$'),
        UnifiedConnectorLeadExtractCallbackView.as_view(),
        name='unified_connector_lead_extract_callback',
    ),
    re_path(
        get_api_path(r'callback/assisted-tagging-draft-entry-prediction/$'),
        AssistedTaggingDraftEntryPredictionCallbackView.as_view(),
        name='assisted_tagging_draft_entry_prediction_callback',
    ),
    re_path(
        get_api_path(r'callback/auto-assisted-tagging-draft-entry-prediction/$'),
        AutoTaggingDraftEntryPredictionCallbackView.as_view(),
        name='auto-assisted_tagging_draft_entry_prediction_callback',
    ),

    re_path(
        get_api_path(r'callback/analysis-topic-model/$'),
        AnalysisTopicModelCallbackView.as_view(),
        name='analysis_topic_model_callback',
    ),
    re_path(
        get_api_path(r'callback/analysis-automatic-summary/$'),
        AnalysisAutomaticSummaryCallbackView.as_view(),
        name='analysis_automatic_summary_callback',
    ),
    re_path(
        get_api_path(r'callback/analysis-automatic-ngram/$'),
        AnalyticalStatementNGramCallbackView.as_view(),
        name='analysis_automatic_ngram_callback',
    ),
    re_path(
        get_api_path(r'callback/analysis-geo/$'),
        AnalyticalStatementGeoCallbackView.as_view(),
        name='analysis_geo_callback',
    ),

    # Combined API View
    re_path(get_api_path(r'combined/$'), CombinedView.as_view()),

    # Viewsets
    re_path(get_api_path(''), include(router.urls)),

    # DRF auth, TODO: logout
    re_path(r'^api-auth/', include('rest_framework.urls',
                                   namespace='rest_framework')),

    re_path(r'^project-viz/(?P<project_stat_id>\d+)/(?P<token>[0-9a-f-]+)/$',
            ProjectPublicVizView.as_view(), name='project-stat-viz-public'),

    re_path(r'^favicon.ico$',
            RedirectView.as_view(url=get_frontend_url('favicon.ico')),
            name="favicon"),

    re_path('ses-bounce/?$', ses_bounce_handler_view, name='ses_bounce'),
] + [
    # graphql patterns
    re_path('^graphql/?$', csrf_exempt(CustomGraphQLView.as_view())),
    re_path(r'^favicon.ico$',
            RedirectView.as_view(
                url=get_frontend_url('favicon.ico'),
            ),
            name="favicon"),
] + static.static(
    settings.MEDIA_URL,
    view=xframe_options_exempt(serve),
    document_root=settings.MEDIA_ROOT
)


if settings.DEBUG:
    import debug_toolbar
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        urlpatterns += [
            re_path('__debug__/', include(debug_toolbar.urls)),
        ]
    urlpatterns += [
        re_path('^graphiql/?$', csrf_exempt(CustomGraphQLView.as_view(graphiql=True))),
        re_path(r'^pr-email/$', PasswordReset.as_view()),
        re_path(r'^pc-email/$', PasswordChanged.as_view()),
        re_path(r'^aa-email/$', AccountActivate.as_view()),
        re_path(r'^pj-email/$', ProjectJoinRequest.as_view()),
        re_path(r'^ec-email/$', EntryCommentEmail.as_view()),
        re_path(r'^erc-email/$', EntryReviewCommentEmail.as_view()),
        re_path(r'^render-debug/$', RenderChart.as_view()),

    ]


handler404 = Api_404View.as_view()

# TODO Uncomment after fixing custom autofixtures
# autofixture.autodiscover()
