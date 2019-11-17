from math import*
import numpy as np

"""
Author: Stefan Bruenner
Date: 2019/10/31

Description:
Rn222 mean lifetime [1/s]
Rn222 half lifetime 3.84 days.

Variables:
- NONE

Return:
- Rn222 mean lifetime [1/s]
"""
def lRn():
    return -log(0.5)/(3.84*24*60*60)


"""
Author: Stefan Bruenner
Date: 2019/10/31

Description:
Ra226 mean lifetime [1/s].
Ra226 half lifetime 1602 days.

Variables:
- NONE

Return:
-Ra226 mean lifetime [1/s]
"""
def lRa():
    return -log(0.5)/(1602*365.*24*60*60)


"""
Author: Joaquim Palacio
Date: 2019/10/31

Description:
Po210 mean lifetime [1/s].
Po210 half lifetime 138376 days.

Variables:
- NONE

Return:
- Po210 mean lifetime [1/s]
"""
def lPo210():
    return -log(0.5)/(138376*24*60*60)


"""
Author: Stefan Bruenner
Date: 2019/10/31

Description:
Emanation sample strength based on the emanation time.
The emanation sample did not reach its emanation equilibrium yet.

Variables:
- t = emanation time [day]
- lambda_ = mean lifetime of the source [1/s]

Return
- percentatge of strength [%*0.01]
"""
def source_strength(t,lambda_):
    return (1-np.exp(-lambda_*t*(24*60*60)))


"""
Author: Stefan Bruenner
Date: 2019/10/31

Description:
Error assosiated to the emanation sample strength based on the emanation time.
The emanation sample did not reach its emanation equilibrium yet.

Variables:
- t = emanation time [day]
- dt = Error emanation time [day]
- lambda_ = mean lifetime of the source [1/s]

Return:
- Error percentatge of strength [%*0.01]
"""
def err_source_strength(t,dt,lambda_):
    return (np.exp(-lambda_*t*24*60*60)*dt)


"""
Author: Stefan Bruenner
Date: 2019/10/31
Description:
Some of the sample decayed before the start of DAQ

Variables:
- t = Time between emanation stop of the sample and the start of the measurement [s]
- lambda_ = mean lifetime of the source [1/s]

Return:
- percentatge of decayed sample [%*0.01]
"""
def decay_before_measurement(t,lambda_):
    return exp(-lambda_*t)


"""
Author: Stefan Bruenner
Date: 2019/10/31

Description:
Not all the gass is analyzed during the extraction.
% of the gas that could not be extracted.

Variables:
- p0 = pressure begin extraction [mbar]
- p1 = pressure end extraction [mbar]

Return:
- percentatge of gas extracted [%*0.01]
"""
def gas_extracted(p0,p1):
    return 1.-p1/p0


"""
Author: Stefan Bruenner
Date: 2019/10/31
Description:
Not all the gass is analyzed during the extraction.
Error in % of the gas that could not be extracted.

Variables:
- p0 = pressure begin extraction [mbar]
- p1 = pressure end extraction [mbar]
- ep = error pressure [mbar]

Return:
- Error in percentatge of gas extracted [%*0.01]

"""
def error_gas_extracted(p0,p1,ep):
    return sqrt((ep/p0)**2 + (ep*p1/p0**2)**2)


"""
Author: Stefan Bruenner
Date: 2019/10/31
Description:
Activity of a given source.
The activity filled into the detector (i.e. the activity when started the measurement) is generally given by

$$A = \frac{c\cdot \lambda_{Rn}}{\epsilon} \cdot \frac{1}{1-e^{-\lambda_{Rn}\cdot \Delta t}}$$

Where $c$ is the number of counts, $\epsilon$ the detector efficiency and $\Delta t$ the run time of the measurement.

Variables:
- ncount = # events [#]
- tt1 = initial time of measurement [s]
- tt2 = final time of measurement [s]
- eff = efficiency of the detector [%*0.01]
- lambda_ = mean lifetime of the source [1/s]

Return:
- Measured activity [bq]
"""
def act(ncount,tt1,tt2,eff,lambda_):
    return ncount*lambda_/(eff*(1-np.exp(-lambda_*(tt2-tt1))))

