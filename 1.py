import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import requests

class MapParams:
    def __init__(self):
        self.lat = 61.665279
        self.lon = 50.813492
        self.zoom = 16

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

        zoom_in_button = QPushButton('Увеличить масштаб')
        zoom_in_button.clicked.connect(self.zoom_in)
        buttons_layout.addWidget(zoom_in_button)

        zoom_out_button = QPushButton('Уменьшить масштаб')
        zoom_out_button.clicked.connect(self.zoom_out)
        buttons_layout.addWidget(zoom_out_button)

        search_layout = QHBoxLayout()
        layout.addLayout(search_layout)

        self.search_input = QLineEdit()
        self.search_input.returnPressed.connect(self.search_object)
        search_layout.addWidget(self.search_input)

        search_button = QPushButton('Искать')
        search_button.clicked.connect(self.search_object)
        search_layout.addWidget(search_button)

        self.load_map()

    def load_map(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.mp.ll()}&z={self.mp.zoom}&l=map&pt={self.mp.ll()},pm2al"
        response = requests.get(map_request)
        if response.status_code == 200:
            with open("map.png", "wb") as file:
                file.write(response.content)

            pixmap = QPixmap("map.png")
            self.map_label.setPixmap(pixmap.scaled(600, 400, Qt.KeepAspectRatio))

    def zoom_in(self):
        if self.mp.zoom < 19:
            self.mp.zoom += 1
            self.load_map()

    def zoom_out(self):
        if self.mp.zoom > 1:
            self.mp.zoom -= 1
            self.load_map()

    def search_object(self):
        query = self.search_input.text()
        if query:
            geocoder_api_server = "https://geocode-maps.yandex.ru/1.x/"
            geocoder_params = {
                "format": "json",
                "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
                "geocode": query
            }
            response = requests.get(geocoder_api_server, params=geocoder_params)
            if response:
                json_response = response.json()
                try:
                    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                    self.mp.lat = float(toponym["Point"]["pos"].split()[1])
                    self.mp.lon = float(toponym["Point"]["pos"].split()[0])
                    self.load_map()
                except IndexError:
                    print("не найденно")

def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
