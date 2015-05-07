#!/Users/leclercq/miniconda/bin/python

import numpy as np 
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pylab as plt
import gaussbeam
import sys
from numpy import pi
from astropy.io import fits


gal_hdu=fits.open('/Users/leclercq/galfacts/dqa.311/S1/GALFACTS_S1_average_image_I.fits') 
gal_im=gal_hdu[0].data
gal_im=np.asarray(gal_im[0,20:1044,0:5120])
gal_head=gal_hdu[0].header

gal_nan=np.where(np.isnan(gal_im))
gal_im[gal_nan]=0.0

gal_im_2=np.asarray(gal_im[:,2048:3072])
ft_final=np.fft.fftshift(np.fft.fft2(gal_im_2))

ft_beam=gaussbeam.makeFTgaussian(1024,fwhm=3.5)

ft_final=ft_final/ft_beam

ft_pwr=(ft_final*np.conj(ft_final)).real

#plt.imshow(ft_final.real)
plt.imshow(ft_pwr)

