#!/Users/leclercq/miniconda/bin/python

import numpy as np
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pylab as plt
import sys

filein=sys.argv[1]
nozeros=sys.argv[2]

nz=np.load(nozeros)
#print nz.shape


scale=filein[0:2]
field=filein[7:9]
chunk=filein[11:13]

bins_axis,power,ee,bb,source=np.loadtxt(filein)
nonzero=nz[0]
nonzero_ee=nz[1]
nonzero_bb=nz[2]
nonzero_source=nz[3]
print ee
#print nonzero_ee[0]
ee_70=ee/(1.4/70.)**-6.2
print ee_70
ee_70*=1E6
print ee_70
fig,ax=plt.subplots()
ax.plot(bins_axis,ee,'b+',label='EE')
ax.plot(bins_axis[nonzero_ee[0]],ee[nonzero_ee[0]],'b-',alpha=0.5)

ax.set_xscale('log')
ax.set_yscale('log')
plt.xlim(1.,1E4)
plt.ylim(1E-5,1E7)

plt.show()
