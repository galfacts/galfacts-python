#!/usr/local/bin/python

import numpy as np
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pylab as plt
import sys

filein=sys.argv[1]
i_ra_ratio,q_ra_ratio,u_ra_ratio,v_ra_ratio,ra,channel=np.loadtxt(filein)

fileout="S1_ra_ratio_"+str(np.int(channel[0]+1))+".pdf"

matplotlib.rcParams.update({'font.size':12})

fig,ax=plt.subplots()
ax.plot(ra,i_ra_ratio,color="black",lw=1,label='I ratio')
ax.plot(ra,q_ra_ratio,color="green",lw=1,label='Q ratio')
ax.plot(ra,u_ra_ratio,color="blue",lw=1,label='U ratio')
ax.plot(ra,v_ra_ratio,color="red",lw=1,label='V ratio')
ax.legend(loc=1)
ax.set_xlabel('Right Ascension [deg]')
ax.set_ylabel('Noise ratio')
ax.set_title('Noise ratios vs right ascension in GALFACTS S1 DQA 3.1, channel {0:d}'.format(np.int(channel[0]+1)))

fig.savefig(fileout,dpi=300)

plt.show()

matplotlib.rcParams.update({'font.size': 12, 'font.family': 'sans', 'text.usetex': False})
