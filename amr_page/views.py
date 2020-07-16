# Create your views here.

from typing import Dict

from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import *
from .downloader import Download

import random

amr_data: Dict[str, bytes] = {}

@login_required()
def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        print('POST')
        # create a form instance and populate it with data from the request:
        form = DownloadForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            try:
                key = ''.join([random.choice(list('0123456789abcdef')) for i in range(16)])
                search: bool = form.cleaned_data['yt_search']
                print('SEARCH:',search)
                amr_data[key] = Download.yt_url(search if search else form.cleaned_data['yt_url'], quality=form.cleaned_data['quality'], search=(search != None))

                return HttpResponseRedirect('amr-data/' + key + '.amr')
            except OSError as err:
                # raise err
                return HttpResponseServerError('<h2>Error 500</h2><br/>Internal server error.<br/><pre>{}</pre>'.format(str(err)))

    # if a GET (or any other method) we'll create a blank form
    else:
        download_form = DownloadForm()

        page = loader.get_template('index.html')

        return render(request, 'index.html', {'download_form': download_form})

def get_amrdata(request):
    try:
        key = request.path.split('/')[-1][:-4]      # -4 gets rid of .amr
        data = amr_data.pop(key)
        return HttpResponse(content=data, content_type='audio/AMR')
    except KeyError:
        return HttpResponseNotFound(content="<h2>Error 404</h2><br/>Page not found.")
