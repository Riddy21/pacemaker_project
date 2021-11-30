import serial
import sys
import glob
import serial.tools.list_ports
import matplotlib.pyplot as plt
import numpy as np

MODES = {
    'Atrium': 1,
    'Ventricle': 2,
    'Both': 3
}

plt.style.use('ggplot')

#Hardcoded Baud Rate
#Use little Endian

class SerialManager(object):

    def __init__(self):

        self.port = ""
        self.serialPort = ""
        self.continue_plotting = False

    def _get_ports(self):

        available_ports = serial.tools.list_ports.comports(False)
        port_names = []
        for port in available_ports:
            print(port.name)
            port_names.append(port.name)

        return port_names

    def _init_serial(self, newport):
        try:
            
            self.port = newport

            self.serialPort = serial.Serial(newport, 115200)

            print(self.serialPort.name)

        except:
            print("Unable to establish serial connection")

    def _serial_out(self, serialOut, valid_parameters, parameters_dict):

        #Send pacemaker data

        try:
            if(serialOut.is_open):

                outData = []

                #Start Flag
                outData.append(b'\x16')

                #Append all valid parameters to output
                for parameter in sorted(parameters_dict.items()):
                    if parameter in valid_parameters:
                        outData.append(parameter)

                #write each parameter to output
                for parameter in outData:
                    serialOut.write(parameter)

        except:
            print("Unable to send data")


        #Verify data
        #XOR bytes


    def _serial_in(serialIn):
        
        try:
            if(serialIn.is_open):
                inData = []

                while():
                    inData.append(serialIn.read)
        except:
            print("Could not recieve data")
    
    def is_plotting_egram(self):
        return self.continue_plotting;
    
    def display_egram(self, mode):
        # TODO: Send command to pacemaker to start receiving egram information

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
        # TODO: Send stop command to pacemaker to stop receiving egram information
        self.continue_plotting = False

    def plot(self, x, y, data, ax, mode):
        if data==[]:
            data, = ax.plot(x,y)        
            ax.title.set_text('%s Electrogram' % (mode))
            plt.show()
        
        data.set_ydata(y)    
        plt.pause(0.1)
        return data