
#This script must be run in the directory containing all the mjd directories.

import numpy as np
import sys
import os
import fnmatch
import getopt
from astropy.io import ascii
from astropy.io import fits

## def make_psf_map(fwhm, cellsize, beamwidths):
##     scale = cellsize * 60.0
##     radius = beamwidths * fwhm / scale
##     maxdist = radius * scale

##     psf_map_size = radius*2+1
##     psf_map=np.zeros((psf_map_size,psf_map_size))
##     for i in range(psf_map_size):
##         for j in range(psf_map_size):
##             xpos=i-radius
##             ypos=j-radius
##             dist=sqrt(xpos**2+ypos**2)*scale
##             if  dist > maxdist:
##                 psf_map[i,j] = 0.0
##             else:
##                 psf_map[i,j] = np.exp(-2.772589*(dist/fwhm)*(dist/fwhm))

##     return psf_map_size,psf_map

def usage():
    print "Usage of view_tracks.py:"
    print "This script must be run in a directory containing all the mjd directories from cal output, e.g. /researchdata/fhgfs/arecibo-scratch/s1band0/"
    print "view_tracks.py -l (or --lookup) x y example.npy field outputs a list of beam/mjd combinations contributing to the pixel (x,y), if a lookup table is present"
    print "view_tracks.py -f (or --fits) outfile.fits field generates a fits cube with one plane per day showing which days contribute to which pixel"
    print "view_tracks.py -t (or --table) outfile field generates a lookup table in binary .npy format which can then be read using the -l flag"

def get_mjds():
    beams=[]
    for b in range(0,7):
        beams.append("beam"+str(b))

    files=next(os.walk('.'))[1]
    mjds=fnmatch.filter(files,'55[0-9][0-9][0-9]')
    if len(mjds) < 1:
        print "Error: no mjd directories in working dir"
        sys.exit(0)
    mjds.sort()

    return beams,mjds

def get_field_params(field_name): #gets ra and dec min and max, and map size, for a given field.
    if field_name == 's1':
        #insert ramin and ramax settings
        ramin = 59.1
        ramax = 145.0
        decmin = -0.875
        decmax = 17.025
        n1=5155
        n2=1074

    #if field_name == 's2':

    #if field_name == 's3':

    #if field_name == 's4':

    #if field_name == 'n1':

    #if field_name == 'n2':

    #if field_name == 'n3':

    #if field_name == 'n4':

    return ramin, ramax, decmin, decmax, n1, n2

    

def lookup(x,y,infile,field):
    try:
        lookup_tab=np.load(infile)
    except IOError:
        print "Error: No lookup table found. Generate one by running this script with flag -t"
        sys.exit(0)
    beams,mjds=get_mjds()
    mjds=np.array(mjds)
    ramin,ramax,decmin,decmax,n1,n2=get_field_params(field)
    print "Looking up beam/day combinations contributing to pixel ("+x+","+y+")"
    x_int,y_int=int(x),int(y)
    bit_int_arr=np.empty(len(beams))
    for i in range(len(beams)):
        bit_int_arr[i]=lookup_tab[i,x_int*n1+y_int]
    bit_int_arr.astype('uint32',copy=False)
    bin_string_arr=[]
    for i in range(len(beams)):
        bin_string=bin(bit_int_arr[i].astype('uint32'))[2:]
        bin_string_arr.append(bin_string)

    
    table_output=field+'_'+x+'_'+y+'_lookup.txt'
    f=open(table_output,'w')
    f.write("Beam/day combinations corresponding to pixel ("+x+","+y+") \n")
    for i,beam in enumerate(beams):
        s=(len(mjds)-len(bin_string_arr[i]))*'0'+bin_string_arr[i]
        a=np.asarray(list(s),dtype='int').astype(bool)
        mjds_temp=mjds[a]
        f.write("\n")
        f.write(beam+": \n")
        print beam+":"
        if len(mjds_temp)<1:
            print "none"
            f.write("none \n")
        else:
            for mjd in mjds_temp:
                f.write(mjd+"\n")
                print mjd
    f.close()
    print "Output also written to "+table_output
    
    
    
