from datetime import datetime,timedelta
import datetime
import time
import sys
import os, shutil
from ftplib import FTP
import numpy as np
from itertools import groupby
import tempfile, shutil,sys
import calendar
from netCDF4 import Dataset
import gdal
import osr
import ogr
import requests


def extractRasters(input_dir,output_dir):



    for file in sorted(os.listdir(input_dir)):
        in_loc = os.path.join(input_dir,file)
        output_dir = os.path.join(output_dir,"")
        lis_fid = Dataset(in_loc, 'r')  # Reading the netcdf file
        lis_var = lis_fid.variables  # Get the netCDF variables
        var = "SMCI_1m"  # Specifying the variable key. This parameter will be used to retrieve information about the netCDF file
        xsize, ysize, GeoT, Projection, NDV = get_netcdf_info(in_loc, var)
        lis_time = lis_var['startday'][:]
        current_year = file.split('_')[2]
        start_date = '01/01/'+str(current_year)
        date_str = datetime.datetime.strptime(start_date, "%m/%d/%Y")

        for timestep, v in enumerate(lis_time):
            current_time_step = lis_var[var][timestep, :, :]  # Getting the index of the current timestep

            if timestep == 0:
                end_date = date_str
            else:
                end_date = date_str + timedelta(days=float(v-1))  # Actual human readable date of the timestep

            ts_file_name = end_date.strftime("%Y_%m_%d")  # Changing the date string format

            data = lis_var[var][timestep, :, :]
            data = data[::-1, :]
            driver = gdal.GetDriverByName('GTiff')
            DataSet = driver.Create(output_dir + ts_file_name + '.tif', xsize, ysize, 1, gdal.GDT_Float32)
            DataSet.SetGeoTransform(GeoT)
            srs = osr.SpatialReference()
            srs.ImportFromEPSG(4326)
            DataSet.SetProjection(srs.ExportToWkt())

            DataSet.GetRasterBand(1).WriteArray(data)
            DataSet.GetRasterBand(1).SetNoDataValue(NDV)
            DataSet.FlushCache()

            DataSet = None

    return date_str

#Get info from the netCDF file. This info will be used to convert the shapefile to a raster layer
def get_netcdf_info(filename,var_name):

    nc_file = gdal.Open(filename)

    if nc_file is None:
        sys.exit()

    #There are more than two variables, so specifying the lwe_thickness variable

    if nc_file.GetSubDatasets() > 1:
        subdataset = 'NETCDF:"'+filename+'":'+var_name #Specifying the subset name
        src_ds_sd = gdal.Open(subdataset) #Reading the subset
        NDV = src_ds_sd.GetRasterBand(1).GetNoDataValue() #Get the nodatavalues
        xsize = src_ds_sd.RasterXSize #Get the X size
        ysize = src_ds_sd.RasterYSize #Get the Y size
        GeoT = src_ds_sd.GetGeoTransform() #Get the GeoTransform
        Projection = osr.SpatialReference() #Get the SpatialReference
        Projection.ImportFromWkt(src_ds_sd.GetProjectionRef()) #Setting the Spatial Reference
        src_ds_sd = None #Closing the file
        nc_file = None #Closing the file

        return xsize,ysize,GeoT,Projection,NDV #Return data that will be used to convert the shapefile

    # Upload GeoTiffs to geoserver
def upload_tiff(dir, region, geoserver_rest_url, workspace, uname, pwd):

    headers = {
        'Content-type': 'image/tiff',
    }

    dir = os.path.join(dir,"")

    for file in sorted(os.listdir(dir)):  # Looping through all the files in the given directory
        if file is None:
            sys.exit()
        data = open(dir + file, 'rb').read()  # Read the file
        store_name = file.split('.')[0] # Creating the store name dynamically

        request_url = '{0}workspaces/{1}/coveragestores/{2}/file.geotiff'.format(geoserver_rest_url, workspace,
                                                                                 store_name)  # Creating the rest url

        requests.put(request_url, headers=headers, data=data,
                     auth=(uname, pwd))  # Creating the resource on the geoserver


#extractRasters('/home/rheas/di_nc2','/home/rheas/di_rasters2')
#upload_tiff('/home/rheas/di_rasters2','hkh','http://tethys.byu.edu:8181/geoserver/rest/','hkh_di_index','admin','geoserver')

