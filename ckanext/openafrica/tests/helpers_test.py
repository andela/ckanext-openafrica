# encoding: utf-8

'''Tests for the ckanext.openafrica extension.

'''
import datetime
import ckanext.openafrica.lib.helpers as helpers
import ckan.tests.legacy as tests


class TestHelpers(tests.WsgiAppCase):

    def test_current_year(self):
        year = helpers.current_year()
        assert year == datetime.datetime.now().year
        assert type(year) == int

    def test_is_plugin_enabled(self):
        enabled_plugin = helpers.is_plugin_enabled('stats')
        unenabled_plugin = helpers.is_plugin_enabled('thisISnotEnabled')
        assert type(enabled_plugin) == bool
        assert type(unenabled_plugin) == bool
        assert enabled_plugin == True
        assert unenabled_plugin == False
