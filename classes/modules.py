from multiprocessing import Process
from .state_machine import QSM

import traceback
import sys
import os


class Module(Process, QSM):
    """A Module implementing a QSM with all of the standard states filled in"""
    def __init__(self, **kwargs):
        Process.__init__(self, **kwargs)
        QSM.__init__(self)
        self.states[self.initial] = self.module_init
        self.states[self.idle] = self.module_event_check
        self.states[self.error] = self.module_err
        self.states[self.exit] = self.module_exit
        self.states[self.unknown] = self.module_unknown_state

        self.is_stopping = False

    def run(self):
        while not self.is_stopping:
            try:
                self.get_next()
            except Exception as e:
                print(e)
                self.add_state(self.error, sys.exc_info())
        self.module_STOP()

    def module_unknown_state(self, data=None):
        """This state is executed if the state does not currently exist in the state dictionary"""
        pass

    def module_init(self, data=None):
        """This is always the first state to be run"""
        pass

    def module_event_check(self, data=None):
        """This module is used as an idle state, whenever the module is not doing computation, it sits here."""
        pass

    def module_err(self, data: tuple):
        """Handles errors that might be raised during operation"""
        et, v, tb = data
        traceback.print_exception(et, v, tb)
        self.add_state(self.exit)

    def module_exit(self, data=None):
        """Called when the module is exitting,
        put any states that you need to be called before completely stopping here."""
        self.is_stopping = True

    def module_STOP(self, data=None):
        """This state is always the last state to execute"""
        self.__del__()


class ConsoleModule(Module):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stdin = os.fdopen(os.dup(sys.stdin.fileno()))
        self.stdout = os.fdopen(os.dup(sys.stdout.fileno()))
        self.stderr = os.fdopen(os.dup(sys.stderr.fileno()))

    def run(self):
        # Should ensure that print() and input() functions work.
        import sys
        sys.stdin = self.stdin
        sys.stdout = self.stdout
        sys.stderr = self.stderr

        super().run()

    def module_STOP(self, data=None):
        self.stdin.close()
        self.stdout.close()
        self.stderr.close()

