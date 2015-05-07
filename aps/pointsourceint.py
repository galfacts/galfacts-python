import numpy as np
from scipy import integrate

def integrand(x):
    a3=-0.07
    a2=0.191
    a1=0.614
    a0=0.878
    lx=np.log10(x)
    poly3=a3*lx**3+a2*lx**2+a1*lx+a0
    return x**(-0.5)*(10**poly3)

    
