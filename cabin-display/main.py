"""Main application entry point"""
import sys
from PyQt6.QtWidgets import QApplication
from ui.dashboard_window import DashboardWindow


def main():
    app = QApplication(sys.argv)
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()