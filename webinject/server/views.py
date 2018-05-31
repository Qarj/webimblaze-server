# Create your views here.

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from itertools import chain
import subprocess

def index(request):
    return HttpResponse("Hello, world. You're at the Webinject Server index.")

def run(request):
    path = request.GET.get('path', None)

    print ('Started existing test execution:', path)
    result_stdout = run_wif_for_test_file_at_path(path)
    print ('Finished existing test execution:', path)

    page_title = path
    page_heading = 'Run existing test: ' + path
    error = ''

    context = {
        'page_title': page_title,
        'page_heading': page_heading,
        'result_stdout': result_stdout,
        'error': error,
    }
    
    return render(request, 'server/run.html', context)

#    return HttpResponse (
#        'Run existing test:' + path +
#        '\n<br /><br />\n' +
#        '<pre><code>' +
#        response +
#        '</code></pre>'
#    )

def run_wif_for_test_file_at_path(path):
    cmd = get_wif_command(path)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
    output, errors = proc.communicate()
    decoded = output.decode('cp850') # western european Windows code page is cp850
    return decoded

def get_wif_command(path):

    cmd = ['perl', wif_location(), path, '--env', 'DEV', '--target', 'team1', '--batch', 'WebInject-Server', '--no-update-config']
    return cmd

def wif_location():
    return r'C:\git\WebInject-Framework\wif.pl'

