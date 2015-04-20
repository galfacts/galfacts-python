#!/usr/bin/python

#This script takes the field name as argument, and must be run in the directory containing all the mjd directories.

import numpy as np
import sys
import os
from astropy.io import ascii
from astropy.io import fits

def writetemptablefits(datarray,outfile,colname):
 col=fits.Column(name=colname,format='1E',array=datarray)
 tbhdu=fits.BinTableHDU.from_columns([col])
 tbhdu.writeto(outfile)
 return

def writepointfits(pointarray1,pointarray2,outsamples,outfile):
 col1=fits.Column(name='theta',format='1D',array=pointarray1)
 col2=fits.Column(name='phi',format='1D',array=pointarray2)
 col3=fits.Column(name='psi',format='1D',array=np.zeros(outsamples,dtype=np.float64))
 cols=fits.ColDefs([col1,col2,col3])
 tbhdu=fits.BinTableHDU.from_columns(cols)
 tbhdu.writeto(outfile)
 return

field=sys.argv[1]
nobeams=7

outpath_tod="/local/scratch/Madam_test/v0.2/"+field+"/tod/"
outpath_pnt="/local/scratch/Madam_test/v0.2/"+field+"/pnt/"

days=next(os.walk('.'))[1]
print "List of days: ",days
nofiles=len(days)    

for i in range(nobeams):
 
 print "processing beam", i
 for j in range (0,nofiles):
  filename="./"+days[j].rstrip()+"/beam"+str(i) +"/balance0000.dat"
  print "reading in file"
  try:
   t0=ascii.read(filename)
  except IOError:
   print "There is no", filename
   continue
  data=np.array(t0,copy=False)
  print "writing out file number {0} of {1}".format((i*nofiles)+j+1, nofiles*nobeams)
  i_fileout=outpath_tod+"stokesI/"+field+"_I_beam"+str(i)+"_mjd_"+days[j].rstrip()+".fits"
  q_fileout=outpath_tod+"stokesQ/"+field+"_Q_beam"+str(i)+"_mjd_"+days[j].rstrip()+".fits"
  u_fileout=outpath_tod+"stokesU/"+field+"_U_beam"+str(i)+"_mjd_"+days[j].rstrip()+".fits"
  v_fileout=outpath_tod+"stokesV/"+field+"_V_beam"+str(i)+"_mjd_"+days[j].rstrip()+".fits"
  point_fileout=outpath_pnt+field+"_pnt_beam"+str(i)+"_mjd_"+days[j].rstrip()+".fits"
  
  writetemptablefits(data['I'],i_fileout,'I_TOD')
  writetemptablefits(data['Q'],q_fileout,'Q_TOD')
  writetemptablefits(data['U'],u_fileout,'U_TOD')
  writetemptablefits(data['V'],v_fileout,'V_TOD')
  writepointfits(90.0-data['DEC'],data['RA'],len(t0),point_fileout)


print"done!"
                         
