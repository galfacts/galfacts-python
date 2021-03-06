#!/opt/exp_soft/python-2.7.3/bin/python

#Python version of stack2 IDL program created to average down ~300 channel GALFACTS cubes for estimation of noise dependence and angles.
# run using: python stack2.py path_to_input 

#bad_channels must be a tuple of individual channel numbers and/or slice objects for a range of contiguous channels, e.g. (56,slice(75,96),134,slice(300,321)) will remove channels 57, 76-96, 135, 301-321 based on the cyberSKA viewer indexing which starts at 1.



import sys
import numpy as np 
from astropy.io import fits


#Get command line argument

filein=sys.argv[1]
bad=(59,112,178,slice(248,251),slice(331,375))
stokes=filein[32]

#Read in fits file
cube_hdu=fits.open(filein,ignore_missing_end=True)
cube_im=cube_hdu[0].data
cube_head=cube_hdu[0].header

#Get shape of cube, create array with same number of channels
s=np.shape(cube_im)
nchan=s[0]
channels=np.arange(nchan)

#Create array containing frequencies
f0=cube_head['CRVAL3']
df=cube_head['CDELT3']
freq=np.arange(nchan)*df+f0

#Set up array of bad channel indices using the provided tuple of slices and individual indices
elem_bad=len(bad)
badchans=np.array([])

for i in xrange(elem_bad):
    badchans=np.hstack((badchans,channels[bad[i]]))

nchan_bad=np.size(badchans)
nchan_good=nchan-nchan_bad

print '{0} good channels'.format(nchan_good)

#Create new cube with bad channels completely removed

badchans=badchans.astype('int')
goodchans=np.delete(channels,badchans)
goodfreq=np.delete(freq,badchans)
goodcube=cube_im[goodchans,:,:]

print np.shape(goodcube)



#Set up averaging loop
width=10
bins=nchan_good/width
bins_r=np.remainder(nchan_good,width)
print 'There will be {0} bins, of which the first {1} will contain 11 channels and the remaining {2} will contain 10'.format(bins,bins_r,bins-bins_r)


k0=0
k1=0

binned_cube=np.empty((bins,s[1],s[2]))
err_cube=np.empty((bins,s[1],s[2]))
mfr=np.empty(bins)
bin_numbers=np.empty(bins)
start_channel=np.empty(bins)
end_channel=np.empty(bins)

#the loop itself

for i_bin in xrange(bins):

    if i_bin < bins_r:
        binw=11
    else:
        binw=10
        
    k1=k1+binw
    print 'Start of loop {2}: k0 = {0}, k1={1}'.format(k0,k1, i_bin)
    print 'Averaging channels {0} to {1} into bin {2}'.format(goodchans[k0],goodchans[k1-1],i_bin)

    binned_cube[i_bin,:,:]=np.nanmean(goodcube[k0:k1,:,:],axis=0)

    err_cube[i_bin]=np.nanstd(goodcube[k0:k1,:,:],axis=0)

    mfr[i_bin]=np.nanmean(goodfreq[k0:k1])

    start_channel[i_bin]=goodchans[k0]

    end_channel[i_bin]=goodchans[k1-1]

    bin_numbers[i_bin]=i_bin

    k0=k1


#Format list of bad channels to be written to header

badstring=np.array_str(badchans,max_line_width=68)
comments=badstring.split('\n')
comlen=len(comments)

#
#Modify the header and write new file as the primary binned image, an image extension with the error, and a binary table containing bin number, start channel and end channel.

cube_head['EXTEND']=('T',)
cube_head['CRPIX3']=(1.0)
cube_head['CDELT3']=(1.0)
cube_head['CRVAL3']=(1.0)
cube_head['BUNIT']=('K')
cube_head['OBJECT']=('GALFACTS S2 3.1.1 Stokes {0}'.format(stokes))
#cube_head['CTYPE3']=('FREQUENCY')
cube_head['ORIGINAL']=(filein,'Original file')
cube_head['COMMENT']='{0} channels in original'.format(nchan)
cube_head['COMMENT']='Channels removed (starting at 0):'
for ic in range(comlen):
    cube_head['COMMENT']=comments[ic]

print 'Setting up fits file and extensions...'
#Write the actual data:

#create primary HDU and HDUlist
binnedhdu=fits.PrimaryHDU(binned_cube,header=cube_head)
binnedhdulist=fits.HDUList([binnedhdu])

#create image extension with binning stdev and append to existing hdulist
cube_head['OBJECT']=('GALFACTS binned S2 error map')
errhdu=fits.ImageHDU(err_cube,header=cube_head)
binnedhdulist.append(errhdu)

#create binary table extension and append to existing hdulist

col1=fits.Column(name='bin',format='d',array=bin_numbers)
col2=fits.Column(name='start_channel',format='d', array=start_channel)
col3=fits.Column(name='end_channel',format='d', array=end_channel)
col4=fits.Column(name='mean_frequency',format='E',array=mfr)

cols=fits.ColDefs([col1,col2,col3,col4])
bintablehdu=fits.BinTableHDU.from_columns(cols)

binnedhdulist.append(bintablehdu)



fileout='/local/scratch/GALFACTS/3.1.2/s2band0/binned/S2_binned_'+stokes+'.fits'


print '...done!'
#write to file:
print 'Writing to file'
binnedhdulist.writeto(fileout)
print 'The binned file has been written to {0}'.format(fileout)

    
    













































