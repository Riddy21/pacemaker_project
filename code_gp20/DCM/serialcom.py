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

ACTIVITY_THRESHOLD = {
    'V-Low': 1,
    'Low': 2,
    'Med-Low': 3,
    'Med': 4,
    'Med-High': 5,
    'High': 6,
    'V-High': 7
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

    def _serial_out(self, valid_parameters, parameters_dict, operating_mode):

        #Send pacemaker data

        try:
            if(self.serialPort.is_open):

                outData = []

                #Start Flag
                outData.append(b'\x16')

                #New write parameters
                outData.append[parameters_dict.get('operating_mode')]
                #atrial amp     double
                if('atrial_amplitude' in valid_parameters[operating_mode]):
                    outData.append(np.double(parameters_dict.get('atrial_amplitude')))
                else:
                    outData.append(np.double(0))
                #atrial pw      unit16
                if('atrial_pw' in valid_parameters[operating_mode]):
                    outData.append(np.unit16(parameters_dict.get('atrial_pw')))
                else:
                    outData.append(np.unit16(0))
                #arp            uint16
                if('arp' in valid_parameters[operating_mode]):
                    outData.append(np.unit16(parameters_dict.get('arp')))
                else:
                    outData.append(np.unit16(0))
                #vrp            uint16
                if('vrp' in valid_parameters[operating_mode]):
                    outData.append(np.unit16(parameters_dict.get('vrp')))
                else:
                    outData.append(np.unit16(0))
                #atrial amp     double
                if('atrial_amplitude' in valid_parameters[operating_mode]):
                    outData.append(np.double(parameters_dict,get('atrial_amplitude')))
                else:
                    outData.append(np.double(0))
                #vent amp       double
                if('ventricular_amplitude' in valid_parameters[operating_mode]):
                    outData.append(np.double(parameters_dict.get('ventricular_amplitude')))
                else:
                    outData.append(np.double(0))
                #vent pw        uint16
                if('ventricular_pw' in valid_parameters[operating_mode]):
                    outData.append(np.unit16(parameters_dict.get('ventricular_pw')))
                else:
                    outData.append(np.unit16(0))
                #av_delay       uint16
                if('fixed_av_delay' in valid_parameters[operating_mode]):
                    outData.append(np.unit16(parameters_dict.get('fixed_av_delay')))
                else:
                    outData.append(np.unit16(0))
                #reaction       double
                if('reaction_time' in valid_parameters[operating_mode]):
                    outData.append(np.double(parameters_dict.get('reaction_time')))
                else:
                    outData.append(np.double(0))
                #recovery       double
                if('recovery_time' in valid_parameters[operating_mode]):
                    outData.append(np.double(parameters_dict.get('recovery_time')))
                else:
                    outData.append(np.double(0))
                #threshold      single
                if('activity_threshold' in valid_parameters[operating_mode]):
                    outData.append(np.single(ACTIVITY_THRESHOLD.get(parameters_dict.get('activity_threshold'))))
                else:
                    outData.append(np.single(0))
                #msr            double
                if('max_sensor_rate' in valid_parameters[operating_mode]):
                    outData.append(np.double(parameters_dict.get('max_sensor_rate')))
                else:
                    outData.append(np.double(0))
                #lrl            uint16
                if('lrl' in valid_parameters[operating_mode]):
                    outData.append(np.unit16(parameters_dict.get('lrl')))
                else:
                    outData.append(np.unit16(0))
                
                #End flag
                outData.append(b'\x17')

                for data in outData:
                    self.serialPort.write(data)

                #Wait for confirmation
                recieved = False

                while(not recieved):
                    dataIn = self.serialPort.read()
                    if dataIn == 1:
                        return True
                

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
        try:
            self.serialPort.write(MODES[mode]) # Request data from pacemaker based on egram-plotting mode
        except:
            print('Unable to request egram data from pacemaker')
            return

        self.continue_plotting = True
        try:
            if (mode == 'Atrium' or mode == 'Ventricle'):
                self._create_single_plot(mode)
            elif (mode == 'Both'):
                self._create_double_plot()
        except:
            print('Unable to receive egram data from pacemaker')
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
            y[-1] = self.serialPort.read()
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
        ax_v.set_ylim([-3,3])
        x_v = np.linspace(0,1,size+1)[0:-1]
        y_v = [0]*len(x_a)
        data_v = []

        while self.continue_plotting:
            y = self.serialPort.read()
            y_a[-1] = np.random.randn() # TODO: figure out how A/V data is going to be differentiated
            y_v[-1] = np.random.randn() # TODO: figure out how A/V data is going to be differentiated
            data_a = self._plot(x_a, y_a, data_a, ax_a, 'Atrium') # updates data for atrium
            data_v = self._plot(x_v, y_v, data_v, ax_v, 'Ventricle') # updates data for ventricle
            y_a = np.append(y_a[1:],0.0)
            y_v = np.append(y_v[1:],0.0)
            fig.canvas.mpl_connect('close_event', self._on_close)
    
    def _on_close(self, event):
        self.serialPort.write(4) # Stop command to pacemaker
        self.continue_plotting = False

    def _plot(self, x, y, data, ax, mode):
        if data==[]:
            data, = ax.plot(x,y)        
            ax.title.set_text('%s Electrogram' % (mode))
            plt.show()
        
        data.set_ydata(y)
        plt.pause(0.1)
        return data