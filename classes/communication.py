from multiprocessing import Queue
from .modules import Module


class Message:
    """Represents a message that can be sent between modules

    @param msg[optional]('') command to send, can be overriden if unnecessary

    """
    def __init__(self, msg: str = ''):
        self.command = msg

    @property
    def data(self):
        return None


class IonLink:
    """Represents a linked object that can be connected to an IonProcessor,
    it enables communication with other modules in an application"""
    def __init__(self, tx: Queue, rx: Queue):
        self.tx = tx
        self.rx = rx

    def send_message(self, msg: Message):
        """Sends a message via the tx queue"""
        self.tx.put(msg)

    def wait_for_message(self):
        """Waits for a message to be received"""
        return self.rx.get()


class IonModule(Module, IonLink):
    """Represents a Module Object that inherits from an IonLink, the module_event_check state is overriden with an
    event handler that waits for events from the rx Queue."""
    def __init__(self, tx: Queue, rx: Queue, **kwargs):
        Module.__init__(self, **kwargs)
        IonLink.__init__(self, tx, rx)

    def module_event_check(self, data=None):
        msg = self.wait_for_message()
        if msg.command in self.states:
            self.add_state(msg.command, msg)


class IonProcessor(Module):
    """Represents a central hub for communication, IonLinks can register here to receive and send Messages
    back and forth between other IonLinks.
    """

    global_q = Queue()

    def __init__(self):
        super().__init__()
        self.mods = []

    def register_module(self, mod: IonLink):
        """Registers an IonLink's tx Queue to send to this processor, all messages received here are then sent to
        this module as well as all others.

        Must be called before starting the process!
        """
        mod.tx = self.global_q
        self.mods.append(mod.rx)

    def module_event_check(self, data=None):
        msg = self.global_q.get()
        for m in self.mods:
            m.put(msg)

        if msg.command == 'exit':
            self.add_state(self.exit)
