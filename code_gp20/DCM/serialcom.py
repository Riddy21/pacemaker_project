import serial
import sys
import glob
import serial.tools.list_ports

#Hardcoded Baud Rate
#Use little Endian

class SerialManager(object):

    def __init__(self):

        self.port = ""
        self.serialPort = ""

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