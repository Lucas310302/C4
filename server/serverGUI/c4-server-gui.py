import sys
import pyperclip
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import QIcon, QFont, QClipboard

class ControlServerUI(QWidget):
    def __init__(self):
        
        #Function for creating buttons with some default values plus easier icon creation
        def CreateButton(icon_path: str = None, icon_size: QSize = None, set_button_to_icon_size: bool = None, button_text: str = None) -> QPushButton:
            button = QPushButton()
            if icon_path and icon_size:
                temp_icon = QIcon(QDir.current().filePath(icon_path))
                button.setIcon(temp_icon)
                button.setIconSize(icon_size)
            if set_button_to_icon_size:
                button.setMinimumSize(icon_size)
                button.setMaximumSize(icon_size)
            button.setText(button_text)
            button.setCursor(Qt.PointingHandCursor)
            return button
        
        super().__init__()
        self.setWindowTitle("C4")
        self.setWindowFlags(Qt.CustomizeWindowHint)

        main_layout = QGridLayout()
        self.setLayout(main_layout)
        
        #↓HEADER↓#
        
        header_widget = QWidget()
        header_widget.setObjectName("header_widget")
        header_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        header_layout = QHBoxLayout(header_widget)

        name_label = QLabel("-C4-")
        name_label.setObjectName("window_title")
        header_layout.addWidget(name_label, alignment=Qt.AlignLeft)

        header_layout.addStretch()
        
        minimize_button = CreateButton("server/serverGUI/icon/minimize_icon.png", QSize(30, 30), True)
        minimize_button.clicked.connect(self.showMinimized)
        header_layout.addWidget(minimize_button, alignment=Qt.AlignRight)
        
        exit_button = CreateButton("server/serverGUI/icon/exit_icon.png", QSize(30, 30), True)
        exit_button.clicked.connect(QApplication.quit)
        header_layout.addWidget(exit_button, alignment=Qt.AlignRight)
        
        #↑HEADER↑#
        #↓PAGES↓#
        
        pages_widget = QWidget()
        pages_layout = QVBoxLayout(pages_widget)
        pages_widget.setFixedSize(750, 600)
        pages_widget.setObjectName("pages")
        
        #Homepage GUI#
        homepage_widget = QWidget()
        homepage_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        homepage_widget.setObjectName("homepage")
        homepage_layout = QVBoxLayout(homepage_widget)
        homepage_layout.setContentsMargins(0, 0, 0, 0)
        
        #Homepage elements
        homepage_title = QLabel("Welcome to C4")
        homepage_title.setObjectName("homepage-title")
        
        homepage_title2 = QLabel('"easy to use, and destructive"')
        homepage_title2.setObjectName("homepage-undertitle")
        homepage_title2.setFont(QFont("Helvetica", italic=True))
        
        xmr_wallet_donation_link = "85XhwdmegungjeHM6vU3PzRtXQycZm5UmRBpbR34b5WX3qYUB5Md4qo5fSpBQei2QzDWjfrtC31dJVJkQ6kNg25SDnveHDw"
        
        xmr_donation = CreateButton(button_text=f"Donate XMR\n(Click to copy address to clipboard)")
        xmr_donation.setObjectName("donation-link")
        xmr_donation.setFixedSize(250, 60)
        xmr_donation.clicked.connect(lambda: pyperclip.copy(xmr_wallet_donation_link))
        
        
        #setting up the homepage layout
        homepage_layout.addStretch()
        homepage_layout.addWidget(homepage_title, alignment=Qt.AlignmentFlag.AlignCenter)
        homepage_layout.addWidget(homepage_title2, alignment=Qt.AlignmentFlag.AlignCenter)
        homepage_layout.addStretch()
        homepage_layout.addWidget(xmr_donation, alignment=Qt.AlignmentFlag.AlignCenter)
        homepage_layout.addStretch()
        
        #Overview GUI#
        overview_widget = QWidget()
        
        #Terminal GUI#
        terminal_widget = QWidget()
        
        #Map GUI#
        map_widget = QWidget()
        
        #pages layout#
        pages_layout.addWidget(homepage_widget)
        pages_layout.addWidget(overview_widget)
        pages_layout.addWidget(terminal_widget)
        pages_layout.addWidget(map_widget)
        
        #Switch pages logic#
        pages_list = [homepage_widget, overview_widget, terminal_widget, map_widget]
        def gotoPage(index : int):
            for i in range(len(pages_list)):
                if index == i:
                    pages_list[i].setVisible(True)
                else:
                    pages_list[i].setVisible(False)
                
        
        #↑PAGES↑#
        #↓SIDE MENU↓#

        #Side Menu Container
        menu_widget = QWidget()
        menu_widget.setObjectName("menu_widget")
        menu_widget.setFixedSize(50, 600)
        menu_widget.setMinimumSize(50, 600)
        menu_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        #Side Menu Layout
        menu_layout = QVBoxLayout(menu_widget)
        menu_layout.addStretch()
        
        #Home
        home_button = CreateButton("server/serverGUI/icon/home_icon.png", QSize(24, 24), False)
        home_button.setObjectName("side_menu_buttons")
        home_button.clicked.connect(lambda: gotoPage(0))
        menu_layout.addWidget(home_button)
        
        #Overview
        overview_button = CreateButton("server/serverGUI/icon/overview_icon.png", QSize(24, 24), False)
        overview_button.setObjectName("side_menu_buttons")
        overview_button.clicked.connect(lambda: gotoPage(1))
        menu_layout.addWidget(overview_button)
        
        #Terminal
        terminal_button = CreateButton("server/serverGUI/icon/terminal_icon.png", QSize(24, 24), False)
        terminal_button.setObjectName("side_menu_buttons")
        terminal_button.clicked.connect(lambda: gotoPage(2))
        menu_layout.addWidget(terminal_button)
        
        #Global Map
        map_button = CreateButton("server/serverGUI/icon/map_icon.png", QSize(24, 24), False)
        map_button.setObjectName("side_menu_buttons")
        map_button.clicked.connect(lambda: gotoPage(3))
        menu_layout.addWidget(map_button)
        
        menu_layout.addStretch()
        
        #↑SIDE MENU↑#
        #↓MAIN LAYOUT SETUP↓#
        
        main_layout.addWidget(header_widget, 0, 0, 1, 2)
        main_layout.addWidget(pages_widget, 1, 1)
        main_layout.addWidget(menu_widget, 1, 0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        #↑MAIN LAYOUT SETUP↑#
        #↓STYLESHEET↓#
        
        with open("./server/serverGUI/stylesheet.txt", "r") as f:
            stylesheet = f.read()
            f.close()

        self.setStyleSheet(stylesheet)
        
        #↑STYLESHEET↑#


if __name__ == "__main__":
    app = QApplication([])

    widget = ControlServerUI()
    widget.setFixedSize(800, 600)
    widget.show()

    sys.exit(app.exec())