import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import requests

class MapParams:
    def __init__(self):
        self.lat = 61.665279
        self.lon = 50.813492
        self.spn = 0.0005

    def ll(self):
        return str(self.lon) + "," + str(self.lat)

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.mp = MapParams()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 600, 450)
        self.setWindowTitle('Карта')

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.map_label = QLabel()
        layout.addWidget(self.map_label)

        buttons_layout = QVBoxLayout()
        layout.addLayout(buttons_layout)

        zoom_in_button = QPushButton('Уменьшить масштаб')
        zoom_in_button.clicked.connect(self.zoom_in)
        buttons_layout.addWidget(zoom_in_button)

        zoom_out_button = QPushButton('Увеличить масштаб')
        zoom_out_button.clicked.connect(self.zoom_out)
        buttons_layout.addWidget(zoom_out_button)

        self.load_map()

    def load_map(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.mp.ll()}&spn={self.mp.spn},{self.mp.spn}&l=map"
        response = requests.get(map_request)
        if response.status_code == 200:
            with open("map.png", "wb") as file:
                file.write(response.content)

            pixmap = QPixmap("map.png")
            self.map_label.setPixmap(pixmap.scaled(600, 400, Qt.KeepAspectRatio))

    def zoom_in(self):
        if self.mp.spn < 19:
            self.mp.spn += 0.0001
            self.load_map()

    def zoom_out(self):
        if self.mp.spn > 0.0001:
            self.mp.spn -= 0.0001
            self.load_map()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_S:
            self.move_up()
        elif event.key() == Qt.Key_W:
            self.move_down()
        elif event.key() == Qt.Key_A:
            self.move_left()
        elif event.key() == Qt.Key_D:
            self.move_right()

    def move_up(self):
        spn = self.mp.spn
        self.mp.lat = max(-90, self.mp.lat - spn)
        self.load_map()

    def move_down(self):
        spn = self.mp.spn
        self.mp.lat = min(90, self.mp.lat + spn)
        self.load_map()

    def move_left(self):
        spn = self.mp.spn
        self.mp.lon = max(-180, self.mp.lon - spn)
        self.load_map()

    def move_right(self):
        spn = self.mp.spn
        self.mp.lon = min(180, self.mp.lon + spn)
        self.load_map()

def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
