# encoding: utf-8

'''Tests for the ckanext.openafrica extension.

'''
from ckanext.openafrica.controller import CustomPageController
from ckanext.openafrica.plugin import OpenAfricaPlugin

class TestPlugin():
    def test_plugin(self):
        open_plugin = OpenAfricaPlugin()
        helpers = open_plugin.get_helpers()
        assert 'current_year' in helpers
        assert 'is_plugin_enabled' in helpers
        assert callable(helpers['current_year'])
        assert callable(helpers['is_plugin_enabled'])


