from classes.application import Application
from classes.communication import IonModule, Message

from multiprocessing import Queue


class ChatMessage(Message):
    def __init__(self, msg: str = ''):
        super().__init__('chat')
        self.msg = msg


class Transmitter(IonModule):
    def module_event_check(self, data=None):
        msg = input('Say something: ')
        self.send_message(ChatMessage(msg))


class Receiver(IonModule):
    def __init__(self, tx: Queue, rx: Queue):
        super().__init__(tx, rx)
        self.states['chat'] = self.rx_chat_msg

    def rx_chat_msg(self, msg: ChatMessage):
        print('Received message: {}'.format(msg.msg))


class MyApp(Application):
    def __init__(self):
        super().__init__()
        self.modules.extend([Transmitter, Receiver])

        
if __name__ == "__main__":
    app = MyApp()
    app.start()
