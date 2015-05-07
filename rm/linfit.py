import numpy as np
#from scipy import special

def linfit(y, x=None, y_unc=None):
  '''
    Fits a line to 2D data, optionally with errors in y.

    The method is robust to roundoff error.

    Parameters
    ----------
    y: ndarray
        Ordinates, any shape.
    x: ndarray
        Abcissas, same shape.  Defaults to np.indices(y.length))
    y_unc: ndarray
        Uncertainties in y.  If scalar or 1-element array, applied
        uniformly to all y values.  [NOT IMPLEMENTED YET!]  Must be
        positive.

    Returns
    -------
    a: scalar
        0 Fitted intercept
    b: scalar
        1 Fitted slope
    a_unc: scalar
        2 Uncertainty of fitted intercept
    b_unc: scalar
        3 Uncertainty of fitted slope
    chisq: scalar
        4 Chi-squared
    prob: scalar
        5 Probability of finding worse Chi-squared for this model with
          these uncertainties.
    covar: ndarray
        6 Covariance matrix: [[a_unc**2,  covar_ab],
		              [covar_ab,  b_unc**2]]
    yfit: ndarray
        7 Model array calculated for our abcissas
    
    Notes
    -----
    
    If prob > 0.1, you can believe the fit.  If prob > 0.001 and the
    errors are not Gaussian, you could believe the fit.  Otherwise
    do not believe it.

    See Also
    --------
    Press, et al., Numerical Recipes in C, 2nd ed, section 15.2,
    or any standard data analysis text.

    Examples
    --------
    >>> import linfit

    >>> a = 1.
    >>> b = 2.
    >>> nx = 10
    >>> x = np.arange(10, dtype='float')
    >>> y = a + b * x
    >>> y_unc = numpy.ones(nx)
    >>> y[::2]  += 1
    >>> y[1::2] -= 1
    >>> a, b, sa, sb, chisq, prob, covar, yfit = linfit.linfit(y, x, y_unc)
    >>> print(a, b, sa, sb, chisq, prob, covar, yfit)
(1.272727272727272, 1.9393939393939394, 0.58775381364525869, 0.11009637651263605, 9.6969696969696937, 0.28694204178663996, array([[ 0.34545455, -0.05454545],
       [-0.05454545,  0.01212121]]), array([  1.27272727,   3.21212121,   5.15151515,   7.09090909,
         9.03030303,  10.96969697,  12.90909091,  14.84848485,
        16.78787879,  18.72727273]))

    Revisons
    --------
    2007-09-23 0.1  jh@physics.ucf.edu	Initial version
    2007-09-25 0.2  jh@physics.ucf.edu	Fixed bug reported by Kevin Stevenson.
    2008-10-09 0.3  jh@physics.ucf.edu	Fixed doc bug.
    2009-10-01 0.4  jh@physics.ucf.edu  Updated docstring, imports.
  '''
  # standardize and test inputs
  if x == None:
    x = np.indices(y.length, dtype=y.dtype)
    x.shape = y.shape

  if y_unc == None:
      y_unc = np.ones(y.shape, dtype=y.dtype)
  
  # NR Eq. 15.2.4
  ryu2  = 1. / y_unc**2
  S     = np.sum(1.    * ryu2)
  Sx    = np.sum(x     * ryu2)
  Sy    = np.sum(y     * ryu2)
  # Sxx = np.sum(x**2  * ryu2) # not used in the robust method
  # Sxy = np.sum(x * y * ryu2) # not used in the robust method

  # NR Eq. 15.2.15 - 15.2.18 (i.e., the robust method)
  t = 1. / y_unc * (x - Sx / S)
  Stt = np.sum(t**2)

  b = 1. / Stt * np.sum(t * y / y_unc)
  a = (Sy - Sx * b) / S

  covab = -Sx / (S * Stt)                  # NR Eq. 15.2.21

  sa = np.sqrt(1. / S * (1. - Sx * covab)) # NR Eq. 15.2.19
  sb = np.sqrt(1. / Stt)                   # NR Eq. 15.2.20

  rab = covab / (sa * sb)                  # NR Eq. 15.2.22
  
  #covar = np.array([[sa**2, covab],
                    #[covab, sb**2]])
  
  yfit = a + b * x
  chisq = np.sum( ((y - yfit) / y_unc)**2 )
  
  #prob = 1. - special.gammainc( (y.size - 2.) / 2., chisq / 2.)
  
  return a, b, sa, sb, chisq, #prob, covar, yfit
