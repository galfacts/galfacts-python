#!/Users/leclercq/miniconda/bin/python

import numpy as np 
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pylab as plt
import gaussbeam
import sys
from numpy import pi
from astropy.io import fits
from scipy import integrate
from scipy import stats
from astropy import units as u
from astropy.coordinates import Longitude
from astropy.coordinates import Latitude

i_in=sys.argv[1]
q_in=sys.argv[2]
u_in=sys.argv[3]
chunk=sys.argv[4]
scale=sys.argv[5]

field=i_in[9:11]


######################################################
#General utilities; consider writing separate function

#define pixel step and pixel area in rad
pixstep=pi/(60.*180.)
pixarea=pixstep**2

#Generate white noise as reference scaling factor
wnoise=np.random.randn(1024,1024)
wnoiseft=np.fft.fftshift(np.fft.fft2(wnoise))
wnoiseft2=(wnoiseft*np.conj(wnoiseft)).real
noisepwr_rms=np.sqrt(np.mean(wnoiseft2**2))
scaling=noisepwr_rms/pixarea


#Calculate area of FT'd chunk in steradian

def dA_Sphere(phi, theta):
        return  np.sin(phi)

def chunk_area(field):
    if field =='S1':
        rastart=Longitude('03h15m').radian
        rastop=Longitude('09h40m').radian
        decstop=pi/2.-Latitude('-01d05m').radian
        decstart=pi/2.-Latitude('17d07m').radian

    elif field =='S2':
        rastart=Longitude('09h30m').radian
        rastop=Longitude('15h40m').radian
        decstop=pi/2.-Latitude('-01d05m').radian
        decstart=pi/2.-Latitude('17d07m').radian

    elif field =='S3':
        rastart=Longitude('15h30m').radian
        rastop=Longitude('21h40m').radian
        decstop=pi/2.-Latitude('-01d05m').radian
        decstart=pi/2.-Latitude('17d07m').radian
        
    elif field =='N3':
        rastart=Longitude('13h10m').radian
        rastop=Longitude('19h10m').radian
        decstop=pi/2.-Latitude('19d42m').radian
        decstart=pi/2.-Latitude('37d20m').radian

    elif field =='N4':
        rastart=Longitude('00h00m').radian
        rastop=Longitude('06h20m').radian
        decstop=pi/2.-Latitude('19d42m').radian
        decstart=pi/2.-Latitude('37d20m').radian

    omega,erromega=integrate.dblquad(dA_Sphere, rastart, rastop, lambda theta: decstart, lambda theta: decstop )

    return omega
    
#######################################################


# first step is to get images and import header and data into numpy arrays, scale is either 'dl' or 'cl'

gal_hdu=fits.open(i_in) 
gal_im=gal_hdu[0].data
gal_im=np.asarray(gal_im[0,20:1044,0:5120])
gal_head=gal_hdu[0].header

q_hdu=fits.open(q_in) 
q_im=q_hdu[0].data
q_im=np.asarray(q_im[0,20:1044,0:5120])
q_head=q_hdu[0].header

u_hdu=fits.open(u_in) 
u_im=u_hdu[0].data
u_im=np.asarray(u_im[0,20:1044,0:5120])
u_head=u_hdu[0].header

#Asisgn zero to blanks

q_nan=np.where(np.isnan(q_im))
q_im[q_nan]=0.0

u_nan=np.where(np.isnan(u_im))
u_im[u_nan]=0.0

gal_nan=np.where(np.isnan(gal_im))
gal_im[gal_nan]=0.0

#Divide images into 5 1024x1024 chunks

gal_im_0=np.asarray(gal_im[:,0:1024])
gal_im_1=np.asarray(gal_im[:,1024:2048])
gal_im_2=np.asarray(gal_im[:,2048:3072])
gal_im_3=np.asarray(gal_im[:,3072:4096])
gal_im_4=np.asarray(gal_im[:,4096:5120])

u_im_0=np.asarray(u_im[:,0:1024])
u_im_1=np.asarray(u_im[:,1024:2048])
u_im_2=np.asarray(u_im[:,2048:3072])
u_im_3=np.asarray(u_im[:,3072:4096])
u_im_4=np.asarray(u_im[:,4096:5120])

