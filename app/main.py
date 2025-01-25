import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QComboBox, QScrollArea)
from PyQt5.QtCore import QTimer, Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime
from app.api.coingecko import CoinGeckoAPI
from app.utils.alerts import AlertManager, NotificationManager

SUPPORTED_COINS = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Dogecoin": "dogecoin",
    "Cardano": "cardano",
    "Solana": "solana"
}

class CryptoMonitor(QMainWindow):
    def __init__(self, alert_manager):
        super().__init__()
        self.alert_manager = alert_manager
        self.setWindowTitle("Crypto Price Monitor")
        self.setGeometry(100, 100, 800, 600)
        
        self.api = CoinGeckoAPI()
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Coin selector
        coin_layout = QHBoxLayout()
        self.coin_selector = QComboBox()
        self.coin_selector.addItems(SUPPORTED_COINS.keys())
        self.coin_selector.currentTextChanged.connect(self.on_coin_changed)
        coin_layout.addWidget(QLabel("Select Cryptocurrency:"))
        coin_layout.addWidget(self.coin_selector)
        coin_layout.addStretch()
        layout.addLayout(coin_layout)
        
        self.price_label = QLabel("Current Price: $0.00")
        self.price_label.setAlignment(Qt.AlignCenter)
        self.price_label.setStyleSheet("font-size: 24px;")
        layout.addWidget(self.price_label)
        
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        alert_layout = QHBoxLayout()
        self.direction_combo = QComboBox()
        self.direction_combo.addItems(["Above", "Below"])
        alert_layout.addWidget(self.direction_combo)
        
        self.alert_input = QLineEdit()
        self.alert_input.setPlaceholderText("Enter price threshold")
        alert_button = QPushButton("Set Alert")
        alert_button.clicked.connect(self.set_alert)
        self.alert_input.returnPressed.connect(self.set_alert)
        alert_layout.addWidget(self.alert_input)
        alert_layout.addWidget(alert_button)
        layout.addLayout(alert_layout)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        self.alerts_layout = QVBoxLayout(scroll_widget)
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)
        
        self.prices = []
        self.timestamps = []
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_price)
        self.timer.start(20000)
        self.update_price()

    def on_coin_changed(self):
        self.prices = []
        self.timestamps = []
        self.update_price()
        self.alert_manager.clear_alerts()
        self.update_alert_display()

    def get_selected_coin_id(self):
        return SUPPORTED_COINS[self.coin_selector.currentText()]

    def update_price(self):
        try:
            coin_id = self.get_selected_coin_id()
            price = self.api.get_price(coin_id)
            self.price_label.setText(f"Current Price: ${price:,.2f}")
            
            self.prices.append(price)
            self.timestamps.append(datetime.now())
            
            if len(self.prices) > 50:
                self.prices.pop(0)
                self.timestamps.pop(0)
            
            self.ax.clear()
            self.ax.plot(self.timestamps, self.prices)
            self.ax.set_title(f"{self.coin_selector.currentText()} Price History")
            self.ax.tick_params(axis='x', rotation=45)
            self.figure.tight_layout()
            self.canvas.draw()
            
            self.alert_manager.check_alerts(price)
            self.update_alert_display()
            
        except Exception as e:
            print(f"Error updating price: {e}")

    def set_alert(self):
        try:
            threshold = float(self.alert_input.text())
            direction = self.direction_combo.currentText().lower()
            self.alert_manager.add_alert(threshold, direction)
            self.alert_input.clear()
            self.update_alert_display()
        except ValueError:
            pass

    def delete_alert(self, alert):
        self.alert_manager.remove_alert(alert)
        self.update_alert_display()

    def update_alert_display(self):
        while self.alerts_layout.count():
            child = self.alerts_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for alert in self.alert_manager.get_active_alerts():
            alert_widget = QWidget()
            h_layout = QHBoxLayout(alert_widget)
            
            direction = "above" if alert.direction == "above" else "below"
            label = QLabel(f"${alert.threshold:,.2f} ({direction})")
            h_layout.addWidget(label)
            
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda checked, a=alert: self.delete_alert(a))
            h_layout.addWidget(delete_button)
            
            self.alerts_layout.addWidget(alert_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    notification_manager = NotificationManager()
    alert_manager = AlertManager(notification_manager.show_notification)
    window = CryptoMonitor(alert_manager)
    window.show()
    sys.exit(app.exec_())