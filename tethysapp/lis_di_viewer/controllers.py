from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import *
from utilities import *
import os
from datetime import datetime

@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    geotiff_dir = '/home/rheas/di_rasters'
    sorted_files = sorted(os.listdir(geotiff_dir), key=lambda x: datetime.strptime(x, '%Y_%m_%d.tif'))
    layers_length = len(sorted_files)

    di_layer_options = []

    for file in sorted_files:
        year = int(file[:-4].split('_')[0])
        month = int(file[:-4].split('_')[1])
        day = int(file[:-4].split('_')[2])
        date_str = datetime(year, month, day)
        date_str = date_str.strftime("%Y %B %d")
        di_layer_options.append([date_str, file[:-4]])

    select_layer = SelectInput(display_text='Select a day',
                               name='select_layer',
                               multiple=False,
                               options=di_layer_options, )


    context = {
        "select_layer":select_layer,
        "slider_max":layers_length
    }

    return render(request, 'lis_di_viewer/home.html', context)