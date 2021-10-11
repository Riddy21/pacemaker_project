import tkinter as tk
from tkinter.constants import W

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
        self.create_welcome_screen()

        # Update loop
        self.update()

    # Creates menu GUI
    def create_welcome_screen(self):
        # Delete previous frame
        self.frame.destroy()

        self.window.resizable(1, 1) 
        self.window.minsize(500, 450)

        # Create a frame and pack with interface
        self.frame = tk.Frame(self.window)
        title = tk.Label(self.frame, width=50, text="Welcome to Group 20's \npacemaker DCM!", pady=60)
        register = tk.Button(self.frame, text="Create a New Account", width=50, pady=30, command=lambda: self.create_register_screen())
        login = tk.Button(self.frame, text='Login to existing account', width=50, pady=30, command=lambda: self.create_login_screen())
        close = tk.Button(self.frame, text='Close', width=50, pady=10, command=lambda: self.quit_win())
        title.grid(row=0)
        register.grid(row=1)
        login.grid(row=2)
        close.grid(row=3)
        self.frame.pack()

        self.state = 'Welcome'


    def create_login_screen(self):
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
        # TODO: redirect to verification
        loginButton = tk.Button(self.frame, text='Login', pady=5, width=15, command=lambda: self.create_dcm_screen())
        backButton = tk.Button(self.frame, text='Back', pady=5, width=15, command=lambda: self.create_welcome_screen())
        title.grid(row=0, columnspan=2)
        username.grid(row=1, column=0)
        usernameEntry.grid(row=1, column=1)
        password.grid(row=2, column=0)
        passwordEntry.grid(row=2, column=1)
        backButton.grid(row=3, column=0)
        loginButton.grid(row=3, column=1)
        self.frame.pack()

        self.state = 'Login'

    def create_register_screen(self):
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
        # TODO: redirect to verification
        submitButton = tk.Button(self.frame, text='Submit', pady=5, width=15, command=lambda:self.create_dcm_screen())
        backButton = tk.Button(self.frame, text='Back', pady=5, width=15, command=lambda: self.create_welcome_screen())
        title.grid(row=0, columnspan=2)
        username.grid(row=1, column=0)
        usernameEntry.grid(row=1, column=1)
        password.grid(row=2, column=0)
        passwordEntry.grid(row=2, column=1)
        submitButton.grid(row=3, column=1)
        backButton.grid(row=3, column=0)
        self.frame.pack()

        self.state = 'Register'

    def create_dcm_screen(self):
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

        lower_rate_limit_entry = tk.Entry(self.frame) #all
        upper_rate_limit_entry = tk.Entry(self.frame) #all
        atrial_amplitude_entry = tk.Entry(self.frame) #AOO, AAI
        atrial_pw_entry = tk.Entry(self.frame) #AAO, AAI
        ventricular_amplitude_entry = tk.Entry(self.frame) #VOO, VVI
        ventricular_pw_entry = tk.Entry(self.frame) #VOO, VVI
        vrp_entry = tk.Entry(self.frame) #VVI
        arp_entry = tk.Entry(self.frame) #AAI

        # Operating modes
        modes_label = tk.Label(self.frame, text='Operating Modes', pady=15)
        aoo = tk.Button(self.frame, text='AOO', width=10, height=5)
        voo = tk.Button(self.frame, text='VOO', width=10, height=5)
        aai = tk.Button(self.frame, text='AAI', width=10, height=5)
        vvi = tk.Button(self.frame, text='VVI', width=10, height=5)
        
        # Status
        status_label = tk.Label(self.frame, text='Status', pady=15)
        device_connection = tk.Label(self.frame, fg='red', text='Device disconnected')
        device_information = tk.Label(self.frame, fg='red', text='No device data available')

        # TODO: Change to logout procedure
        logout_button = tk.Button(self.frame, text='Logout', command=lambda: self.create_welcome_screen())
        close_button = tk.Button(self.frame, text='Close', command=lambda: self.quit_win())

        # Title locations
        parameter_label.grid(row=0, column=0, columnspan=2)
        modes_label.grid(row=0, column=2)
        status_label.grid(row=0, column=3)

        # Parameter button locations
        lower_rate_limit.grid(row=1, column=0)
        upper_rate_limit.grid(row=2, column=0)
        atrial_amplitude.grid(row=3, column=0)
        atrial_pw.grid(row=4, column=0)
        ventricular_amplitude.grid(row=5, column=0)
        ventricular_pw.grid(row=6, column=0)
        vrp.grid(row=7, column=0)
        arp.grid(row=8, column=0)

        lower_rate_limit_entry.grid(row=1, column=1)
        upper_rate_limit_entry.grid(row=2, column=1)
        atrial_amplitude_entry.grid(row=3, column=1)
        atrial_pw_entry.grid(row=4, column=1)
        ventricular_amplitude_entry.grid(row=5, column=1)
        ventricular_pw_entry.grid(row=6, column=1)
        vrp_entry.grid(row=7, column=1)
        arp_entry.grid(row=8, column=1)

        # Operating mode buttons
        aoo.grid(row=1, column=2, rowspan=2)
        voo.grid(row=3, column=2, rowspan=2)
        aai.grid(row=5, column=2, rowspan=2)
        vvi.grid(row=7, column=2, rowspan=2)

        # Status
        device_connection.grid(row=1, column=3, columnspan=2)
        device_information.grid(row=3, column=3, columnspan=2)

        # exit buttons
        logout_button.grid(row=9, column=0, columnspan=2)
        close_button.grid(row=9, column=2, columnspan=2)

        self.frame.pack()

        self.state = "DCM"


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
    
    # FIXME: Just a popup that we can use later if needed
    # Makes a popup frame for paw promotion
    def make_popup(self):
        # Make popup window
        self.popup = tk.Tk()

        # configure and style
        self.popup.title("Popup")
        self.popup.geometry("315x50")
        self.popup.resizable(0, 0)

        # add closing handler
        self.popup.protocol("WM_DELETE_WINDOW", self.on_closing)

        # if not interactive
        self.popup.update()

    # Quits the popup
    def destroy_popup(self):
        try:
            self.popup.destroy()
        except:
            pass


