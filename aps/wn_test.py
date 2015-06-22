import numpy as np 
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pylab as plt

pi=np.pi


pixstep=pi/(60.*180.)
pixarea=pixstep**2
allsky_pix=4*pi/pixarea
area1024=1024.*1024.*pixarea

#Generate white noise as reference scaling factor
wnoise=np.random.randn(1000,1000)
wnoiseft=np.fft.fftshift(np.fft.fft2(wnoise))
wnoise_pwr=np.abs(wnoiseft)**2


#get fft spatial frequencies
freq_1d=np.fft.fftshift(np.fft.fftfreq(1024,pixstep))

ell_1d= 2*pi*freq_1d

ellx,elly=np.meshgrid(ell_1d,ell_1d)

#define radii of constant ell
ell_r=np.sqrt((ellx)**2+(elly)**2)
ell_ref=ell_r
ell_max=np.max(ell_ref)

bins_high=np.logspace(np.log10(10.0),np.log10(ell_max),50).astype(np.uint64)
bins=bins_high
ell_scale=bins*(bins+1)/2.*pi
print bins

#use histogram function to take average (using weights)

power_hist=np.histogram(ell_r,bins,weights=wnoise_pwr)[0]
ell_hist=np.histogram(ell_r,bins)[0]
power_average=np.zeros(power_hist.size)
nonzero=np.where(power_hist!=0)
power_average[nonzero]=power_hist[nonzero]/(1024**2*ell_hist[nonzero]) ###this is the important bit: to get correct power divide by number of pixels in DFT

print np.mean(power_average)
print np.median(power_average)
print np.mean(wnoise_pwr)
print 1024*1024


#plot plot plot


bins_center=np.zeros((bins_high.size)-1)

for i in range((bins_high.size)-1):
    bins_center[i]=bins_high[i]+(bins_high[i+1]-bins_high[i])/2.

bins_axis=bins_center

fig,ax=plt.subplots(figsize=(8,8))

ax.set_xlabel('$\ell$',fontsize=16 )

ax.plot(bins_axis,power_average,'rx',label='TT')

ax.set_xscale('log')
ax.set_yscale('log')

plt.show()
