import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QPushButton

class Example(QWidget):

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
        self.move(600, 200)
        self.setWindowTitle('Oyun Alanı')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    x = 5
    y = 4
    ex = Example(x, y)
    sys.exit(app.exec_())