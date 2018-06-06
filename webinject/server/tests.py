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

simple_steps = """
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


class ServerIndexViewTests(TestCase):
    def test_index(self):
        """
        Server index page exists
        """
        response = self.client.get(reverse('server:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'style.css')
        self.assertContains(response, 'Run an existing test example')
        self.assertContains(response, 'href="run/?path=examples%2Ftest.xml"')
        self.assertContains(response, 'Submit test steps for immediate run')

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

    def get_submit(self, debug=False, batch='', target=''):
        return self._get_url( self._build_submit_url(batch, target), debug )

    def submit(self, steps, debug=False, batch='', target=''):
        body = {'steps': steps}
        return self._post_url_and_body( self._build_submit_url(batch, target), body, debug )

    def _build_submit_url(self, batch, target):
        kwargs={}
        if (batch):
            kwargs['batch'] = batch
        if (target):
            kwargs['target'] = target
        return my_reverse('server:submit', query_kwargs=kwargs)

    def _get_url(self, url, debug=False):
        response = self.client.get(url)
        if (debug):
            print('\nDebug URL:', url)
            print(response.content.decode('utf-8'), '\n')
        return response

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
        response = self.runit('examples*test.xml', False, batch='RunBatch', target='team2')  # can use * instead of /
        self.assertContains(response, 'Result at: http')
        self.assertContains(response, '>Batch [RunBatch] Target [team2]<')

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
        
        response = self.submit(simple_steps, debug=False)
        self.assertContains(response, 'class="pass">WEBINJECT TEST PASSED<')
        self.assertContains(response, '>Result<')

    def test_can_submit_a_test_with_batch_and_target(self):
        
        response = self.submit(simple_steps, batch='SubmitBatch', target='team2', debug=False)
        self.assertContains(response, 'class="pass">WEBINJECT TEST PASSED<')
        self.assertContains(response, '>Batch [SubmitBatch] Target [team2]<')

    def test_can_get_an_empty_submit_form(self):
        response = self.get_submit(debug=False)
        self.assertContains(response, 'Paste the test steps here')
        self.assertContains(response, 'Submit test for immediate run')
        self.assertContains(response, '>Submit<') # page title
        self._assertNotRegex(response, '>Steps:<')
        self.assertContains(response, 'cols="140" rows="40"')
        self.assertContains(response, 'class="steps"')
        self.assertContains(response, 'class="submit-button"')
        self.assertContains(response, 'Headless (http) example')
        self.assertContains(response, 'Selenium example')

    def test_can_get_an_empty_submit_form_with_batch_and_target(self):
        response = self.get_submit(batch='MyBatch', target='MyTarget', debug=False)
        self.assertContains(response, '/server/submit/?batch=MyBatch&amp;target=MyTarget')

# \Apache24\bin\httpd -k restart

# MVP Tests
    # Can specify batch name for submit
    # Can specify target for submit
    # Index - example with batch and target name
    # Is is possible to make a generic builder?
    # Can post the form from NUNIT
    # add a canary page

# Ref  - form for posting a test https://docs.djangoproject.com/en/2.0/topics/forms/



## https://cgoldberg.github.io/python-unittest-tutorial/
