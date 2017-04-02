import os
import time

from threading import Thread


COMMAND_LIGTH_ON = 'LIGTH_ON'
COMMAND_LIGTH_OFF = 'LIGTH_OFF'
COMMAND_STOP = 'STOP'


pipe_name = '/tmp/heimdall'


class Controller(object):

    _light_status = 0
    _red_light_status = 0
    _running = False

    def start(self):
        thread_commands = Thread(target=self._listen_to_commands)
        thread_onrunning = Thread(target=self._on_running)
        self._running = True
        thread_commands.start()
        thread_onrunning.start()

    def _listen_to_commands(self):
        if not os.path.exists(pipe_name):
            os.mkfifo(pipe_name)
        with open(pipe_name) as f:
            while self._running:
                command = f.read()
                if command:
                    command = command.rstrip('\r\n')
                    print ('Received: {0}'.format(command))
                    self.execute(command)
            os.remove(pipe_name)

    def _on_running(self):
        while self._running:
            print ("RUN")
            time.sleep(2)
            if not self.is_enlightening:
                self.red_light_on()
                time.sleep(0.2)
                self.red_light_off()

    @property
    def is_enlightening(self):
        return self._light_status

    def light_on(self):
        self._light_status = 1

    def light_off(self):
        self._light_status = 0

    def red_light_on(self):
        self._red_light_status = 1

    def red_light_off(self):
        self._red_light_status = 0

    def stop(self):
        self._running = False

    def execute(self, command):
        if command == COMMAND_LIGTH_ON:
            self.light_on()
            self.red_light_off()
        elif command == COMMAND_LIGTH_OFF:
            self.light_off()
            self.red_light_on()
        elif command == COMMAND_STOP:
            self.light_off()
            self.red_light_off()
            self.stop()