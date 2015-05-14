
#imsmooth script, to smooth reduced galfacts Q & U images for all fields

print "Running imsmooth script, producing smooth reduced galfacts Q & U for comparison with DRAO maps"

galbeam={"major":"36arcmin","minor":"36arcmin","pa":"0deg"}


####################################################
########               S1                  #########
####################################################

print "smoothing S1"

importfits('S1_binned_Q_first.fits','s1galqfirst.image')
importfits('S1_binned_U_first.fits','s1galufirst.image')
importfits('S1_binned_Q_last.fits','s1galqlast.image')
importfits('S1_binned_U_last.fits','s1galulast.image')

imsmooth(imagename='s1galqfirst.image',beam=galbeam,targetres=True,outfile='s1galqfirstsmooth.image')
imsmooth(imagename='s1galufirst.image',beam=galbeam,targetres=True,outfile='s1galufirstsmooth.image')
imsmooth(imagename='s1galqlast.image',beam=galbeam,targetres=True,outfile='s1galqlastsmooth.image')
imsmooth(imagename='s1galulast.image',beam=galbeam,targetres=True,outfile='s1galulastsmooth.image')

exportfits('s1galqfirstsmooth.image','S1_Q_first_smooth.fits')
exportfits('s1galufirstsmooth.image','S1_U_first_smooth.fits')
exportfits('s1galqlastsmooth.image','S1_Q_last_smooth.fits')
exportfits('s1galulastsmooth.image','S1_U_last_smooth.fits')

####################################################
########               S2                  #########
####################################################

print "smoothing S2"

importfits('S2_binned_Q_first.fits','s2galqfirst.image')
importfits('S2_binned_U_first.fits','s2galufirst.image')
importfits('S2_binned_Q_last.fits','s2galqlast.image')
importfits('S2_binned_U_last.fits','s2galulast.image')

imsmooth(imagename='s2galqfirst.image',beam=galbeam,targetres=True,outfile='s2galqfirstsmooth.image')
imsmooth(imagename='s2galufirst.image',beam=galbeam,targetres=True,outfile='s2galufirstsmooth.image')
imsmooth(imagename='s2galqlast.image',beam=galbeam,targetres=True,outfile='s2galqlastsmooth.image')
imsmooth(imagename='s2galulast.image',beam=galbeam,targetres=True,outfile='s2galulastsmooth.image')

exportfits('s2galqfirstsmooth.image','S2_Q_first_smooth.fits')
exportfits('s2galufirstsmooth.image','S2_U_first_smooth.fits')
exportfits('s2galqlastsmooth.image','S2_Q_last_smooth.fits')
exportfits('s2galulastsmooth.image','S2_U_last_smooth.fits')


####################################################
########               S3                  #########
####################################################

print "smoothing S3"

importfits('S3_binned_Q_first.fits','s3galqfirst.image')
importfits('S3_binned_U_first.fits','s3galufirst.image')
importfits('S3_binned_Q_last.fits','s3galqlast.image')
importfits('S3_binned_U_last.fits','s3galulast.image')

imsmooth(imagename='s3galqfirst.image',beam=galbeam,targetres=True,outfile='s3galqfirstsmooth.image')
imsmooth(imagename='s3galufirst.image',beam=galbeam,targetres=True,outfile='s3galufirstsmooth.image')
imsmooth(imagename='s3galqlast.image',beam=galbeam,targetres=True,outfile='s3galqlastsmooth.image')
imsmooth(imagename='s3galulast.image',beam=galbeam,targetres=True,outfile='s3galulastsmooth.image')

exportfits('s3galqfirstsmooth.image','S3_Q_first_smooth.fits')
exportfits('s3galufirstsmooth.image','S3_U_first_smooth.fits')
exportfits('s3galqlastsmooth.image','S3_Q_last_smooth.fits')
exportfits('s3galulastsmooth.image','S3_U_last_smooth.fits')

####################################################
########               N4                  #########
####################################################

print "smoothing N4"

importfits('N4_binned_Q_first.fits','n4galqfirst.image')
importfits('N4_binned_U_first.fits','n4galufirst.image')
importfits('N4_binned_Q_last.fits','n4galqlast.image')
importfits('N4_binned_U_last.fits','n4galulast.image')

imsmooth(imagename='n4galqfirst.image',beam=galbeam,targetres=True,outfile='n4galqfirstsmooth.image')
imsmooth(imagename='n4galufirst.image',beam=galbeam,targetres=True,outfile='n4galufirstsmooth.image')
imsmooth(imagename='n4galqlast.image',beam=galbeam,targetres=True,outfile='n4galqlastsmooth.image')
imsmooth(imagename='n4galulast.image',beam=galbeam,targetres=True,outfile='n4galulastsmooth.image')

exportfits('n4galqfirstsmooth.image','N4_Q_first_smooth.fits')
exportfits('n4galufirstsmooth.image','N4_U_first_smooth.fits')
exportfits('n4galqlastsmooth.image','N4_Q_last_smooth.fits')
exportfits('n4galulastsmooth.image','N4_U_last_smooth.fits')

