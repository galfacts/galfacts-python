#/Users/leclercq/miniconda/bin/python

import numpy as np 
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pylab as plt
import gaussbeam
import sys
from numpy import pi
from astropy.io import fits
from scipy import stats
pi=np.pi

q_in=sys.argv[1]
u_in=sys.argv[2]
chunk=sys.argv[3]
field=sys.argv[4]
#scale=sys.argv[4]

def apodize(na,nb,radius):

    ni=int(na*radius)
    dni=na-ni
    nj=int(radius*nb)
    dnj=nb-nj

    tap1d_x=np.ones(na)
    tap1d_y=np.ones(nb)

    tap1d_x[0:dni]= (np.cos(3.*pi/2.+pi/2.*(np.arange(dni,dtype=np.float32)/(dni-1))))
    tap1d_x[na-dni:]= (np.cos(0.+pi/2.*(np.arange(dni,dtype=np.float32)/(dni-1))))
    tap1d_y[0:dnj]= (np.cos(3.*pi/2.+pi/2.*(np.arange(dnj,dtype=np.float32)/(dnj-1))))
    tap1d_x[nb-dnj:]= (np.cos(0.+pi/2.*(np.arange(dnj,dtype=np.float32)/(dnj-1))))

    taper=np.empty((nb,na))
    for i in range (nb):
        taper[i,:]=tap1d_x
    for i in range (na):
        taper[:,i]=taper[i,:]*tap1d_y

    return taper

#define pixel step and pixel area in rad
pixstep=pi/(60.*180.)
pixarea=pixstep**2
area1024=1024.*1024.*pixarea


# first step is to get images and import header and data into numpy arrays, scale is either 'dl' or 'cl'
q_hdu=fits.open(q_in) 
q_im=q_hdu[0].data
q_im=np.asarray(q_im[0,32:1032,0:5000])
q_head=q_hdu[0].header

u_hdu=fits.open(u_in) 
u_im=u_hdu[0].data
u_im=np.asarray(u_im[0,32:1032,0:5000])
u_head=u_hdu[0].header

#Assign zero to blanks

q_nan=np.where(np.isnan(q_im))
q_im[q_nan]=0.0

u_nan=np.where(np.isnan(u_im))
u_im[u_nan]=0.0

#Divide images into 5 1000x1000 chunks

u_im_0=np.asarray(u_im[:,0:1000])
u_im_1=np.asarray(u_im[:,1000:2000])
u_im_2=np.asarray(u_im[:,2000:3000])
u_im_3=np.asarray(u_im[:,3000:4000])
u_im_4=np.asarray(u_im[:,4000:5000])

q_im_0=np.asarray(q_im[:,0:1000])
q_im_1=np.asarray(q_im[:,1000:2000])
q_im_2=np.asarray(q_im[:,2000:3000])
q_im_3=np.asarray(q_im[:,3000:4000])
q_im_4=np.asarray(q_im[:,4000:5000])

#remove mean?

q_im_0=u_im_0-np.mean(q_im_0)
q_im_1=u_im_1-np.mean(q_im_1)
q_im_2=u_im_2-np.mean(q_im_2)
q_im_3=u_im_3-np.mean(q_im_3)
q_im_4=u_im_4-np.mean(q_im_4)

u_im_0=u_im_0-np.mean(u_im_0)
u_im_1=u_im_1-np.mean(u_im_1)
u_im_2=u_im_2-np.mean(u_im_2)
u_im_3=u_im_3-np.mean(u_im_3)
u_im_4=u_im_4-np.mean(u_im_4)


#Make taper, set up padding before doing FT

ft_taper=apodize(1000,1000,0.98)

#Do FTs

if chunk == 'all':
#taper, pad
    q_im_0=np.pad(q_im_0*ft_taper,(12,),mode='constant')
    q_im_1=np.pad(q_im_1*ft_taper,(12,),mode='constant')
    q_im_2=np.pad(q_im_2*ft_taper,(12,),mode='constant')
    q_im_3=np.pad(q_im_3*ft_taper,(12,),mode='constant')
    q_im_4=np.pad(q_im_4*ft_taper,(12,),mode='constant')

    u_im_0=np.pad(u_im_0*ft_taper,(12,),mode='constant')
    u_im_1=np.pad(u_im_1*ft_taper,(12,),mode='constant')
    u_im_2=np.pad(u_im_2*ft_taper,(12,),mode='constant')
    u_im_3=np.pad(u_im_3*ft_taper,(12,),mode='constant')
    u_im_4=np.pad(u_im_4*ft_taper,(12,),mode='constant')
   
