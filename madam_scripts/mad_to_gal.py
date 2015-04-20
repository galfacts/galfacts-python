#!/usr/bin/python

import numpy as np
from astropy.io import fits
from astropy.io import ascii
import sys
import os
import struct


#Read in files one by one - use os.walk
#Run from s1band0/raw
beams=[]
for b in range(0,7):
    beams.append("beam"+str(b))

print "beams used: ",beams

field=sys.argv[1]
baseline=sys.argv[2]
nside= sys.argv[3]

tab_dir="/local/scratch/Madam_test/v0.2/"+field+"band0/b"+baseline+"/"+nside+"/"
tod_dir="/local/scratch/Madam_test/v0.2/"+field+"/tod/b"+baseline+"/"+nside+"/"

mjds=next(os.walk('./raw'))[1]
mjds.sort()


for day in mjds:
    for beam in beams:
        print "Converting day {0}, {1}".format(day,beam)
        tabname=tab_dir+day+"/"+beam+"/balance0000.dat"
        i_name=tod_dir+"stokesI/"+field+"_I_"+beam+"_mjd_"+day+"_destriped.fits"
        q_name=tod_dir+"stokesQ/"+field+"_Q_"+beam+"_mjd_"+day+"_destriped.fits"
        u_name=tod_dir+"stokesU/"+field+"_U_"+beam+"_mjd_"+day+"_destriped.fits"
        v_name=tod_dir+"stokesV/"+field+"_V_"+beam+"_mjd_"+day+"_destriped.fits"
        try:
            temp_tab=ascii.read(tabname)
        except IOError:
            print "There is no",tabname
            continue
        numrecords=len(temp_tab)

        hdui=fits.open(i_name)
        idata=hdui[1].data
        hdui.close()
        
        hduq=fits.open(q_name)
        qdata=hduq[1].data
        hduq.close()
        
        hduu=fits.open(u_name)
        udata=hduu[1].data
        hduu.close()
        
        hduv=fits.open(v_name)
        vdata=hduv[1].data
        hduv.close()

        dummy1=tab_dir+day+"/"+beam+"/destriped.dat"
        dummy2=tab_dir+day+"/"+beam+"/destriped.dat_cfg"
        d=open(dummy1,'w')
        d.write('dummy data file')
        d.close()

        d=open(dummy2,'w')
        d.write('dummy config file')
        d.close()
        
        outname=tab_dir+day+"/"+beam+"/average.dat"
        print "opening file ",outname
        ftemp=open(outname,'wb')
        ftemp.write(struct.pack('i',numrecords))
        if (baseline == 'pp'):
            ibase=3000
        else:
            ibase=int(baseline)
        print numrecords
        print ibase
        print numrecords/ibase
        for i in range(numrecords):
            row=i/ibase
            index=i%ibase
            
            ftemp.write(struct.pack('f',temp_tab['RA'][i]))
            ftemp.write(struct.pack('f',temp_tab['DEC'][i]))
            ftemp.write(struct.pack('f',temp_tab['AST'][i]))
            ftemp.write(struct.pack('f',idata['galfactsI'][row][index]))
            ftemp.write(struct.pack('f',qdata['galfactsQ'][row][index]))
            ftemp.write(struct.pack('f',udata['galfactsU'][row][index]))
            ftemp.write(struct.pack('f',vdata['galfactsV'][row][index]))

        ftemp.close()

print "done!"
            
            
            
            
            
