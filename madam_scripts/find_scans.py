#!/usr/bin/python

#Python script that reads in the ascii balance files and determines the length and number of up and down scans on a beam-by-beam basis. Run this in s1band0/raw

import sys
import os
import numpy as np
from astropy.io import ascii

field = "s1"

#get mjds and beams:

beams=[]
for b in range(0,7):
    beams.append("beam"+str(b))

mjds=next(os.walk('.'))[1]
mjds.sort()

print "total files to process: ",len(mjds)*len(beams)

scan_no = 0

scan_lengths=[]
ss_no = 1
n1=0
n2=0

for beam in beams:
    print "processing days in ",beam
    for mjd in mjds:
        up = False
        down = False
        tab_path= "./"+mjd+"/"+beam+"/balance0000.dat"
        file_scan_no=0
        try:
            t0=ascii.read(tab_path)
        except IOError:
            print tab_path," not found. Moving on to next file."
            continue
        print "Opened ",tab_path
        data=np.array(t0,copy=False)
        dec=data['DEC']
        if (file_scan_no == 0 and n1 == 0 and n2 == 0 ):
            n1=dec[0]
            n2=dec[1]
        else:
            n1=n2
            n2=dec[i]
        for i in range (1,len(dec)):
            if ( n2 > n1 ):
                if( up ):
                    ss_no += 1
                else:
                    if(file_scan_no == 1):
                        ss_no+=1
                    if(file_scan_no > 0):
                        scan_lengths.append(ss_no)    
                    scan_no += 1
                    file_scan_no +=1
                    #print "Starting scan",scan_no," at sample ",i-1
                    ss_no = 1
                    up = True
                    down = False
            elif (n2 < n1):
                if(down):
                    ss_no += 1
                else:
                    if(file_scan_no == 1):
                        ss_no += 1
                    if (file_scan_no > 0):
                        scan_lengths.append(ss_no)
                    scan_no += 1
                    file_scan_no += 1
                    #print "Starting scan",scan_no," at sample ",i-1
                    ss_no = 1
                    down = True
                    up = False
            n1=n2
            n2=dec[i]
        ss_no += 1
        scan_lengths.append(ss_no)
        n1=0
        n2=0
        
        #print "number of scans in file",file_scan_no
        #print "number of samples in file: ",len(dec)
        #print "sum of samples in scans:",np.sum(np.array(scan_lengths)[scan_no-file_scan_no:scan_no])
        
        
            
print "scans found, writing out to s1_pp.txt"
f=open("../s1_pp.txt",'w')
f.write(scan_no)
for j in range(scan_no):
    f.write(str(j+1)+" "+str(scan_lengths[j])+"\n")
f.close()
        

    
        
        
