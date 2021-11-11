import matplotlib.pyplot as plt
import numpy as np

plt.style.use('ggplot')
continue_plotting = True


class Device(object):
    def __init__(self):
        # open serial port
        self.connected: bool = True
        self.device_id = 123
    
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
        continue_plotting = True
        
        plt.ion()
        fig = plt.figure(figsize=(13,6))
        ax = fig.add_subplot(111)
        size = 100
        x = np.linspace(0,1,size+1)[0:-1]
        y = [0]*len(x)
        data = []
        while continue_plotting:
            y[-1] = np.random.randn() # TODO: do serial read to get new value
            data = plot(x, y, data, ax) # updates data
            y = np.append(y[1:],0.0)
            fig.canvas.mpl_connect('close_event', on_close)

def on_close(event):
    print('Closed')
    continue_plotting = False

def plot(x, y, data, ax):
    if data==[]:
        data, = ax.plot(x,y)        
        plt.title('Electrogram')
        plt.show()
    
    data.set_ydata(y)    
    plt.pause(0.1)
    return data