class ParameterManager(object):
    def __init__(self, valid_parameters, parameters_dict):
        """
        Constructor for validating the parameters of the pacemaker, valid parameters for the operating
        mode will not be checked (this is checked earlier)

        Inputs:
            valid_parameters:
                Required: True
                Description: List of valid parameter strings for the mode that is selected
                Example: ['lower_rate_limit',
                         'upper_rate_limit',
                         'atrial_amplitude',
                         'atrial_pw']
            parameters_dict:
                Required: True
                Description: dictionary with parameter name strings as keys and tk entry objects as values
                Example: {'lower_rate_limit': <tkinter.Entry object .!frame6.!entry>, 
                          'upper_rate_limit': <tkinter.Entry object .!frame6.!entry2>,
                          'atrial_amplitude': <tkinter.Entry object .!frame6.!entry3>,
                          'atrial_pw': <tkinter.Entry object .!frame6.!entry4>,
                          'ventricular_amplitude': <tkinter.Entry object .!frame6.!entry5>,
                          'ventricular_pw': <tkinter.Entry object .!frame6.!entry6>,
                          'vrp': <tkinter.Entry object .!frame6.!entry7>,
                          'arp': <tkinter.Entry object .!frame6.!entry8>}
        """
        pass
    # TODO: Cross Checks
    # TODO: Interval Checks
    # TODO: Range Checks
    # TODO: Return parameters
