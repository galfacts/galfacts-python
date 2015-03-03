#!/usr/bin/python

import numpy as np
from astropy.io import fits
from astropy.io import ascii
import sys
import struct


#Read in files one by one - use list of files
#Use list of beams + days read in from file to construct filenames
beams=[]
for b in range(0,7):
    beams.append("beam"+str(b))

print "beams used: ",beams

mjd_file=sys.argv[1]

mjds=open(mjd_file).read().splitlines()

for day in mjds:
    for beam in beams:
        print "Converting day {0}, {1}".format(day,beam)
        tabname="/local/scratch/Madam_test/galfacts/balance_data/"+day+"/"+beam+"/balance0000.dat"
        i_name="/local/scratch/Madam_test/galfacts/madam_output/tod/n4_I_"+beam+"_mjd_"+day+"_destriped.fits"
        q_name="/local/scratch/Madam_test/galfacts/madam_output/tod/n4_Q_"+beam+"_mjd_"+day+"_destriped.fits"
        u_name="/local/scratch/Madam_test/galfacts/madam_output/tod/n4_U_"+beam+"_mjd_"+day+"_destriped.fits"
        v_name="/local/scratch/Madam_test/galfacts/madam_output/tod/n4_V_"+beam+"_mjd_"+day+"_destriped.fits"
        temp_tab=ascii.read(tabname)
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

        dummy1="/local/scratch/Madam_test/galfacts/balance_data/"+day+"/"+beam+"/detstriped.dat"
        dummy2="/local/scratch/Madam_test/galfacts/balance_data/"+day+"/"+beam+"/destriped.dat_cfg"
        d=open(dummy1,'w')
        d.write('dummy data file')
        d.close()

        d=open(dummy2,'w')
        d.write('dummy config file')
        d.close()
        
        outname="/local/scratch/Madam_test/galfacts/balance_data/"+day+"/"+beam+"/average.dat"
        print "opening file ",outname
        ftemp=open(outname,'wb')
        ftemp.write(struct.pack('i',numrecords))

        for i in range(numrecords):
            row=i/5000
            index=i%5000
            ftemp.write(struct.pack('f',temp_tab['RA'][i]))
            ftemp.write(struct.pack('f',temp_tab['DEC'][i]))
            ftemp.write(struct.pack('f',temp_tab['AST'][i]))
            ftemp.write(struct.pack('f',idata['alfa'][row][index]))
            ftemp.write(struct.pack('f',qdata['alfa'][row][index]))
            ftemp.write(struct.pack('f',udata['alfa'][row][index]))
            ftemp.write(struct.pack('f',vdata['alfa'][row][index]))

        ftemp.close()

print "done!"
            
            
            
            
            