q_im_0=np.asarray(q_im[:,0:1024])
q_im_1=np.asarray(q_im[:,1024:2048])
q_im_2=np.asarray(q_im[:,2048:3072])
q_im_3=np.asarray(q_im[:,3072:4096])
q_im_4=np.asarray(q_im[:,4096:5120])

#Do FTs

if chunk == 'all':

    ft0=np.fft.fftshift(np.fft.fft2(gal_im_0))
    ft1=np.fft.fftshift(np.fft.fft2(gal_im_1))
    ft2=np.fft.fftshift(np.fft.fft2(gal_im_2))
    ft3=np.fft.fftshift(np.fft.fft2(gal_im_3))
    ft4=np.fft.fftshift(np.fft.fft2(gal_im_4))

    qft0=np.fft.fftshift(np.fft.fft2(q_im_0))
    qft1=np.fft.fftshift(np.fft.fft2(q_im_1))
    qft2=np.fft.fftshift(np.fft.fft2(q_im_2))
    qft3=np.fft.fftshift(np.fft.fft2(q_im_3))
    qft4=np.fft.fftshift(np.fft.fft2(q_im_4))

    uft0=np.fft.fftshift(np.fft.fft2(u_im_0))
    uft1=np.fft.fftshift(np.fft.fft2(u_im_1))
    uft2=np.fft.fftshift(np.fft.fft2(u_im_2))
    uft3=np.fft.fftshift(np.fft.fft2(u_im_3))
    uft4=np.fft.fftshift(np.fft.fft2(u_im_4))

    ftstack=np.dstack((ft0,ft1,ft2,ft3,ft4))
    uftstack=np.dstack((uft0,uft1,uft2,uft3,uft4))
    qftstack=np.dstack((qft0,qft1,qft2,qft3,qft4))

    ft_final=np.mean(ftstack,axis=2)
    uft_final=np.mean(uftstack,axis=2)
    qft_final=np.mean(qftstack,axis=2)

elif chunk == '0':
    #print 'Taking FT of chunk 0'
    ft_final=np.fft.fftshift(np.fft.fft2(gal_im_0))
    qft_final=np.fft.fftshift(np.fft.fft2(q_im_0))
    uft_final=np.fft.fftshift(np.fft.fft2(u_im_0))

elif chunk == '1':
    ft_final=np.fft.fftshift(np.fft.fft2(gal_im_1))
    qft_final=np.fft.fftshift(np.fft.fft2(q_im_1))
    uft_final=np.fft.fftshift(np.fft.fft2(u_im_1))

elif chunk == '2':
    ft_final=np.fft.fftshift(np.fft.fft2(gal_im_2))
    qft_final=np.fft.fftshift(np.fft.fft2(q_im_2))
    uft_final=np.fft.fftshift(np.fft.fft2(u_im_2))

elif chunk == '3':
    ft_final=np.fft.fftshift(np.fft.fft2(gal_im_3))
    qft_final=np.fft.fftshift(np.fft.fft2(q_im_3))
    uft_final=np.fft.fftshift(np.fft.fft2(u_im_3))

elif chunk == '4':
    ft_final=np.fft.fftshift(np.fft.fft2(gal_im_4))
    qft_final=np.fft.fftshift(np.fft.fft2(q_im_4))
    uft_final=np.fft.fftshift(np.fft.fft2(u_im_4))

else :
    print 'Invalid chunk'
    exit()



print 'end of if loop'
#get fft spatial frequencies
freq_1d=np.fft.fftshift(np.fft.fftfreq(1024,pixstep))

ell_1d= 2*pi*freq_1d

ellx,elly=np.meshgrid(ell_1d,ell_1d)

#define radii of constant ell
ell_r=np.sqrt((ellx)**2+(elly)**2)
ell_ref=ell_r

#set up grid of phis
phi_ell=np.arctan2(elly,ellx)


#divide out beam

ft_beam=gaussbeam.makeFTgaussian(1024,fwhm=3.5)

ft_final=ft_final/ft_beam
uft_final=uft_final/ft_beam
qft_final=qft_final/ft_beam

#Calculate E and B mode functions

