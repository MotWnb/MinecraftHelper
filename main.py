import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt

import srv_resolve


class InputBoxManager:
    def __init__(self, input_box, resolve_button, result_text):
        self.input_box = input_box
        self.resolve_button = resolve_button
        self.result_text = result_text

    def show_result_text(self, text):
        self.result_text.setText(text)
        self.result_text.show()


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle('MinecraftHelper')
        self.setFixedSize(800, 600)

        top_bar = QWidget(self)
        top_bar.setGeometry(0, 0, 800, 70)
        top_bar.setStyleSheet('background-color: #204a87')

        close_button = QPushButton('×', top_bar)
        close_button.setGeometry(743, 13, 44, 44)
        close_button.setStyleSheet('QPushButton {background-color: #204a87; color: #ffffff; border: none}'
                                   'QPushButton:hover {background-color: #68a9ef}')
        close_button.clicked.connect(self.close)

        srv_button = QPushButton('SRV解析', top_bar)
        srv_button.setGeometry(290, 13, 80, 44)
        srv_button.setStyleSheet('QPushButton {background-color: #204a87; color: #ffffff; border: none}'
                                 'QPushButton:hover {background-color: #68a9ef}')
        srv_button.clicked.connect(self.on_srv_button_clicked)

        scan_button = QPushButton('服务器扫描', top_bar)
        scan_button.setGeometry(422, 13, 80, 44)
        scan_button.setStyleSheet('QPushButton {background-color: #204a87; color: #ffffff; border: none}'
                                 'QPushButton:hover {background-color: #68a9ef}')
        scan_button.clicked.connect(self.on_srv_button_clicked)

        container = QWidget(self)
        container.setGeometry(200, 100, 400, 300)

        # 创建垂直布局
        layout = QVBoxLayout(container)

        # 创建输入框
        input_layout = QHBoxLayout()
        self.srv_input_box = QLineEdit(self)
        input_layout.addWidget(self.srv_input_box)
        self.srv_input_box.hide()
        layout.addLayout(input_layout)

        # 创建解析按钮
        self.srv_resolve_button = QPushButton('解析', container)
        self.srv_resolve_button.clicked.connect(self.on_resolve_button_clicked)
        self.srv_resolve_button.hide()
        layout.addWidget(self.srv_resolve_button)

        # 创建结果显示文本框
        self.srv_result_text = QLabel("", container)
        self.srv_result_text.hide()
        layout.addWidget(self.srv_result_text)

        self.input_box_manager = InputBoxManager(self.srv_input_box, self.srv_resolve_button, self.srv_result_text)
        self.oldPos = None

    def on_srv_button_clicked(self):
        self.srv_resolve_button.show()
        self.srv_input_box.show()
        self.srv_result_text.show()
        pass

    def on_resolve_button_clicked(self):
        input_text = self.srv_input_box.text()
        # 在这里处理输入框中的文本并将结果显示在文本框中
        try:
            output = srv_resolve.srv_resolve(input_text)
            self.input_box_manager.show_result_text(output)
        except Exception as e:
            print(e)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton and event.y() < 70:
            self.oldPos = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self.oldPos:
            self.move(event.globalPos() - self.oldPos)

    def mouseReleaseEvent(self, event):
        self.oldPos = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())