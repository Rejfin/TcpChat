from PyQt5.QtCore import QObject, pyqtSignal


class Receiver(QObject):
    messageSignal = pyqtSignal(str)

    def __init__(self, client):
        super().__init__()
        self.ENCODE_FORMAT = "utf-8"
        self.client = client

    def run(self):
        try:
            while True:
                message_length = self.client.recv(4)
                message = self.client.recv(int.from_bytes(message_length, 'big')).decode(self.ENCODE_FORMAT)
                self.messageSignal.emit(message)
        except Exception:
            self.messageSignal.emit("disconnected from server")