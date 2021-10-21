import tkinter as tk
from tkinter.constants import W
from db import create_user, get_user, get_number_of_users, update_parameters
from tkinter import messagebox
from validateentry import *

VALID_PARAMETERS = {'aoo': ['lower_rate_limit',
                            'upper_rate_limit',
                            'atrial_amplitude',
                            'atrial_pw'],
                    'voo': ['lower_rate_limit',
                            'upper_rate_limit',
                            'ventricular_amplitude', 
                            'ventricular_pw'],
                    'aai': ['lower_rate_limit', 
                            'upper_rate_limit', 
                            'atrial_amplitude', 
                            'atrial_pw', 
                            'arp'],
                    'vvi': ['lower_rate_limit', 
                            'upper_rate_limit', 
                            'ventricular_amplitude', 
                            'ventricular_pw',
                            'vrp']}

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

    def _on_submit_login(self, username: str, password: str):
        self.user = get_user(username)
        if self.user is None:
            tk.Label(self.frame, width=50, text="User not found.", pady=60).grid(row=4,columnspan=2)
        elif self.user['password'] == password:
            self._create_dcm_screen()
        else:
            tk.Label(self.frame, width=50, text="Incorrect password.", pady=60).grid(row=4,columnspan=2)
    
    def _on_submit_register(self, username: str, password: str):
        user_created = create_user(username, password)
        device_id = 123 # change for assignment 2
        if (get_number_of_users(device_id) >= 10):
            tk.Label(self.frame, width=50, text="Maximum number of users reached.", pady=60).grid(row=4,columnspan=2)
        elif(len(username)==0 or len(password)==0):
            tk.Label(self.frame, width=50, text="Username and password cannot be empty.", pady=60).grid(row=4,columnspan=2)
        elif user_created:
            self._create_dcm_screen()
        else:
            tk.Label(self.frame, width=50, text="User with that username already exists.", pady=60).grid(row=4,columnspan=2)

    def _display_error_message(self, msg):
        messagebox.showerror("Error", msg)
    
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
        self.window.minsize(800, 450)

        # Parameters
        parameter_label = tk.Label(self.frame, text='DCM Parameters', pady=15)
        lower_rate_limit = tk.Label(self.frame, text='Lower rate limit', pady=10) #all
        upper_rate_limit = tk.Label(self.frame, text='Upper rate limit', pady=10)#all
        atrial_amplitude = tk.Label(self.frame, text='Atrial amplitude', pady=10)#AOO, AAI
        atrial_pw = tk.Label(self.frame, text='Atrial PW', pady=10)#AAO, AAI
        ventricular_amplitude = tk.Label(self.frame, text='Ventricular Amplitude', pady=10)#VOO, VVI
        ventricular_pw = tk.Label(self.frame, text='Ventyricular PW', pady=10)#VOO, VVI
        vrp = tk.Label(self.frame, text='VRP', pady=10)#VVI
        arp = tk.Label(self.frame, text='ARP', pady=10)#AAI

        self.parameters_dict['lower_rate_limit'] = tk.Entry(self.frame) #all
        self.parameters_dict['upper_rate_limit'] = tk.Entry(self.frame) #all
        self.parameters_dict['atrial_amplitude'] = tk.Entry(self.frame) #AOO, AAI
        self.parameters_dict['atrial_pw'] = tk.Entry(self.frame) #AAO, AAI
        self.parameters_dict['ventricular_amplitude'] = tk.Entry(self.frame) #VOO, VVI
        self.parameters_dict['ventricular_pw'] = tk.Entry(self.frame) #VOO, VVI
        self.parameters_dict['vrp'] = tk.Entry(self.frame) #VVI
        self.parameters_dict['arp'] = tk.Entry(self.frame) #AAI

        # Operating modes
        modes_label = tk.Label(self.frame, text='Operating Modes', pady=15)
        self.modes_dict['aoo'] = tk.Button(self.frame, text='AOO', width=10, height=5, command=lambda: self._set_mode('aoo'))
        self.modes_dict['voo'] = tk.Button(self.frame, text='VOO', width=10, height=5, command=lambda: self._set_mode('voo'))
        self.modes_dict['aai'] = tk.Button(self.frame, text='AAI', width=10, height=5, command=lambda: self._set_mode('aai'))
        self.modes_dict['vvi'] = tk.Button(self.frame, text='VVI', width=10, height=5, command=lambda: self._set_mode('vvi'))
        
        # Status
        status_label = tk.Label(self.frame, text='Status', pady=15)
        device_connection = tk.Label(self.frame, fg='red', text='Device disconnected')
        device_information = tk.Label(self.frame, fg='red', text='No device data available')

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
        atrial_amplitude.grid(row=3, column=1)
        atrial_pw.grid(row=4, column=1)
        ventricular_amplitude.grid(row=5, column=1)
        ventricular_pw.grid(row=6, column=1)
        vrp.grid(row=7, column=1)
        arp.grid(row=8, column=1)

        self.parameters_dict['lower_rate_limit'].grid(row=1, column=2)
        self.parameters_dict['upper_rate_limit'].grid(row=2, column=2)
        self.parameters_dict['atrial_amplitude'].grid(row=3, column=2)
        self.parameters_dict['atrial_pw'].grid(row=4, column=2)
        self.parameters_dict['ventricular_amplitude'].grid(row=5, column=2)
        self.parameters_dict['ventricular_pw'].grid(row=6, column=2)
        self.parameters_dict['vrp'].grid(row=7, column=2)
        self.parameters_dict['arp'].grid(row=8, column=2)

        # Operating mode buttons
        self.modes_dict['aoo'].grid(row=1, column=0, rowspan=2)
        self.modes_dict['voo'].grid(row=3, column=0, rowspan=2)
        self.modes_dict['aai'].grid(row=5, column=0, rowspan=2)
        self.modes_dict['vvi'].grid(row=7, column=0, rowspan=2)

        # Status
        device_connection.grid(row=1, column=3, columnspan=2)
        device_information.grid(row=3, column=3, columnspan=2)

        # Submit button
        submit_button.grid(row=7, column=3, rowspan=2, columnspan=2)

        # exit buttons
        logout_button.grid(row=10, column=1)
        close_button.grid(row=10, column=3)

        self.frame.pack()

        self.state = "DCM"
        
    def _load_user_defaults(self):
        # get the right state
        self._set_mode(self.user['operating_mode'])

        for parameter, entry in self.parameters_dict.items():
            entry.insert(0, self.user['parameters'][parameter])

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

    def _find_parameters_for_mode(self, parameters_dict, mode):
        parameters_for_mode = dict()
        for parameter, entry in parameters_dict.items():
            if parameter in VALID_PARAMETERS[mode]:
                parameters_for_mode[parameter] = entry

        return parameters_for_mode


    def _submit_parameters(self):
        valid_parameters = self._find_parameters_for_mode(self.parameters_dict, self.mode)
        valid, errors = self._validate_parameters(self.mode)
        if (valid):
            update_parameters(self.user.username, valid_parameters)
        else:
            print(errors)

    def _validate_parameters(self, mode):
        valid = True
        errormessageset = {}

        #lrl
        valid, errormessage = validate_lrl(self.parameters_dict['lower_rate_limit'].get())
        if(errormessage != ''):
            errormessageset.add(errormessage)
            
        #url
        valid, errormessage = validate_url(self.parameters_dict['upper_rate_limit'].get())
        if(errormessage != ''):
            errormessageset.add(errormessage)

        #aa
        if(mode == "aoo" or mode == "aai"):
            valid, errormessage = validate_regulated_atrial_amp(self.parameters_dict['atrial_amplitude'].get())
            if(errormessage != ''):
                errormessageset.add(errormessage)

        #apw
        if(mode == "aoo" or mode == "aai"):
            valid, errormessage = validate_atrial_pw(self.parameters_dict['atrial_pw'].get())
            if(errormessage != ''):
                errormessageset.add(errormessage)

        #va
        if(mode == "voo" or mode == "vvi"):
            valid, errormessage = validate_regulated_ventricular_amp(self.parameters_dict['ventrical_amplitude'].get())
            if(errormessage != ''):
                errormessageset.add(errormessage)

        #vpw
        if(mode == "voo" or mode == "vvi"):
            valid, errormessage = validate_ventricular_pw(self.parameters_dict['ventrical_pw'].get())
            if(errormessage != ''):
                errormessageset.add(errormessage)

        #vrp
        if(mode == "vvi"):
            valid, errormessage = validate_vrp(self.parameters_dict['vrp'].get())
            if(errormessage != ''):
                errormessageset.add(errormessage)

        #arp
        if(mode == "aai"):
            valid, errormessage = validate_arp(self.parameters_dict['arp'].get())
            if(errormessage != ''):
                errormessageset.add(errormessage)
            
        return valid, errormessageset

                
    def quit_win(self):
        # console message
        print("Quitting DCM")

        # Quit
        self.window.quit()

        self.update()


    # Put gui in mainloop
    def loop(self):
        self.window.mainloop()

    # Updates gui for one cycle
    def update(self):
        self.window.update()
    