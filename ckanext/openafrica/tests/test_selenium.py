import os
import unittest
import ckan.model as model
from selenium import webdriver
from random import choice
import ckan.lib.search.index as search_index
import ckanext.datarequests.db as db
import pexpect



class TestSelenium(unittest.TestCase):
    def register_sysadmin(cls):
        try:
            # Create a sysadmin user using paster
            cls.sysadmin = 'selenium_admin'
            cls.sysadmin_pwd = 'selenium'
            child = pexpect.spawn('paster', ['--plugin=ckan', 'sysadmin', 'add', cls.sysadmin, '-c', '/etc/ckan/default/production.ini'])
            child.expect('Create new user: .+')
            child.sendline('y')
            child.expect('Password: ')
            child.sendline(cls.sysadmin_pwd)
            child.expect('Confirm password: ')
            child.sendline(cls.sysadmin_pwd)
            child.expect('Added .+ as sysadmin')
        except pexpect.EOF:
            # Sysadmin probably exists already
            pass

    def setUp(self):
        env = os.environ.copy()
        env['DEBUG'] = 'True'
        env['OAUTHLIB_INSECURE_TRANSPORT'] = 'True'
        self.driver = webdriver.Chrome(env["WEB_DRIVER_URL"])
        self.base_url = 'http://127.0.0.1:5000'
        self.register_sysadmin()

    

    def create_organization(self, name, description):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_link_text('Organizations').click()
        driver.find_element_by_link_text('Add Organization').click()
        driver.find_element_by_id('field-name').clear()
        driver.find_element_by_id('field-name').send_keys(name)
        driver.find_element_by_id('field-description').clear()
        driver.find_element_by_id('field-description').send_keys(description)
        driver.find_element_by_name('save').click()

    def test_landing_page(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        self.assertIn("CKAN", driver.title)
        elem = driver.find_element_by_name("q")
        elem.send_keys("kenya")
        elem.send_keys(Keys.RETURN)
        assert "No results found" in driver.page_source

    def test_organization_create(self):
        self.register_sysadmin()
        self.login("selenium_admin", "selenium")
        title = "test_org"
        description = "test_organization"
        self.create_organization(title, description)

    def tearDown(self):
        self.driver.close()
        self.remove_sysadmin()


if __name__ == "__main__":
    unittest.main()
