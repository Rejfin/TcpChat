from PyQt5 import QtWidgets
import sys
import splashScreen

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = splashScreen.SplashScreen()
    sys.exit(app.exec_())