def make_fits(field,outfile):
    #get constants, list of beams and mjds
    cellsize=1./60.
    beams,mjds=get_mjds()
    ramin,ramax,decmin,decmax,n1,n2=get_field_params(field)
    
    print "number of days to process: ",len(mjds)
    print "total files to process: ",len(mjds)*len(beams)

    #initialise fits cube
    cube=np.zeros((len(mjds),n2,n1))

    print "Creating cube for FITS file"

    #loop over beams and mjds
    for beam in beams:
        print "processing beam ",beam

        for idx,mjd in enumerate(mjds):
            tab_path= "./"+mjd+"/"+beam+"/balance0000.dat"
            try:
                t0=ascii.read(tab_path) #open balance data file
            except IOError:
                print tab_path," not found. Moving on to next file."
                continue
            print "Opened ",tab_path
            data=np.array(t0,copy=False)
            tempdec=data['DEC']
            tempra=data['RA']
            for i in range(len(tempdec)): # loop through data, finding the corresponding pixel in the right plane and setting it to one
                if ramin < tempra[i] < ramax and decmin < tempdec[i] < decmax:
                    x=int(n1-(tempra[i]-ramin)/cellsize)
                    y=int((tempdec[i]-decmin)/cellsize)
                    cube[idx,y,x]=1
                else:
                    continue

    print "final cube has shape ",cube.shape
    

    print "Writing fits file to "+outfile

    head=fits.Header()
    head['COMMENT'] = "Ordered list of mjds in cube, one per plane:"
    for day in mjds:
        head['COMMENT']=day
    hdu=fits.PrimaryHDU(cube,header=head)
    hdulist=fits.HDUList([hdu])
    hdulist.writeto('outfile')
)

def make_table(field, outfile):

    #get constants, list of beams and mjds
    cellsize=1./60.
    beams,mjds=get_mjds()
    ramin,ramax,decmin,decmax,n1,n2=get_field_params(field)

    print "number of days to process: ",len(mjds)
    print "total files to process: ",len(mjds)*len(beams)

    #initialise table of values
    table_array=np.empty((len(beams),n1*n2))
    print "Creating lookup table"

    #loop over mjds, beams
    for b_ind,beam in enumerate(beams):
        print "processing beam ",beam
        beam_cube=np.zeros((len(mjds),n2,n1)) #temporary cube is made for each beam
        for idx,mjd in enumerate(mjds):
            tab_path= "./"+mjd+"/"+beam+"/balance0000.dat"
            try:
                t0=ascii.read(tab_path) #open the balance data file
            except IOError:
                print tab_path," not found. Moving on to next file."
                continue
            print "Opened ",tab_path
            data=np.array(t0,copy=False)
            tempdec=data['DEC']
            tempra=data['RA']
            for i in range(len(tempdec)): # loop through data, finding the corresponding pixel in the right plane and setting it to one
                if ramin < tempra[i] < ramax and decmin < tempdec[i] < decmax:
                    x=int(n1-(tempra[i]-ramin)/cellsize)
                    y=int((tempdec[i]-decmin)/cellsize)
                    beam_cube[idx,y,x]=1
                else:
                    continue
        bitwise_map=np.zeros((n2,n1)) #initialise 2d array which will hold info about pixels in a bit-per -bit basis
        for x in range(n1):
            for y in range(n2):
                print x,y
                bitwise_map[y,x]=np.uint32(int( "".join(np.asarray(beam_cube[:,y,x].astype(int),dtype='str')),2))
        table_array[b_ind,:]=np.ravel(bitwise_map) #store this int in an array with (n1*n2) rows and len(beams) columns
    print "Writing out lookup table in .npy binary format"
    np.save(outfile,table_array)

    

    

def main(argv):
    if len(argv)<1:
        print "Please provide appropriate arguments"
        usage()
        sys.exit(0)
    try:
        opts,args=getopt.getopt(argv,"hlf:t:",["help","lookup","fits=","table="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-l","--lookup"):
            x=args[0]
            y=args[1]
            infile=args[2]
            field=args[3]
            lookup(x,y,infile,field)
        elif opt in ("-f","--fits"):
            outfile=arg
            field=args[0]
            make_fits(field,outfile)
        elif opt in ("-t","--table"):
            outfile=arg
            field=args[0]
            make_table(field,outfile)
        elif opt in ("-h","--help"):
            usage()
            sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
            


                         
