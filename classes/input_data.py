class Input_Data:

    """A class that stores the information for each different variable
       that belongs to a certain data set
       
       mass        = experimentally recorded mass                             (array)
       time        = experimentally recorded time                             (array)
       temperature = experimental recorded temperature                        (array)
       temp_units  = the units of the recorded temperature                    (string)
       conversion  = experimentally recorded conversion                       (array)
       a_invfit    = fitted conversion from the 'inverse fit'                 (array)
       t_invfit    = fitted time from the 'inverse fit'                       (array)
       t_poly      = the polynomial that describes the 'inverse fit' t = f(a) (class)
       a_nrmfit    = fitted conversion from the 'normal fit'                  (array)
       t_nrmfit    = fitted time from the 'normal fit'                        (array)
       a_poly      = the polynomial that describes the 'normal fit' a = f(t)  (class)
       rrate       = reaction rate calculated according to the 'normal fit'   (array)
       """

    def __init__(self, mass, time, temperature, temp_units, conversion, a_invfit, t_invfit, t_poly, a_nrmfit, t_nrmfit, a_poly, rrate):
        self.mass        = mass
        self.time        = time
        self.temperature = temperature
        self.temp_units  = temp_units
        self.conversion  = conversion
        self.a_invfit    = a_invfit
        self.t_invfit    = t_invfit
        self.t_poly      = t_poly
        self.a_nrmfit    = a_nrmfit
        self.t_nrmfit    = t_nrmfit
        self.a_poly      = a_poly
        self.rrate       = rrate