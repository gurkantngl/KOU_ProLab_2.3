import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Main Window')
        self.setGeometry(100, 100, 400, 300)

        self.button1 = QPushButton('Open Window 1', self)
        self.button1.clicked.connect(self.open_window1)
        self.button1.move(50, 50)

        self.button2 = QPushButton('Open Window 2', self)
        self.button2.clicked.connect(self.open_window2)
        self.button2.move(50, 100)

    def open_window1(self):
        self.window1 = Window1()
        self.window1.show()

    def open_window2(self):
        self.window2 = Window2(5, 3)
        self.window2.show()

class Window1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Window 1')
        self.setGeometry(150, 150, 400, 300)

class Window2(QMainWindow):
    def __init__(self, x, y):
        super().__init__()

        self.initUI(x, y)

    def initUI(self, x, y):

        grid = QGridLayout()
        self.setLayout(grid)
        
        currX = 0
        currY = 0 

        buttonList = []
        
        for _ in range(y):
            for _ in range(x):
                button = QPushButton(self)
                button.resize(int(800/x), int(600/y))
                button.move(int(currX), int(currY))
                currX += 800 / x
                button.setEnabled(False)
                buttonList.append(button)
            
            currX = 0    
            currY += 600 / y
            
        self.setFixedSize(800, 600)
        self.move(100, 100)
        self.setWindowTitle('Oyun Alanı')
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())