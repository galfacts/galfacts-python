from astropy.io import fits

wolqs1=fits.open('updatedwolQS1.fits',mode='update')
head=wolqs1[0].header
head['EQUINOX']=2000.0
head.remove('CTYPE3')
head.remove('CRVAL3')
head.remove('CDELT3')
head.remove('CROTA3')
head.remove('CRPIX3')
wolqs1.flush()
wolqs1.close()


wolus1=fits.open('updatedwolUS1.fits',mode='update')
head=wolus1[0].header
head['EQUINOX']=2000.0
head.remove('CTYPE3')
head.remove('CRVAL3')
head.remove('CDELT3')
head.remove('CROTA3')
head.remove('CRPIX3')
wolus1.flush()
wolus1.close()


wolqs2=fits.open('updatedwolQS2.fits',mode='update')
head=wolqs2[0].header
head['EQUINOX']=2000.0
head.remove('CTYPE3')
head.remove('CRVAL3')
head.remove('CDELT3')
head.remove('CROTA3')
head.remove('CRPIX3')
wolqs2.flush()
wolqs2.close()


wolus2=fits.open('updatedwolUS2.fits',mode='update')
head=wolus2[0].header
head['EQUINOX']=2000.0
head.remove('CTYPE3')
head.remove('CRVAL3')
head.remove('CDELT3')
head.remove('CROTA3')
head.remove('CRPIX3')
wolus2.flush()
wolus2.close()

wolqs3=fits.open('updatedwolQS3.fits',mode='update')
head=wolqs3[0].header
head['EQUINOX']=2000.0
head.remove('CTYPE3')
head.remove('CRVAL3')
head.remove('CDELT3')
head.remove('CROTA3')
head.remove('CRPIX3')
wolqs3.flush()
wolqs3.close()


wolus3=fits.open('updatedwolUS3.fits',mode='update')
head=wolus3[0].header
head['EQUINOX']=2000.0
head.remove('CTYPE3')
head.remove('CRVAL3')
head.remove('CDELT3')
head.remove('CROTA3')
head.remove('CRPIX3')
wolus3.flush()
wolus3.close()

wolqn4=fits.open('updatedwolQN4.fits',mode='update')
head=wolqn4[0].header
head['EQUINOX']=2000.0
head.remove('CTYPE3')
head.remove('CRVAL3')
head.remove('CDELT3')
head.remove('CROTA3')
head.remove('CRPIX3')
wolqn4.flush()
wolqn4.close()


wolun4=fits.open('updatedwolUN4.fits',mode='update')
head=wolun4[0].header
head['EQUINOX']=2000.0
head.remove('CTYPE3')
head.remove('CRVAL3')
head.remove('CDELT3')
head.remove('CROTA3')
head.remove('CRPIX3')
wolun4.flush()
wolun4.close()