#ft
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
#stack & average
    uftstack=np.dstack((uft0,uft1,uft2,uft3,uft4))
    qftstack=np.dstack((qft0,qft1,qft2,qft3,qft4))

    uft_final=np.mean(uftstack,axis=2)
    qft_final=np.mean(qftstack,axis=2)

elif chunk == '0':
    print 'Taking FT of chunk 0'
    q_im_0=np.pad(q_im_0*ft_taper,(12,),mode='constant')
    qft_final=np.fft.fftshift(np.fft.fft2(q_im_0))
    u_im_0=np.pad(u_im_0*ft_taper,(12,),mode='constant')
    uft_final=np.fft.fftshift(np.fft.fft2(u_im_0))

elif chunk == '1':
    q_im_1=np.pad(q_im_1*ft_taper,(12,),mode='constant')
    qft_final=np.fft.fftshift(np.fft.fft2(q_im_1))
    u_im_1=np.pad(u_im_1*ft_taper,(12,),mode='constant')
    uft_final=np.fft.fftshift(np.fft.fft2(u_im_1))

elif chunk == '2':
    q_im_2=np.pad(q_im_2*ft_taper,(12,),mode='constant')
    qft_final=np.fft.fftshift(np.fft.fft2(q_im_2))
    u_im_2=np.pad(u_im_2*ft_taper,(12,),mode='constant')
    uft_final=np.fft.fftshift(np.fft.fft2(u_im_2))

elif chunk == '3':
    q_im_3=np.pad(q_im_3*ft_taper,(12,),mode='constant')
    qft_final=np.fft.fftshift(np.fft.fft2(q_im_3))
    u_im_3=np.pad(u_im_3*ft_taper,(12,),mode='constant')
    uft_final=np.fft.fftshift(np.fft.fft2(u_im_3))
    
elif chunk == '4':
    q_im_4=np.pad(q_im_4*ft_taper,(12,),mode='constant')
    qft_final=np.fft.fftshift(np.fft.fft2(q_im_4))
    u_im_4=np.pad(u_im_4*ft_taper,(12,),mode='constant')
    uft_final=np.fft.fftshift(np.fft.fft2(u_im_4))

else :
    print 'Invalid chunk'
    exit()


#get fft spatial frequencies
freq_1d=np.fft.fftshift(np.fft.fftfreq(1024,pixstep))

ell_1d= 2*pi*freq_1d

ellx,elly=np.meshgrid(ell_1d,ell_1d)

#define radii of constant ell
ell_r=np.sqrt((ellx)**2+(elly)**2)
ell_ref=ell_r
ell_max=np.max(ell_ref)

#set up grid of phis
phi_ell=np.arctan2(elly,ellx)

#Calculate E and B mode functions

emode=qft_final*np.cos(2.*phi_ell)+uft_final*np.sin(2.*phi_ell)
bmode=-qft_final*np.sin(2.*phi_ell)+uft_final*np.cos(2.*phi_ell)

#compute correlations (EE,BB)
ee=np.abs(emode)**2
bb=np.abs(bmode)**2

#divide out beam & account for size of array, and average over ells:

#use square of beam, divide out from ee
ft_beam=gaussbeam.makeFTgaussian(1024,fwhm=3.5)
ft_beam_sq=np.abs(ft_beam)**2

ee=ee/ft_beam
bb=bb/ft_beam

ee_scaled=ee/1024**2
bb_scaled=bb/1024**2


#Use these bins so far

bins=np.logspace(np.log10(10.0),np.log10(ell_max),50).astype(np.uint64)
ell_scale=bins*(bins+1)/2.*pi
print bins

ell_hist=np.histogram(ell_r,bins)[0]

ee_hist=np.histogram(ell_r,bins,weights=ee_scaled)[0]
ee_average=np.zeros(ee_hist.size)
nonzero_ee=np.where(ee_hist!=0)
ee_average[nonzero_ee]=area1024*ee_hist[nonzero_ee]/ell_hist[nonzero_ee]
#ee_70=ee_average/(1.4/70.)**-6.2
#if scale == 'dl':
    #ee_dl=ee_average*ell_scale[1:]
    

