from collections import deque


class StateMachine:
    """A Class representing a state machine, it can be inherited from to create custom state machines"""

    def __init__(self):
        self.states = {}

    def __del__(self):
        self.states = {}

    def execute_state(self, s: str):
        """Executes a state contained in the state machine

        Arguments:
        @param s state to execute

        """
        if s in self.states:
            self.states[s]()


class QSM(StateMachine):
    def __init__(self, idle: str = 'event check', initial: str = 'initialize',
                 error: str = 'error', stop: str = 'exit', unknown: str = 'unknown state'):
        super().__init__()
        self.idle = idle
        self.initial = initial
        self.error = error
        self.exit = stop
        self.unknown = unknown

        self.q = deque([self.initial])

    def __del__(self):
        self.q = None

    def add_state(self, s: str = ''):
        """Adds a single states to the queue

        Arguments:
        @param s[optional]('') string to append to the queue, if '', then idle is appended instead.

        """
        if s == '':
            self.q.append(self.idle)
        else:
            self.q.append(s)

    def add_states(self, s: list = None):
        """Adds a series of states to the state queue

        Arguments:
        @param s[optional](None) list to append to the queue, if None, then idle is appended instead.

        """
        if s is None:
            self.q.append(self.idle)
        else:
            self.q.extend(s)

    def get_next(self, execute: bool = True):
        """Retrieves the next state from the queue, if there isn't one, it returns the idle state

        Arguments:
        @param execute[optional](True) if true, then the next state is executed instead of returned.

        @returns Returns the next state in the queue
        """
        if len(self.q) == 0:
            state = self.idle
        else:
            state = self.q.popleft()
            if state not in self.states:
                state = self.unknown

        if execute:
            self.execute_state(state)
        else:
            return self.states[state]
