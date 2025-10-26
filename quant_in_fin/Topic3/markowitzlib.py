import cvxopt
import numpy as np
from math import *
import pandas as pd

def read_return_history():
    """Read the ukx.xlsx file into a vector of returns"""

    excel_data = pd.read_excel('ukx.xlsx', header=None)

    num_rows = excel_data.shape[0]
    num_cols = excel_data.shape[1]

    num_stocks = ceil(num_cols/3) #Round up to the nearest integer
    num_weeks = num_rows-2

    price_history = np.zeros( [num_weeks, num_stocks ] )
    for i in range(0,num_stocks):
        col = i*3 + 1
        price_history[:,i]=excel_data[col][2:]

    start_prices = price_history[:-1,:]
    end_prices = price_history[1:,:]
    return_history = (end_prices-start_prices)/start_prices
    return return_history

def solve_markowitz( sigma, mu, R ):
    """Solve the markowiz optimisation problem described in the handouts"""
    n = len( mu )

    P = 2*sigma
    q = np.zeros(n)
    A = np.array([np.ones(n),
         mu ])
    b = np.array([1,
         R]).T

    res = cvxopt.solvers.qp(
        cvxopt.matrix(P),
        cvxopt.matrix(q),
        None,
        None,
        cvxopt.matrix(A),
        cvxopt.matrix(b))

    # Res is a map with keys, status, x and primal objective
    ret = {}
    assert res['status']=='optimal'

    w = res['x']
    var = res['primal objective']

    sd = sqrt(var)

    ret['weights']=w
    ret['sd']=sd

    return ret