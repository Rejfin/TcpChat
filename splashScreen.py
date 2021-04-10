import socket
from time import sleep
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QEvent
from PyQt5.QtWidgets import QMainWindow
from mainScreen import MainScreen
from splash_ui import Ui_SplashScreen


# noinspection PyUnresolvedReferences
class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)
        self.ui.progressBar.setVisible(False)
        self.ui.label_error.setVisible(False)
        self.ui.label_loading.setVisible(False)
        self.ui.pushButton_connect.clicked.connect(self.connect_to_server)
        self.ui.plainTextEdit_nick.installEventFilter(self)
        self.ui.pushButton_exit.clicked.connect(self.on_close)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.show()

    def connect_to_server(self):
        nick = self.ui.plainTextEdit_nick.toPlainText().strip()
        if nick != "":
            self.ui.label_error.setVisible(False)
            self.ui.progressBar.setVisible(True)
            self.ui.label_loading.setVisible(True)
            self.ui.pushButton_connect.setEnabled(False)
            self.ui.plainTextEdit_nick.setEnabled(False)
            self.establish_connection(nick)

    def establish_connection(self, nick):
        self.servCon = ServerConnect()
        self.servCon.count_signal.connect(self.on_count_change)
        self.servCon.error_signal.connect(self.on_error_occurre)
        self.servCon.close_signal.connect(self.on_close)
        self.servCon.start_conn(nick)

    def on_count_change(self, value):
        self.ui.progressBar.setValue(value)

    def on_error_occurre(self, message):
        self.ui.label_error.setText(message)
        self.ui.label_error.setVisible(True)
        self.ui.progressBar.setVisible(False)
        self.ui.label_loading.setVisible(False)
        self.ui.pushButton_connect.setEnabled(True)
        self.ui.plainTextEdit_nick.setEnabled(True)

    def on_close(self):
        self.close()

    def keyPressEvent(self, key: QtGui.QKeyEvent):
        if key.key() == Qt.Key_Return:
            self.connect_to_server()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and obj is self.ui.plainTextEdit_nick:
            if event.key() == Qt.Key_Return and obj.hasFocus():
                self.connect_to_server()
                return True
            else:
                return False
        else:
            return super().eventFilter(obj, event)


# noinspection PyUnresolvedReferences
class ServerConnect(QThread):
    HOST = '127.0.0.1'
    PORT = 60453
    ENCODE_FORMAT = "utf-8"

    count_signal = pyqtSignal(int)
    error_signal = pyqtSignal(str)
    close_signal = pyqtSignal()

    def start_conn(self, nick):
        x = 0
        while x < 101:
            if x == 50:
                try:
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client.connect((self.HOST, self.PORT))
                    client.send(f"nick:{nick}".encode(self.ENCODE_FORMAT))
                except ConnectionRefusedError:
                    self.error_signal.emit("Connection refused. Are you sure server is running?")
                    break
                except Exception:
                    self.error_signal.emit("An unexpected error has occurred")
                    break

            self.count_signal.emit(x)
            x += 1
            sleep(0.015)

        # 100% reach, load main window
        if x >= 100:
            self.main = MainScreen(client)
            self.main.show()
            self.close_signal.emit()




