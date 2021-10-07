import tkinter as tk

class GUI(object):
    def __init__(self):
        # Create window
        self.window = tk.Tk()

        # Setup window
        self.window.title("DCM")
        self.window.geometry("500x500")
        self.window.resizable(0, 0)

        # Make GUI frame
        self.frame = ""

        # Make popup window
        self.popup = ""

        # GUI state
        self.state = "Welcome"

        # Setup menu
        #self.create_menu()

        # Update loop
        self.update()

    # Put gui in mainloop
    def loop(self):
        self.window.mainloop()

    # Updates gui for one cycle
    def update(self):
        self.window.update()

