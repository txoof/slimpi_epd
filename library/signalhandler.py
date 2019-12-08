import signal

class SignalHandler(object):
    '''handle specific signals and allow graceful exiting while loop
        https://stackoverflow.com/a/31464349/5530152
    
    Signals Handled Gracefully:
        SIGINT
        SIGTERM
    Atributes:
        kill_now (bool) default: False
    '''
    kill_now = False
    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)
    
    def exit_gracefully(self, signum, frame):
        self.kill_now = True