bb_hist=np.histogram(ell_r,bins,weights=bb_scaled)[0]
bb_average=np.zeros(bb_hist.size)
nonzero_bb=np.where(bb_hist!=0)
bb_average[nonzero_bb]=area1024*bb_hist[nonzero_bb]/ell_hist[nonzero_bb]
#if scale =='dl':
    #bb_dl=bb_average*ell_scale[1:]



#plot plot plot


bins_center=np.zeros((bins.size)-1)

for i in range((bins.size)-1):
    bins_center[i]=bins[i]+(bins[i+1]-bins[i])/2.

bins_axis=bins_center


slope,offset,c,d,e=stats.linregress(np.log10(bins_axis[15:35]),np.log10(ee_average[15:35]))

print slope,offset
pwr_label="power-law fit, slope="+str(slope)[:6]
print pwr_label

fig,ax=plt.subplots(figsize=(8,8))
title='APS of GALFACTS DR3.2 '+field+' chunk{0}'.format(chunk)
ax.set_title(title)
ax.set_xlabel('$\ell$',fontsize=16 )
## if scale == 'dl':
##     ax.plot(bins_axis,ee_dl,'bx',label='EE')
##     #ax.plot(bins_axis[nonzero_ee],ee_dl[nonzero_ee],'b-',alpha=0.5)
##     ax.plot(bins_axis,bb_dl,'gx',label='BB')
##     #ax.plot(bins_axis[nonzero_bb],bb_dl[nonzero_bb],'g-',alpha=0.5)
##     #ax.plot(bins_axis,d_ell,'rx',label='TT')
##     #ax.plot(bins_axis[nonzero],d_ell[nonzero],'r-',alpha=0.5)
##     #ax.plot(bins_axis,source_dl,'kx',label='simulated point sources')
##     #ax.plot(bins_axis[nonzero_source],source_dl[nonzero_source],'k-',alpha=0.5)
##     ax.plot(bins_axis[17:],10**((slope+2)*np.log10(bins_axis[17:])+offset),'k--',linewidth=2,label='power-law fit')    #ax.plot(bins_axis,10**(2.0*np.log10(bins_axis)-11.164778353099964
## #),label='line of slope 2 with calculated offset')
##     ax.set_ylabel('$\ell(\ell+1)C_{\ell}[K^2]$',fontsize=16)
ax.plot(bins_axis,ee_average,'bx',label='EE')
#ax.plot(bins_axis[nonzero_ee],ee_average[nonzero_ee],'b-',alpha=0.5)
ax.plot(bins_axis,bb_average,'gx',label='BB')
#ax.plot(bins_axis[nonzero_bb],bb_average[nonzero_bb],'g-',alpha=0.5)
#ax.plot(bins_axis,power_average,'rx',label='TT')
#ax.plot(bins_axis[nonzero],power_average[nonzero],'r-',alpha=0.5)
ax.plot(bins_axis[15:35],10**(slope*np.log10(bins_axis[15:35])+offset),'k-',linewidth=1.5,label=pwr_label)
#matplotlib.text.Text(1E2,1E-10,'$\beta=$'+str(slope)[0:4])
## ax.plot(bins_axis,source_average,'kx',label='simulated point sources')
## ax.plot(bins_axis[nonzero_source],source_average[nonzero_source],'k-',alpha=0.5)
ax.set_ylabel('$C_{\ell}[K^2]$',fontsize=16)
ax.legend(loc='lower left')
ax.set_xscale('log')
ax.set_yscale('log')
#plt.xlim(10,1E4)
#plt.ylim(1E-6,10)
## if scale == 'dl':
##     plt.ylim(1E-6,1.)
## else:
##     plt.ylim(1E-12,1E-4)

#ax.set_aspect('equal')

## if scale == 'dl':
##     fig.savefig("./aps/"+field+"_aps_dqa3.1_c"+str(chunk)+"_dl_withps_talk.pdf",dpi=100)
#else:
fig.savefig("/Users/leclercq/galfacts/aps/plots/"+field+"_aps_dqa3.2_c"+str(chunk)+"nobeam_ps.pdf",dpi=100)
#plt.show()
