import tkinter as tk

class GUI(object):
    def __init__(self):
        # Create window
        self.window = tk.Tk()

        # Setup window
        self.window.title("DCM")
        self.window.geometry("600x500")
        self.window.resizable(0, 0)

        # Make GUI frame
        self.frame = ""

        # Make popup window
        self.popup = ""

        # GUI state
        self.state = "Welcome"

        # Setup menu
        self.create_menu()

        # Update loop
        self.update()

    # Creates menu GUI
    def create_menu(self):
        # console message
        print("Starting Menu....")

        # Create a frame and pack with interface
        self.frame = tk.Frame(self.window)
        title = tk.Label(self.frame, pady=85, text="Welcome to Group 20's \npacemaker DCM!")
        register = tk.Button(self.frame, text="Create a New Account", padx=220, pady=50, command=lambda: self.main.goto_1p())
        login = tk.Button(self.frame, text='Login to existing account', padx=220, pady=50, command=lambda: self.main.goto_2p())
        close = tk.Button(self.frame, text='Close', padx=230, pady=20, command=lambda: self.main.quit_win())
        title.grid(row=0)
        register.grid(row=1)
        login.grid(row=2)
        close.grid(row=3)
        self.frame.pack()


    def create_login_screen(self):
        self.frame = tk.Frame(self.window)
        title = tk.Label(self.frame, pady=85, text="Login")
        register = tk.Button(self.frame, text="Create a New Account", padx=220, pady=50, command=lambda: self.main.goto_1p())
        login = tk.Button(self.frame, text='Login to existing account', padx=220, pady=50, command=lambda: self.main.goto_2p())
        close = tk.Button(self.frame, text='Close', padx=230, pady=20, command=lambda: self.main.quit_win())
        title.grid(row=0)
        register.grid(row=1)
        login.grid(row=2)
        close.grid(row=3)
        self.frame.pack()

    # TODO: Make register screen

    # TODO: Make DCM screen

    # Put gui in mainloop
    def loop(self):
        self.window.mainloop()

    # Updates gui for one cycle
    def update(self):
        self.window.update()

