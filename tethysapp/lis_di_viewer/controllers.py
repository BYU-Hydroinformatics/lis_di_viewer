from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import *
from utilities import *
import os
from datetime import datetime,timedelta
import datetime


def home(request):
    """
    Controller for the app home page.
    """
    # geotiff_dir = '/home/rheas/di_rasters'
    # sorted_files = sorted(os.listdir(geotiff_dir), key=lambda x: datetime.datetime.strptime(x, '%Y_%m_%d.tif'))
    
    di_layer_options = []

    for year in range(2001, 2012):
        start_date = '01/01/' + str(year)
        date_str = datetime.datetime.strptime(start_date, "%m/%d/%Y")
        days = 1
        for i in range(37):
            if i == 0:
                end_date = date_str
            else:
                days += 10
                end_date = date_str + timedelta(days=float(days - 1))

            ts_file_name = end_date.strftime("%Y_%m_%d")
            year = int(ts_file_name.split('_')[0])
            month = int(ts_file_name.split('_')[1])
            day = int(ts_file_name.split('_')[2])
            new_date_str = datetime.datetime(year, month, day)
            new_date_str = new_date_str.strftime("%Y %B %d")
            di_layer_options.append([new_date_str,ts_file_name])

    layers_length = len(di_layer_options)
    # for file in sorted_files:
    #     year = int(file[:-4].split('_')[0])
    #     month = int(file[:-4].split('_')[1])
    #     day = int(file[:-4].split('_')[2])
    #     date_str = datetime.datetime(year, month, day)
    #     date_str = date_str.strftime("%Y %B %d")
    #     di_layer_options.append([date_str, file[:-4]])

    select_layer = SelectInput(display_text='Select a day',
                               name='select_layer',
                               multiple=False,
                               options=di_layer_options, )








    context = {
        "select_layer":select_layer,
        "slider_max":layers_length
    }

    return render(request, 'lis_di_viewer/home.html', context)