emode=qft_final*np.cos(2.*phi_ell)+uft_final*np.sin(2.*phi_ell)
bmode=-qft_final*np.sin(2.*phi_ell)+uft_final*np.cos(2.*phi_ell)

#compute correlations (EE,BB) and scale these
ft_pwr=(ft_final*np.conj(ft_final)).real
ee=(emode*np.conj(emode)).real
bb=(bmode*np.conj(bmode)).real

ft_scaled=ft_pwr/scaling
ee_scaled=ee/scaling
bb_scaled=bb/scaling

#Calculate field area

#sph_area=chunk_area(field)
area1024=pixarea*(1024**2)

#Figure out where the beam goes to half its peak value
halfbeam=np.where(ft_beam < 0.5)

#create bins - single integer ell values for 2-52 and then logarithmically spaced for the rest.
ell_ref[halfbeam]=0.0
ell_max=np.max(ell_ref)

print ell_max

#ell_max=np.max(ell_r).astype(np.int)
bins_low=np.arange(2,53).astype(np.uint64)
bins_high=np.logspace(np.log10(20.0),np.log10(ell_max),50).astype(np.uint64)
bins=bins_high
ell_scale=bins*(bins+1)/2.*pi
#print bins

#get simulated point source contribution
sourcesim=fits.getdata('/Users/leclercq/galfacts/source_sim.fits')
ftsources=np.fft.fftshift(np.fft.fft2(sourcesim))
source_pwr=(ftsources*np.conj(ftsources)).real
source_scaled=source_pwr/scaling


#use histogram function to take average (using weights)

power_hist=np.histogram(ell_r,bins,weights=ft_scaled)[0]
ell_hist=np.histogram(ell_r,bins)[0]
power_average=np.zeros(power_hist.size)
nonzero=np.where(power_hist!=0)
power_average[nonzero]=area1024*power_hist[nonzero]/ell_hist[nonzero]
#print power_average
if scale == 'dl':
    d_ell=power_average*ell_scale[1:]

ee_hist=np.histogram(ell_r,bins,weights=ee_scaled)[0]
ee_average=np.zeros(ee_hist.size)
nonzero_ee=np.where(ee_hist!=0)
ee_average[nonzero_ee]=area1024*ee_hist[nonzero_ee]/ell_hist[nonzero_ee]

if scale == 'dl':
    ee_dl=ee_average*ell_scale[1:]
    

bb_hist=np.histogram(ell_r,bins,weights=bb_scaled)[0]
bb_average=np.zeros(bb_hist.size)
nonzero_bb=np.where(bb_hist!=0)
bb_average[nonzero_bb]=area1024*bb_hist[nonzero_bb]/ell_hist[nonzero_bb]
if scale =='dl':
    bb_dl=bb_average*ell_scale[1:]

source_hist=np.histogram(ell_r,bins,weights=source_scaled)[0]
source_average=np.zeros(source_hist.size)
nonzero_source=np.where(source_hist!=0)
source_average[nonzero_source]=area1024*source_hist[nonzero_source]/ell_hist[nonzero_source]
print source_average
if scale == 'dl':
    source_dl=source_average*ell_scale[1:]

#plot plot plot


bins_center=np.zeros((bins_high.size)-1)

for i in range((bins_high.size)-1):
    bins_center[i]=bins_high[i]+(bins_high[i+1]-bins_high[i])/2.

bins_axis=bins_center

##if scale =='dl':
    #poissona,poissonb,c,d,e=stats.linregress(np.log10(bins_axis[nonzero][17:25]),np.log10(d_ell[nonzero][17:25]))
    #print poissona,poissonb

if scale == 'dl':
    outfile='dl_data'+field+'_c'+chunk+'.txt'
    np.savetxt(outfile,(bins_center,d_ell,ee_dl,bb_dl,source_dl))

else:
    outfile='cl_data'+field+'_c'+chunk+'.txt'

nz=np.asarray([nonzero,nonzero_ee,nonzero_bb,nonzero_source])
#print nz
np.savetxt(outfile,(bins_center,power_average,ee_average,bb_average,source_average))

np.save('nonzeros'+field+'_c'+chunk,nz)



