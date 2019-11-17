import numpy as np

"""
Author: Stefan Bruenner
Date: 2019/10/31
Description:
Bin intervals of Po-214, Po-218, Po-210.

Variables:
- NONE

Return:
- Pol_214_min [bin number]
- Pol_214_max [bin number]
- Pol_218_min [bin number]
- Pol_218_max [bin number]
- Pol_210_min [bin number]
- Pol_210_max [bin number]
"""
def def_Pol_ranges(Pol):

    #Po-214 selection window
    # lower bound
    x1 = 275.
    # upper bound
    x2 = 360.

    ### Po-218 selection window
    # lower bound
    x3 = 245.
    # upper bound
    x4 = x1

    ### Po-210 selection window
    # lower bound
    x5 = 180.
    # upper bound
    x6 = x3

    returnvalue=0
    if Pol == 'Pol_214_min':
        returnvalue=x1
    elif Pol == 'Pol_214_max':
        returnvalue=x2
    elif Pol == 'Pol_218_min':
        returnvalue=x3
    elif Pol == 'Pol_218_max':
        returnvalue=x4
    elif Pol == 'Pol_210_min':
        returnvalue=x5
    elif Pol == 'Pol_210_max':
        returnvalue=x6

    return returnvalue

"""
Date: 2019/10/31
Description:
How much time do we blind the data after starting HVs

Variables:
- Blind time. By default is 300 min. [min]

Return:
- Blind time [min]
"""
def blindingTime(tblind=300):

    return tblind

"""
Author: Stefan Bruenner
Date: 2019/10/31
Description:
Finds the value mostly repeated from elements on a given list

Variables:
- NONE

Return:
- Maximum number of repetitions
"""
def find_max(data_list):

    sort = []

    for i in range (0,max(data_list)):
        count = 0
        for e in range (0,len(data_list)-1):
            if i == data_list[e]:
                count = count +1
        sort.append(count)
    return max(sort)


"""
Author: Stefan Bruenner
Date: 2019/10/31
Description:
Sets efficiency of rd-monitor.
By default is 21%, the one from MonA in N2 at 1300 mbar and HV=-1 kV.

Variables:
- NONE

Return:
- Assumed efficiency of rd-Monitor [%*0.01]
"""
def set_ef_rdMonitor(eff=0.21):

    return eff


"""
Author: Stefan Bruenner
Date: 2019/10/31
Description:
Sets error Efficiency of rd-monitor.
By default is 1%, the one from MonA in N2 at 1300 mbar and HV=-1 kV.

Variables:
- NONE

Return:
- Assumed error efficiency of rd-Monitor [%*0.01]
"""
def set_error_ef_rdMonitor(eeff=0.01):

    return eeff


"""
Author: Stefan Bruenner
Date: 2019/10/31
Description:
Calculates efficiency of rd-monitor.

Variables:
- c  = number of counts [#]
- a  = activity of the standard [Bq]
- lambda_ = mean lifetime of the source [1/s]
- t1 = time between emanation stop of the source and the start of the measurement. [s]
- t2 = time of measurement (after removing the blind time) [s]

Return:
- Measured efficiency of rd-Monitor [%*0.01]
"""
def calc_eff_rdMonitor(c,a,lambda_,t1,t2):
    return c/((a/lambda_)*(-np.exp(-lambda_*t2) + np.exp(-lambda_*t1)))


"""
Author: Stefan Bruenner
Date: 2019/10/31
Description:
Calculates efficiency of rd-monitor.

Variables:
- c  = number of counts [#]
- ec  = number of counts [#]
- a  = activity of the standard [Bq]
- ea  = error activity of the standard [Bq]
- lambda_ = mean lifetime of the source [1/s]
- t1 = time between emanation stop of the source and the start of the measurement. [s]
- t2 = time of measurement (after removing the blind time) [s]

Return:
- Measured efficiency of rd-Monitor [%*0.01]
"""
def calc_err_eff_rdMonitor(c,ec,a,ea,lambda_,t1,t2):
    return np.sqrt((ec*lambda_/((np.exp(-lambda_*t1) - np.exp(-lambda_*t2))*a))**2 + (ea*c*lambda_/((np.exp(-lambda_*t1)-np.exp(-lambda_*t2))*a**2))**2)


"""
Author: Stefan Bruenner
Date: 2019/10/31
Description:
Calculates standard activity.

Variables:
- a  = Intrinsic activity [Bq]
- t  = Time during emanation [day]
- lambda_ =  mean lifetime of the source [1/s]


Return:
- Activity of the standard at the moment of expansion [Bq]
"""
def standard_strength(a,t,lambda_):
    return a*(1-np.exp(-lambda_*t*(24*60*60)))


"""
Author: Stefan Bruenner
Date: 2019/10/31
Description:
Calculates standard activity.

Variables:
- a  = Intrinsic activity [Bq]
- ea = Error intrinsic activity [Bq]
- t  = Time during emanation [day]
- t  = Error time during emanation [day]
- lambda_ =  mean lifetime of the source [1/s]


Return:
- Activity of the standard at the moment of expansion [Bq]
"""
def err_standard_strength(a,ea,t,et,lambda_):
    return np.sqrt(((1-np.exp(-lambda_*t*24*60*60))*ea)**2+(a*np.exp(-lambda_*t*24*60*60)*et)**2)
