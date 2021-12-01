import tkinter as tk
import sys
import glob
import serial.tools.list_ports
import tkinter.ttk as ttk
from tkinter.constants import W
from db import *
from tkinter import messagebox
from validateentry import ParameterManager, ParameterError
from serialcom import SerialManager 
#from serial import *
from valid_parameters import VALID_PARAMETERS

class GUI(object):
    def __init__(self):
        # Create window
        self.window = tk.Tk()

        # Setup window
        self.window.title("DCM")
        self.window.resizable(1, 1) 
        self.window.minsize(500, 450)
        

        # Make GUI frame
        self.frame = tk.Frame()

        # Make popup window
        self.popup = ""

        # GUI state
        self.state = "Init"

        # Setup menu
        self._create_welcome_screen()

        # Update loop
        self.update()

        # Default user
        self.user = None
        
        #Mode arbitrarily selecting default
        self.mode = ""

        # declare needed buttons and entries
        self.modes_dict = dict()
        self.parameters_dict = dict()

        # Default serial manager
        self.serial = SerialManager()
        self.port_selection = None

    def _on_submit_login(self, username: str, password: str):
        self.user = get_user(username)
        if self.user is None:
            tk.Label(self.frame, width=50, text="User not found.", fg='red', pady=60).grid(row=4,columnspan=2)
        elif self.user['password'] == password:
            self._create_dcm_screen()
        else:
            tk.Label(self.frame, width=50, text="Incorrect password.", fg='red', pady=60).grid(row=4,columnspan=2)
    
    def _on_submit_register(self, username: str, password: str):
        user_created = False
        device_id = 123 # change for assignment 2
        if (get_number_of_users(device_id) > 10):
            tk.Label(self.frame, width=50, text="Maximum number of users reached.", fg='red', pady=60).grid(row=4,columnspan=2)
            return
        elif(len(username)==0 or len(password)==0):
            tk.Label(self.frame, width=50, text="Username and password cannot be empty.", fg='red', pady=60).grid(row=4,columnspan=2)
            return
        else:
            user_created = create_user(username, password)

        if user_created:
            self.user = get_user(username)
            self._create_dcm_screen()
        else:
            tk.Label(self.frame, width=50, text="User with that username already exists.", fg='red', pady=60).grid(row=4,columnspan=2)

    # Creates menu GUI
    def _create_welcome_screen(self):
        # Delete previous frame
        self.frame.destroy()

        self.window.resizable(1, 1) 
        self.window.minsize(500, 450)

        # Create a frame and pack with interface
        self.frame = tk.Frame(self.window)
        title = tk.Label(self.frame, width=50, text="Welcome to Group 20's \npacemaker DCM!", pady=60)
        register = tk.Button(self.frame, text="Create a New Account", width=50, pady=30, command=lambda: self._create_register_screen())
        login = tk.Button(self.frame, text='Login to existing account', width=50, pady=30, command=lambda: self._create_login_screen())
        close = tk.Button(self.frame, text='Close', width=50, pady=10, command=lambda: self.quit_win())
        title.grid(row=0)
        register.grid(row=1)
        login.grid(row=2)
        close.grid(row=3)
        self.frame.pack()

        self.state = 'Welcome'

    def _create_login_screen(self):
        # Delete previous frame
        self.frame.destroy()

        self.window.resizable(1, 1) 
        self.window.minsize(500, 300)

        # Create a frame and pack with interface
        self.frame = tk.Frame(self.window)
        title = tk.Label(self.frame, width=50, text='Login', pady=25)
        username = tk.Label(self.frame, text='Username',pady=10)
        password = tk.Label(self.frame, text='Password',pady=10)
        usernameEntry = tk.Entry(self.frame)
        passwordEntry = tk.Entry(self.frame, show='•')
        # redirect to verification
        loginButton = tk.Button(self.frame, text='Login', pady=5, width=15, command=lambda: self._on_submit_login(usernameEntry.get(),passwordEntry.get()))
        backButton = tk.Button(self.frame, text='Back', pady=5, width=15, command=lambda: self._create_welcome_screen())
        title.grid(row=0, columnspan=2)
        username.grid(row=1, column=0)
        usernameEntry.grid(row=1, column=1)
        password.grid(row=2, column=0)
        passwordEntry.grid(row=2, column=1)
        backButton.grid(row=3, column=0)
        loginButton.grid(row=3, column=1)
        self.frame.pack()

        self.state = 'Login'

    def _create_register_screen(self):
        # Delete previous frames
        self.frame.destroy()
        
        self.window.resizable(1, 1) 
        self.window.minsize(500, 300)

        # Create a frame and pack with interface
        self.frame = tk.Frame(self.window)
        title = tk.Label(self.frame, width=50, text='Create a New User', pady=25)
        username = tk.Label(self.frame, text='Username', pady=10)
        password = tk.Label(self.frame, text='Password', pady=10)
        usernameEntry = tk.Entry(self.frame)
        passwordEntry = tk.Entry(self.frame, show='•')
        # redirect to verification
        submitButton = tk.Button(self.frame, text='Submit', pady=5, width=15, command=lambda:self._on_submit_register(usernameEntry.get(),passwordEntry.get()))
        backButton = tk.Button(self.frame, text='Back', pady=5, width=15, command=lambda: self._create_welcome_screen())
        title.grid(row=0, columnspan=2)
        username.grid(row=1, column=0)
        usernameEntry.grid(row=1, column=1)
        password.grid(row=2, column=0)
        passwordEntry.grid(row=2, column=1)
        submitButton.grid(row=3, column=1)
        backButton.grid(row=3, column=0)
        self.frame.pack()

        self.state = 'Register'

    def _create_dcm_screen(self):
        # Delete previous frames
        self.frame.destroy()
        
        # create a frame and pack with interface
        self.frame = tk.Frame(self.window)

        # Resize window
        self.window.minsize(900, 750)

        # Parameters
        parameter_label = tk.Label(self.frame, text='DCM Parameters', pady=15)
        lower_rate_limit = tk.Label(self.frame, text='Lower rate limit (ppm)', pady=5) #all
        upper_rate_limit = tk.Label(self.frame, text='Upper rate limit (ppm)', pady=5)#all
        max_sensor_rate = tk.Label(self.frame, text='Maximum sensor rate (ppm)', pady=5)
        fixed_av_delay = tk.Label(self.frame, text='Fixed AV delay (ms)', pady=5)
        atrial_amplitude = tk.Label(self.frame, text='Atrial amplitude (V)', pady=5)#AOO, AAI
        atrial_pw = tk.Label(self.frame, text='Atrial pulse width (ms)', pady=5)#AAO, AAI
        atrial_sensitivity = tk.Label(self.frame, text='Atrial sensitivity (V)', pady=5)
        ventricular_amplitude = tk.Label(self.frame, text='Ventricular Amplitude (V)', pady=5)#VOO, VVI
        ventricular_pw = tk.Label(self.frame, text='Ventricular pulse width (ms)', pady=5)#VOO, VVI
        ventricular_sensitivity = tk.Label(self.frame, text='Ventricular sensitivity (V)', pady=5)
        vrp = tk.Label(self.frame, text='VRP (ms)', pady=5)#VVI
        arp = tk.Label(self.frame, text='ARP (ms)', pady=5)#AAI
        pvarp = tk.Label(self.frame, text='PVARP (ms)', pady=5)
        hysteresis = tk.Label(self.frame, text='Hysteresis rate limit (ppm) (Set to 0 if Off)', pady=5)
        rate_smoothing = tk.Label(self.frame, text='Rate Smoothing (%) (Set to 0 if Off)', pady=5)
        activity_threshold = tk.Label(self.frame, text='Activity threshold', pady=5)
        reaction_time = tk.Label(self.frame, text='Reaction Time (sec)', pady=5)
        response_factor = tk.Label(self.frame, text='Response Factor', pady=5)
        recovery_time = tk.Label(self.frame, text='Recovery Time (min)', pady=5)

        # FIXME: Think of way to have radio button for Hysteresis implemented
        # FIXME: Find way to implement activity threshold correctly
        # FIXME: ask team how they handle parameters passed to DCM

        rate_smoothing_options = ['On', 'Off']
        activity_threshold_options = ['V-Low', 'Low', 'Med-Low', 'Med', 'Med-High', 'High', 'V-High']
        self.parameters_dict['lower_rate_limit'] = tk.Entry(self.frame) #all
        self.parameters_dict['upper_rate_limit'] = tk.Entry(self.frame) #all
        self.parameters_dict['max_sensor_rate'] = tk.Entry(self.frame)
        self.parameters_dict['fixed_av_delay'] = tk.Entry(self.frame)
        self.parameters_dict['atrial_amplitude'] = tk.Entry(self.frame) #AOO, AAI
        self.parameters_dict['atrial_pw'] = tk.Entry(self.frame) #AAO, AAI
        self.parameters_dict['atrial_sensitivity'] = tk.Entry(self.frame)
        self.parameters_dict['ventricular_amplitude'] = tk.Entry(self.frame) #VOO, VVI
        self.parameters_dict['ventricular_pw'] = tk.Entry(self.frame) #VOO, VVI
        self.parameters_dict['ventricular_sensitivity'] = tk.Entry(self.frame)
        self.parameters_dict['vrp'] = tk.Entry(self.frame) #VVI
        self.parameters_dict['arp'] = tk.Entry(self.frame) #AAI
        self.parameters_dict['pvarp'] = tk.Entry(self.frame)
        self.parameters_dict['hysteresis'] = tk.Entry(self.frame)
        self.parameters_dict['rate_smoothing'] = tk.Entry(self.frame)
        self.parameters_dict['activity_threshold'] = ttk.Combobox(self.frame, value=activity_threshold_options)
        self.parameters_dict['reaction_time'] = tk.Entry(self.frame)
        self.parameters_dict['response_factor'] = tk.Entry(self.frame)
        self.parameters_dict['recovery_time'] = tk.Entry(self.frame)

        # Operating modes
        modes_label = tk.Label(self.frame, text='Operating Modes', pady=15)
        self.modes_dict['aoo'] = tk.Button(self.frame, text='AOO', width=10, command=lambda: self._set_mode('aoo'))
        self.modes_dict['voo'] = tk.Button(self.frame, text='VOO', width=10, command=lambda: self._set_mode('voo'))
        self.modes_dict['aai'] = tk.Button(self.frame, text='AAI', width=10, command=lambda: self._set_mode('aai'))
        self.modes_dict['vvi'] = tk.Button(self.frame, text='VVI', width=10, command=lambda: self._set_mode('vvi'))
        self.modes_dict['doo'] = tk.Button(self.frame, text='DOO', width=10, command=lambda: self._set_mode('doo'))
        self.modes_dict['aoor'] = tk.Button(self.frame, text='AOOR', width=10, command=lambda: self._set_mode('aoor'))
        self.modes_dict['voor'] = tk.Button(self.frame, text='VOOR', width=10, command=lambda: self._set_mode('voor'))
        self.modes_dict['aair'] = tk.Button(self.frame, text='AAIR', width=10, command=lambda: self._set_mode('aair'))
        self.modes_dict['vvir'] = tk.Button(self.frame, text='VVIR', width=10, command=lambda: self._set_mode('vvir'))
        self.modes_dict['door'] = tk.Button(self.frame, text='DOOR', width=10, command=lambda: self._set_mode('door'))

        # Status
        status_label = tk.Label(self.frame, text='Status', pady=15)

        submit_button = tk.Button(self.frame, text='Submit', width=10, height=5, command=lambda: self._submit_parameters())
        logout_button = tk.Button(self.frame, text='Logout', command=lambda: self._create_welcome_screen())
        close_button = tk.Button(self.frame, text='Close', command=lambda: self.quit_win())

        # Load in user defaults
        self._load_user_defaults()

        # Title locations
        parameter_label.grid(row=0, column=1, columnspan=2)
        modes_label.grid(row=0, column=0)
        status_label.grid(row=0, column=3)

        # Parameter button locations
        lower_rate_limit.grid(row=1, column=1)
        upper_rate_limit.grid(row=2, column=1)
        max_sensor_rate.grid(row=3, column=1)
        fixed_av_delay.grid(row=4, column=1)
        atrial_amplitude.grid(row=5, column=1)
        atrial_pw.grid(row=6, column=1)
        atrial_sensitivity.grid(row=7, column=1)
        ventricular_amplitude.grid(row=8, column=1)
        ventricular_pw.grid(row=9, column=1)
        ventricular_sensitivity.grid(row=10, column=1)
        vrp.grid(row=11, column=1)
        arp.grid(row=12, column=1)
        pvarp.grid(row=13, column=1)
        hysteresis.grid(row=14, column=1)
        rate_smoothing.grid(row=15, column=1)
        activity_threshold.grid(row=16, column=1)
        reaction_time.grid(row=17, column=1)
        response_factor.grid(row=18, column=1)
        recovery_time.grid(row=19, column=1)

        self.parameters_dict['lower_rate_limit'].grid(row=1, column=2)
        self.parameters_dict['upper_rate_limit'].grid(row=2, column=2)
        self.parameters_dict['max_sensor_rate'].grid(row=3, column=2)
        self.parameters_dict['fixed_av_delay'].grid(row=4, column=2)
        self.parameters_dict['atrial_amplitude'].grid(row=5, column=2)
        self.parameters_dict['atrial_pw'].grid(row=6, column=2)
        self.parameters_dict['atrial_sensitivity'].grid(row=7, column=2)
        self.parameters_dict['ventricular_amplitude'].grid(row=8, column=2)
        self.parameters_dict['ventricular_pw'].grid(row=9, column=2)
        self.parameters_dict['ventricular_sensitivity'].grid(row=10, column=2)
        self.parameters_dict['vrp'].grid(row=11, column=2)
        self.parameters_dict['arp'].grid(row=12, column=2)
        self.parameters_dict['pvarp'].grid(row=13, column=2)
        self.parameters_dict['hysteresis'].grid(row=14, column=2)
        self.parameters_dict['rate_smoothing'].grid(row=15, column=2)
        self.parameters_dict['activity_threshold'].grid(row=16, column=2)
        self.parameters_dict['reaction_time'].grid(row=17, column=2)
        self.parameters_dict['response_factor'].grid(row=18, column=2)
        self.parameters_dict['recovery_time'].grid(row=19, column=2)

        # Operating mode buttons
        # TODO: add new operating modes
        self.modes_dict['aoo'].grid(row=1, column=0, rowspan=2)
        self.modes_dict['voo'].grid(row=3, column=0, rowspan=2)
        self.modes_dict['aai'].grid(row=5, column=0, rowspan=2)
        self.modes_dict['vvi'].grid(row=7, column=0, rowspan=2)
        self.modes_dict['doo'].grid(row=9, column=0, rowspan=2)
        self.modes_dict['aoor'].grid(row=11, column=0, rowspan=2)
        self.modes_dict['voor'].grid(row=13, column=0, rowspan=2)
        self.modes_dict['aair'].grid(row=15, column=0, rowspan=2)
        self.modes_dict['vvir'].grid(row=17, column=0, rowspan=2)
        self.modes_dict['door'].grid(row=19, column=0, rowspan=2)

        # Status
        if not self.serial.serialPort:
            connect_button = tk.Button(self.frame, text='Connect', width=10, height=2, command=lambda: self._setup_device())
            refresh_button = tk.Button(self.frame, text='Refresh', width=10, height=2, command=lambda: self._refresh_devices())
            self.port_selection = ttk.Combobox(self.frame, value=self.serial._get_ports())
            device_connection = tk.Label(self.frame, fg='red', text='Device disconnected')
            device_information = tk.Label(self.frame, fg='red', text='No device data\navailable')

            connect_button.grid(row=1, column = 3, columnspan=2)
            refresh_button.grid(row=2, column = 3, columnspan=2)
            self.port_selection.grid(row=3, column = 3, columnspan=2)
            device_connection.grid(row=4, column=3, columnspan=2)
            device_information.grid(row=5, column=3, columnspan=2)
        else:
            disconnect_button = tk.Button(self.frame, text='Disconnect', width=10, height=2, command=lambda: self._disconnect_device())
            egram_label = tk.Label(self.frame, text='Electrogram')
            egram_options = [
                'Atrium',
                'Ventricle',
                'Both'
            ]
            egram_variable = tk.StringVar(self.frame)
            egram_variable.set(egram_options[0])
            egram_dropdown = tk.OptionMenu(self.frame, egram_variable, *egram_options)
            egram_button = tk.Button(self.frame, text='View Egram', width=10, height=1, command=lambda: self.serial.display_egram(egram_variable.get()))

            disconnect_button.grid(row=1, column = 3, columnspan=2)
            egram_label.grid(row=3, column=3, columnspan=2)
            egram_dropdown.grid(row=4, column=3)
            egram_button.grid(row=4, column=4)

        # Submit button
        submit_button.grid(row=7, column=3, rowspan=2, columnspan=2)

        # exit buttons
        logout_button.grid(row=20, column=1)
        close_button.grid(row=20, column=3)

        self.frame.pack()

        self.state = "DCM"
    
    def _setup_device(self):

        available_ports = self.serial._get_ports()

        selectedPort = self.port_selection.get()

        self.serial._init_serial(selectedPort)

        self._create_dcm_screen()

    def _refresh_devices(self):
        self._create_dcm_screen()
    
    def _disconnect_device(self):
        self.serial.serialPort = None
        self._create_dcm_screen()
        
    def _load_user_defaults(self):
        # get the right state
        self._set_mode(self.user['operating_mode'])

        for parameter, field in self.parameters_dict.items():
            prev_state = field['state']
            field['state'] = 'normal'
            field.delete(0, tk.END)
            field.insert(0, self.user['parameters'][parameter])
            field['state'] = prev_state

    def _set_mode(self, input_mode):
        if input_mode == '':
            return

        # disable the button
        for mode, button in self.modes_dict.items():
            if mode == input_mode:
                button['state'] = 'disabled'
                self.mode = input_mode
            else:
                button['state'] = 'normal'

        # enable all the currect entries
        for parameter, entry in self.parameters_dict.items():
            if parameter in VALID_PARAMETERS[input_mode]:
                entry['state'] = 'normal'
            else:
                entry['state'] = 'disabled'

    def _submit_parameters(self):
        if self.mode == '':
            messagebox.showerror("Error", 'No operating mode has been selected')
            return

        if self.serial == None:
            messagebox.showerror("Error", "No device connected")
            return
        
        if self.serial.is_plotting_egram():
            messagebox.showerror("Error", "Exit egram before submitting parameters")
            return

        param_manager = ParameterManager(VALID_PARAMETERS[self.mode], self.parameters_dict)
        error = param_manager.run_checks()
        valid_parameters = param_manager.get_parameters()
        self._update_parameter_entries(valid_parameters)

        if error:
            messagebox.showerror("Error", error)
            return

        success = self.serial._serial_out(VALID_PARAMETERS, valid_parameters, self.mode)
        if(success):
            messagebox.showerror("Success", 'Parameters saved and submitted') 
        else:
            messagebox.showerror("Error", "Parameters not successfully submitted")

    # update entry based on increments when submitting
    def _update_parameter_entries(self, valid_parameters):
        # update the parameter entries to use the new parameter values
        for name, value in valid_parameters.items():
            self.parameters_dict[name].delete(0, tk.END)
            self.parameters_dict[name].insert(0, str(value))

        self.update()

                
    def quit_win(self):
        # console message
        print("Quitting DCM")

        # Quit
        self.window.quit()

        self.update()

        exit(0)


    # Put gui in mainloop
    def loop(self):
        self.window.mainloop()

    # Updates gui for one cycle
    def update(self):
        self.window.update()
    
