import tkinter as tk
from tkinter.constants import W
from db import create_user, get_user, get_number_of_users
from tkinter import messagebox

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

        # declare needed buttons and entries as emtpy string
        self.aoo = None
        self.voo = None
        self.aai = None
        self.vvi = None
        self.lower_rate_limit_entry = None
        self.upper_rate_limit_entry = None #all
        self.atrial_amplitude_entry = None #AOO, AAI
        self.atrial_pw_entry = None #AAO, AAI
        self.ventricular_amplitude_entry = None #VOO, VVI
        self.ventricular_pw_entry = None #VOO, VVI
        self.vrp_entry = None #VVI
        self.arp_entry = None #AAI

    def _on_submit_login(self, username: str, password: str):
        user = get_user(username)
        if user is None:
            tk.Label(self.frame, width=50, text="User not found.", pady=60).grid(row=4,columnspan=2)
        elif user['password'] == password:
            self._create_dcm_screen()
        else:
            tk.Label(self.frame, width=50, text="Incorrect password.", pady=60).grid(row=4,columnspan=2)
    
    def on_submit_register(self, username: str, password: str):
        user_created = create_user(username, password)
        if (get_number_of_users() >= 10):
            tk.Label(self.frame, width=50, text="Maximum number of users reached.", pady=60).grid(row=4,columnspan=2)
        elif(len(username)==0 or len(password)==0):
            tk.Label(self.frame, width=50, text="Username and password cannot be empty.", pady=60).grid(row=4,columnspan=2)
        elif user_created:
            self.create_dcm_screen()
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
        passwordEntry = tk.Entry(self.frame)
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
        passwordEntry = tk.Entry(self.frame)
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
        vrp = tk.Label(self.frame, text='CRP', pady=10)#VVI
        arp = tk.Label(self.frame, text='ARP', pady=10)#AAI

        self.lower_rate_limit_entry = tk.Entry(self.frame) #all
        self.upper_rate_limit_entry = tk.Entry(self.frame) #all
        self.atrial_amplitude_entry = tk.Entry(self.frame) #AOO, AAI
        self.atrial_pw_entry = tk.Entry(self.frame) #AAO, AAI
        self.ventricular_amplitude_entry = tk.Entry(self.frame) #VOO, VVI
        self.ventricular_pw_entry = tk.Entry(self.frame) #VOO, VVI
        self.vrp_entry = tk.Entry(self.frame) #VVI
        self.arp_entry = tk.Entry(self.frame) #AAI

        # Operating modes
        modes_label = tk.Label(self.frame, text='Operating Modes', pady=15)
        self.aoo = tk.Button(self.frame, text='AOO', width=10, height=5, command=lambda: self._set_AOO_mode())
        self.voo = tk.Button(self.frame, text='VOO', width=10, height=5, command=lambda: self._set_VOO_mode())
        self.aai = tk.Button(self.frame, text='AAI', width=10, height=5, command=lambda: self._set_AAI_mode())
        self.vvi = tk.Button(self.frame, text='VVI', width=10, height=5, command=lambda: self._set_VVI_mode())
        
        # Status
        status_label = tk.Label(self.frame, text='Status', pady=15)
        device_connection = tk.Label(self.frame, fg='red', text='Device disconnected')
        device_information = tk.Label(self.frame, fg='red', text='No device data available')

        logout_button = tk.Button(self.frame, text='Logout', command=lambda: self._create_welcome_screen())
        close_button = tk.Button(self.frame, text='Close', command=lambda: self.quit_win())
        
        # TODO: Create Submit button and functionality

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

        self.lower_rate_limit_entry.grid(row=1, column=2)
        self.upper_rate_limit_entry.grid(row=2, column=2)
        self.atrial_amplitude_entry.grid(row=3, column=2)
        self.atrial_pw_entry.grid(row=4, column=2)
        self.ventricular_amplitude_entry.grid(row=5, column=2)
        self.ventricular_pw_entry.grid(row=6, column=2)
        self.vrp_entry.grid(row=7, column=2)
        self.arp_entry.grid(row=8, column=2)

        # Operating mode buttons
        self.aoo.grid(row=1, column=0, rowspan=2)
        self.voo.grid(row=3, column=0, rowspan=2)
        self.aai.grid(row=5, column=0, rowspan=2)
        self.vvi.grid(row=7, column=0, rowspan=2)

        # Status
        device_connection.grid(row=1, column=3, columnspan=2)
        device_information.grid(row=3, column=3, columnspan=2)

        # exit buttons
        logout_button.grid(row=9, column=0, columnspan=2)
        close_button.grid(row=9, column=2, columnspan=2)

        self.frame.pack()

        self.state = "DCM"
    
    def _set_AOO_mode(self):
        # disable the button
        self.aoo['state'] = 'disabled'
        self.voo['state'] = 'normal'
        self.aai['state'] = 'normal'
        self.vvi['state'] = 'normal'

        # enable all the currect entries
        self.lower_rate_limit_entry['state'] = 'normal'
        self.upper_rate_limit_entry['state'] = 'normal'
        self.atrial_amplitude_entry['state'] = 'normal'
        self.atrial_pw_entry['state'] = 'normal'
        self.ventricular_amplitude_entry['state'] = 'disabled'
        self.ventricular_pw_entry['state'] = 'disabled'
        self.vrp_entry['state'] = 'disabled'
        self.arp_entry['state'] = 'disabled'

    def _set_VOO_mode(self):
        # disable the button
        self.aoo['state'] = 'normal'
        self.voo['state'] = 'disabled'
        self.aai['state'] = 'normal'
        self.vvi['state'] = 'normal'

        # enable all the currect entries
        self.lower_rate_limit_entry['state'] = 'normal'
        self.upper_rate_limit_entry['state'] = 'normal'
        self.atrial_amplitude_entry['state'] = 'disabled'
        self.atrial_pw_entry['state'] = 'disabled'
        self.ventricular_amplitude_entry['state'] = 'normal'
        self.ventricular_pw_entry['state'] = 'normal'
        self.vrp_entry['state'] = 'disabled'
        self.arp_entry['state'] = 'disabled'

    def _set_AAI_mode(self):
        # disable the button
        self.aoo['state'] = 'normal'
        self.voo['state'] = 'normal'
        self.aai['state'] = 'disabled'
        self.vvi['state'] = 'normal'

        # enable all the currect entries
        self.lower_rate_limit_entry['state'] = 'normal'
        self.upper_rate_limit_entry['state'] = 'normal'
        self.atrial_amplitude_entry['state'] = 'normal'
        self.atrial_pw_entry['state'] = 'normal'
        self.ventricular_amplitude_entry['state'] = 'disabled'
        self.ventricular_pw_entry['state'] = 'disabled'
        self.vrp_entry['state'] = 'disabled'
        self.arp_entry['state'] = 'normal'

    def _set_VVI_mode(self):
        # disable the button
        self.aoo['state'] = 'normal'
        self.voo['state'] = 'normal'
        self.aai['state'] = 'normal'
        self.vvi['state'] = 'disabled'

        # enable all the currect entries
        self.lower_rate_limit_entry['state'] = 'normal'
        self.upper_rate_limit_entry['state'] = 'normal'
        self.atrial_amplitude_entry['state'] = 'disabled'
        self.atrial_pw_entry['state'] = 'disabled'
        self.ventricular_amplitude_entry['state'] = 'normal'
        self.ventricular_pw_entry['state'] = 'normal'
        self.vrp_entry['state'] = 'normal'
        self.arp_entry['state'] = 'disabled'
    
    def _submit_parameters(self):
        pass

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
    