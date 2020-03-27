import numpy as np
import scipy.optimize

def fit_exp(vals, do_sigma=True):
    # takes pd.Series of values with datetime index
    # and returns dictionary with exponential fit results
    # `do_sigma` toggles on poisson errors (clipped to be at least 2.0
    # to be roughly correct for observed points of 0)

    if vals.max() < 2: return dict()

    secs = vals.index.to_numpy().astype(int)/1e9
    secs -= secs.min()
    days = secs/86400.
    cases = vals.values

    xs, ys = days, cases

    extra = dict()
    if do_sigma:
        extra["sigma"] = np.clip(vals**0.5, 2.0, None)
    try:
        def func(x,a=1.0,b=0.5,c=0.):
            return a*np.exp(b*(x-c))
        pars,cov = scipy.optimize.curve_fit(func,  xs,  ys, **extra)
    except:
        return dict()
        
    ypred = func(xs, *pars)
    # doubling time in days
    td = 1.0/(pars[1]*np.log(np.exp(1))/np.log(2))
    return dict(xs=xs, ys=ys, ypred=ypred, pars=pars, cov=cov, td=td)
