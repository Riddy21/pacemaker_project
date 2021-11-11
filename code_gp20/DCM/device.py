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
    
    def display_egram(self):
        self._write('egram')
        # egram = read from port
        # plot egram in real time (new window)
        # figure out how to exit egram mode
