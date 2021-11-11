class ParameterError(Exception):
    """
    Error in parameter due to parameter checks
    """
    pass

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
        # filters required parameters from the parameters dict and saves in new dict
        self._parameters_dict = self._find_parameters_for_mode(valid_parameters, parameters_dict)
        print(self._parameters_dict)

    ##################
    # Public methods #
    ##################
    # TODO: run checks
    def run_checks(self):
        """
        Run all the checks for the parameters
        Returns error if failed and None if pass
        """
        # Convert parameters into the right types and output errors if it hits any
        try:
            self._convert_parameter_types()
            self._do_cross_checks()
            self._do_interval_checks()
            self._do_range_checks()
        except ParameterError as error:
            return repr(error)

        return None
    # TODO: Return parameters
    def get_parameters(self):
        """
        Getter for final parameters
        """
        return self._parameters_dict

    ###################
    # Private methods #
    ###################
    # TODO: find_parameters for mode
    def _find_parameters_for_mode(self, valid_parameters, parameters_dict):
        """
        Find all the valid parameters in parameter_dict using valid_parameters
        and saves in new list
        """
        _parameters_dict_new = dict()
        # Find all parameters and saves in new dict
        for parameter in valid_parameters:
            # NOTE: Only has strings, not entry objects
            _parameters_dict_new[parameter] = parameters_dict[parameter].get()
        # Returns new dict
        return _parameters_dict_new

    # TODO  Create type conversions
    def _convert_parameter_types(self):
        """
        Converts the parameters_dict values into the correct type
        """
        # Try to convert the types of each by calling the function
        # Save to the parameters dict
        # If a value error or some other error occurs
            # Raise ParameterError with message
        pass

    # TODO: Cross Checks
    def _do_cross_checks(self):
        """
        Checks the compatibility of parameters on other related parameters
        """
        pass

    # TODO: Interval Checks
    def _do_interval_checks(self):
        """
        Checks the intervals of parameters
        """
        pass

    # TODO: Range Checks
    def _do_range_checks(self):
        """
        Checks the range of the parameters to make sure they are in correct range
        """
        pass
