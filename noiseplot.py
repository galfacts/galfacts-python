#!/usr/local/bin/python

import numpy as np
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pylab as plt
import sys

filein=sys.argv[1]
i_noise_ratio,q_noise_ratio,u_noise_ratio,v_noise_ratio,mfr=np.loadtxt(filein)



matplotlib.rcParams.update({'font.size':14})

fig,ax=plt.subplots()
ax.plot(mfr,i_noise_ratio,color="black",lw=2,ls='*', marker="+",ms=10,mew=2,fillstyle='none',label='I ratio')
ax.plot(mfr,q_noise_ratio,color="green",lw=2,ls='*', marker="4",ms=10,mew=2,fillstyle='none',label='Q ratio')
ax.plot(mfr,u_noise_ratio,color="blue",lw=2,ls='*', marker="x",ms=8,mew=2,fillstyle='none',label='U ratio')
ax.plot(mfr,v_noise_ratio,color="red",lw=2,ls='*', marker="1",ms=10,mew=2,fillstyle='none',label='V ratio')
ax.legend(loc=1)
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Noise ratio')
ax.set_title('Noise ratio per binned channel in GALFACTS S1 DQA3.1')

fig.savefig("S1_noise_ratio.pdf", dpi=300)

plt.show()


matplotlib.rcParams.update({'font.size': 12, 'font.family': 'sans', 'text.usetex': False})

