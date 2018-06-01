# Create your tests here.

from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode

import re

#
# Test Helpers
#

# https://stackoverflow.com/questions/4995279/including-a-querystring-in-a-django-core-urlresolvers-reverse-call
def my_reverse(viewname, kwargs=None, query_kwargs=None):
    """
    Custom reverse to add a query string after the url
    Example usage:
    url = my_reverse('my_test_url', kwargs={'pk': object.id}, query_kwargs={'next': reverse('home')})
    """
    url = reverse(viewname, kwargs=kwargs)

    if query_kwargs:
        return u'%s?%s' % (url, urlencode(query_kwargs))

    return url

class ServerIndexViewTests(TestCase):
    def test_index(self):
        """
        Server index page exists
        """
        response = self.client.get(reverse('server:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'style.css')
        self.assertContains(response, 'Run an existing test example')
        self.assertContains(response, 'href="/webinject/server/run/?path=examples%2Ftest.xml"')

class RunWebInjectFrameWorkTests(TestCase):
    
    #
    # test helpers
    #

    def runit(self, path, debug=False, batch='', target=''):
        kwargs={'path': path}
        if (batch):
            kwargs['batch'] = batch
        if (target):
            kwargs['target'] = target
        url = my_reverse('server:run', query_kwargs=kwargs)
        return self._get_url(url, debug)

    def _get_url(self, url, debug=False):
        response = self.client.get(url)
        if (debug):
            print('\nDebug URL:', url)
            print(response.content.decode('utf-8'), '\n')
        return response

    def number_of_instances(self, response, target):
        return response.content.decode('utf-8').count(target)

    def _assertRegex(self, response, regex):
        self.assertRegex(response.content.decode('utf-8'), regex)

    def _assertNotRegex(self, response, regex):
        self.assertNotRegex(response.content.decode('utf-8'), regex)

    #
    # Run WebInject Framework Tests
    #

    def test_run_simple_test_in_webinject_examples(self):
        response = self.runit('examples/test.xml', False)
        self.assertContains(response, 'Test that WebInject can run a very basic test')
        self.assertContains(response, '<pre><code>')
        self.assertContains(response, '</code></pre>')
        self.assertContains(response, 'Result at: http')
        self._assertRegex(response, r'\sFailed Positive Verification') # i.e. no ANSI code like 1;33m
        self.assertContains(response, 'style.css')
        self.assertContains(response, 'class="pass">WEBINJECT TEST PASSED<')
        self._assertNotRegex(response, r'Batch ')
        self._assertNotRegex(response, r'Target ')
        self._assertRegex(response, r'a href="[^"]*results_[0-9]{4}')

    def test_run_simple_test_in_webinject_examples_with_options(self):
        response = self.runit('examples*test.xml', False, batch='CustomBatch', target='team2')  # can use * instead of /
        self.assertContains(response, 'Result at: http')
        self.assertContains(response, '>Batch [CustomBatch] Target [team2]<')

    def test_run_failing_test_webinject_examples(self):
        response = self.runit('examples/fail.xml', False, target='team2')
        self.assertContains(response, 'Test Cases Passed: 0')
        self.assertContains(response, 'class="fail">WEBINJECT TEST FAILED<')
        self._assertNotRegex(response, r'Batch \[\]')
        self.assertContains(response, '>Target [team2]<')

    def test_run_non_existing_test_is_an_error(self):
        response = self.runit('examples/testdoesnotexist.xml', False)
        self._assertRegex(response, r'class="error">WEBINJECT TEST ERROR<')
        self.assertEqual(500, response.status_code, 'Response code 500 not found, was ' + str(response.status_code))

# \Apache24\bin\httpd -k restart

# Post POC Hardening Tests
#   - Index page gives examples of how to run tests
#   - Time that it takes to run slow displayed on index
#   - Logo improved - plain blue S with alpha


# MVP Tests
#   - POST URL server/submit with POSTBODY of webinject test cases.
#   - form for posting a test


## https://cgoldberg.github.io/python-unittest-tutorial/
