#!/usr/bin/python

#This script takes the field name as argument, and must be run in the directory containing all the mjd directories.

import numpy as np
import sys
import os
import fnmatch
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

files=next(os.walk('.'))[1]
mjds=fnmatch.filter(files,'55[0-9][0-9][0-9]')
mjds.sort()

print "number of days to process: ",len(mjds)
print "total files to process: ",len(mjds)*len(beams)

cube=np.zeros((len(mjds),n2,n1))

for idx,mjd in enumerate(mjds):
    print "processing day ",mjd
    
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
                x=int(n1-(tempra[i]-ramin)/cellsize)
                y=int((tempdec[i]-decmin)/cellsize)
                cube[idx,y,x]=1
            else:
                continue

print "final cube has shape ",cube.shape


#outpath_fits="./"
outfile="track_cube_"+field+".fits"  #change this as required

print "Writing fits file to "+outfile

fits.writeto(outfile,cube)

print"done!"
                         
