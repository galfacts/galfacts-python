#/Users/leclercq/miniconda/bin/python

import numpy as np
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pylab as plt
import sys

filein1=sys.argv[1]
i_noise_ratio1,q_noise_ratio1,u_noise_ratio1,v_noise_ratio1,mfr1=np.loadtxt(filein1)

filein2=sys.argv[2]
i_noise_ratio2,q_noise_ratio2,u_noise_ratio2,v_noise_ratio2,mfr2=np.loadtxt(filein2)

filein3=sys.argv[3]
i_noise_ratio3,q_noise_ratio3,u_noise_ratio3,v_noise_ratio3,mfr3=np.loadtxt(filein3)

filein4=sys.argv[4]
i_noise_ratio4,q_noise_ratio4,u_noise_ratio4,v_noise_ratio4,mfr4=np.loadtxt(filein4)

outfile="noise/images/noise_ratio_all.pdf"


mfr1=mfr1/1E6
print mfr1
mfr2=mfr2/1E6
mfr3=mfr3/1E6
mfr4=mfr4/1E6

matplotlib.rcParams.update({'font.size':14})
from matplotlib.ticker import FixedLocator,AutoMinorLocator,FormatStrFormatter,FixedFormatter

majortoplocator= FixedLocator((mfr1[0],mfr1[9],mfr1[19],mfr1[len(mfr1)-1]))
majorbottomlocator= FixedLocator((1370,1420,1470,1520))
minortoplocator= FixedLocator(mfr1)
minorbottomlocator=AutoMinorLocator(n=5)
majorbottomformatter=FormatStrFormatter('%d')
majortopformatter=FixedFormatter(('1','10','20',str(len(mfr1))))
fig,((ax1,ax2),(ax3,ax4))=plt.subplots(2,2,figsize=(18,18),squeeze=True)
fig.subplots_adjust(left= 0.05,right=0.98)


ax1.plot(mfr1,i_noise_ratio1,color="black",lw=2,ls='*', marker="+",ms=10,mew=2,fillstyle='none',label='I ratio')
ax1.plot(mfr1,q_noise_ratio1,color="green",lw=2,ls='*', marker="4",ms=10,mew=2,fillstyle='none',label='Q ratio')
ax1.plot(mfr1,u_noise_ratio1,color="blue",lw=2,ls='*', marker="x",ms=8,mew=2,fillstyle='none',label='U ratio')
ax1.plot(mfr1,v_noise_ratio1,color="red",lw=2,ls='*', marker="1",ms=10,mew=2,fillstyle='none',label='V ratio')
ax1.legend(loc=1)
ax1.text(0.3,0.93,'GALFACTS {0} DQA 3.1.2'.format(filein1[19:21]),ha='center',va='center',transform=ax1.transAxes)
ax1.xaxis.set_major_locator(majorbottomlocator)
ax1.xaxis.set_major_formatter(majorbottomformatter)
ax1.xaxis.set_minor_locator(minorbottomlocator)
ax1.set_xlim([1350,1530])
ax1.set_xlabel('Frequency (MHz)')
ax1.set_ylabel('Noise ratio')

ax1b=ax1.twiny()
ax1b.set_xlim([1350,1530])
ax1b.plot(mfr1,i_noise_ratio1,color="black",marker="None",ls="None")
ax1b.xaxis.set_major_locator(majortoplocator)
ax1b.xaxis.set_minor_locator(minortoplocator)
ax1b.xaxis.set_major_formatter(majortopformatter)
ax1b.set_xlabel(r"Channel number")
ax1.set_ylim([1.0,5.0])


majortoplocator= FixedLocator((mfr2[0],mfr2[9],mfr2[19],mfr2[len(mfr2)-1]))
minortoplocator= FixedLocator(mfr2)
majortopformatter=FixedFormatter(('1','10','20',str(len(mfr2))))

ax2.plot(mfr2,i_noise_ratio2,color="black",lw=2,ls='*', marker="+",ms=10,mew=2,fillstyle='none',label='I ratio')
ax2.plot(mfr2,q_noise_ratio2,color="green",lw=2,ls='*', marker="4",ms=10,mew=2,fillstyle='none',label='Q ratio')
ax2.plot(mfr2,u_noise_ratio2,color="blue",lw=2,ls='*', marker="x",ms=8,mew=2,fillstyle='none',label='U ratio')
ax2.plot(mfr2,v_noise_ratio2,color="red",lw=2,ls='*', marker="1",ms=10,mew=2,fillstyle='none',label='V ratio')
ax2.legend(loc=1)
ax2.text(0.3,0.93,'GALFACTS {0} DQA 3.1.2'.format(filein2[19:21]),ha='center',va='center',transform=ax2.transAxes)
ax2.xaxis.set_major_locator(majorbottomlocator)
ax2.xaxis.set_major_formatter(majorbottomformatter)
ax2.xaxis.set_minor_locator(minorbottomlocator)
ax2.set_xlim([1350,1530])
ax2.set_xlabel('Frequency (MHz)')
ax2.set_ylabel('Noise ratio')

