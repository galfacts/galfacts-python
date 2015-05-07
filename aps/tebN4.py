#!/Users/leclercq/miniconda/bin/python

import numpy as np 
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pylab as plt
import gaussbeam
import sys
from numpy import pi
from astropy.io import fits

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
#######################################################


# first step is to get images and import header and data into numpy arrays

i_in=sys.argv[1]
q_in=sys.argv[2]
u_in=sys.argv[3]
chunk=sys.argv[4]
scale=sys.argv[5]

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

    print 'test'
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
    print 'Taking FT of chunk 0'
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

#set up grid of phis
phi_ell=np.arctan2(elly,ellx)

#Stack chunks and average



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

#create bins - single integer ell values for 2-52 and then logarithmically spaced for the rest.

ell_max=np.max(ell_r).astype(np.int)
bins_low=np.arange(2,53).astype(np.uint64)
bins_high=np.logspace(np.log10(53.0),np.log10(ell_max),30).astype(np.uint64)
bins=np.hstack((bins_low,bins_high))
ell_scale=bins*(bins+1)/2.*pi

#use histogram function to take average (using weights)

power_hist=np.histogram(ell_r,bins,weights=ft_scaled)[0]
ell_hist=np.histogram(ell_r,bins)[0]
power_average=np.zeros(power_hist.size)
nonzero=np.where(ell_hist!=0)
power_average[nonzero]=power_hist[nonzero]/ell_hist[nonzero]
if scale == 'dl':
    d_ell=power_average*ell_scale[1:]

ee_hist=np.histogram(ell_r,bins,weights=ee_scaled)[0]

ee_average=np.zeros(ee_hist.size)
nonzero_ee=np.where(ee_hist!=0)
ee_average[nonzero_ee]=ee_hist[nonzero_ee]/ell_hist[nonzero_ee]
if scale == 'dl':
    ee_dl=ee_average*ell_scale[1:]

bb_hist=np.histogram(ell_r,bins,weights=bb_scaled)[0]

bb_average=np.zeros(bb_hist.size)
nonzero_bb=np.where(bb_hist!=0)
bb_average[nonzero_bb]=bb_hist[nonzero_bb]/ell_hist[nonzero_bb]
if scale =='dl':
    bb_dl=bb_average*ell_scale[1:]

#plot plot plot

bins_center=np.zeros((bins_high.size)-1)

for i in range((bins_high.size)-1):
    bins_center[i]=bins_high[i]+(bins_high[i+1]-bins_high[i])/2.

bins_axis=np.hstack((bins_low,bins_center))

fig,ax=plt.subplots(figsize=(8,8))
title='TT,EE and BB power spectra of GALFACTS DR3.1 N4 map, chunk {0}'.format(chunk)
ax.set_title(title)
ax.set_xlabel('$\ell$',fontsize=16 )
if scale == 'dl':
    ax.plot(bins_axis,ee_dl,'+',label='EE')
    ax.plot(bins_axis,bb_dl,'x',label='BB')
    ax.plot(bins_axis,d_ell,'o',label='TT')
    ax.set_ylabel('$D_{\ell}[K^2]$',fontsize=16)
else:
    ax.plot(bins_axis,ee_average,'+',label='EE')
    ax.plot(bins_axis,bb_average,'x',label='BB')
    ax.plot(bins_axis,power_average,'o',label='TT')
    ax.set_ylabel('$C_{\ell}[K^2]$',fontsize=16)
ax.legend(loc='upper left')
ax.set_xscale('log')
ax.set_yscale('log')
plt.xlim(0.,1E5)
if scale == 'dl':
    plt.ylim(1E-4,1E14)
else:
    plt.ylim(1E-10,1E6)

if scale == 'dl':
    fig.savefig("N4_aps_dqa3.1_c"+str(chunk)+"_dl.pdf",dpi=100)
else:
    fig.savefig("N4_aps_dqa3.1_c"+str(chunk)+"_cl.pdf",dpi=100)
plt.show()


