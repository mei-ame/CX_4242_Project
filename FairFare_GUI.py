import sys

import time

from qrangeslider import QRangeSlider

from pprint import pprint

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QRadioButton, QTableWidget, QHeaderView,
    QListWidget, QTextEdit, QMessageBox, QDateTimeEdit, QComboBox, QHBoxLayout, QAbstractItemView, QFrame, QTableWidgetItem
)
from PyQt5.QtCore import (
    QDate, Qt
)
from PyQt5.QtGui import (
    QPixmap, QFont, QColor
)
from Google_Flights_Scraper import search_flights  # Import the flight search function
from Google_Hotel_Scraper import search_hotels

import requests
import json
from bs4 import BeautifulSoup
from pprint import pprint
import re
from datetime import datetime

# Stylesheet information for GUI layout

GUI_HEIGHT = 750
GUI_WIDTH = 1300
GUI_PANEL_WIDTH = 300
LEFT_PANEL_HEIGHT = 600

QCOMBO_HEIGHT = 50

# QLABEL_BASE = "QLabel {{background: #{}; color: #00aeef; border: 3px inset #5252cc; font: 'Noto Serif';}}"
# # QLABEL_DEFAULT = "QLabel {background: #002050; color: #00aeef; border: 3px outset #5252cc; font: 'Noto Serif'; font-size: 50pt;}"
# QLABEL_DEFAULT = "QWidget {font: 'Noto Serif'; font-size: 16pt; text-align: center; background: #000000; color: #ffffff; border: 0px outset #696969;} \
                    # QLabel {font: 'Noto Serif'; font-size: 30pt; qproperty-alignment: AlignCenter; background: #000000; color: #ffffff; border: 3px outset #696969;}"
QT_GUI = "QLabel {height: 40; font: 'Noto Serif'; font-size: 16pt; text-align: center; qproperty-alignment: AlignCenter; background: #343f62; color: #ffffff;} \
                QWidget {height: 40; font: 'Noto Serif'; font-size: 16pt; text-align: center; qproperty-alignment: AlignCenter; background: #343f62; color: #ffffff;} \
                QLineEdit {height: 40; font: 'Noto Serif'; font-size: 16pt; text-align: center; qproperty-alignment: AlignCenter; background: #343f62; color: #ffffff;} \
                QPushButton {border: 3px outset #696969; background: #343f62;} \
                QComboBox {font: 'Noto Serif'; font-size: 20pt; border: 3px outset #696969;} \
                QCalendarWidget QWidget{background-color:#343f62; color: white} \
                QCalendarWidget QToolButton{ background-color:#343f62; color: white; icon-size: 30px; } \
                QCalendarWidget QMenu{background-color:#343f62; color: white;}\
                QCalendarWidget QAbstractItemView:enabled{background-color: #343f62; color: gray;}\
                QCalendarWidget QAbstractItemView:disabled{background-color: #343f62 ;color: black;}\
                QCalendarWidget QMenu{background-color: #343f62;}\
                QCalendarWidget QSpinBox{background-color: #343f62;}"  
QLABEL_PANEL = "QLabel {height: 40; font: 'Noto Serif'; font-size: 16pt; text-align: left; qproperty-alignment: AlignCenter; background: #343f62; color: #ffffff;}"
QLABEL_ICON = "QLabel {qproperty-alignment: AlignCenter; border: 0px outset #696969; width: 10; height: 10;}"
QLABEL_TITLE = "QLabel {width: 30; height: 40; font: 'Noto Serif'; font-size: 45pt; text-align: center; qproperty-alignment: AlignCenter; background: #343f62; color: #ffffff; font-weight: bold; font-style: italic;}"
QLABEL_LEFT = "QWidget {text-align: center; qproperty-alignment: AlignTop;} \
               QLabel {text-align: center; qproperty-alignment: AlignCenter;}\
               QLineEdit {text-align: center; qproperty-alignment: AlignCenter;}\
               QRadioButton {text-align: center; qproperty-alignment: AlignTop;}\
                "




# SERP_API_KEY = "b637153e8613b18fc81533dfbf72045c9b43cbdd25323736bc3009ee6c38435a"  
SERP_API_KEY = "8e3b97559f70aeb1a2d6f78da4ca024bab7525e316361ac1c955016a16136cf7"

# Font Code
class Font(QFont):
    def __init__(self, size):
        super().__init__()
        self.setFamily("Noto Serif")
        self.setStyleHint(QFont.StyleHint.Times)
        self.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        self.setPointSize(size)
        self.setHintingPreference(QFont.HintingPreference.PreferFullHinting)

class Pane(QListWidget):
    def __init__(self):
        super(RightPane, self).__init__()
        font = Font(9)
        self.setFont(font)
        self.setDragDropMode(QAbstractItemView.DragDropMode.NoDragDrop)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setAlternatingRowColors(True)
        self.setFixedWidth(80)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

class FlightSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("FairFare")
        self.setGeometry(300, 100, GUI_WIDTH, GUI_HEIGHT)

        app.setStyleSheet(QT_GUI)

        # Get list of all airport codes and locations

        self.get_all_airports()

        self.all_currencies = json.load(open("google-travel-currencies.json"))
        self.all_countries = json.load(open("google-countries.json"))


        ##############################################################################################################
        #   BEGIN FLIGHT PAGE
        ##############################################################################################################

        ########## Input fields for search parameters

            # Departure Airport Code parameter
        self.flight_departure_entry = QLineEdit(self)
        self.flight_departure_entry.setPlaceholderText("Enter departure airport code (e.g., CDG)")
                # Parameter layout
        flight_dep_airport_layout = QVBoxLayout()
        flight_dep_airport_layout.addWidget(QLabel("Departure Airport Code:"))
        flight_dep_airport_layout.addWidget(self.flight_departure_entry)

            # Arrival Airport Code parameter
        self.flight_arrival_entry = QLineEdit(self)
        self.flight_arrival_entry.setPlaceholderText("Enter arrival airport code (e.g., AUS)")
                # Parameter layout
        flight_arr_airport_layout = QVBoxLayout()
        flight_arr_airport_layout.addWidget(QLabel("Arrival Airport Code:"))
        flight_arr_airport_layout.addWidget(self.flight_arrival_entry)

            # Departure Date parameter
        self.flight_departure_date_entry = QDateTimeEdit(self)
        self.flight_departure_date_entry.setCalendarPopup(True)
        self.flight_departure_date_entry.setDate(QDate.currentDate())
        self.flight_departure_date_entry.setDisplayFormat('yyyy-MM-dd')

                # Parameter layout
        flight_out_date_layout = QVBoxLayout()
        flight_out_date_layout.addWidget(QLabel("Departure Date:"))
        flight_out_date_layout.addWidget(self.flight_departure_date_entry)

            # Return Date parameter
        self.flight_return_date_entry = QDateTimeEdit(self)
        self.flight_return_date_entry.setCalendarPopup(True)
        self.flight_return_date_entry.setDate(QDate.currentDate())
        self.flight_return_date_entry.setDisplayFormat('yyyy-MM-dd')
        # self.flight_return_date_entry.setEnabled(False)

                # Parameter Layout
        flight_ret_date_layout = QVBoxLayout()
        self.flight_ret_date_label = QLabel("Return Date:")
        flight_ret_date_layout.addWidget(self.flight_ret_date_label)
        flight_ret_date_layout.addWidget(self.flight_return_date_entry)

            # Currency parameter
        self.flight_currency_entry = QComboBox(self)
        self.flight_currency_entry.addItems(self.all_currencies.keys())
        self.flight_currency_entry.setCurrentText('USD')

                # Parameter Layout
        flight_currency_entry_layout = QVBoxLayout()
        flight_currency_entry_layout.addWidget(QLabel("Currency:"))
        flight_currency_entry_layout.addWidget(self.flight_currency_entry)

                # Currency Description
        self.flight_currency_details = QLabel(self.all_currencies[self.flight_currency_entry.currentText()])
        self.flight_currency_entry.currentTextChanged.connect(lambda _: self.flight_currency_details.setText(self.all_currencies[self.flight_currency_entry.currentText()]))
        self.flight_currency_details.setVisible(False)

        flight_currency_layout = QHBoxLayout()
        flight_currency_layout.addLayout(flight_currency_entry_layout)
        flight_currency_layout.addWidget(self.flight_currency_details)

        ########## Input fields for optional search parameters

        # Trip Type
        
        self.flight_trip_round = QRadioButton("Round Trip")
        self.flight_trip_one = QRadioButton("One Way")
        self.flight_trip_multi = QRadioButton("Multi-city")

        self.flight_trip_round.clicked.connect(self.on_radio_button_toggled)
        self.flight_trip_one.clicked.connect(self.on_radio_button_toggled)
        self.flight_trip_multi.clicked.connect(self.on_radio_button_toggled)

        self.flight_trip_round.setChecked(True)
        self.flight_trip_one.setChecked(False)
        self.flight_trip_multi.setChecked(False)

        self.flight_trip_type = "Round Trip"

        flight_trip_layout = QVBoxLayout()
        flight_trip_layout.addWidget(QLabel("Trip Type"))
        flight_trip_layout.addWidget(self.flight_trip_round)
        # flight_trip_layout.addWidget(QLabel(" "))
        flight_trip_layout.addWidget(self.flight_trip_one)
        # flight_trip_layout.addWidget(QLabel(" "))
        flight_trip_layout.addWidget(self.flight_trip_multi)
        # flight_trip_layout.setSpacing(1)

        # Permit Layovers

        self.flight_exclude_layovers = QCheckBox("Layovers")

        flight_exclude_layout = QVBoxLayout()
        flight_exclude_layout.addWidget(QLabel("Exclude"))
        flight_exclude_layout.addWidget(self.flight_exclude_layovers)

        # Min and Max Flight Time

        self.flight_time_min_entry = QLineEdit(self)
        self.flight_time_min_entry.setPlaceholderText("-")

        flight_time_min_layout = QVBoxLayout()
        flight_time_min_layout.addWidget(QLabel("Min"))
        flight_time_min_layout.addWidget(self.flight_time_min_entry)

        self.flight_time_max_entry = QLineEdit(self)
        self.flight_time_max_entry.setPlaceholderText("-")

        flight_time_max_layout = QVBoxLayout()
        flight_time_max_layout.addWidget(QLabel("Max"))
        flight_time_max_layout.addWidget(self.flight_time_max_entry)

        flight_time_range_layout = QHBoxLayout()
        flight_time_range_layout.addLayout(flight_time_min_layout)
        flight_time_range_layout.addWidget(QLabel(" - "))
        flight_time_range_layout.addLayout(flight_time_max_layout)

        flight_time_layout = QVBoxLayout()
        flight_time_layout.addWidget(QLabel("Flight Time (min)"))
        flight_time_layout.addLayout(flight_time_range_layout)

        # Min and Max Cost

        self.flight_cost_min_entry = QLineEdit(self)
        self.flight_cost_min_entry.setPlaceholderText("-")

        flight_cost_min_layout = QVBoxLayout()
        flight_cost_min_layout.addWidget(QLabel("Min"))
        flight_cost_min_layout.addWidget(self.flight_cost_min_entry)

        self.flight_cost_max_entry = QLineEdit(self)
        self.flight_cost_max_entry.setPlaceholderText("-")

        flight_cost_max_layout = QVBoxLayout()
        flight_cost_max_layout.addWidget(QLabel("Max"))
        flight_cost_max_layout.addWidget(self.flight_cost_max_entry)

        flight_cost_range_layout = QHBoxLayout()
        flight_cost_range_layout.addLayout(flight_cost_min_layout)
        flight_cost_range_layout.addWidget(QLabel(" - "))
        flight_cost_range_layout.addLayout(flight_cost_max_layout)

        flight_cost_layout = QVBoxLayout()
        flight_cost_layout.addWidget(QLabel("Cost ($)"))
        flight_cost_layout.addLayout(flight_cost_range_layout)

        ########## Output for search results
        
        # Search button

        flight_search_button = QPushButton("Search Flights", self)
        flight_search_button.clicked.connect(self.on_search_clicked)
        
        # List widget for displaying departure flights
        
        self.flight_departure_token_list = []
        
        # Text edit for displaying flight details

        self.flight_details = QTextEdit(self)
        self.flight_details.setReadOnly(True)


        # Table widget for departure flight information

        departure_flight_table_columns = ["Airline", "Price", "Type", "Departure", "Dpt Date", "Arrival", "Arr Date", "Travel Class"]
        self.departure_flight_table_label = QLabel("Departure Flights")
        self.departure_flight_table = QTableWidget(self)
        self.departure_flight_table.setColumnCount(len(departure_flight_table_columns))
        self.departure_flight_table.setRowCount(1)
        for i in range(self.departure_flight_table.columnCount()):
            self.departure_flight_table.setItem(0 , i, QTableWidgetItem(departure_flight_table_columns[i]))
            self.departure_flight_table.item(0, i).setBackground(QColor(30,38,64))
        self.departure_flight_table.horizontalHeader().setVisible(False)
        self.departure_flight_table.verticalHeader().setVisible(False)
        self.departure_flight_table.cellClicked.connect(self.on_departure_flight_row_clicked)
        self.departure_flight_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.departure_flight_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.departure_flight_table.setShowGrid(False)
        self.departure_token = ""

        # Table widget for return flight information

        return_flight_table_columns = ["Airline", "Price", "Type", "Departure", "Dpt Date", "Arrival", "Arr Date", "Travel Class"]
        self.return_flight_table_label = QLabel("Return Flights")
        self.return_flight_table = QTableWidget(self)
        self.return_flight_table.setColumnCount(len(return_flight_table_columns))
        self.return_flight_table.setRowCount(1)
        for i in range(self.return_flight_table.columnCount()):
            self.return_flight_table.setItem(0 , i, QTableWidgetItem(return_flight_table_columns[i]))
            self.return_flight_table.item(0, i).setBackground(QColor(30,38,64))
        self.return_flight_table.horizontalHeader().setVisible(False)
        self.return_flight_table.verticalHeader().setVisible(False)
        self.return_flight_table.cellClicked.connect(self.on_return_flight_row_clicked)
        self.return_flight_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.return_flight_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.return_flight_table.setShowGrid(False)
        

        ########## Insert all data in layout

        airport_code_layout = QHBoxLayout()
        airport_code_layout.addLayout(flight_dep_airport_layout)
        airport_code_layout.addLayout(flight_arr_airport_layout)

        flight_date_layout = QHBoxLayout()
        flight_date_layout.addLayout(flight_out_date_layout)
        flight_date_layout.addLayout(flight_ret_date_layout)

        flight_code_and_date_layout = QHBoxLayout()
        flight_code_and_date_layout.addLayout(airport_code_layout)
        flight_code_and_date_layout.addLayout(flight_date_layout)
        
        flight_info_layout = QHBoxLayout()
        # flight_info_layout.addWidget(self.departure_flight_list)
        flight_info_layout.addWidget(self.flight_details)
        # self.departure_flight_list.setVisible(False)
        self.flight_details.setVisible(False)

        flight_left_panel_layout = QVBoxLayout()
        flight_left_panel_layout.addLayout(flight_trip_layout)
        flight_left_panel_layout.addWidget(QLabel(" "))
        flight_left_panel_layout.addLayout(flight_time_layout)
        flight_left_panel_layout.addWidget(QLabel(" "))
        flight_left_panel_layout.addLayout(flight_cost_layout)
        flight_left_panel_layout.addWidget(QLabel(" "))
        flight_left_panel_layout.addLayout(flight_currency_layout)
        flight_left_panel_layout.addWidget(QLabel(" "))
        flight_left_panel_layout.addLayout(flight_exclude_layout)
        flight_left_panel_layout.setSpacing(0)

        self.flight_left_panel = QFrame(self)
        self.flight_left_panel.setLayout(flight_left_panel_layout)
        self.flight_left_panel.setFixedWidth(200)
        self.flight_left_panel.setStyleSheet(QLABEL_LEFT)
        self.flight_left_panel.setFixedHeight(LEFT_PANEL_HEIGHT)


        flight_main_panel_layout = QVBoxLayout()
        flight_main_panel_layout.addLayout(flight_code_and_date_layout)
        flight_main_panel_layout.addWidget(flight_search_button)
        flight_main_panel_layout.addLayout(flight_info_layout)
        flight_main_panel_layout.addWidget(self.departure_flight_table_label)
        flight_main_panel_layout.addWidget(self.departure_flight_table)
        flight_main_panel_layout.addWidget(self.return_flight_table_label)
        flight_main_panel_layout.addWidget(self.return_flight_table)

        self.flight_main_panel = QFrame(self)
        self.flight_main_panel.setLayout(flight_main_panel_layout)

        flight_frame_layout = QHBoxLayout()
        flight_frame_layout.addWidget(self.flight_left_panel)
        flight_frame_layout.addWidget(self.flight_main_panel)

        self.flight_frame = QFrame(self)
        self.flight_frame.setLayout(flight_frame_layout)

        ##############################################################################################################
        #   END FLIGHT PAGE
        ##############################################################################################################

        ##############################################################################################################
        #   BEGIN HOTEL PAGE
        ##############################################################################################################

        self.hotel_temp_page = QLabel("THIS IS THE HOTEL PAGE")

        self.hotel_location_entry = QLineEdit(self)
        self.hotel_location_entry.setPlaceholderText("Hotel Location")

        hotel_location_layout = QVBoxLayout()
        hotel_location_layout.addWidget(QLabel("Location:"))
        hotel_location_layout.addWidget(self.hotel_location_entry)
        
            # Check-In Date parameter
        self.hotel_in_date_entry = QDateTimeEdit(self)
        self.hotel_in_date_entry.setCalendarPopup(True)
        self.hotel_in_date_entry.setDate(QDate.currentDate())
        self.hotel_in_date_entry.setDisplayFormat('yyyy-MM-dd')

                # Parameter layout
        hotel_in_date_layout = QVBoxLayout()
        hotel_in_date_layout.addWidget(QLabel("Check-In Date:"))
        hotel_in_date_layout.addWidget(self.hotel_in_date_entry)

            # Check-Out Date parameter
        self.hotel_out_date_entry = QDateTimeEdit(self)
        self.hotel_out_date_entry.setCalendarPopup(True)
        self.hotel_out_date_entry.setDate(QDate.currentDate())
        self.hotel_out_date_entry.setDisplayFormat('yyyy-MM-dd')
        # self.flight_return_date_entry.setEnabled(False)

                # Parameter Layout
        hotel_out_date_layout = QVBoxLayout()
        hotel_out_date_layout.addWidget(QLabel("Check-Out Date:"))
        hotel_out_date_layout.addWidget(self.hotel_out_date_entry)

        hotel_date_layout = QHBoxLayout()
        hotel_date_layout.addLayout(hotel_in_date_layout)
        hotel_date_layout.addLayout(hotel_out_date_layout)

        hotel_loc_and_date_layout = QHBoxLayout()
        hotel_loc_and_date_layout.addLayout(hotel_location_layout)
        hotel_loc_and_date_layout.addLayout(hotel_date_layout)

            # Currency parameter
        self.hotel_currency_entry = QComboBox(self)
        self.hotel_currency_entry.addItems(self.all_currencies.keys())
        self.hotel_currency_entry.setCurrentText('USD')

                # Parameter Layout
        hotel_currency_entry_layout = QVBoxLayout()
        hotel_currency_entry_layout.addWidget(QLabel("Currency:"))
        hotel_currency_entry_layout.addWidget(self.hotel_currency_entry)

            # Min and Max Cost Time
        self.hotel_cost_min_entry = QLineEdit(self)
        self.hotel_cost_min_entry.setPlaceholderText("-")

        hotel_cost_min_layout = QVBoxLayout()
        hotel_cost_min_layout.addWidget(QLabel("Min"))
        hotel_cost_min_layout.addWidget(self.hotel_cost_min_entry)

        self.hotel_cost_max_entry = QLineEdit(self)
        self.hotel_cost_max_entry.setPlaceholderText("-")

        hotel_cost_max_layout = QVBoxLayout()
        hotel_cost_max_layout.addWidget(QLabel("Max"))
        hotel_cost_max_layout.addWidget(self.hotel_cost_max_entry)

        hotel_cost_range_layout = QHBoxLayout()
        hotel_cost_range_layout.addLayout(hotel_cost_min_layout)
        hotel_cost_range_layout.addWidget(QLabel(" - "))
        hotel_cost_range_layout.addLayout(hotel_cost_max_layout)

        hotel_cost_layout = QVBoxLayout()
        hotel_cost_layout.addWidget(QLabel("Cost ($)"))
        hotel_cost_layout.addLayout(hotel_cost_range_layout)

            # Min and Max Ratings
        self.hotel_rating_min_entry = QLineEdit(self)
        self.hotel_rating_min_entry.setPlaceholderText("-")

        hotel_rating_min_layout = QVBoxLayout()
        hotel_rating_min_layout.addWidget(QLabel("Min"))
        hotel_rating_min_layout.addWidget(self.hotel_rating_min_entry)

        self.hotel_rating_max_entry = QLineEdit(self)
        self.hotel_rating_max_entry.setPlaceholderText("-")

        hotel_rating_max_layout = QVBoxLayout()
        hotel_rating_max_layout.addWidget(QLabel("Max"))
        hotel_rating_max_layout.addWidget(self.hotel_rating_max_entry)

        hotel_rating_range_layout = QHBoxLayout()
        hotel_rating_range_layout.addLayout(hotel_rating_min_layout)
        hotel_rating_range_layout.addWidget(QLabel(" - "))
        hotel_rating_range_layout.addLayout(hotel_rating_max_layout)

        hotel_rating_layout = QVBoxLayout()
        hotel_rating_layout.addWidget(QLabel("Rating"))
        hotel_rating_layout.addLayout(hotel_rating_range_layout)

        self.hotel_amenities = []

        hotel_search_button = QPushButton("Search Hotels", self)
        # hotel_search_button.clicked.connect(self.on_search_clicked)

        hotel_table_columns = ["Name", "Price per Night", "Total Price", "Rating", "Address", "Amenities", "Thumbnail"]
        self.hotel_table_label = QLabel("Hotels")
        self.hotel_table = QTableWidget(self)
        self.hotel_table.setColumnCount(len(hotel_table_columns))
        self.hotel_table.setRowCount(1)
        for i in range(self.hotel_table.columnCount()):
            self.hotel_table.setItem(0 , i, QTableWidgetItem(hotel_table_columns[i]))
            self.hotel_table.item(0, i).setBackground(QColor(30,38,64))
        self.hotel_table.horizontalHeader().setVisible(False)
        self.hotel_table.verticalHeader().setVisible(False)
        # self.hotel_table.cellClicked.connect()
        self.hotel_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.hotel_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.hotel_table.setShowGrid(False)

        hotel_table_layout = QVBoxLayout()
        hotel_table_layout.addWidget(self.hotel_table)
        hotel_table_layout.addWidget(self.hotel_table_label)

        hotel_left_panel_layout = QVBoxLayout()
        hotel_left_panel_layout.addLayout(hotel_cost_layout)
        hotel_left_panel_layout.addWidget(QLabel(" "))
        hotel_left_panel_layout.addLayout(hotel_rating_layout)
        hotel_left_panel_layout.addWidget(QLabel(" "))
        hotel_left_panel_layout.addLayout(hotel_currency_entry_layout)
        hotel_left_panel_layout.addWidget(QLabel(" "))
        hotel_left_panel_layout.setSpacing(0)

        self.hotel_left_panel = QFrame(self)
        self.hotel_left_panel.setLayout(hotel_left_panel_layout)
        self.hotel_left_panel.setFixedWidth(200)
        self.hotel_left_panel.setStyleSheet(QLABEL_LEFT)
        self.hotel_left_panel.setFixedHeight(LEFT_PANEL_HEIGHT)

        hotel_main_panel_layout = QVBoxLayout()
        hotel_main_panel_layout.addWidget(self.hotel_temp_page)
        hotel_main_panel_layout.addLayout(hotel_loc_and_date_layout)
        hotel_main_panel_layout.addWidget(hotel_search_button)
        hotel_main_panel_layout.addLayout(hotel_table_layout)

        self.hotel_main_panel = QFrame(self)
        self.hotel_main_panel.setLayout(hotel_main_panel_layout)

        hotel_frame_layout = QHBoxLayout()
        hotel_frame_layout.addWidget(self.hotel_left_panel)
        hotel_frame_layout.addWidget(self.hotel_main_panel)

        self.hotel_frame = QFrame(self)
        self.hotel_frame.setLayout(hotel_frame_layout)
        self.hotel_frame.setVisible(False)

        ##############################################################################################################
        #   END HOTEL PAGE
        ##############################################################################################################

        ##############################################################################################################
        #   BEGIN PAGE INSERTION
        ##############################################################################################################

        logo_label = QLabel(self)
        logo_label.setPixmap(QPixmap("logo.png")) #.scaled(10, 20, Qt.KeepAspectRatio))
        logo_label.setFixedWidth(100)
        logo_label.setFixedHeight(100)
        logo_label.setScaledContents(True)
        logo_label.setStyleSheet(QLABEL_ICON)

        logo_title = QLabel("FAIRFARE")
        logo_title.setStyleSheet(QLABEL_TITLE)

        logo_panel_layout = QHBoxLayout()
        logo_panel_layout.setAlignment(Qt.AlignCenter)
        logo_panel_layout.addWidget(logo_label)
        logo_panel_layout.addWidget(logo_title)

        self.logo_panel = QFrame(self)
        self.logo_panel.setLayout(logo_panel_layout)

        
        self.flight_menu_button = QPushButton("Flights")
        self.flight_menu_button.clicked.connect(self.on_menu_button_clicked)
        self.hotel_menu_button = QPushButton("Hotels")
        self.hotel_menu_button.clicked.connect(self.on_menu_button_clicked)

        menu_frame_layout = QHBoxLayout()
        menu_frame_layout.addWidget(self.flight_menu_button)
        menu_frame_layout.addWidget(self.hotel_menu_button)

        self.menu_frame = QFrame(self)
        self.menu_frame.setLayout(menu_frame_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.logo_panel)

        layout.addWidget(self.menu_frame)
        layout.addWidget(self.flight_frame)
        layout.addWidget(self.hotel_frame)

        layout.addWidget(QLabel("THIS IS A TEST"))
        self.setLayout(layout)

    def on_search_clicked(self):
        # Clear previous search results
        # self.departure_flight_list.clear()
        self.flight_departure_token_list = []
        self.departure_token = ""
        self.flight_details.clear()

        for i in range(1, self.departure_flight_table.rowCount()):
                self.departure_flight_table.removeRow(1)

        for i in range(1, self.return_flight_table.rowCount()):
                self.return_flight_table.removeRow(1)

        if self.flight_trip_type == "Round Trip":
            self.return_flight_table.setVisible(True)
            self.return_flight_table_label.setVisible(True)
        else:
            self.return_flight_table.setVisible(False)
            self.return_flight_table_label.setVisible(False)

        # Retrieve input values
        departure_id = self.flight_departure_entry.text().upper()
        arrival_id = self.flight_arrival_entry.text().upper()
        departure_date = self.flight_departure_date_entry.text()
        return_date = self.flight_return_date_entry.text()
        currency = self.flight_currency_entry.currentText()
        max_cost = None if self.flight_cost_max_entry.text() == "" else self.flight_cost_max_entry.text()  # Optional max cost input
        min_time = None if self.flight_time_min_entry.text() == "" else self.flight_time_min_entry.text() # Optional minimum time input
        max_time = None if self.flight_time_max_entry.text() == "" else self.flight_time_max_entry.text() # Optional maximum time input

        # # Check for required fields
        # if not all([departure_id, arrival_id, departure_date, return_date, currency]):
        #     QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
        #     return
            
        # Check date validity
        if self.flight_return_date_entry.dateTime() < self.flight_departure_date_entry.dateTime():
            QMessageBox.warning(self, "Input Error", "Please ensure return date is not before departure date.")
            return

        # Check cost validity
        if (not self.flight_cost_min_entry.text().isnumeric() and self.flight_cost_min_entry.text())\
            or\
            (not self.flight_cost_max_entry.text().isnumeric() and self.flight_cost_max_entry.text()):
            QMessageBox.warning(self, "Input Error", "Please ensure costs are numeric values.")
            return

        # Check time validity
        if (not self.flight_time_min_entry.text().isnumeric() and self.flight_time_min_entry.text())\
            or\
            (not self.flight_time_max_entry.text().isnumeric() and self.flight_time_max_entry.text()):
            QMessageBox.warning(self, "Input Error", "Please ensure flight times are numeric values.")
            return

        # Check for required fields
        if not all([departure_id, arrival_id, departure_date, return_date, currency]):
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return

        # Get flight data with optional parameters
        flight_data = search_flights(
            departure_id, arrival_id, departure_date, return_date, currency,
            max_price=max_cost if max_cost else None,
            min_time=min_time if min_time else None,
            max_time=max_time if max_time else None,
            departure_token = None
        )

        # Handle no results or errors
        if not flight_data or isinstance(flight_data, str):
            QMessageBox.information(self, "No Results", str(flight_data) if flight_data else "No flights found.")
            return

        # Display flight options in the list

        for flight in flight_data:
            pprint(flight)
            self.flight_departure_token_list.append(flight['departure_token'])

            # Add flight information into the table ["Airline", "Price", "Type", "Departure", "Arrival", "Travel Class"]
            format_string = "%Y-%m-%d %H:%M"
            rowPosition = self.departure_flight_table.rowCount()
            self.departure_flight_table.insertRow(rowPosition)
            self.departure_flight_table.setItem(rowPosition , 0, QTableWidgetItem(flight['flights'][0]['airline']))
            self.departure_flight_table.setItem(rowPosition , 1, QTableWidgetItem("$" + str(flight['price'])))
            self.departure_flight_table.setItem(rowPosition , 2, QTableWidgetItem(flight['type']))
            self.departure_flight_table.setItem(rowPosition , 3, QTableWidgetItem(self.time_to_12(flight['flights'][0]['departure_time'])))
            self.departure_flight_table.setItem(rowPosition , 4, QTableWidgetItem(self.date_to_mmm(flight['flights'][0]['departure_time'])))
            self.departure_flight_table.setItem(rowPosition , 5, QTableWidgetItem(self.time_to_12(flight['flights'][-1]['arrival_time'])))
            self.departure_flight_table.setItem(rowPosition , 6, QTableWidgetItem(self.date_to_mmm(flight['flights'][0]['arrival_time'])))
            self.departure_flight_table.setItem(rowPosition , 7, QTableWidgetItem(flight['flights'][0]['travel_class']))

        # Save the flight data to display when an item is selected
        self.current_flight_data = flight_data

    def on_hotel_search_clicked(self):

        # Retrieve input values
        # location = self.hotel_location_entry.text().upper()
        # check_in_date = self.hotel_in_date_entry.text().upper()
        # check_out_date = self.hotel_out_date_entry.text()
        # currency = self.hotel_currency_entry.currentText()
        # max_price = None if self.hotel_cost_max_entry.text() == "-" else self.hotel_cost_max_entry.text()  # Optional maximum price input
        # min_price = None if self.hotel_cost_min_entry.text() == "-" else self.hotel_cost_min_entry.text() # Optional minimum price input
        # min_rating = None if self.hotel_rating_min_entry.text() == "-" else self.hotel_rating_min_entry.text() # Optional minimum rating input
        # amenities = None if self.hotel_amenities == [] else self.hotel_amenities # Optional amenities input

        # Check for required fields
        # if not all([departure_id, arrival_id, departure_date, return_date, currency]):
        #     QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
        #     return

        # # Check date validity
        # if self.hotel_in_date_entry.dateTime() < self.hotel_out_date_entry.dateTime():
        #     QMessageBox.warning(self, "Input Error", "Please ensure return date is not before departure date.")
        #     return

        # Get hotel data with optional parameters
        # flight_data = search_hotels(
        #     location, check_in_date, check_out_date, 
        #     currency="USD", 
        #     max_price=None, 
        #     min_price=None, 
        #     min_rating=None, 
        #     amenities=None
        # )
        pass

    def on_departure_date_calendar_clicked(self):
    # Toggle calendar widget once clicked
        self.flight_departure_date_entry.setText(self.departure_date_calendar.selectedDate().toString())
        self.flight_departure_date_calendar.setVisible(False)

    def on_return_date_calendar_clicked(self):
    # Toggle calendar widget once clicked
        self.flight_return_date_entry.setText(self.return_date_calendar.selectedDate().toString())
        self.flight_return_date_calendar.setVisible(False)

    def on_radio_button_toggled(self):
        radio_button = self.sender()
        if radio_button == self.flight_trip_round:
            self.flight_return_date_entry.setEnabled(True)
            self.flight_return_date_entry.setVisible(True)
            self.flight_ret_date_label.setVisible(True)

            self.return_flight_table.setVisible(True)
            self.return_flight_table_label.setVisible(True)
        else:
            self.flight_return_date_entry.setEnabled(False)
            self.flight_return_date_entry.setVisible(False)
            self.flight_ret_date_label.setVisible(False)

            self.return_flight_table.setVisible(False)
            self.return_flight_table_label.setVisible(False)
        self.flight_trip_type = radio_button.text()

    def on_menu_button_clicked(self):
        push_button = self.sender()
        if push_button == self.flight_menu_button:
            self.hotel_frame.setVisible(False)
            self.flight_frame.setVisible(True)

        if push_button == self.hotel_menu_button:
            self.flight_frame.setVisible(False)
            self.hotel_frame.setVisible(True)

    def get_all_airports(self):
    # Get all airport abbreviations and names
        try:
            r = requests.get("https://www.bts.gov/topics/airlines-and-airports/world-airport-codes")
            soup = BeautifulSoup(r.text, "html.parser")
            table = soup.find('tbody')
            rows = table.find_all('tr')
            self.all_airports = {i.find_all('td')[0].text : {'City':i.find_all('td')[1].text.split(': ')[0], 'Airport':i.find_all('td')[1].text.split(': ')[0]} for i in rows}
            # print(self.all_airports)
        except:
            print("No airports found.")

    def on_return_flight_row_clicked(self, row, column):
        if row > 0:
            self.return_flight_table.selectRow(row)

    def on_departure_flight_row_clicked(self, row, column):
        if row > 0:
            self.departure_flight_table.selectRow(row)
            # print(self.flight_departure_token_list)
            self.departure_token = self.flight_departure_token_list[row - 1]

            print(self.flight_departure_token_list)
            print(self.departure_token)
            pprint("===============RETURN FLIGHTS==================")

            ###################################################################################################################
            # RETURN FLIGHT INFORMATION
            ###################################################################################################################
            if self.flight_trip_type == "Round Trip" and self.departure_token != "":
                # Clear previous search results
                for i in range(1, self.return_flight_table.rowCount()):
                    self.return_flight_table.removeRow(1)

                # Retrieve input values
                departure_id = self.flight_departure_entry.text().upper()
                arrival_id = self.flight_arrival_entry.text().upper()
                departure_date = self.flight_departure_date_entry.text()
                return_date = self.flight_return_date_entry.text()
                currency = self.flight_currency_entry.currentText()
                max_cost = None if self.flight_cost_max_entry.text() == "" else self.flight_cost_max_entry.text()  # Optional max cost input
                min_time = None if self.flight_time_min_entry.text() == "" else self.flight_time_min_entry.text() # Optional minimum time input
                max_time = None if self.flight_time_max_entry.text() == "" else self.flight_time_max_entry.text() # Optional maximum time input
                departure_token = self.departure_token
                print(departure_token)

                self.return_flight_table.setShowGrid(False)

                # # Check for required fields
                # if not all([departure_id, arrival_id, departure_date, return_date, currency]):
                #     QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
                #     return
                    
                # Check date validity
                if self.flight_return_date_entry.dateTime() < self.flight_departure_date_entry.dateTime():
                    QMessageBox.warning(self, "Input Error", "Please ensure return date is not before departure date.")
                    return

                # Check cost validity
                if (not self.flight_cost_min_entry.text().isnumeric() and self.flight_cost_min_entry.text())\
                    or\
                    (not self.flight_cost_max_entry.text().isnumeric() and self.flight_cost_max_entry.text()):
                    QMessageBox.warning(self, "Input Error", "Please ensure costs are numeric values.")
                    return

                # Check time validity
                if (not self.flight_time_min_entry.text().isnumeric() and self.flight_time_min_entry.text())\
                    or\
                    (not self.flight_time_max_entry.text().isnumeric() and self.flight_time_max_entry.text()):
                    QMessageBox.warning(self, "Input Error", "Please ensure flight times are numeric values.")
                    return

                # Check for required fields
                if not all([departure_id, arrival_id, departure_date, return_date, currency]):
                    QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
                    return

                # Get flight data with optional parameters
                flight_data = search_flights(
                    departure_id, arrival_id, departure_date, return_date, currency,
                    max_price=max_cost if max_cost else None,
                    min_time=min_time if min_time else None,
                    max_time=max_time if max_time else None,
                    departure_token=departure_token
                )

                # Handle no results or errors
                if not flight_data or isinstance(flight_data, str):
                    QMessageBox.information(self, "No Results", str(flight_data) if flight_data else "No flights found.")
                    return

                # Display flight options in the list

                for flight in flight_data:
                    pprint(flight)

                    # Add flight information into the table ["Airline", "Price", "Type", "Departure", "Arrival", "Travel Class"]
                    format_string = "%Y-%m-%d %H:%M"
                    rowPosition = self.return_flight_table.rowCount()
                    self.return_flight_table.insertRow(rowPosition)
                    self.return_flight_table.setItem(rowPosition , 0, QTableWidgetItem(flight['flights'][0]['airline']))
                    self.return_flight_table.setItem(rowPosition , 1, QTableWidgetItem("$" + str(flight['price'])))
                    self.return_flight_table.setItem(rowPosition , 2, QTableWidgetItem(flight['type']))
                    self.return_flight_table.setItem(rowPosition , 3, QTableWidgetItem(self.time_to_12(flight['flights'][0]['departure_time'])))
                    self.return_flight_table.setItem(rowPosition , 4, QTableWidgetItem(self.date_to_mmm(flight['flights'][0]['departure_time'])))
                    self.return_flight_table.setItem(rowPosition , 5, QTableWidgetItem(self.time_to_12(flight['flights'][-1]['arrival_time'])))
                    self.return_flight_table.setItem(rowPosition , 6, QTableWidgetItem(self.date_to_mmm(flight['flights'][0]['arrival_time'])))
                    self.return_flight_table.setItem(rowPosition , 7, QTableWidgetItem(flight['flights'][0]['travel_class']))

            else:
                print("Not a round trip.")

            # Save the flight data to display when an item is selected
            # self.current_flight_data = flight_data

        ###################################################################################################################
        ###################################################################################################################


    def time_to_12(self, time):
        return "12:" + time.split(" ")[-1].split(":")[1] + " PM" \
            if int(time.split(" ")[-1].split(":")[0]) == 12 \
            else "12:" + time.split(" ")[-1].split(":")[1] + " AM" \
            if int(time.split(" ")[-1].split(":")[0]) == 24 \
            else time.split(" ")[-1].split(":")[0].lstrip("0") + ":" + time.split(" ")[-1].split(":")[1] + " AM" \
            if int(time.split(" ")[-1].split(":")[0]) < 12 \
            else str(int(time.split(" ")[-1].split(":")[0]) % 12).lstrip("0") + ":" + time.split(" ")[-1].split(":")[1] + " PM" \

    def date_to_mmm(self, date):
        months = {"1":"Jan", "2":"Feb", "3":"Mar", "4":"Apr", "5":"May", "6":"Jun", "7":"Jul", "8":"Aug", "9":"Sep", "10":"Oct", "11":"Nov", "12":"Dec"}
        return months[date.split(" ")[0].split("-")[1]] + " " + date.split(" ")[0].split("-")[2] + ", " + date.split(" ")[0].split("-")[0]

    def display_flight_details(self, item):
    # Get index of the selected item
        # index = self.departure_flight_list.row(item)

        if index != 0:

            # Get the corresponding flight details
            flight = self.current_flight_data[index]
            flight_text = f"Price: ${flight['price']}\nType: {flight['type']}\nDuration: {flight['total_duration']} min\n\n"

            for leg in flight['flights']:
                # Assuming 'departure_airport' and 'arrival_airport' are strings
                flight_text += (
                    f"Flight {leg['flight_number']} ({leg['airline']})\n"
                    f"  Departure: {leg['departure_airport']} at {leg['departure_time']}\n"
                    f"  Arrival: {leg['arrival_airport']} at {leg['arrival_time']}\n"
                    f"  Duration: {leg['duration']} min\n\n"
                )

            self.flight_details.setText(flight_text)
            # self.right_panel.setVisible(True)
            # self.right_panel.setText(flight_text)

            # self.rightpane.addItem


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlightSearchApp()
    window.show()
    sys.exit(app.exec_())
