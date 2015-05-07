#!/Users/leclercq/miniconda/bin/python

import numpy as np
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pylab as plt
import sys

sys.argv[1]=filein1

scale=filein[0:2]
field=filein[7:9]
chunk=filein[11:13]

bins_axis,power,ee,bb,source,nz=np.loadtxt(filein1)
nonzero=nz[0]
nonzero_ee=nz[1]
nonzero_bb=nz[2]
nonzero_source=nz[3]



fig,ax=plt.subplots(figsize=(8,8))
title='Power spectra of GALFACTS DR3.1 '+field+' chunk{0}'.format(chunk)
ax.set_title(title)
ax.set_xlabel('$\ell$',fontsize=16 )
if scale == 'dl':
    ax.plot(bins_axis,ee,'b+',label='EE')
    ax.plot(bins_axis[nonzero_ee],ee[nonzero_ee],'b-',alpha=0.5)
    ax.plot(bins_axis,bb,'g+',label='BB')
    ax.plot(bins_axis[nonzero_bb],bb[nonzero_bb],'g-',alpha=0.5)
    ax.plot(bins_axis,power,'r+',label='TT')
    ax.plot(bins_axis[nonzero],power[nonzero],'r-',alpha=0.5)
    ax.plot(bins_axis,source,'k+',label='simulated point sources')
    ax.plot(bins_axis[nonzero_source],source[nonzero_source],'k-',alpha=0.5)
    #ax.plot(bins_axis,10**(poissona*np.log10(bins_axis)+poissonb),label='point sources fit')
    #ax.plot(bins_axis,10**(2.0*np.log10(bins_axis)-11.164778353099964
#),label='line of slope 2 with calculated offset')
    ax.set_ylabel('$D_{\ell}[K^2]$',fontsize=16)
else:
    ax.plot(bins_axis,ee,'b+',label='EE')
    ax.plot(bins_axis[nonzero_ee],ee[nonzero_ee],'b-',alpha=0.5)
    ax.plot(bins_axis,bb,'g+',label='BB')
    ax.plot(bins_axis[nonzero_bb],bb[nonzero_bb],'g-',alpha=0.5)
    ax.plot(bins_axis,power,'r+',label='TT')
    ax.plot(bins_axis[nonzero],power[nonzero],'r-',alpha=0.5)
    ax.plot(bins_axis,source,'k+',label='simulated point sources')
    ax.plot(bins_axis[nonzero_source],source[nonzero_source],'k-',alpha=0.5)
    ax.set_ylabel('$C_{\ell}[K^2]$',fontsize=16)
ax.legend(loc='upper left')
ax.set_xscale('log')
ax.set_yscale('log')
plt.xlim(1.,1E4)
if scale == 'dl':
    plt.ylim(1E-6,1E2)
else:
    plt.ylim(1E-12,1E-4)

ax.set_aspect('equal')

if scale == 'dl':
    fig.savefig("./aps/"+field+"_aps_dqa3.1_c"+str(chunk)+"_dl_withps.pdf",dpi=100)
else:
    fig.savefig("./aps/"+field+"_aps_dqa3.1_c"+str(chunk)+"_cl_withps.pdf",dpi=100)
plt.show()
