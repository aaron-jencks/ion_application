from .communication import IonProcessor

from multiprocessing import Queue


class Application:
    def __init__(self):
        super().__init__()
        self.ion_processor = IonProcessor()
        self.modules = []  # <-- Add your modules to this list
        self.initialized_mods = []

    def start(self):
        """Launches the application"""
        self.modules_initialize()
        self.modules_setup()
        self.modules_start()
        self.modules_cleanup()

    def modules_initialize(self):
        """Instantiates each module by calling their constructors and linking them to the ion_processor"""
        self.initialized_mods = [m(tx=self.ion_processor.global_q, rx=Queue()) for m in self.modules]

    def modules_setup(self):
        """Links each modules up to the ion_processor for communication"""
        for m in self.initialized_mods:
            self.ion_processor.register_module(m)

    def modules_start(self):
        """Launches all of the modules"""
        for m in self.initialized_mods:
            m.start()

    def modules_cleanup(self):
        """Waits for all of the modules to finish running"""
        for m in self.initialized_mods:
            m.join()
