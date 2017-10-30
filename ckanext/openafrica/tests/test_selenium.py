import os
import unittest
from selenium import webdriver
from random import choice
import pexpect
import ckan.logic as logic
from string import ascii_uppercase
from ckan.config.environment import load_environment
from selenium.webdriver.common.by import By
from paste.deploy import appconfig


def generate_random_string(length):
    return ''.join(choice(ascii_uppercase) for i in range(length))


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
        self.driver = webdriver.Chrome()
        self.base_url = 'http://127.0.0.1:5000'
        self.register_sysadmin()
        self.driver.set_window_size(1024, 768)
        conf = appconfig('config:/etc/ckan/default/production.ini', relative_to='.')
        load_environment(conf.global_conf, conf.local_conf)

    def create_organization(self, name, description):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_link_text('Organisations').click()
        driver.find_element_by_link_text('Add Organization').click()
        driver.find_element_by_id('field-name').clear()
        driver.find_element_by_id('field-name').send_keys(name)
        driver.find_element_by_id('field-description').clear()
        driver.find_element_by_id('field-description').send_keys(description)
        driver.find_element_by_name('save').click()

    def register_user(self, username, fullname, mail, password):
        # register a normal user
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_link_text('Register').click()
        driver.find_element_by_id('field-username').clear()
        driver.find_element_by_id('field-username').send_keys(username)
        driver.find_element_by_id('field-fullname').clear()
        driver.find_element_by_id('field-fullname').send_keys(fullname)
        driver.find_element_by_id('field-email').clear()
        driver.find_element_by_id('field-email').send_keys(mail)
        driver.find_element_by_id('field-password').clear()
        driver.find_element_by_id('field-password').send_keys(password)
        driver.find_element_by_id('field-confirm-password').clear()
        driver.find_element_by_id('field-confirm-password').send_keys(password)
        driver.find_element_by_name('save').click()
        self.logout()

    def default_register(self, user):
        self.register(user, user, '%s@conwet.com' % user, user)

    def login(self, username, password):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_link_text('Log in').click()
        driver.find_element_by_id('field-login').clear()
        driver.find_element_by_id('field-login').send_keys(username)
        driver.find_element_by_id('field-password').clear()
        driver.find_element_by_id('field-password').send_keys(password)
        driver.find_element_by_id('field-remember').click()
        driver.find_element_by_css_selector('button.btn.btn-primary').click()

    def logout_user(self):
        self.driver.delete_all_cookies()
        self.driver.get(self.base_url)

    def remove_sysadmin(cls):
        # Remove sysadmin user using paster.
        try:
            child = pexpect.spawn('paster', ['--plugin=ckan', 'sysadmin', 'remove', cls.sysadmin, '-c', '/etc/ckan/default/production.ini'])
            child.expect('Access OK.')
        except pexpect.EOF:
            # Sysadmin probably exists already
            pass

    def complete_dataset_form(self, title, description):
        driver = self.driver
        driver.find_element_by_id('field-title').clear()
        driver.find_element_by_id('field-title').send_keys(title)
        driver.find_element_by_id('field-notes').clear()
        driver.find_element_by_id('field-notes').send_keys(description)
        button = driver.find_element_by_name('save')
        button.click()

    def create_dataset(self, title, description):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_link_text('Datasets').click()
        driver.find_element_by_link_text('Add Dataset').click()
        self.complete_dataset_form(title, description)
        return driver.current_url.split('/')[-1]

    def delete_dataset(self):
        self.child = pexpect.spawn('paster', ['--plugin=ckan', 'dataset', 'purge', 'test_dataset', '-c', '/etc/ckan/default/production.ini'])
        self.child.expect('test_dataset purged')

    def delete_org(self, name):
        logic.get_action('organization_purge')({'ignore_auth': True}, {'id': name})

    def test_organization_create(self):
        self.register_sysadmin()
        self.login("selenium_admin", "selenium")
        self.create_organization("test_organisation", "test")
        self.driver.get(self.base_url + "/organization")
        assert "test_organisation" in self.driver.page_source
        self.delete_org("test_organisation")

    def test_landing_page(self):
        driver = self.driver
        driver.get(self.base_url)
        assert "Welcome - CKAN" in driver.title

    def test_about_page(self):
        driver = self.driver
        driver.get(self.base_url + "/about")
        assert "About" in self.driver.title

    def test_dataset_create(self):
        self.register_sysadmin()
        self.login("selenium_admin", "selenium")
        title = "test_dataset"
        description = generate_random_string(20)
        self.create_dataset(title, description)
        self.driver.get(self.base_url + "/dataset/test_dataset")
        self.assertIn("test_dataset", self.driver.title)
        self.delete_dataset()

    def test_dataset_update(self):
        self.register_sysadmin()
        self.login("selenium_admin", "selenium")
        title = 'test_dataset'
        description = 'patiently'
        self.create_dataset(title, description)
        updated_description = 'updated description'
        driver = self.driver
        driver.get(self.base_url + '/dataset/test_dataset')
        driver.find_element_by_link_text('Manage').click()
        self.complete_dataset_form(title, updated_description)
        driver.get(self.base_url + '/dataset/test_dataset')
        description_assert = driver.find_element_by_css_selector('p')
        assert "updated description" in description_assert.text
        self.delete_dataset()

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
