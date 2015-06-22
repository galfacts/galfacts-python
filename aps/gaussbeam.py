import numpy as np
 
def makeGaussian(size, fwhm = 3, center=None):
    """ Make a square gaussian kernel.
 
    size is the length of a side of the square
    fwhm is full-width-half-maximum, which
    can be thought of as an effective radius.
    """
 
    x = np.arange(0, size, 1, float)
    y = x[:,np.newaxis]
    
    if center is None:
        x0 = y0 = size // 2
    else:
        x0 = center[0]
        y0 = center[1]
    
    return np.exp(-4*np.log(2) * ((x-x0)**2 + (y-y0)**2) / fwhm**2)


def makeFTgaussian(size, fwhm = 3, center=None):
    """ Make the fourier transform of a gaussian of given size and fwhm in the image plane.
 
    size is the length of a side of the square
    fwhm is full-width-half-maximum, which
    can be thought of as an effective radius.
    """
 
    x = np.arange(0, size, 1, float)
    y = x[:,np.newaxis]
    
    if center is None:
        x0 = y0 = size // 2
    else:
        x0 = center[0]
        y0 = center[1]
    
    return np.exp(-fwhm**2 * np.pi**2 * ((x-x0)**2 + (y-y0)**2) /(4*size**2*np.log(2)))
