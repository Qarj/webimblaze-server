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

class WebInjectServerTests(TestCase):
    
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

    def get_submit(self, debug=False):
        url = my_reverse('server:submit')
        return self._get_url(url, debug)

    def _get_url(self, url, debug=False):
        response = self.client.get(url)
        if (debug):
            print('\nDebug URL:', url)
            print(response.content.decode('utf-8'), '\n')
        return response

    def submit(self, steps, debug=False, batch='', target=''):
        kwargs={}
        if (batch):
            kwargs['batch'] = batch
        if (target):
            kwargs['target'] = target
        url = my_reverse('server:submit', query_kwargs=kwargs)
        body = {'steps': steps}
        return self._post_url_and_body(url, body, debug)

    def _post_url_and_body(self, url, body, debug=False):
        response = self.client.post(url, body)
        if (debug):
            print('\nDebug URL :', url)
            print('\nDebug Body:', body)
            print('\nDebug Response Content Start\n', response.content.decode('utf-8'), '\n')
            print('\nDebug Response Content End\n')
        return response

    def number_of_instances(self, response, target):
        return response.content.decode('utf-8').count(target)

    def _assertRegex(self, response, regex):
        self.assertRegex(response.content.decode('utf-8'), regex)

    def _assertNotRegex(self, response, regex):
        self.assertNotRegex(response.content.decode('utf-8'), regex)

    #
    # Run WebInject Framework existing test through WebInject Framework
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

    #
    # Submit test to run through WebInject-Framework
    #

    def test_can_submit_a_simple_test_and_see_result(self):
        steps = """
<testcases repeat="1">

<case
    id="10"
    description1="Check that WebInject Server can run a simple submitted test"
    method="cmd"
    command="REM This and that"
    verifypositive1="This and that"
/>

<case
    id="20"
    description1="Subsequent step - retry {RETRY}"
    method="cmd"
    command="REM Not much more - retry {RETRY}"
    verifypositive="retry 0"
    verifynegative="Nothing much"
/>

</testcases>
"""        
        
        response = self.submit(steps, debug=False)
        self.assertContains(response, 'class="pass">WEBINJECT TEST PASSED<')

    def test_can_get_an_empty_submit_form(self):
        response = self.get_submit(debug=True)
        self.assertContains(response, 'Paste the test steps here')

# \Apache24\bin\httpd -k restart

# MVP Tests
# Can get form
# Form has heading
# Custom form rendering (removes steps)
# Custom form rendering - make text area much larger
# Custom form rendering - background colour of text area is light grey
# Custom form rendering - Style submit button
# Can run more than one test at once
# Temporary file deletion
# Is dedupe of code possible between submit and run?
# What if form doesn't pass validation? How is this possible?
# Can specify batch name for submit
# Can specify target for submit
# Submit form has page title
# Index has link to submit
# Submit form has hello world example
# Submit form has get totaljobs homepage example
# Submit form has get cwjobs homepage example - selenium!
# Can post the form from NUNIT

# Ref  - form for posting a test https://docs.djangoproject.com/en/2.0/topics/forms/



## https://cgoldberg.github.io/python-unittest-tutorial/
