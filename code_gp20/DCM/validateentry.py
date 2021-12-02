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
        try:
            # filters required parameters from the parameters dict and saves in new dict
            self._parameters_dict = self._find_parameters_for_mode(valid_parameters, parameters_dict)
        except ParameterError as error:
            return str(error)

    ##################
    # Public methods #
    ##################
    # run checks
    def run_checks(self):
        """
        Run all the checks for the parameters
        Returns error if failed and None if pass
        """
        # Convert parameters into the right types and output errors if it hits any
        try:
            self._convert_parameter_types()
            self._do_range_checks()
            self._do_cross_checks()
        except ParameterError as error:
            return str(error)

        return None
    # Return parameters
    def get_parameters(self):
        """
        Getter for final parameters
        """
        return self._parameters_dict

    ###################
    # Private methods #
    ###################
    # find_parameters for mode
    def _find_parameters_for_mode(self, valid_parameters, parameters_dict):
        """
        Find all the valid parameters in parameter_dict using valid_parameters
        and saves in new list
        """
        _parameters_dict_new = dict()
        # Find all parameters and saves in new dict
        try:
            for parameter in valid_parameters:
                # NOTE: Only has strings, not entry objects
                _parameters_dict_new[parameter] = parameters_dict[parameter].get()
        except KeyError:
            raise ParameterError('Error: Not enough parameters have been passed to the manager')
        # Returns new dict
        return _parameters_dict_new
    
    #-----------------------------------------------------------
    # Type conversions 
    #-----------------------------------------------------------

    def _convert_parameter_types(self):
        """
        Converts the parameters_dict values into the correct type
        """
        # Try to convert the types of each by calling the function
        for parameter_name, parameter_value in self._parameters_dict.items():
            # Save to the parameters dict
            convert_func = getattr(self, "_convert_%s_value" % parameter_name)
            self._parameters_dict[parameter_name] = convert_func(parameter_value)

    def _convert_lower_rate_limit_value(self, value):
        """
        Lower rate limit input must be an integer incremented by 5
        """
        try:
            lrl = float(value)
            if 50 <= lrl <= 90:
                lrl = int(round(lrl))
            else:
                lrl = int(5 * round(lrl/5))
            return lrl
        except ValueError:
            self._parameters_dict['lower_rate_limit'] = ""
            raise ParameterError('Error: Lower rate limit input must be a number')

    def _convert_upper_rate_limit_value(self, value):
        """
        Upper rate limit input must be an integer incremented by 5
        """
        try:
            url = float(value)
            url = int(5 * round(url/5))
            return url
        except ValueError:
            self._parameters_dict['upper_rate_limit'] = ""
            raise ParameterError('Error: Upper rate limit input must be a number')

    def _convert_atrial_amplitude_value(self, value):
        """
        Atrial amplitude must be float incremented by 0.1V
        """
        try:
            aa = float("{:.1f}".format(float(value)))
            ##if (3.5 <= aa <= 7.0):
            ##    aa = round(2 * aa) / 2.0
            return aa
        except ValueError:
            self._parameters_dict['atrial_amplitude'] = ""
            raise ParameterError('Error: Atrial amplitude input must be a number')

    def _convert_atrial_pw_value(self, value):
        """
        Atrial pw must be float incremented by 0.1ms
        """
        try:
            #apw = float("{:.1f}".format(float(value)))
            apw = int(value)
            return apw
        except ValueError:
            self._parameters_dict['atrial_pw'] = ""
            raise ParameterError('Error: Atrial pulse width input must be a number')

    def _convert_ventricular_amplitude_value(self, value):
        """
        Ventricular amplitude must be float incremented by 0.1V
        """
        try:
            va = float("{:.1f}".format(float(value)))
            #if (3.5 <= va <= 7.0):
            #    va = round(2 * va) / 2.0
            return va
        except ValueError:
            self._parameters_dict['ventricular_amplitude'] = ""
            raise ParameterError('Error: Ventricular amplitude input must be a number')

    def _convert_ventricular_pw_value(self, value):
        """
        Ventricular pulse width must be float incremented by 1ms
        """
        try:
            #vpw = float("{:.1f}".format(float(value)))
            vpw = int(value)
            return vpw
        except ValueError:
            self._parameters_dict['ventricular_pw'] = ""
            raise ParameterError('Error: Ventricular pulse width input must be a number')

    def _convert_vrp_value(self, value):
        """
        VRP input must be an integer with 10 ms increments
        """
        try:
            vrp = float(value)
            vrp = int(10 * round(vrp/10))
            return vrp
        except ValueError:
            self._parameters_dict['vrp'] = ""
            raise ParameterError('Error: VRP input must be a number')

    def _convert_arp_value(self, value):
        """
        ARP input must be an integer with 10 ms increments
        """
        try:
            arp = float(value)
            arp = int(10 * round(arp/10))
            return arp
        except ValueError:
            self._parameters_dict['arp'] = ""
            raise ParameterError('Error: ARP input must be a number')

    def _convert_max_sensor_rate_value(self, value):
        """
        max sensor rate must be a integer with 5 ppm increments
        """
        try:
            max_sensor_rate = float(value)
            max_sensor_rate = int(5 * round(max_sensor_rate/5))
            return max_sensor_rate
        except ValueError:
            self._parameters_dict['max_sensor_rate'] = ""
            raise ParameterError('Error: Max sensor rate must be a number')

    def _convert_fixed_av_delay_value(self, value):
        """
        fixed av delay must be integer with increments of 10
        """
        try:
            fixed_av_delay = float(value)
            fixed_av_delay = int(10 * round(fixed_av_delay/10))
            return fixed_av_delay
        except ValueError:
            self._parameters_dict['fixed_av_delay'] = ""
            raise ParameterError('Error: Fixed av delay must be a number')

    def _convert_atrial_sensitivity_value(self, value):
        """
        atrial sensitivity must be a float with increments of 0.5mV
        """
        if value == '':
            return ''
        try:
            atrial_sens = float("{:.1f}".format(float(value)))
            #if (0 <= atrial_sens <= 1.0):
            #    atrial_sens = round(4 * atrial_sens) / 4.0
            #else:
            #    atrial_sens = round(2 * atrial_sens) / 2.0

            return atrial_sens
        except ValueError:
            self._parameters_dict['atrial_sensitivity'] = ""
            raise ParameterError('Error: Atrial sensitivity must be a number')

    def _convert_ventricular_sensitivity_value(self, value):
        """
        ventricular sensitivity must be a float with increments of 0.5mV
        """
        if value == '':
            return ''
        try:
            ventricular_sens = float("{:.1f}".format(float(value)))
            #if (0 <= ventricular_sens <= 1.0):
            #    ventricular_sens = round(4 * ventricular_sens) / 4.0
            #else:
            #    ventricular_sens = round(2 * ventricular_sens) / 2.0

            return ventricular_sens
        except ValueError:
            self._parameters_dict['ventricular_sensitivity'] = ""
            raise ParameterError('Error: Ventricular sensitivity must be a number')

    def _convert_pvarp_value(self, value):
        """
        PVARP must be an integer with 10 ms increments
        """
        try:
            pvarp = float(value)
            pvarp = int(10 * round(pvarp/10))
            return pvarp
        except ValueError:
            self._parameters_dict['pvarp'] = ""
            raise ParameterError('Error: PVARP must be a number')

    def _convert_hysteresis_value(self, value):
        """
        Hysteresis must be an integer with increments of 1 or 5
        """
        try:
            hysteresis = float(value)
            if 50 <= hysteresis <= 90:
                hysteresis = int(round(hysteresis))
            else:
                hysteresis = int(5 * round(hysteresis/5))
            return hysteresis
        except ValueError:
            self._parameters_dict['hysteresis'] = ""
            raise ParameterError('Error: Hysteresis input must be a number')

    def _convert_rate_smoothing_value(self, value):
        """
        Rate smoothing must be an integer with multiple of 3
        """
        try:
            rate_smoothing = float(value)
            rate_smoothing = int(3*round(rate_smoothing/3))
            if rate_smoothing == 24:
                rate_smoothing = 25
            return rate_smoothing
        except ValueError:
            self._parameters_dict['rate_smoothing'] = ""
            raise ParameterError('Error: Rate smoothing input must be a number')

    def _convert_activity_threshold_value(self, value):
        """
        Activity threshold must be a string value
        """
        # No need for checking because it is a dropdown and cannot have errors
        return value

    def _convert_reaction_time_value(self, value):
        """
        Reaction time must be an integer with 10 increments
        """
        try:
            reaction_time = float(value)
            reaction_time = int(10 * round(reaction_time/10))
            return reaction_time
        except ValueError:
            self._parameters_dict['reaction_time'] = ""
            raise ParameterError('Error: Reaction time must be a number')

    def _convert_response_factor_value(self, value):
        """
        Response factor must be an integer from 1 - 16
        """
        try:
            response_factor = int(round(float(value)))
            return response_factor
        except ValueError:
            self._parameters_dict['response_factor'] = ""
            raise ParameterError('Error: Response factor must be a number')

    def _convert_recovery_time_value(self, value):
        """
        Recovery time must be an integer from 2-16
        """
        try:
            recovery_time = int(round(float(value)))
            return recovery_time
        except ValueError:
            self._parameters_dict['recovery_time'] = ""
            raise ParameterError('Error: Recovery time must be a number')

    #-----------------------------------------------------------
    # Range Checks
    #-----------------------------------------------------------
    def _do_range_checks(self):
        """
        Checks the range of the parameters to make sure they are in correct range
        """
        # Run all range checks for parameters
        for parameter_name, parameter_value in self._parameters_dict.items():
            # Save to the parameters dict
            range_check_func = getattr(self, "_check_%s_range" % parameter_name)
            range_check_func(parameter_value)

    def _check_lower_rate_limit_range(self, value):
        """
        Lower rate limit must be between 30 and 175 ppm
        """
        if not (30 <= value <= 175):
            self._parameters_dict['lower_rate_limit'] = ""
            raise ParameterError('Error: Lower rate limit input must be between 30 - 175 ppm')

    def _check_upper_rate_limit_range(self, value):
        """
        Upper rate limit must be between 50 and 175 ppm
        """
        if not (50 <= value <= 175):
            self._parameters_dict['upper_rate_limit'] = ""
            raise ParameterError('Error: Upper rate limit input must be between 50 - 175 ppm')

    def _check_atrial_amplitude_range(self, value):
        """
        Atrial amplitude range must be in ranges 0-5.0
        """
        if not (0 <= value <= 5.0):
            self._parameters_dict['atrial_amplitude'] = ""
            raise ParameterError('Error: Atrial amplitude must be in ranges 0V - 5V')

    def _check_atrial_pw_range(self, value):
        """
        Atrial pw must be 1-30
        """
        if not (1 <= value <= 30):
            self._parameters_dict['atrial_pw'] = ""
            raise ParameterError('Error: Atrial pulse width must be 1ms - 30ms')

    def _check_ventricular_amplitude_range(self, value):
        """
        Ventricular amplitude range must be in ranges 0-5.0
        """
        if not (0 <= value <= 5.0):
            self._parameters_dict['ventricular_amplitude'] = ""
            raise ParameterError('Error: Ventricular amplitude must be in ranges 0V - 5V')

    def _check_ventricular_pw_range(self, value):
        """
        Ventricular pw must be 1-30
        """
        if not (1 <= value <= 30):
            self._parameters_dict['ventricular_pw'] = ""
            raise ParameterError('Error: Ventricular pulse width must be 1ms - 30ms')

    def _check_vrp_range(self, value):
        """
        Ventricular refactory period must be in range 150ms - 500ms
        """
        if not (150 <= value <= 500):
            self._parameters_dict['vrp'] = ""
            raise ParameterError('Error: Ventricular refactory period must be in range 150ms - 500ms')
    def _check_arp_range(self, value):
        """
        Atrial refactory period must be in range 150ms - 500ms
        """
        if not (150 <= value <= 500):
            self._parameters_dict['arp'] = ""
            raise ParameterError('Error: Atrial refactory period must be in range 150ms - 500ms')

    def _check_max_sensor_rate_range(self, value):
        """
        Max sensor rate must be between 50-175
        """
        if not (50 <= value <= 175):
            self._parameters_dict['max_sensor_rate'] = ""
            raise ParameterError('Error: Max sensor rate must be in range 50ppm - 175ppm')

    def _check_fixed_av_delay_range(self, value):
        """
        Fixed av delay must be betwee 70-300
        """
        if not (70 <= value <= 300):
            self._parameters_dict['fixed_av_delay'] = ""
            raise ParameterError('Error: Fixed AV delay must be in range 70ms - 300ms')

    def _check_atrial_sensitivity_range(self, value):
        """
        Atrial sensitivity must be between 0 and 5
        """
        if value == '':
            return
        if not (0 <= value <= 5):
            self._parameters_dict['atrial_sensitivity'] = ""
            raise ParameterError('Error: Atrial sensitivity must be in range 0V to 5V')

    def _check_ventricular_sensitivity_range(self, value):
        """
        Ventricular sensitivity must be between 0 and 5
        """
        if value == '':
            return
        if not (0 <= value <= 5):
            self._parameters_dict['ventricular_sensitivity'] = ""
            raise ParameterError('Error: Ventricular sensitivity must be in range 0V to 5V')

    def _check_pvarp_range(self, value):
        """
        PVARP must be between 150-500
        """
        if not (150 <= value <= 500):
            self._parameters_dict['pvarp'] = ""
            raise ParameterError('Error: PVARP must be in range 150ms - 500ms')

    def _check_hysteresis_range(self, value):
        """
        Hysteresis must be 0 or 30 - 175
        """
        if not (value == 0) and not (30 <= value <= 175):
            self._parameters_dict['hysteresis'] = ""
            raise ParameterError('Error: Hysteresis range must be 0 or between 30ppm - 175ppm')

    def _check_activity_threshold_range(self, value):
        """
        Must be one of the valid settings
        """
        if value not in ['V-Low', 'Low', 'Med-Low', 'Med', 'Med-High', 'High', 'V-High']:
            self._parameters_dict['activity_threshold'] = "Med"
            raise ParameterError('Error: Activity threshold must be one of the following settings: \
                                  V-Low, Low, Med-Low, Med, Med-High, High, V-High')

    def _check_rate_smoothing_range(self, value):
        """
        Rate smoothing must be between 0 - 25%
        """
        if not (0 <= value <= 25):
            self._parameters_dcit['rate_smoothing'] = ""
            raise ParameterError('Error: Rate smoothing must be in range 0% - 25%')

    def _check_reaction_time_range(self, value):
        """
        Reaction time must be between 10 - 50
        """
        if not (10 <= value <= 50):
            self._parameters_dict['reaction_time'] = ""
            raise ParameterError('Error: Reaction time must be in range 10 sec - 50 sec')

    def _check_response_factor_range(self, value):
        """
        Response factor must be between 1-16
        """
        if not (1 <= value <= 16):
            self._parameters_dict['response_factor'] = ""
            raise ParameterError('Error: Response factor must be in range 1 - 16')
        
    def _check_recovery_time_range(self, value):
        """
        Recovery time must be between 2-16 min
        """
        if not (2 <= value <= 16):
            self._parameters_dict['recovery_time'] = ""
            raise ParameterError('Error: Recovery factor must be in range 2min - 16min')
    #-----------------------------------------------------------
    # Cross Checks
    #-----------------------------------------------------------
    def _do_cross_checks(self):
        """
        Checks the compatibility of parameters on other related parameters
        """
        # Iterate through all combintations of checks and find name
        for parameter_1, value_1 in self._parameters_dict.items():
            for parameter_2, value_2 in self._parameters_dict.items():
                try:
                    cross_check_func = getattr(self, "_cross_check_%s_vs_%s" % (parameter_1, parameter_2))
                    cross_check_func(value_1, value_2)
                except AttributeError:
                    continue

    def _cross_check_lower_rate_limit_vs_upper_rate_limit(self, lrl, url):
        if lrl >= url:
            self._parameters_dict['lower_rate_limit'] = ""
            self._parameters_dict['upper_rate_limit'] = ""
            raise ParameterError("Error: Lower rate limit must be smaller than the upper rate limit")

