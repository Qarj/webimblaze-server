# Create your views here.

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from itertools import chain
import subprocess, re, os.path

def index(request):
    page_title = "WebInject Server"
    page_heading = "Webinject Server"
    error = ''

    context = {
        'page_title': page_title,
        'page_heading': page_heading,
        'error': error,
    }
    
    return render(request, 'server/index.html', context)

def run(request):
    path = substitute_star_with_slash( request.GET.get('path', None) )
    batch = request.GET.get('batch', None)
    target = request.GET.get('target', None)

    print ('Started existing test execution:', path)
    result_stdout = run_wif_for_test_file_at_path(path, batch, target)
    print ('Finished existing test execution:', path)

    http_status, result_status, result_status_message = get_status(result_stdout)
    result_link = get_result_link(result_stdout)
    options = get_options_summary(batch, target)

    page_title = path
    page_heading = 'Run existing test: ' + path
    error = ''

    context = {
        'page_title': page_title,
        'page_heading': page_heading,
        'result_stdout': result_stdout,
        'result_status': result_status,
        'result_status_message': result_status_message,
        'result_link': result_link,
        'options': options,
        'error': error,
    }
    
    return render(request, 'server/run.html', context, status=http_status)

def substitute_star_with_slash(path):
    return path.replace('*','/')

def get_result_link(result_stdout):
    m = re.search(r'Result at: ([^\s]*)', result_stdout)
    if (m):
        return m.group(1)
    else:
        return '/DEV/Summary.xml'

def get_options_summary(batch, target):

    # this is to prevent a leading space if we have a Target but no Batch
    options_summary = summaryBuilder()
    options_summary.append_non_blank_value(batch, 'Batch')
    options_summary.append_non_blank_value(target, 'Target')

    return options_summary.summary

class summaryBuilder:

    already_appended_item = False
    summary = ''
    
    def __init__(self):
        self.already_appended_item = False
        self.summary = ''

    def append_non_blank_value(self, value, desc):
        if (not value):
            return
        if (self.already_appended_item):
            self.summary += ' ' + self.formatted(value, desc)
            return 
        else:
            self.already_appended_item = True
            self.summary += self.formatted(value, desc)
            return

    def formatted(self, value, desc):
        return desc + ' [' + value + ']'

def get_status(result_stdout):
    if ( re.search(r'(Test Cases Failed: 0)', result_stdout) ):
        return 200, 'pass', 'WEBINJECT TEST PASSED'
    if ( re.search(r'(Test Cases Failed: [1-9])', result_stdout) ):
        return 200, 'fail', 'WEBINJECT TEST FAILED'
    return 500, 'error', 'WEBINJECT TEST ERROR'

def run_wif_for_test_file_at_path(path, batch, target):
    cmd = get_wif_command(path, batch, target)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
    output, errors = proc.communicate()
    decoded = output.decode('cp850') # western european Windows code page is cp850
    return decoded

def get_wif_command(path, batch, target):

    if (not batch):
        batch = 'WebInject-Server'

    if (not target):
        target = 'team1'

    return ['perl', wif_location(), path, '--env', 'DEV', '--target', target, '--batch', batch , '--no-update-config']

def wif_location():
    locations = []
    locations.append(r'D:\WebInjectSERVER')
    locations.append(r'C:\WebInjectSERVER')
    locations.append(r'C:\git\WebInject-Framework')
    locations.append(r'C:\WebInject')
    locations.append(r'D:\WebInject')
    locations.append(r'C:\WebInject-Framework')
    for l in locations:
        if ( os.path.isfile(l+r'\wif.pl') ):
            return l+r'\wif.pl'
    return ('WebInject Framework wif.pl file not found - suggest deploying to C:\\WebInjectSERVER\\wif.pl \n\n')
