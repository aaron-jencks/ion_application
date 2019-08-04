# Ion Applications
Applications with State Machines for Python Development

This project creates a modular system for controlling python applications using a MVC layout.
There are 3 basic components:
* Application
* Module
* IonLink/IonProcessor

<em>For extened information on the inheritance and interworkings of the project, please either refer to the source code, 
or take a look at the PlantUML diagram in 'Documentation'.</em>

## Applications
Each Ion Project contains an application. Each application can contain any number of modules, 
and at least one <code>IonProcessor</code>. An Application is itself a <code>multiprocessing.Process</code>

It accepts any number of Modules which are also <code>multiprocessing.Processes</code>

### Execution
When Applications execute, they go through a few states:
* <b>initialize</b><br>
    In the <i>initialize</i> state global variables are created, each of the registered <code>Module</code>s are instantiated 
    via their constructor.
* <b>setup</b><br>
    In the <i>setup</i> state, any pre-execution settings that need to be configured per module, should be configured.
* <b>start</b><br>
    In the <i>start</i> state, every <code>Module</code> is launched asynchronously, along with the <code>IonProcessor</code>.
* <b>cleanup</b><br>
    Here, the <code>Application</code> waits for each of the Modules to finish execution and then performs any 
    post-execution cleanup necessary.
    
## Modules
Each Ion Application consists of any number of Modules, these are <em>Queued-State-Machines</em>(<code>QSM</code>), 
that handle tasks in a program, if you use an <code>IonModule</code> then you can communicate with other modules as well. 
Each <code>StateMachine</code> can have any number of states, but in a module there are a few premade ones:
* <b>initialize</b><br>
    This is always the first state to execute
* <b>event check</b><br>
    This is the idle state, and where the module should check for updates to the model.
* <b>error</b><br>
    This is the state that executes when an exception occurs during the execution of another state.
* <b>exit</b><br>
    This is the state the executes when a <code>Module</code> is about to shutdown.
* <b>STOP</b><br>
    This is always the last state to execute.
    
## IonLinks/IonProcessors
In order to communicate between different <code>Modules</code> you need to inherit from an <code>IonLink</code>, 
this adds a <i>tx</i> and <i>rx</i> <code>multiprocessing.Queue</code>s to your module
the <i>tx</i> of which is connected to the <i>rx</i> of an <code>IonProcessor</code>. To send messages, you need to use 
a <code>Message</code> object, when you send a message, it's received by the <code>IonProcessor</code> whom then takes 
that message and places it into each of its registered modules' <i>rx</i> Queues.

## Usage Examples
To get started, you'll need to create yourself an <code>Application</code>, and an <code>Module</code>.<br>
```python
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
```

<em>For more coding examples, take a look at the 'tests' folder.</em>