"""
Author: Stefan Bruenner
Date: 2019/10/31
Description:
Error on the activity of a given source.
The activity filled into the detector (i.e. the activity when started the measurement) is generally given by

$$A = \frac{c\cdot \lambda_{Rn}}{\epsilon} \cdot \frac{1}{1-e^{-\lambda_{Rn}\cdot \Delta t}}$$

Where $c$ is the number of counts, $\epsilon$ the detector efficiency and $\Delta t$ the run time of the measurement.

Variables:
- ncount = # events [#]
- tt1 = initial time of measurement [s]
- tt2 = final time of measurement [s]
- eff = efficiency of the detector [%*0.01]
- eeff = error on the efficiency of the detector [%*0.01]
- lambda_ = mean lifetime of the source [1/s]

Return:
- Error no the measured activity [bq]
"""
def err_act(ncount,tt1,tt2,eff,eeff,lambda_):
    return np.sqrt((np.sqrt(ncount)*lambda_/(eff*(1-np.exp(-lambda_*(tt2-tt1)))))**2
    + (ncount*lambda_*eeff/(eff*eff*(1-np.exp(-lambda_*(tt2-tt1)))))**2)

"""
Author: Stefan Bruenner
Date: 2019/10/31
Description:
Error on the activity of a given source taking into account the error on the coeficient factors c1, c2 and c3:

- c1: The emanation sample did not reach its emanation equilibrium yet.
- c2: Some of the sample has been decayed before the start of DAQ.
- c3: Only a fraction of the sample has been extracted (not pumped to 0 mbar).

The activity filled into the detector (i.e. the activity when started the measurement) is generally given by

$$A = \frac{c\cdot \lambda_{Rn}}{\epsilon} \cdot \frac{1}{1-e^{-\lambda_{Rn}\cdot \Delta t}}$$

Where $c$ is the number of counts, $\epsilon$ the detector efficiency and $\Delta t$ the run time of the measurement.

Variables:
- A = activity [Bq]
- eA = error acitivity [Bq]
- c1  [%*0.01]
- ec1 [%*0.01]
- c2  [%*0.01]
- ec2 = 0 (not taken into account since it is included in c1)
- c3  [%*0.01]
- ec3 [%*0.01]

Return:
- Error no the measured activity taking into account the errors on the
coeficient factors c1, c2 and c3 [bq]
"""
def err_act_factors(A,eA,c1,ec1,c2,c3,ec3):
    return np.sqrt((eA/(c1*c2*c3))**2 + (A*ec1/(c1**2*c2*c3))**2
    + (A*ec3/(c1*c2*c3**2))**2)


"""
Author: Joaquim Palacio
Date: 2019/10/31
Description:
Ratio between two isotopes/elements

Variables:
ncountA = # events of A [#]
ncountB = # events of B [#]

Return:
- Ratio between isotopes A and B [1]
"""
def element_ratio(ncountA,ncountB):
    ncountA=ncountA*1.
    ncount_element_B=ncountB*1.

    return ncountA/ncountB


"""
Author: Joaquim Palacio
Date: 2019/10/31
Description:
Error in ratio between two isotopes/elements

Variables:
ncountA = # events of A [#]
ncountB = # events of B [#]

Return:
- Error in ratio between isotopes A and B [1]
"""
def error_element_ratio(ncount_element_A,ncount_element_B):

    ncount_element_A=ncount_element_A*1.
    ncount_element_B=ncount_element_B*1.

    return sqrt((sqrt(ncount_element_A)/ncount_element_B)**2
                 + (ncount_element_A*sqrt(ncount_element_B)/ncount_element_B**2)**2)
