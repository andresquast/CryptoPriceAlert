from typing import List, Callable
from dataclasses import dataclass
from datetime import datetime
from PyQt5.QtWidgets import QSystemTrayIcon, QMessageBox
from PyQt5.QtGui import QIcon

@dataclass
class PriceAlert:
    threshold: float
    direction: str  # 'above' or 'below'
    created_at: datetime
    triggered: bool = False

class NotificationManager:
    def __init__(self):
        from PyQt5.QtWidgets import QApplication
        if not QApplication.instance():
            raise RuntimeError("QApplication must be created before NotificationManager")
        
        self.tray_icon = QSystemTrayIcon()
        self.tray_icon.setIcon(QIcon.fromTheme("dialog-information"))
        self.tray_icon.show()

    def show_notification(self, title: str, message: str, threshold: float):
        QMessageBox.information(None, title, message)

class AlertManager:
    def __init__(self, notification_callback: Callable[[str, str, float], None]):
        self.alerts: List[PriceAlert] = []
        self.notification_callback = notification_callback

    def add_alert(self, threshold: float, direction: str = 'above') -> None:
        alert = PriceAlert(threshold=threshold, direction=direction, created_at=datetime.now())
        self.alerts.append(alert)

    def check_alerts(self, current_price: float) -> List[PriceAlert]:
        triggered = []
        for alert in self.alerts:
            should_trigger = (
                (alert.direction == 'above' and current_price >= alert.threshold) or
                (alert.direction == 'below' and current_price <= alert.threshold)
            )
            if not alert.triggered and should_trigger:
                alert.triggered = True
                triggered.append(alert)
                if self.notification_callback:
                    direction_text = "risen above" if alert.direction == 'above' else "fallen below"
                    self.notification_callback(
                        f"Price Alert: ${current_price:,.2f}",
                        f"Price has {direction_text} threshold: ${alert.threshold:,.2f}",
                        alert.threshold
                    )
        return triggered

    def get_active_alerts(self) -> List[PriceAlert]:
        return [a for a in self.alerts if not a.triggered]
        
    def remove_alert(self, alert: PriceAlert) -> None:
        if alert in self.alerts:
            self.alerts.remove(alert)
            
    def clear_alerts(self) -> None:
        self.alerts.clear()