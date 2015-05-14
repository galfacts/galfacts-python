import numpy as np
from astropy.io import fits

wol_hdu=fits.open('wolq_raw_center6h.fits',mode='update')
wol_arc_head=wol_hdu[0].header
#wol_arc_head.rename_keyword('OBSEPOCH','EQUINOX')
#wol_arc_head['CTYPE1']='RA---CAR'
#wol_arc_head['CTYPE2']='DEC--CAR'
wol_arc_head.remove('MATRIX11')
wol_arc_head.remove('MATRIX12')
wol_arc_head.remove('MATRIX13')
wol_arc_head.remove('MATRIX21')
wol_arc_head.remove('MATRIX22')
wol_arc_head.remove('MATRIX23')
wol_arc_head.remove('MATRIX31')
wol_arc_head.remove('MATRIX32')
wol_arc_head.remove('MATRIX33')
wol_arc_head.remove('COMMENT')
wol_arc_head.remove('COMMENT')
wol_arc_head.remove('COMMENT')
wol_hdu.flush()
wol_hdu.close()
