from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox
import sys
import csv
from frontend.api_client import ApiClient

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.api = ApiClient()
        self.setWindowTitle("Система обладнання")

        self.resize(800, 600)

        layout = QVBoxLayout()

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.load_btn = QPushButton("Завантажити список")
        self.load_btn.clicked.connect(self.load_equipment)
        layout.addWidget(self.load_btn)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Id обладнання")
        layout.addWidget(self.id_input)

        self.status_input = QLineEdit()
        self.status_input.setPlaceholderText("Новий стан")
        layout.addWidget(self.status_input)

        self.room_input = QLineEdit()
        self.room_input.setPlaceholderText("Новий кабінет")
        layout.addWidget(self.room_input)

        self.update_btn = QPushButton("Оновити стан")
        self.update_btn.clicked.connect(self.update_status)
        layout.addWidget(self.update_btn)

        self.move_btn = QPushButton("Перемістити")
        self.move_btn.clicked.connect(self.move_equipment)
        layout.addWidget(self.move_btn)

        self.export_btn = QPushButton("Експорт у CSV")
        self.export_btn.clicked.connect(self.export_csv)
        layout.addWidget(self.export_btn)

        self.stats_btn = QPushButton("Показати статистику")
        self.stats_btn.clicked.connect(self.show_stats)
        layout.addWidget(self.stats_btn)

        self.setLayout(layout)

    def show_stats(self):
        stats = self.api.get_stats()
        if not stats or "total" not in stats:
            QMessageBox.warning(self, "Помилка", "Не вдалося отримати статистику від сервера")
            return

        msg = f"Всього обладнання: {stats['total']}\n"
        msg += f"Несправного: {stats['broken']}\n"
        msg += "По кабінетах:\n"
        for room, count in stats["by_room"].items():
            msg += f" - {room}: {count}\n"

        QMessageBox.information(self, "Статистика", msg)

    def export_csv(self):
        data = self.api.get_equipment()
        path, _ = QFileDialog.getSaveFileName(self, "Зберегти файл", "", "CSV Files (*.csv)")
        if path:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Назва", "Стан", "Кабінет", "Проблеми"])
                for eq in data:
                    writer.writerow([eq["id"], eq["name"], eq["status"], eq["room"], eq.get("problems", "")])

    def load_equipment(self):
        data = self.api.get_equipment()
        self.table.setRowCount(len(data))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Назва", "Стан", "Кабінет", "Проблеми"])
        for i, eq in enumerate(data):
            self.table.setItem(i, 0, QTableWidgetItem(str(eq["id"])))
            self.table.setItem(i, 1, QTableWidgetItem(eq["name"]))
            self.table.setItem(i, 2, QTableWidgetItem(eq["status"]))
            self.table.setItem(i, 3, QTableWidgetItem(eq["room"]))
            self.table.setItem(i, 4, QTableWidgetItem(", ".join(eq.get("problems", []))))

    def update_status(self):
        self.api.update_status(int(self.id_input.text()), self.status_input.text())
        self.load_equipment()

    def move_equipment(self):
        self.api.move_equipment(int(self.id_input.text()), self.room_input.text())
        self.load_equipment()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())