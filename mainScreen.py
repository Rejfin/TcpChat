import threading
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QMainWindow
from Receiver import Receiver
from main_ui import Ui_MainWindow

counter = 0


class MainScreen(QMainWindow):
    def __init__(self, client):
        QMainWindow.__init__(self)

        # setup ui
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.bt_send.clicked.connect(self.bt_send_message)
        self.ui.textEdit_message.installEventFilter(self)
        self.ui.textEdit_message.setFocus()

        # declare elements necessary for message list object
        self.client = client
        self.brush = QBrush()
        self.model = QtGui.QStandardItemModel()

        # setup connection info
        self.HOST = '127.0.0.1'
        self.PORT = 60453
        self.ENCODE_FORMAT = "utf-8"
        self.nick = 'nick'

        # create object of Receiver class, connect to messageSignal and run it in separate thread
        self.receiver = Receiver(self.client)
        self.receiver.messageSignal.connect(self.new_message)
        self.thread1 = threading.Thread(target=self.receiver.run)
        self.thread1.start()

    def bt_send_message(self):
        message = self.ui.textEdit_message.toPlainText()
        if message != "":
            self.send_message(message.strip())

    def send_message(self, message):
        # send message length
        self.client.sendall(len(message.encode(self.ENCODE_FORMAT)).to_bytes(2, 'big'))
        # send message
        self.client.sendall(message.encode(self.ENCODE_FORMAT))
        self.ui.textEdit_message.clear()

    # Fire on when new message appear
    def new_message(self, message):

        self.ui.listView_messages.setModel(self.model)

        # if specific message color it on red color, else print message in white color
        if "joined the chat" in message or "connection with" in message or "has left the chat" in message \
                or "disconnected from server" in message:
            self.brush.setColor(Qt.GlobalColor.red)
            item = QtGui.QStandardItem(message)
            item.setForeground(self.brush)
        else:
            self.brush.setColor(Qt.GlobalColor.white)
            item = QtGui.QStandardItem(message)
            item.setForeground(self.brush)

        self.model.appendRow(item)

    # if user press enter and message box is not focused but it's not empty, send message
    def keyPressEvent(self, key: QtGui.QKeyEvent):
        message = self.ui.textEdit_message.toPlainText()
        if key.key() == Qt.Key_Return and message.strip() != "":
            self.send_message(message.strip())

    def eventFilter(self, obj, event):
        # if user press enter and message box will be not empty and has focus on self, send message
        if event.type() == QEvent.KeyPress and obj is self.ui.textEdit_message:
            if event.key() == Qt.Key_Return and obj.hasFocus() and obj.toPlainText().strip() != "":
                self.send_message(obj.toPlainText().strip())
                return True
            else:
                return False
        else:
            return super().eventFilter(obj, event)

