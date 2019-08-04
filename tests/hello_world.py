from classes.application import Application
from classes.modules import Module


class MyModule(Module):
    def module_init(self):
        print("Hello World!")
        self.add_state(self.exit)


class MyApp(Application):
    def __init__(self):
        super().__init__()
        self.modules.append(MyModule)


if __name__ == "__main__":
    app = MyApp()
    app.start()
