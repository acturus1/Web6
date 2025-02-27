import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import requests

class MapParams:
    def __init__(self):
        self.lat = 11
        self.lon = 20
        self.snp = 16

    def ll(self):
        return str(self.lon) + "," + str(self.lat)

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.mp = MapParams()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 600, 450)
        self.setWindowTitle('...')

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.map_label = QLabel()
        layout.addWidget(self.map_label)

        self.load_map()

    def load_map(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.mp.ll()}&z={self.mp.snp}&l=map"
        response = requests.get(map_request)
        if response.status_code == 200:
            with open("map.png", "wb") as file:
                file.write(response.content)

            pixmap = QPixmap("map.png")
            self.map_label.setPixmap(pixmap.scaled(600, 400, Qt.KeepAspectRatio))

def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
