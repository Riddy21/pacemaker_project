import matplotlib.pyplot as plt
import numpy as np

plt.style.use('ggplot')


class Device(object):
    def __init__(self):
        # open serial port
        self.connected: bool = True
        self.device_id = 123
        self.continue_plotting = False
    
    def _write(self, message):
        # write message to port
        print(message)
    
    def upload_parameters(parameters):
        # write parameters dict to pacemaker
        print(parameters)
        # verify parameters were stored correctly
    
    def display_egram(self, mode):
        self._write('egram')
        self._write(mode)
        self.continue_plotting = True
        
        if (mode == 'Atrium' or mode == 'Ventricle'):
            self.create_single_plot(mode)
        elif (mode == 'Both'):
            self.create_double_plot()
    
    def create_single_plot(self, mode):
        plt.ion()
        fig = plt.figure(figsize=(13,6))
        size = 100
        ax = fig.add_subplot(111)
        ax.axes.xaxis.set_visible(False) # x-axis is only used to plot, doesn't mean anything so hidden
        ax.set_ylim([-3,3])
        x = np.linspace(0,1,size+1)[0:-1]
        y = [0]*len(x)
        data = []
        while self.continue_plotting:
            # if mode == Atrium, pin = ATR_SIGNAL
            # if mode == Ventricle, pin = VENT_SIGNAL
            y[-1] = np.random.randn() # TODO: do serial read to get new value
            data = self.plot(x, y, data, ax, mode) # updates data
            y = np.append(y[1:],0.0)
            fig.canvas.mpl_connect('close_event', self.on_close)

    def create_double_plot(self):
        plt.ion()
        fig = plt.figure(figsize=(13,12))
        size = 100

        # Atrium
        ax_a = fig.add_subplot(211)
        ax_a.axes.xaxis.set_visible(False)
        ax_a.set_ylim([-3,3])
        x_a = np.linspace(0,1,size+1)[0:-1]
        y_a = [0]*len(x_a)
        data_a = []

        # Ventricle
        ax_v = fig.add_subplot(212)
        ax_v.axes.xaxis.set_visible(False)
        ax_v.set_ylim([-3,3])
        x_v = np.linspace(0,1,size+1)[0:-1]
        y_v = [0]*len(x_a)
        data_v = []

        while self.continue_plotting:
            # Atrium: pin = ATR_SIGNAL
            # Ventricle: pin = VENT_SIGNAL
            y_a[-1] = np.random.randn() # TODO: do serial read to get new value from atrium
            y_v[-1] = np.random.randn() # TODO: do serial read to get new value from ventricle
            data_a = self.plot(x_a, y_a, data_a, ax_a, 'Atrium') # updates data for atrium
            data_v = self.plot(x_v, y_v, data_v, ax_v, 'Ventricle') # updates data for ventricle
            y_a = np.append(y_a[1:],0.0)
            y_v = np.append(y_v[1:],0.0)
            fig.canvas.mpl_connect('close_event', self.on_close)
    
    def on_close(self, event):
        self.continue_plotting = False

    def plot(self, x, y, data, ax, mode):
        if data==[]:
            data, = ax.plot(x,y)        
            ax.title.set_text('%s Electrogram' % (mode))
            plt.show()
        
        data.set_ydata(y)    
        plt.pause(0.1)
        return data