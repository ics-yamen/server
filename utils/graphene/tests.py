import os
import shutil
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
# dramatiq test case: setupclass is not properly called
# from django_dramatiq.test import DramatiqTestCase
from graphene_django.utils import GraphQLTestCase
from jwt_auth.token import AccessToken, RefreshToken

from deep.tests.test_case import TestCase as DeepTestCase

User = get_user_model()
TEST_MEDIA_ROOT = 'media-temp'
TEST_EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
TEST_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
TEST_CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
TEST_AUTH_PASSWORD_VALIDATORS = []


class CommonSetupClassMixin:
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # add necessary stuffs

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # clear the temporary media files
        try:
            shutil.rmtree(os.path.join(settings.BASE_DIR, TEST_MEDIA_ROOT))
        except FileNotFoundError:
            pass


@override_settings(
    EMAIL_BACKEND=TEST_EMAIL_BACKEND,
    MEDIA_ROOT=TEST_MEDIA_ROOT,
    DEFAULT_FILE_STORAGE=TEST_FILE_STORAGE,
    CACHES=TEST_CACHES,
    AUTH_PASSWORD_VALIDATORS=TEST_AUTH_PASSWORD_VALIDATORS,
)
class GraphqlTestCase(CommonSetupClassMixin, DeepTestCase, GraphQLTestCase):
    GRAPHQL_SCHEMA = 'deep.schema.schema'

    def force_login(self, user=None):
        user = user or self.user
        access = AccessToken.for_user(user)
        refresh = RefreshToken.for_access_token(access)
        self._client.credentials(
            HTTP_AUTHORIZATION='Bearer {}'.format(access.encode())
        )
        # set the session as well
        self._client.force_login(user)

        return access.encode(), refresh.encode()


class ImmediateOnCommitMixin(object):
    """
    Note: shamelessly copied from https://code.djangoproject.com/ticket/30457

    Will be redundant in immediate_on_commit function is actually implemented in Django 3.2
    Check this PR: https://github.com/django/django/pull/12944
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        def immediate_on_commit(func, using=None):
            func()
        # Context manager executing transaction.on_commit() hooks immediately
        # This is required when using a subclass of django.test.TestCase as all tests are wrapped in
        # a transaction that never gets committed.
        cls.on_commit_mgr = patch('django.db.transaction.on_commit', side_effect=immediate_on_commit)
        cls.on_commit_mgr.__enter__()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.on_commit_mgr.__exit__()


@override_settings(
    EMAIL_BACKEND=TEST_EMAIL_BACKEND,
    DEFAULT_FILE_STORAGE=TEST_FILE_STORAGE,
    MEDIA_ROOT=TEST_MEDIA_ROOT,
    CACHES=TEST_CACHES,
    AUTH_PASSWORD_VALIDATORS=TEST_AUTH_PASSWORD_VALIDATORS,
)
class CommonTestCase(CommonSetupClassMixin, ImmediateOnCommitMixin, TestCase):
    pass