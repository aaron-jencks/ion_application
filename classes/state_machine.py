from collections import deque


class StateMachine:
    """A Class representing a state machine, it can be inherited from to create custom state machines"""

    def __init__(self):
        self.states = {}

    def __del__(self):
        self.states = {}

    def execute_state(self, s: str, params=None):
        """Executes a state contained in the state machine

        Arguments:
        @param s state to execute
        @param params[optional](None) data to pass down to the state

        """
        if s in self.states:
            self.states[s](params)


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
        self.data_q = deque([None])

    def __del__(self):
        self.q = None

    def add_state(self, s: str = '', data=None):
        """Adds a single states to the queue

        Arguments:
        @param s[optional]('') string to append to the queue, if '', then idle is appended instead.
        @param data[optional](None) data to be passed to the state upon execution.

        """
        if s == '':
            self.q.append(self.idle)
        else:
            self.q.append(s)

        self.data_q.append(data)

    def add_states(self, s: list = None, data=None):
        """Adds a series of states to the state queue

        Arguments:
        @param s[optional](None) list to append to the queue, if None, then idle is appended instead.
        @param data[optional](None) data to be passed to each of the states upon execution.

        """
        if s is None:
            self.q.append(self.idle)
        else:
            self.q.extend(s)

        self.data_q.extend([data]*len(s))

    def get_next(self, execute: bool = True):
        """Retrieves the next state from the queue, if there isn't one, it returns the idle state

        Arguments:
        @param execute[optional](True) if true, then the next state is executed instead of returned.

        @returns Returns the next state in the queue
        """
        if len(self.q) == 0:
            state = self.idle
            data = None
        else:
            state = self.q.popleft()
            data = self.data_q.popleft()
            if state not in self.states:
                state = self.unknown

        if execute:
            self.execute_state(state, data)
        else:
            return self.states[state]
