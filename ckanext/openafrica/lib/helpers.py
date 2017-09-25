import datetime
import urllib2
from ckan.common import config, json
from ckan.lib import helpers

def current_year():
    year = datetime.datetime.now().year
    return year    

def package_view_count(id):
    u'''
        Calculate dataset/resource view count and return
        the view_count.html snippet.
 
        :param id: package id
    '''
    show_view_count = config.get('show_view_count', False)
    admin_api_key = config.get('admin_api_key', None)
    api = config.get(admin_api_key)
    base_url = config.get('ckan.site_url')
    if (show_view_count == 'True' or show_view_count == 'true') and admin_api_key != None:
        full_url = base_url + '/api/3/action/package_show?id=' + id + '&include_tracking=true'
        request = urllib2.Request(full_url)
        request.add_header('Authorization', admin_api_key)
        response = urllib2.urlopen(request)
        response_dict = json.loads(response.read())
        assert response_dict['success'] is True
        result = response_dict['result']
        number = result['tracking_summary']['total']
        title = 'views: ' + str(number)
        return helpers.snippet('snippets/view_count.html', title=title, number=number)
    else:
        return ''