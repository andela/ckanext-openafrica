# encoding: utf-8

'''Tests for the ckanext.openafrica extension.

'''
from nose.tools import assert_raises
from nose.tools import assert_equal

import ckan.model as model
import ckan.plugins
from ckan.plugins.toolkit import NotAuthorized, ObjectNotFound
import ckan.tests.factories as factories
import ckan.logic as logic

import ckan.tests.helpers as helpers


class HelpersTest(unittest.TestCase):

    def setUp(self):
        self._tk = helpers.tk
        helpers.tk = MagicMock()

        self._model = helpers.model
        helpers.model = MagicMock()

        self._db = helpers.db
        helpers.db = MagicMock()

    def tearDown(self):
        helpers.tk = self._tk
        helpers.model = self._model
        helpers.db = self._db
