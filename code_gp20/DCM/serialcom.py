import serial
import sys
import glob
import serial.tools.list_ports
import matplotlib.pyplot as plt
import numpy as np
import struct
from tkinter import messagebox

ACTIVITY_THRESHOLD = {
    'V-Low': 1,
    'Low': 2,
    'Med-Low': 3,
    'Med': 4,
    'Med-High': 5,
    'High': 6,
    'V-High': 7
}

OPERATING_MODE = {
    'aoo': 1,
    'voo': 2,
    'aai': 3,
    'vvi': 4,
    'doo': 5,
    'aoor': 6,
    'voor': 7,
    'aair': 8,
    'vvir': 9,
    'door': 10
}

plt.style.use('ggplot')

#Hardcoded Baud Rate
#Use little Endian

class SerialManager(object):

    def __init__(self):

        self.port = ""
        self.serialPort = ""
        self.continue_plotting = False

    def get_ports(self):

        available_ports = serial.tools.list_ports.comports(False)
        port_names = []
        for port in available_ports:
            print(port.name)
            port_names.append(port.name)

        return port_names

    def init_serial(self, newport):
        try:
            
            self.port = newport

            self.serialPort = serial.Serial(newport, 115200)

            print(self.serialPort.name)

        except:
            messagebox.showerror("Error","Unable to establish serial connection")

    def serial_out(self, valid_parameters, parameters_dict, operating_mode):

        #Send pacemaker data

        if(self.serialPort.is_open):

            packet = []

            #Start Flag
            self.serialPort.write(b'\x16')
            print(b'\x16')
            print("wrote start flag")

            #operating mode uint8
            self.serialPort.write(np.uint8(OPERATING_MODE[operating_mode]).tobytes())
            print(np.uint8(OPERATING_MODE[operating_mode]).tobytes())
            print("wrote operating mode")

            #atrial amp     double
            if('atrial_amplitude' in valid_parameters[operating_mode]):
                self.serialPort.write(np.double(parameters_dict['atrial_amplitude']).tobytes())
                print(np.double(parameters_dict['atrial_amplitude']).tobytes())
            else:
                self.serialPort.write(np.double(0).tobytes())
                print(np.double(0).tobytes())

            #atrial pw      uint16
            if('atrial_pw' in valid_parameters[operating_mode]):
                self.serialPort.write(np.uint16(parameters_dict['atrial_pw']).tobytes())
                print(np.uint16(parameters_dict['atrial_pw']).tobytes())
            else:
                self.serialPort.write(np.uint16(0).tobytes())
                print(np.uint16(0).tobytes())

            #arp            uint16
            if('arp' in valid_parameters[operating_mode]):
                self.serialPort.write(np.uint16(parameters_dict['arp']).tobytes())
                print(np.uint16(parameters_dict['arp']).tobytes())
            else:
                self.serialPort.write(np.uint16(0).tobytes())
                print(np.uint16(0).tobytes())

            #vrp            uint16
            if('vrp' in valid_parameters[operating_mode]):
                self.serialPort.write(np.uint16(parameters_dict['vrp']).tobytes())
                print(np.uint16(parameters_dict['vrp']).tobytes())
            else:
                self.serialPort.write(np.uint16(0).tobytes())
                print(np.uint16(0).tobytes())

            #vent amp       double
            if('ventricular_amplitude' in valid_parameters[operating_mode]):
                self.serialPort.write(np.double(parameters_dict['ventricular_amplitude']).tobytes())
                print(np.double(parameters_dict['ventricular_amplitude']).tobytes())
            else:
                self.serialPort.write(np.double(0).tobytes())
                print(np.double(0).tobytes())

            #vent pw        uint16
            if('ventricular_pw' in valid_parameters[operating_mode]):
                self.serialPort.write(np.uint16(parameters_dict['ventricular_pw']).tobytes())
                print(np.uint16(parameters_dict['ventricular_pw']).tobytes())
            else:
                self.serialPort.write(np.uint16(0).tobytes())
                print(np.uint16(0).tobytes())

            #av_delay       uint16
            if('fixed_av_delay' in valid_parameters[operating_mode]):
                self.serialPort.write(np.uint16(parameters_dict['fixed_av_delay']).tobytes())
                print(np.uint16(parameters_dict['fixed_av_delay']).tobytes())
            else:
                self.serialPort.write(np.uint16(0).tobytes())
                print(np.uint16(0).tobytes())

            #reaction       double
            if('reaction_time' in valid_parameters[operating_mode]):
                self.serialPort.write(np.double(parameters_dict['reaction_time']).tobytes())
                print(np.double(parameters_dict['reaction_time']).tobytes())
            else:
                self.serialPort.write(np.double(0).tobytes())
                print(np.double(0).tobytes())

            #recovery       double
            if('recovery_time' in valid_parameters[operating_mode]):
                self.serialPort.write(np.double(parameters_dict['recovery_time']).tobytes())
                print(np.double(parameters_dict['recovery_time']).tobytes())
            else:
                self.serialPort.write(np.double(0).tobytes())
                print(np.double(0).tobytes())

            #threshold      single
            if('activity_threshold' in valid_parameters[operating_mode]):
                self.serialPort.write(np.single(ACTIVITY_THRESHOLD[parameters_dict['activity_threshold']]).tobytes())
                print(np.single(ACTIVITY_THRESHOLD[parameters_dict['activity_threshold']]).tobytes())
            else:
                self.serialPort.write(np.single(0).tobytes())
                print(np.single(0).tobytes())

            #msr            double
            if('max_sensor_rate' in valid_parameters[operating_mode]):
                self.serialPort.write(np.double(parameters_dict['max_sensor_rate']).tobytes())
                print(np.double(parameters_dict['max_sensor_rate']).tobytes())
            else:
                self.serialPort.write(np.double(0).tobytes())
                print(np.double(0).tobytes())

            #lrl            uint16
            if('lrl' in valid_parameters[operating_mode]):
                self.serialPort.write(np.uint16(parameters_dict['lrl']).tobytes())
                print(np.uint16(parameters_dict['lrl']).tobytes())
            else:
                self.serialPort.write(np.uint16(0).tobytes())
                print(np.uint16(0).tobytes())
            
            print("wrote parameters")

            #End flag
            self.serialPort.write(b'\x17')
            print(b'\x17')
            print("wrote end flag")

            #Wait for confirmation
            recieved = self.serialPort.read(17)

            print("recieved confirmation")

            for word in recieved:
                print(word.to_bytes)
                if (np.uint8(word).tobytes() == b'\x18'):
                    return True
            print(recieved)
            return False

        else:
            messagebox.showerror("Error","Serial Connection not Established")
            return False


        #Verify data
        #XOR bytes
    
    def is_plotting_egram(self):
        return self.continue_plotting;
    
    def display_egram(self, mode):
        try:
            self.serialPort.write(b'\x16') # Signals to pacemaker to start receiving signal
            for i in range(58):
                self.serialPort.write(b'\x26') # Signal to pacemaker to send egram data
        except:
            messagebox.showerror("Error",'Unable to request egram data from pacemaker')
            return

        self.continue_plotting = True
        try:
            if (mode == 'Atrium' or mode == 'Ventricle'):
                self._create_single_plot(mode)
            elif (mode == 'Both'):
                self._create_double_plot()
        except:
            messagebox.showerror("Error",'Unable to receive egram data from pacemaker')
            return
    
    def _create_single_plot(self, mode):
        plt.ion()
        fig = plt.figure(figsize=(13,6))
        size = 100
        ax = fig.add_subplot(111)
        ax.axes.xaxis.set_visible(False) # x-axis is only used to plot, doesn't mean anything so hidden
        ax.set_ylim([-5,5])
        x = np.linspace(0,1,size+1)[0:-1]
        y = [0]*len(x)
        data = []
        while self.continue_plotting:
            read = self.serialPort.read(17)
            if (mode == 'Atrium'):
                reconstruct = struct.unpack('d', read[1:9])
                y[-1] = reconstruct[0]
            elif (mode == 'Ventricle'):
                reconstruct = struct.unpack('d', read[9:])
                y[-1] = reconstruct[0]
            data = self._plot(x, y, data, ax, mode) # updates data
            y = np.append(y[1:],0.0)
            fig.canvas.mpl_connect('close_event', self._on_close)
    
    def _create_double_plot(self):
        plt.ion()
        fig = plt.figure(figsize=(13,12))
        size = 100

        # Atrium
        ax_a = fig.add_subplot(211)
        ax_a.axes.xaxis.set_visible(False)
        ax_a.set_ylim([-5,5])
        x_a = np.linspace(0,1,size+1)[0:-1]
        y_a = [0]*len(x_a)
        data_a = []

        # Ventricle
        ax_v = fig.add_subplot(212)
        ax_v.axes.xaxis.set_visible(False)
        ax_v.set_ylim([-5,5])
        x_v = np.linspace(0,1,size+1)[0:-1]
        y_v = [0]*len(x_a)
        data_v = []

        while self.continue_plotting:
            read = self.serialPort.read(17)
            reconstruct_a = struct.unpack('d', read[1:9])
            reconstruct_v = struct.unpack('d', read[9:])
            y_a[-1] = reconstruct_a[0]
            y_v[-1] = reconstruct_v[0]
            data_a = self._plot(x_a, y_a, data_a, ax_a, 'Atrium') # updates data for atrium
            data_v = self._plot(x_v, y_v, data_v, ax_v, 'Ventricle') # updates data for ventricle
            y_a = np.append(y_a[1:],0.0)
            y_v = np.append(y_v[1:],0.0)
            fig.canvas.mpl_connect('close_event', self._on_close)
    
    def _on_close(self, event):
        self.continue_plotting = False
        for i in range(59):
                self.serialPort.write(b'\x55') # Signals to pacemaker to stop egram data

    def _plot(self, x, y, data, ax, mode):
        if data==[]:
            data, = ax.plot(x,y)        
            ax.title.set_text('%s Electrogram' % (mode))
            plt.show()
        
        data.set_ydata(y)
        plt.pause(0.1)
        return data