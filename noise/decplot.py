#!/Users/leclercq/miniconda/bin/python

import numpy as np
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pylab as plt
import sys

filein1=sys.argv[1]
i_dec_ratio1,q_dec_ratio1,u_dec_ratio1,v_dec_ratio1,dec1,channel1=np.loadtxt(filein1)

filein2=sys.argv[2]
i_dec_ratio2,q_dec_ratio2,u_dec_ratio2,v_dec_ratio2,dec2,channel2=np.loadtxt(filein2)

filein3=sys.argv[3]
i_dec_ratio3,q_dec_ratio3,u_dec_ratio3,v_dec_ratio3,dec3,channel3=np.loadtxt(filein3)

filein4=sys.argv[4]
i_dec_ratio4,q_dec_ratio4,u_dec_ratio4,v_dec_ratio4,dec4,channel4=np.loadtxt(filein4)


fileout="all_dec_ratio_"+str(np.int(channel1[0]+1))+".pdf"

matplotlib.rcParams.update({'font.size':12})

fig,ax=plt.subplots(1,4,figsize=(20,6),squeeze=True)
#fig.subplots_adjust(left= 0.03,right=0.98)
ax1=ax[0]
ax2=ax[1]
ax3=ax[2]
ax4=ax[3]


ax1.plot(dec1,i_dec_ratio1,color="black",lw=1,label='I ratio')
ax1.plot(dec1,q_dec_ratio1,color="green",lw=1,label='Q ratio')
ax1.plot(dec1,u_dec_ratio1,color="blue",lw=1,label='U ratio')
ax1.plot(dec1,v_dec_ratio1,color="red",lw=1,label='V ratio')
ax1.legend(loc=1)
ax1.set_xlabel('Declination[deg]')
ax1.set_ylabel('Noise ratio')
ax1.set_title('GALFACTS '+filein1[0:2]+' DQA 3.1.2, channel {0:d}'.format(np.int(channel1[0]+1)))
ax1.set_ylim([1.0,8.0])


ax2.plot(dec2,i_dec_ratio2,color="black",lw=1,label='I ratio')
ax2.plot(dec2,q_dec_ratio2,color="green",lw=1,label='Q ratio')
ax2.plot(dec2,u_dec_ratio2,color="blue",lw=1,label='U ratio')
ax2.plot(dec2,v_dec_ratio2,color="red",lw=1,label='V ratio')
ax2.legend(loc=1)
ax2.set_xlabel('Declination[deg]')
ax2.set_ylabel('Noise ratio')
ax2.set_title('GALFACTS '+filein2[0:2]+' DQA 3.1.2, channel {0:d}'.format(np.int(channel2[0]+1)))
ax2.set_ylim([1.0,8.0])

ax3.plot(dec3,i_dec_ratio3,color="black",lw=1,label='I ratio')
ax3.plot(dec3,q_dec_ratio3,color="green",lw=1,label='Q ratio')
ax3.plot(dec3,u_dec_ratio3,color="blue",lw=1,label='U ratio')
ax3.plot(dec3,v_dec_ratio3,color="red",lw=1,label='V ratio')
ax3.legend(loc=1)
ax3.set_xlabel('Declination[deg]')
ax3.set_ylabel('Noise ratio')
ax3.set_title('GALFACTS '+filein3[0:2]+' DQA 3.1.2, channel {0:d}'.format(np.int(channel3[0]+1)))
ax3.set_ylim([1.0,8.0])

ax4.plot(dec4,i_dec_ratio4,color="black",lw=1,label='I ratio')
ax4.plot(dec4,q_dec_ratio4,color="green",lw=1,label='Q ratio')
ax4.plot(dec4,u_dec_ratio4,color="blue",lw=1,label='U ratio')
ax4.plot(dec4,v_dec_ratio4,color="red",lw=1,label='V ratio')
ax4.legend(loc=1)
ax4.set_xlabel('Declination[deg]')
ax4.set_ylabel('Noise ratio')
ax4.set_title('GALFACTS '+filein4[0:2]+' DQA 3.1.2, channel {0:d}'.format(np.int(channel4[0]+1)))
ax4.set_ylim([1.0,8.0])


fig.savefig(fileout,dpi=150)

plt.tight_layout()

matplotlib.rcParams.update({'font.size': 12, 'font.family': 'sans', 'text.usetex': False})
