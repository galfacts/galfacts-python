#!/usr/local/bin/python

import numpy as np
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pylab as plt
import sys

filein=sys.argv[1]
i_dec_ratio,q_dec_ratio,u_dec_ratio,v_dec_ratio,dec,channel=np.loadtxt(filein)

fileout="S1_dec_ratio_"+str(np.int(channel[0]+1))+".pdf"

matplotlib.rcParams.update({'font.size':12})

fig,ax=plt.subplots()
ax.plot(dec,i_dec_ratio,color="black",lw=1,label='I ratio')
ax.plot(dec,q_dec_ratio,color="green",lw=1,label='Q ratio')
ax.plot(dec,u_dec_ratio,color="blue",lw=1,label='U ratio')
ax.plot(dec,v_dec_ratio,color="red",lw=1,label='V ratio')
ax.legend(loc=1)
ax.set_xlabel('Declination[deg]')
ax.set_ylabel('Noise ratio')
ax.set_title('Noise ratios vs declination in GALFACTS S1 DQA 3.1, channel {0:d}'.format(np.int(channel[0]+1)))

fig.savefig(fileout,dpi=300)

plt.show()

matplotlib.rcParams.update({'font.size': 12, 'font.family': 'sans', 'text.usetex': False})
