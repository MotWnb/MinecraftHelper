import sys

from PyQt5.QtCore import Qt, QPoint, QThread
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLineEdit, QTextEdit

import scan_server
import srv_resolve


class async_scan(QThread):

    def __init__(self, host: str):
        super(async_scan, self).__init__()
        self.host = host

    def run(self):

        print(self.host)
        scan_server.main(self.host)


class Window(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(135, 206, 250))
        painter.drawRect(0, 0, self.width(), 50)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.f = None
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle('MinecraftHelper')
        self.setGeometry(100, 100, 600, 400)
        self.m_drag = False
        self.m_DragPosition = QPoint()

        window = Window()
        self.setCentralWidget(window)

        self.close_button = QPushButton('X', self)
        self.close_button.setGeometry(self.width() - 50, 0, 50, 50)
        self.close_button.setStyleSheet('''
            QPushButton {
                background-color: #87CEFA;
                border: none;
            }
            QPushButton:hover {
                background-color: #B0E2FF;
            }
        ''')
        self.close_button.clicked.connect(self.close)

        self.srv_button = QPushButton('SRV解析', self)
        self.srv_button.setGeometry(20, 0, 150, 50)
        self.srv_button.setStyleSheet('''
            QPushButton {
                background-color: #87CEFA;
                border: none;
            }
            QPushButton:hover {
                background-color: #B0E2FF;
            }
        ''')
        self.srv_button.clicked.connect(self.srv_button_clicked)

        self.scan_button = QPushButton('服务器扫描', self)
        self.scan_button.setGeometry(200, 0, 150, 50)
        self.scan_button.setStyleSheet('''
            QPushButton {
                background-color: #87CEFA;
                border: none;
            }
            QPushButton:hover {
                background-color: #B0E2FF;
            }
        ''')
        self.scan_button.clicked.connect(self.scan_button_clicked)

        self.srv_input = QLineEdit(self)
        self.srv_input.setGeometry(20, 70, 150, 30)
        self.srv_input.hide()

        self.scan_input = QLineEdit(self)
        self.scan_input.setGeometry(20, 70, 150, 30)
        self.scan_input.hide()

        self.srv_parse_button = QPushButton('解析', self)
        self.srv_parse_button.setGeometry(20, 110, 80, 30)
        self.srv_parse_button.clicked.connect(self.srv_parse_button_clicked)
        self.srv_parse_button.hide()

        self.scan_parse_button = QPushButton('扫描', self)
        self.scan_parse_button.setGeometry(20, 110, 80, 30)
        self.scan_parse_button.clicked.connect(self.scan_parse_button_clicked)
        self.scan_parse_button.hide()

        self.srv_output = QTextEdit(self)
        self.srv_output.setGeometry(20, 150, 150, 200)
        self.srv_output.setReadOnly(True)  # 设置为只读
        self.srv_output.setAttribute(Qt.WA_TransparentForMouseEvents)  # 禁用鼠标事件，使其透明
        self.srv_output.setStyleSheet('''
            QTextEdit {
                background-color: transparent;
                border: none
            }
        ''')
        self.srv_output.hide()

        self.scan_output = QTextEdit(self)
        self.scan_output.setGeometry(20, 150, 150, 200)
        self.scan_output.setReadOnly(True)  # 设置为只读
        self.scan_output.setAttribute(Qt.WA_TransparentForMouseEvents)  # 禁用鼠标事件，使其透明
        self.scan_output.setStyleSheet('''
            QTextEdit {
                background-color: transparent;
                border: none
            }
        ''')
        self.scan_output.hide()

    def srv_button_clicked(self):
        self.srv_input.show()
        self.srv_parse_button.show()
        self.srv_output.show()
        self.scan_input.hide()
        self.scan_parse_button.hide()
        self.scan_output.hide()

    def scan_button_clicked(self):
        self.scan_input.show()
        self.scan_parse_button.show()
        self.scan_output.show()
        self.srv_input.hide()
        self.srv_parse_button.hide()
        self.srv_output.hide()

    def srv_parse_button_clicked(self):
        input_word = self.srv_input.text()
        output_word = srv_resolve.srv_resolve(input_word)
        self.srv_output.setText(output_word)
        pass

    def scan_parse_button_clicked(self):
        input_word = self.scan_input.text()
        output_word = "请查看python控制台"
        self.f = async_scan(input_word)
        self.f.start()
        self.scan_output.setText(output_word)
        pass

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.y() < 50:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.m_drag:
            self.move(event.globalPos() - self.m_DragPosition)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = False
            event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
