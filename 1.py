import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QLineEdit, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import requests

class MapParams:
    def __init__(self):
        self.lat = 61.665279
        self.lon = 50.813492
        self.spn = 0.0005
        self.theme = 'light'
        self.api = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        self.api2 = '8013b162-6b42-4997-9691-77b7074026e0'
        self.marker_lat = None
        self.marker_lon = None

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

        themes = QComboBox()
        themes.addItem("Светлая")
        themes.addItem("Тёмная")

        themes.currentTextChanged.connect(self.change_theme)
        buttons_layout.addWidget(themes)

        search_layout = QHBoxLayout()
        layout.addLayout(search_layout)

        self.search_input = QLineEdit()
        self.search_input.returnPressed.connect(self.search_object)
        search_layout.addWidget(self.search_input)

        search_button = QPushButton('Искать')
        search_button.clicked.connect(self.search_object)
        search_layout.addWidget(search_button)

        reset_button = QPushButton('Сброс поискового результата')
        reset_button.clicked.connect(self.reset_search_result)
        search_layout.addWidget(reset_button)

        self.load_map()

    def load_map(self):
        if self.mp.marker_lat and self.mp.marker_lon:
            map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.mp.ll()}&theme={self.mp.theme}&spn={self.mp.spn},{self.mp.spn}&l=map&pt={self.mp.marker_lon},{self.mp.marker_lat},pm2al&apikey={self.mp.api}"
        else:
            map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.mp.ll()}&theme={self.mp.theme}&spn={self.mp.spn},{self.mp.spn}&l=map&apikey={self.mp.api}"
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

    def change_theme(self, text):
        if text == "Светлая":
            self.mp.theme = "light"
        elif text == 'Тёмная':
            self.mp.theme = "dark"
        self.load_map()

    def search_object(self):
        query = self.search_input.text()
        if query:
            geocoder_api_server = "https://geocode-maps.yandex.ru/1.x/"
            geocoder_params = {
                "format": "json",
                "apikey": self.mp.api2,
                "geocode": query
            }
            response = requests.get(geocoder_api_server, params=geocoder_params)
            if response:
                json_response = response.json()
                try:
                    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                    self.mp.lat = float(toponym["Point"]["pos"].split()[1])
                    self.mp.lon = float(toponym["Point"]["pos"].split()[0])
                    self.mp.marker_lat = self.mp.lat
                    self.mp.marker_lon = self.mp.lon
                    self.load_map()
                except IndexError:
                    print("Объект не найден")

    def reset_search_result(self):
        self.mp.marker_lat = None
        self.mp.marker_lon = None
        self.load_map()

def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
