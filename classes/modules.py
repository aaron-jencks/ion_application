from multiprocessing import Process
from .state_machine import QSM

import traceback
import sys


class Module(Process, QSM):
    """A Module implementing a QSM with all of the standard states filled in"""
    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
        self.states[self.initial] = self.module_init
        self.states[self.idle] = self.module_event_check
        self.states[self.error] = self.module_err
        self.states[self.exit] = self.module_exit

        self.is_stopping = False
        self.raised_error = None

    def start(self):
        while not self.is_stopping:
            try:
                self.get_next()
            except Exception:
                self.raised_error = sys.exc_info()
                self.add_state(self.error)
        self.module_STOP()

    def module_unknown_state(self):
        """This state is executed if the state does not currently exist in the state dictionary"""
        pass

    def module_init(self):
        """This is always the first state to be run"""
        pass

    def module_event_check(self):
        """This module is used as an idle state, whenever the module is not doing computation, it sits here."""
        pass

    def module_err(self):
        """Handles errors that might be raised during operation"""
        et, v, tb = self.raised_error
        traceback.print_exception(et, v, tb)
        self.add_state(self.exit)

    def module_exit(self):
        """Called when the module is exitting,
        put any states that you need to be called before completely stopping here."""
        self.is_stopping = True

    def module_STOP(self):
        """This state is always the last state to execute"""
        self.__del__()

