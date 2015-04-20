#!/usr/bin/python  -- replace with python path

#This script takes the field name as argument, and must be run in the directory containing all the mjd directories.

import numpy as np
import sys
import os
from astropy.io import ascii
from astropy.io import fits

field=sys.argv[1]

cellsize = 1./60.

if field == 's1':
    #insert ramin and ramax settings
    ramin = 59.1
    ramax = 145.0
    decmin = -0.875
    decmax = 17.025
    n1=5155
    n2=1074

#if field == 's2':

#if field == 's3':

#if field == 's4':

#if field == 'n1':

#if field == 'n2':

#if field == 'n3':

#if field == 'n4':



beams=[]
for b in range(0,7):
    beams.append("beam"+str(b))

mjds=next(os.walk('.'))[1]
mjds.sort()

print "number of days to process: ",len(mjds)
print "total files to process: ",len(mjds)*len(beams)

for idx,mjd in enumerate(mjds):
    print "processing day ",mjd
    dayplane=np.zeros((n1,n2))
    for beam in beams:
        tab_path= "./"+mjd+"/"+beam+"/balance0000.dat"
        try:
            t0=ascii.read(tab_path)
        except IOError:
            print tab_path," not found. Moving on to next file."
            continue
        print "Opened ",tab_path
        data=np.array(t0,copy=False)
        tempdec=data['DEC']
        tempra=data['RA']
        for i in range(len(tempdec)):
            if ramin < tempra[i] < ramax and decmin < tempdec[i] < decmax:
                x= n1-(tempra[i]-ramin)/cellsize
                y= (tempdec[i]-decmin)/cellsize
                dayplane[x,y]=1
            else:
                continue
    if idx == 0:
        cube = dayplane
    else:
        cube = np.dstack([cube,dayplane])
        print "plane added to existing cube, shape is now ",cube.shape

print "Final cube has shape ",cube.shape

#outpath_fits="./"
outfile="track_cube_"+field+".fits"  #change this as required

print "Writing fits file to "+outfile

fits.writeto(outfile,cube)

print"done!"
                         
