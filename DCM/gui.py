import tkinter as tk
from tkinter.constants import W

class GUI(object):
    def __init__(self):
        # Create window
        self.window = tk.Tk()

        # Setup window
        self.window.title("DCM")
        self.window.geometry("500x500")
        self.window.resizable(0, 0)

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

        # Create a frame and pack with interface
        self.frame = tk.Frame(self.window)
        title = tk.Label(self.frame, width=50, text="Welcome to Group 20's \npacemaker DCM!")
        register = tk.Button(self.frame, text="Create a New Account", width=50, pady=50, command=lambda: self.create_register_screen())
        login = tk.Button(self.frame, text='Login to existing account', width=50, pady=50, command=lambda: self.create_login_screen())
        close = tk.Button(self.frame, text='Close', width=50, pady=20, command=lambda: self.quit_win())
        title.grid(row=0)
        register.grid(row=1)
        login.grid(row=2)
        close.grid(row=3)
        self.frame.pack()

        self.state = 'Welcome'


    def create_login_screen(self):
        # Delete previous frame
        self.frame.destroy()

        # Create a frame and pack with interface
        self.frame = tk.Frame(self.window)
        title = tk.Label(self.frame, width=50, text='Login')
        username = tk.Label(self.frame, text='Username')
        password = tk.Label(self.frame, text='Password')
        usernameEntry = tk.Entry(self.frame)
        passwordEntry = tk.Entry(self.frame)
        # TODO: redirect to verification
        loginButton = tk.Button(self.frame, text='Login', command=lambda: self.create_dcm_screen())
        backButton = tk.Button(self.frame, text='Back', command=lambda: self.create_welcome_screen())
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
        
        # Create a frame and pack with interface
        self.frame = tk.Frame(self.window)
        title = tk.Label(self.frame, width=50, text='Create a New User')
        username = tk.Label(self.frame, text='Username')
        password = tk.Label(self.frame, text='Password')
        usernameEntry = tk.Entry(self.frame)
        passwordEntry = tk.Entry(self.frame)
        # TODO: redirect to verification
        submitButton = tk.Button(self.frame, text='Submit', command=lambda:self.create_dcm_screen())
        backButton = tk.Button(self.frame, text='Back', command=lambda: self.create_welcome_screen())
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

        # Operating modes
        modes_label = tk.Label(self.frame, text='Operating Modes')
        aoo = tk.Button(self.frame, text='AOO')
        voo = tk.Button(self.frame, text='VOO')
        aai = tk.Button(self.frame, text='AAI')
        vvi = tk.Button(self.frame, text='VVI')

        # Parameters
        parameter_label = tk.Label(self.frame, text='DCM Parameters')
        lower_rate_limit = tk.Label(self.frame, text='Lower rate limit') #all
        upper_rate_limit = tk.Label(self.frame, text='Lower rate limit')#all
        atrial_amplitude = tk.Label(self.frame, text='Lower rate limit')#AOO, AAI
        atrial_pw = tk.Label(self.frame, text='Lower rate limit')#AAO, AAI
        ventricular_amplitude = tk.Label(self.frame, text='Lower rate limit')#VOO, VVI
        ventricular_pw = tk.Label(self.frame, text='Lower rate limit')#VOO, VVI
        vrp = tk.Label(self.frame, text='Lower rate limit')#VVI
        arp = tk.Label(self.frame, text='Lower rate limit')#AAI

        lower_rate_limit_entry = tk.Entry(self.frame) #all
        upper_rate_limit_entry = tk.Entry(self.frame) #all
        atrial_amplitude_entry = tk.Entry(self.frame) #AOO, AAI
        atrial_pw_entry = tk.Entry(self.frame) #AAO, AAI
        ventricular_amplitude_entry = tk.Entry(self.frame) #VOO, VVI
        ventricular_pw_entry = tk.Entry(self.frame) #VOO, VVI
        vrp_entry = tk.Entry(self.frame) #VVI
        arp_entry = tk.Entry(self.frame) #AAI
        
        # Status
        status_label = tk.Label(self.frame, text='Status')
        device_connection = tk.Label(self.frame, fg='red', text='Device disconnected')
        device_information = tk.Label(self.frame, fg='red', text='No device data available')

        # TODO: Change to logout procedure
        logout_Button = tk.Button(self.frame, text='Logout', command=lambda: self.create_welcome_screen())

        parameter_label.grid(row=0, column=0)
        modes_label.grid(row=0, column=1)
        status_label.grid(row=0, column=2)

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


