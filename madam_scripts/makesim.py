#!/usr/bin/python

#This script makes the parameter and simulation files for a given field/baseline combination. The destriping resolution is nside. Run this from the field directory e.g. s1, n4...
import os

field='s1'
baseline='pp'
nside= '2048'
pp=True
pp_baseline='3000'

stokes=['I','Q','U','V']
pntfiles=next(os.walk('./pnt'))[2]
pntfiles.sort()
nofiles=len(pntfiles)

for param in stokes:
 
 simfile_alpher="./params/simulation_"+field+"_"+param+"_"+baseline+"_"+nside+".txt"
 simfile_coma="/share/c48/leclercq/v0.2/s1/params/simulation_"+field+"_"+param+"_"+baseline+"_"+nside+".txt"
 parfile_alpher="./params/parameters_"+field+"_"+param+"_"+baseline+"_"+nside+".par"
 parfile_coma="/share/c48/leclercq/v0.2/s1/params/parameters_"+field+"_"+param+"_"+baseline+"_"+nside+".par"
 pathpoint="/share/c48/leclercq/v0.2/s1/pnt/"
 pathtod="/share/c48/leclercq/v0.2/s1/tod/b"+baseline+"/"+nside+"/stokes"+param+"/"
 f=open(parfile_alpher,'w')
 f.write("#parameters for program Madam, version 3.7.4\n")
 f.write("#\n")
 f.write("#\n")
 f.write("simulation     =     "+simfile_coma+"\n")
 f.write("tod1           =     galfacts"+param+"\n")
 f.write("info           =      5\n")
 f.write(" \n")
 f.write("#detectors\n")
 f.write("detector_1     =     galfacts"+param+"\n")
 f.write(" \n")
 f.write("#Destriping scheme\n")
 f.write(" \n")
 f.write("kfirst	 =      T     #default\n")
 f.write("ksecond    	 =      F	   #default\n")
 f.write("kfilter        =      F	   #default\n")
 if param == 'I':
  f.write("file_inmask = /share/c48/leclercq/v0.2/s1/"+field+"_mask_3.8K_"+nside+".fits  #the mask input file\n")
 f.write(" \n")
 f.write("#Baseline length\n")
 f.write(" \n")
 if (pp):
   f.write("base_first="+pp_baseline+" # baseline length/samples\n")
   f.write("file_pntperiod = /share/c48/leclercq/v0.2/s1/s1_pp.txt\n")
 else:
   f.write("base_first="+baseline+" # baseline length/samples\n")
 f.write(" \n")
 f.write("#Resolution\n")
 f.write(" \n")
 f.write("nside_map ="+nside+"    #default\n")
 f.write(" \n")
 f.write("#Output\n")
 f.write(" \n")
 f.write("path_output =      /share/c48/leclercq/v0.2/"+field+"/output\n")
 f.write("file_map = galfacts_"+field+"_"+param+"_"+nside+".fits\n")
 f.write("write_tod = T\n")
 f.write(" \n")
 f.write("#Other stuff\n")
 f.write(" \n")
 f.write("noloops_time =      1\n")
 f.write("noloops_point =	     1\n")
 f.write("noloops_buffer =	     1\n")
 f.write("mission_time =	     0\n")
 f.write("start_time =	     0\n")


 g=open(simfile_alpher,'w')
 g.write("# file: "+simfile_coma+"\n")
 g.write("#\n")
 g.write("fsample = 5\n")
 g.write("nofiles = "+str(nofiles)+"\n")
 g.write("#\n")
 g.write("# TOD components\n")
 g.write("#          tod_ID   weight   name\n")
 g.write("tod_info =    1       1      galfacts"+param+"\n")
 g.write("#\n")
 g.write("# detector info\n")
 g.write("#                 det_ID  psi_pol  pol  sigma  slope  fknee  fmin  point_ID  name\n")
 g.write("detector_info  =    1      0.0       F      1.  -1.7    na    na         1    galfacts"+param+"\n")
 g.write("#\n")
 g.write("# pointing info\n")
 g.write("#                 point_id   phi_uv   theta_uv  psi_uv\n")
 g.write("#\n")
 g.write("# detector pointing files\n")
 g.write("path_point   =        "+pathpoint+"\n")
 for i in range (0,nofiles):
     g.write("file_point   =  1   "+pntfiles[i]+"\n")
 g.write("#\n")
 g.write("# TOD files\n")
 g.write("#            tod_ID det_ID\n")
 g.write("path_tod   =   1       "+pathtod+"\n")
 todfiles=next(os.walk('./tod/raw/stokes'+param))[2]
 todfiles.sort()
 notodfiles=len(todfiles)
 for j in range(0,notodfiles):
     g.write("file_tod   = 1   1  "+todfiles[j]+"\n")
 g.close()

 
 

