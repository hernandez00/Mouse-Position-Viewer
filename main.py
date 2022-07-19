# Documentação da biblioteca Pynput:
# https://pynput.readthedocs.io/en/latest/keyboard.html#monitoring-the-keyboard

import pyautogui, sys
from PyQt6.QtWidgets            import QApplication, QMainWindow, QTableWidgetItem
from _window.position_viewer    import Ui_MainWindow
from threading                  import Thread
from pynput.mouse               import Listener
from time                       import sleep

class MousePositionViewer(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.thread_1_Exec()
        self.thread_2_Exec()
        self.rowPosition = 0

    def locateMousePosition(self):
        while True:
            sleep(0.05)
            x, y = pyautogui.position()
            self.xLabel.setText(str(x))
            self.yLabel.setText(str(y))

    def listenMouseClick(self):
        def on_click(x, y, button, pressed):
            print('{0} at {1}'.format('Pressed' if pressed else 'Released', (x, y)))
            MousePositionViewer.putYXValue(self, pressed, x, y)

        listener = Listener(on_click=on_click)

        listener.start()
        try:    
            listener.join()
        finally:
            listener.stop() 

    def putYXValue(self, press, x, y):
        x, y = str(x), str(y)
        self.tableWidget.setRowCount(self.rowPosition + 1)

        if press:
            self.xLabelMouseDown.setText(x)
            self.yLabelMouseDown.setText(y)
            self.listWidget.addItem('Click: ' + 'X: ' + x + ' : ' + 'Y:' + y)
            self.tableWidget.setItem(self.rowPosition, 0, QTableWidgetItem('Click'))
            self.tableWidget.setItem(self.rowPosition, 1, QTableWidgetItem(f'X: {x}'))
            self.tableWidget.setItem(self.rowPosition, 2, QTableWidgetItem(f'Y: {y}'))
        else:
            self.xLabelMouseUp.setText(x)
            self.yLabelMouseUp.setText(y)
            self.listWidget.addItem('Release: ' + 'X: ' + x + ' : ' + 'Y:' + y)
            self.tableWidget.setItem(self.rowPosition, 0, QTableWidgetItem('Release'))
            self.tableWidget.setItem(self.rowPosition, 1, QTableWidgetItem(f'X: {x}'))
            self.tableWidget.setItem(self.rowPosition, 2, QTableWidgetItem(f'Y: {y}'))
        
        self.rowPosition += 1

    def thread_1_Exec(self):
        t1 = Thread(target=self.locateMousePosition, daemon=True)
        t1.start() 

    def thread_2_Exec(self):
        t2 = Thread(target=self.listenMouseClick, daemon=True)
        t2.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MousePositionViewer()
    window.show()
    app.exec()
    
    