ax2b=ax2.twiny()
ax2b.set_xlim([1350,1530])
ax2b.plot(mfr2,i_noise_ratio2,color="black",marker="None",ls="None")
ax2b.xaxis.set_major_locator(majortoplocator)
ax2b.xaxis.set_minor_locator(minortoplocator)
ax2b.xaxis.set_major_formatter(majortopformatter)
ax2b.set_xlabel(r"Channel number")
ax2.set_ylim([1.0,5.0])


majortoplocator= FixedLocator((mfr3[0],mfr3[9],mfr3[19],mfr3[len(mfr3)-1]))
minortoplocator= FixedLocator(mfr3)
majortopformatter=FixedFormatter(('1','10','20',str(len(mfr3))))

ax3.plot(mfr3,i_noise_ratio3,color="black",lw=2,ls='*', marker="+",ms=10,mew=2,fillstyle='none',label='I ratio')
ax3.plot(mfr3,q_noise_ratio3,color="green",lw=2,ls='*', marker="4",ms=10,mew=2,fillstyle='none',label='Q ratio')
ax3.plot(mfr3,u_noise_ratio3,color="blue",lw=2,ls='*', marker="x",ms=8,mew=2,fillstyle='none',label='U ratio')
ax3.plot(mfr3,v_noise_ratio3,color="red",lw=2,ls='*', marker="1",ms=10,mew=2,fillstyle='none',label='V ratio')
ax3.legend(loc=1)
ax3.text(0.3,0.93,'GALFACTS {0} DQA 3.1.2'.format(filein3[19:21]),ha='center',va='center',transform=ax3.transAxes)
ax3.xaxis.set_major_locator(majorbottomlocator)
ax3.xaxis.set_major_formatter(majorbottomformatter)
ax3.xaxis.set_minor_locator(minorbottomlocator)
ax3.set_xlim([1350,1530])
ax3.set_xlabel('Frequency (MHz)')
ax3.set_ylabel('Noise ratio')

ax3b=ax3.twiny()
ax3b.set_xlim([1350,1530])
ax3b.plot(mfr3,i_noise_ratio3,color="black",marker="None",ls="None")
ax3b.xaxis.set_major_locator(majortoplocator)
ax3b.xaxis.set_minor_locator(minortoplocator)
ax3b.xaxis.set_major_formatter(majortopformatter)
ax3b.set_xlabel(r"Channel number")
ax3.set_ylim([1.0,5.0])

majortoplocator= FixedLocator((mfr4[0],mfr4[9],mfr4[19],mfr4[len(mfr4)-1]))
minortoplocator= FixedLocator(mfr4)
majortopformatter=FixedFormatter(('1','10','20',str(len(mfr4))))

ax4.plot(mfr4,i_noise_ratio4,color="black",lw=2,ls='*', marker="+",ms=10,mew=2,fillstyle='none',label='I ratio')
ax4.plot(mfr4,q_noise_ratio4,color="green",lw=2,ls='*', marker="4",ms=10,mew=2,fillstyle='none',label='Q ratio')
ax4.plot(mfr4,u_noise_ratio4,color="blue",lw=2,ls='*', marker="x",ms=8,mew=2,fillstyle='none',label='U ratio')
ax4.plot(mfr4,v_noise_ratio4,color="red",lw=2,ls='*', marker="1",ms=10,mew=2,fillstyle='none',label='V ratio')
ax4.legend(loc=1)
ax4.text(0.3,0.93,'GALFACTS {0} DQA 3.1.2'.format(filein4[19:21]),ha='center',va='center',transform=ax4.transAxes)
ax4.xaxis.set_major_locator(majorbottomlocator)
ax4.xaxis.set_major_formatter(majorbottomformatter)
ax4.xaxis.set_minor_locator(minorbottomlocator)
ax4.set_xlim([1350,1530])
ax4.set_xlabel('Frequency (MHz)')
ax4.set_ylabel('Noise ratio')

ax4b=ax4.twiny()
ax4b.set_xlim([1350,1530])
ax4b.plot(mfr4,i_noise_ratio4,color="black",marker="None",ls="None")
ax4b.xaxis.set_major_locator(majortoplocator)
ax4b.xaxis.set_minor_locator(minortoplocator)
ax4b.xaxis.set_major_formatter(majortopformatter)
ax4b.set_xlabel(r"Channel number")
ax4.set_ylim([1.0,5.0])


fig.savefig(outfile, dpi=150)

plt.tight_layout()


matplotlib.rcParams.update({'font.size': 12, 'font.family': 'sans', 'text.usetex': False})

