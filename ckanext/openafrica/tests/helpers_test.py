# encoding: utf-8

'''Tests for the ckanext.openafrica extension.

'''
import pprint
import ckanext.openafrica.lib.helpers as helpers

print('Start')

def helper_test():
    pprint.pprint('Start')
    print(helpers.current_year())
    return 'Start'

def test_me():
    pprint.pprint('My')
    assert helper_test() == 'Start'
