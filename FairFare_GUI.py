import sys

import time

from qrangeslider import QRangeSlider

from pprint import pprint

from PyQt5.QtWidgets import (
	QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QRadioButton, QTableWidget, QHeaderView,
	QListWidget, QTextEdit, QMessageBox, QDateTimeEdit, QComboBox, QHBoxLayout, QAbstractItemView, QFrame, QTableWidgetItem,
	QButtonGroup, QSlider
)
from PyQt5.QtCore import (
	QDate, Qt
)
from PyQt5.QtGui import (
	QPixmap, QFont, QColor
)
from Google_Flights_Scraper import search_flights  # Import the flight search function
from Google_Hotel_Scraper import search_hotels
from distance_calc import calculate_distance

import requests
import json
from bs4 import BeautifulSoup
from pprint import pprint
import re
from datetime import datetime

import pandas as pd
import numpy as np

# Stylesheet information for GUI layout

GUI_HEIGHT = 910
GUI_WIDTH = 1600
GUI_PANEL_WIDTH = 300
LEFT_PANEL_HEIGHT = 700
LEFT_PANEL_WIDTH = 300

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
				QCalendarWidget QSpinBox{background-color: #343f62;}\
				QToolTip{color: black ; font: 16pt}"  
QLABEL_PANEL = "QLabel {height: 40; font: 'Noto Serif'; font-size: 16pt; text-align: left; qproperty-alignment: AlignCenter; background: #343f62; color: #ffffff;}"
QLABEL_ICON = "QLabel {qproperty-alignment: AlignCenter; border: 0px outset #696969; width: 10; height: 10;}"
QLABEL_TITLE = "QLabel {width: 30; height: 30; font: 'Noto Serif'; font-size: 45pt; text-align: center; qproperty-alignment: AlignCenter; background: #343f62; color: #ffffff; font-weight: bold; font-style: italic;}"
QLABEL_LEFT = "QWidget {text-align: center; qproperty-alignment: AlignTop;} \
			   QLabel {text-align: center; qproperty-alignment: AlignCenter;}\
			   QLineEdit {text-align: center; qproperty-alignment: AlignCenter;}\
			   QRadioButton {text-align: center; qproperty-alignment: AlignTop;}\
				"




# SERP_API_KEY = "b637153e8613b18fc81533dfbf72045c9b43cbdd25323736bc3009ee6c38435a"  
# SERP_API_KEY = "8e3b97559f70aeb1a2d6f78da4ca024bab7525e316361ac1c955016a16136cf7"
SERP_API_KEY = "a9deee9173656ca6302d2fed79e2b999494e4e0bcd7d177aad40ea88be63aa17"

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
		self.showMaximized()

		app.setStyleSheet(QT_GUI)

		# Get list of all airport codes and locations

		self.get_all_airports()

		self.all_currencies = json.load(open("google-travel-currencies.json"))
		self.all_countries = json.load(open("google-countries.json"))

		##############################################################################################################
		#   BEGIN WELCOME PAGE
		##############################################################################################################

		self.welcome_start_button = QPushButton("Get Started")
		self.welcome_start_button.clicked.connect(self.on_start_button_clicked)
		self.welcome_start_button.setFixedWidth(400)
		self.welcome_start_button.setFixedHeight(100)

		##############################################################################################################
		#   END WELCOME PAGE
		##############################################################################################################



		##############################################################################################################
		#   BEGIN FLIGHT PAGE
		##############################################################################################################

		########## Input fields for search parameters

		self.current_dep_flight_data = None
		self.current_ret_flight_data = None
		self.current_hotel_data = None

		self.current_dep_flight = None
		self.current_ret_flight = None
		self.current_hotel = None

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
		self.flight_departure_date_entry.dateTimeChanged.connect(self.on_departure_date_calendar_date_changed)

				# Parameter layout
		flight_out_date_layout = QVBoxLayout()
		flight_out_date_layout.addWidget(QLabel("Departure Date:"))
		flight_out_date_layout.addWidget(self.flight_departure_date_entry)

			# Return Date parameter
		self.flight_return_date_entry = QDateTimeEdit(self)
		self.flight_return_date_entry.setCalendarPopup(True)
		self.flight_return_date_entry.setDate(QDate.currentDate())
		self.flight_return_date_entry.setDisplayFormat('yyyy-MM-dd')
		self.flight_return_date_entry.dateTimeChanged.connect( lambda: self.hotel_out_date_entry.setDateTime(self.flight_return_date_entry.dateTime()))
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
		# self.flight_trip_multi = QRadioButton("Multi-city")

		self.flight_trip_round.clicked.connect(self.on_radio_button_toggled)
		self.flight_trip_one.clicked.connect(self.on_radio_button_toggled)
		# self.flight_trip_multi.clicked.connect(self.on_radio_button_toggled)

		self.flight_trip_round.setChecked(True)
		self.flight_trip_one.setChecked(False)
		# self.flight_trip_multi.setChecked(False)

		self.flight_trip_type = "Round Trip"

		flight_trip_layout = QVBoxLayout()
		flight_trip_layout.addWidget(QLabel("Trip Type"))
		flight_trip_layout.addWidget(self.flight_trip_round)
		# flight_trip_layout.addWidget(QLabel(" "))
		flight_trip_layout.addWidget(self.flight_trip_one)
		# flight_trip_layout.addWidget(QLabel(" "))
		# flight_trip_layout.addWidget(self.flight_trip_multi)
		# flight_trip_layout.setSpacing(1)

		# Permit Layovers

		# self.flight_exclude_layovers = QCheckBox("Layovers")

		# flight_exclude_layout = QVBoxLayout()
		# flight_exclude_layout.addWidget(QLabel("Exclude"))
		# flight_exclude_layout.addWidget(self.flight_exclude_layovers)

		# Min and Max Flight Time

		self.flight_time_min_entry = QLineEdit(self)
		self.flight_time_min_entry.setPlaceholderText("-")

		flight_time_min_layout = QVBoxLayout()
		# flight_time_min_layout.addWidget(QLabel("Min"))
		flight_time_min_layout.addWidget(self.flight_time_min_entry)

		self.flight_time_max_entry = QLineEdit(self)
		self.flight_time_max_entry.setPlaceholderText("-")

		flight_time_max_layout = QVBoxLayout()
		# flight_time_max_layout.addWidget(QLabel("Max"))
		flight_time_max_layout.addWidget(self.flight_time_max_entry)

		flight_time_range_layout = QHBoxLayout()
		flight_time_range_layout.addLayout(flight_time_min_layout)
		# flight_time_range_layout.addWidget(QLabel(" - "))
		flight_time_range_layout.addLayout(flight_time_max_layout)

		flight_time_layout = QVBoxLayout()
		# flight_time_layout.addWidget(QLabel("Flight Time (min)"))
		flight_time_layout.addLayout(flight_time_range_layout)

		# Min and Max Cost

		self.flight_cost_min_entry = QLineEdit(self)
		self.flight_cost_min_entry.setPlaceholderText("-")

		flight_cost_min_layout = QVBoxLayout()
		# flight_cost_min_layout.addWidget(QLabel("Min"))
		flight_cost_min_layout.addWidget(self.flight_cost_min_entry)

		self.flight_cost_max_entry = QLineEdit(self)
		self.flight_cost_max_entry.setPlaceholderText("-")

		flight_cost_max_layout = QVBoxLayout()
		# flight_cost_max_layout.addWidget(QLabel("Max"))
		flight_cost_max_layout.addWidget(self.flight_cost_max_entry)

		flight_cost_range_layout = QHBoxLayout()
		flight_cost_range_layout.addLayout(flight_cost_min_layout)
		# flight_cost_range_layout.addWidget(QLabel(" - "))
		flight_cost_range_layout.addLayout(flight_cost_max_layout)

		flight_cost_layout = QVBoxLayout()
		# flight_cost_layout.addWidget(QLabel("Cost ($)"))
		flight_cost_layout.addLayout(flight_cost_range_layout)

		########## DISABLING FLIGHT TIME MIN/MAX AND COST MIN/MAX
		self.flight_time_min_entry.setVisible(False)
		self.flight_time_max_entry.setVisible(False)
		self.flight_cost_min_entry.setVisible(False)
		self.flight_cost_max_entry.setVisible(False)

			# Leg Priority
		self.flight_leg_box_1 = QCheckBox("Nonstop only")
		self.flight_leg_box_2 = QCheckBox("1 or less connecting flights")
		self.flight_leg_box_3 = QCheckBox("2 or less connecting flights")

		self.flight_leg_box_1.toggled.connect(self.on_leg_box_button_toggled)
		self.flight_leg_box_2.toggled.connect(self.on_leg_box_button_toggled)
		self.flight_leg_box_3.toggled.connect(self.on_leg_box_button_toggled)

		flight_leg_layout = QVBoxLayout()
		flight_leg_layout.addWidget(QLabel("Layovers"))
		flight_leg_layout.addWidget(self.flight_leg_box_1)
		flight_leg_layout.addWidget(self.flight_leg_box_2)
		flight_leg_layout.addWidget(self.flight_leg_box_3)

			# Departure Time Priority
		self.flight_time_box_1 = QCheckBox("Early 12am-8am")
		self.flight_time_box_2 = QCheckBox("Mid-day 8am-4pm")
		self.flight_time_box_3 = QCheckBox("Late 4pm-12am")

		self.flight_time_box_1.toggled.connect(self.on_time_box_button_toggled)
		self.flight_time_box_2.toggled.connect(self.on_time_box_button_toggled)
		self.flight_time_box_3.toggled.connect(self.on_time_box_button_toggled)

		flight_time_layout = QVBoxLayout()
		flight_time_layout.addWidget(QLabel("Departure Time"))
		flight_time_layout.addWidget(self.flight_time_box_1)
		flight_time_layout.addWidget(self.flight_time_box_2)
		flight_time_layout.addWidget(self.flight_time_box_3)

			# Ranking Input
		self.flight_rank_leg = QComboBox(self)
		self.flight_rank_leg.setToolTip("1 - Most Important, 2 - Least Important")
		self.flight_rank_leg.addItems(['1','2'])
		self.flight_rank_leg.setCurrentText('1')

		self.flight_rank_time = QComboBox(self)
		self.flight_rank_time.setToolTip("1 - Most Important, 2 - Least Important")
		self.flight_rank_time.addItems(['1','2'])
		self.flight_rank_time.setCurrentText('1')

		flight_rank_layout_leg = QHBoxLayout()
		flight_rank_layout_leg.addWidget(QLabel("Layovers \t"))
		flight_rank_layout_leg.addWidget(self.flight_rank_leg)

		flight_rank_layout_time = QHBoxLayout()
		flight_rank_layout_time.addWidget(QLabel("Departure\t"))
		flight_rank_layout_time.addWidget(self.flight_rank_time)

		flight_rank_options_layout = QVBoxLayout()
		flight_rank_options_layout.addLayout(flight_rank_layout_leg)
		# hotel_rank_layout.addWidget(QLabel(" "))
		flight_rank_options_layout.addLayout(flight_rank_layout_time)

		self.flight_rank_options_frame = QFrame(self)
		self.flight_rank_options_frame.setLayout(flight_rank_options_layout)
		self.flight_rank_options_frame.setVisible(False)

		self.flight_rank_button = QPushButton("Priorities")
		self.flight_rank_button.setToolTip("Rank your filter priorities")
		self.flight_rank_button.clicked.connect(lambda: self.flight_rank_options_frame.setVisible(not self.flight_rank_options_frame.isVisible()))

		flight_rank_layout = QHBoxLayout()
		flight_rank_layout.addWidget(self.flight_rank_button)
		flight_rank_layout.addWidget(self.flight_rank_options_frame)	


		########## Output for search results
		
		# Search button

		flight_search_button = QPushButton("Search Flights", self)
		flight_search_button.clicked.connect(self.on_search_clicked)


		# Table widget for departure flight information

		departure_flight_table_columns = ["Airline", "Price", "Type", "Departure", "Dpt Date", "Arrival", "Arr Date", "Travel Class"]
		self.departure_flight_table_label = QLabel("Departure Flights")
		self.departure_flight_table_button = QPushButton("Select Flight")
		self.departure_flight_table_button.clicked.connect(self.on_departure_flight_select_clicked)
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
		self.departure_flight_table.setWordWrap(True)


		flight_details = \
			f'\
Airline:\t\t \n\
Price:\t\t \n\
Type:\t\t \n\
Departure:\t \n\
Arrival:\t\t \n\
Class:\t\t \n\
Layover Flights:\t \
'
		self.dep_flight_table_details_label = QLabel("Departure Flight Details")
		self.dep_flight_table_details = QLabel(flight_details)
		self.dep_flight_table_details.setStyleSheet("QLabel {text-align: left; qproperty-alignment: AlignLeft;}")
		self.dep_flight_table_details.setFixedWidth(350)

		self.ret_flight_table_details_label = QLabel("Return Flight Details")
		self.ret_flight_table_details = QLabel(flight_details)
		self.ret_flight_table_details.setStyleSheet("QLabel {text-align: left; qproperty-alignment: AlignLeft;}")
		self.ret_flight_table_details.setFixedWidth(350)

		self.departure_token = ""

		# Table widget for return flight information

		return_flight_table_columns = ["Airline", "Price", "Type", "Departure", "Dpt Date", "Arrival", "Arr Date", "Travel Class"]
		self.return_flight_table_label = QLabel("Return Flights")
		self.return_flight_table_button = QPushButton("Select Flight")
		self.return_flight_table_button.clicked.connect(self.on_return_flight_select_clicked)
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
		self.return_flight_table.setWordWrap(True)
		

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
		
		# flight_info_layout = QHBoxLayout()
		# # flight_info_layout.addWidget(self.departure_flight_list)
		# flight_info_layout.addWidget(self.flight_details)
		# # self.departure_flight_list.setVisible(False)
		# self.flight_details.setVisible(False)

		flight_left_panel_layout = QVBoxLayout()
		flight_left_panel_layout.addLayout(flight_trip_layout)
		flight_left_panel_layout.addWidget(QLabel(" "))	
		flight_left_panel_layout.addLayout(flight_leg_layout)
		flight_left_panel_layout.addWidget(QLabel(" "))	
		flight_left_panel_layout.addLayout(flight_time_layout)
		flight_left_panel_layout.addWidget(QLabel(" "))	
		flight_left_panel_layout.addLayout(flight_currency_layout)
		flight_left_panel_layout.addWidget(QLabel(" "))	
		flight_left_panel_layout.addLayout(flight_rank_layout)


		# flight_left_panel_layout.addWidget(QLabel(" "))
		# flight_left_panel_layout.addLayout(flight_exclude_layout)



		flight_left_panel_layout.setSpacing(0)

		self.flight_left_panel = QFrame(self)
		self.flight_left_panel.setLayout(flight_left_panel_layout)
		self.flight_left_panel.setFixedWidth(LEFT_PANEL_WIDTH)
		self.flight_left_panel.setStyleSheet(QLABEL_LEFT)
		self.flight_left_panel.setFixedHeight(LEFT_PANEL_HEIGHT)

		flight_main_panel_dep_left_top_layout = QHBoxLayout()
		flight_main_panel_dep_left_top_layout.addWidget(self.departure_flight_table_label)
		flight_main_panel_dep_left_top_layout.addWidget(self.departure_flight_table_button)

		flight_main_panel_dep_left_layout = QVBoxLayout()
		flight_main_panel_dep_left_layout.addLayout(flight_main_panel_dep_left_top_layout)
		flight_main_panel_dep_left_layout.addWidget(self.departure_flight_table)

		flight_main_panel_dep_right_layout = QVBoxLayout()
		flight_main_panel_dep_right_layout.addWidget(self.dep_flight_table_details_label)
		flight_main_panel_dep_right_layout.addWidget(self.dep_flight_table_details)

		flight_main_panel_dep_layout = QHBoxLayout()
		flight_main_panel_dep_layout.addLayout(flight_main_panel_dep_left_layout)
		flight_main_panel_dep_layout.addLayout(flight_main_panel_dep_right_layout)

		flight_main_panel_ret_left_top_layout = QHBoxLayout()
		flight_main_panel_ret_left_top_layout.addWidget(self.return_flight_table_label)
		flight_main_panel_ret_left_top_layout.addWidget(self.return_flight_table_button)

		flight_main_panel_ret_left_layout = QVBoxLayout()
		flight_main_panel_ret_left_layout.addLayout(flight_main_panel_ret_left_top_layout)
		flight_main_panel_ret_left_layout.addWidget(self.return_flight_table)

		flight_main_panel_ret_right_layout = QVBoxLayout()
		flight_main_panel_ret_right_layout.addWidget(self.ret_flight_table_details_label)
		flight_main_panel_ret_right_layout.addWidget(self.ret_flight_table_details)

		flight_main_panel_ret_layout = QHBoxLayout()
		flight_main_panel_ret_layout.addLayout(flight_main_panel_ret_left_layout)
		flight_main_panel_ret_layout.addLayout(flight_main_panel_ret_right_layout)

		flight_main_panel_layout = QVBoxLayout()
		flight_main_panel_layout.addLayout(flight_code_and_date_layout)
		flight_main_panel_layout.addWidget(flight_search_button)
		flight_main_panel_layout.addLayout(flight_main_panel_dep_layout)
		flight_main_panel_layout.addLayout(flight_main_panel_ret_layout)

		self.flight_main_panel = QFrame(self)
		self.flight_main_panel.setLayout(flight_main_panel_layout)

		flight_frame_layout = QHBoxLayout()
		flight_frame_layout.addWidget(self.flight_left_panel)
		flight_frame_layout.addWidget(self.flight_main_panel)

		self.flight_frame = QFrame(self)
		self.flight_frame.setLayout(flight_frame_layout)
		self.flight_frame.setVisible(False)

		##############################################################################################################
		#   END FLIGHT PAGE
		##############################################################################################################

		##############################################################################################################
		#   BEGIN HOTEL PAGE
		##############################################################################################################

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
		self.hotel_in_date_entry.dateTimeChanged.connect( lambda: self.hotel_out_date_entry.setDateTime(self.hotel_in_date_entry.dateTime()))

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

			# Ratings Priority
		self.hotel_rating_box_1 = QCheckBox("5 stars")
		self.hotel_rating_box_2 = QCheckBox("4 or more stars")
		self.hotel_rating_box_3 = QCheckBox("3 or more stars")

		self.hotel_rating_box_1.toggled.connect(self.on_rating_box_button_toggled)
		self.hotel_rating_box_2.toggled.connect(self.on_rating_box_button_toggled)
		self.hotel_rating_box_3.toggled.connect(self.on_rating_box_button_toggled)

		hotel_rating_layout = QVBoxLayout()
		hotel_rating_layout.addWidget(QLabel("Rating"))
		hotel_rating_layout.addWidget(self.hotel_rating_box_1)
		hotel_rating_layout.addWidget(self.hotel_rating_box_2)
		hotel_rating_layout.addWidget(self.hotel_rating_box_3)

			# Distance Priority
		self.hotel_distance_box_1 = QCheckBox("Within 5 miles")
		self.hotel_distance_box_2 = QCheckBox("Within 10 miles")
		self.hotel_distance_box_3 = QCheckBox("Within 25 miles")

		self.hotel_distance_box_1.toggled.connect(self.on_distance_box_button_toggled)
		self.hotel_distance_box_2.toggled.connect(self.on_distance_box_button_toggled)
		self.hotel_distance_box_3.toggled.connect(self.on_distance_box_button_toggled)

		hotel_distance_layout = QVBoxLayout()
		hotel_distance_layout.addWidget(QLabel("Distance"))
		hotel_distance_layout.addWidget(self.hotel_distance_box_1)
		hotel_distance_layout.addWidget(self.hotel_distance_box_2)
		hotel_distance_layout.addWidget(self.hotel_distance_box_3)

			# Amenities Priority

		self.hotel_amenities = []
		self.hotel_amenities_box_1 = QCheckBox("Free wifi")
		self.hotel_amenities_box_2 = QCheckBox("Free breakfast")

		hotel_amenities_layout = QVBoxLayout()
		hotel_amenities_layout.addWidget(QLabel("Amenities"))
		hotel_amenities_layout.addWidget(self.hotel_amenities_box_1)
		hotel_amenities_layout.addWidget(self.hotel_amenities_box_2)

			# Ranking Input
		self.hotel_rank_rating = QComboBox(self)
		self.hotel_rank_rating.setToolTip("1 - Most Important, ..., 4 - Least Important")
		self.hotel_rank_rating.addItems(['1','2','3','4'])
		self.hotel_rank_rating.setCurrentText('1')

		self.hotel_rank_distance = QComboBox(self)
		self.hotel_rank_distance.setToolTip("1 - Most Important, ..., 4 - Least Important")
		self.hotel_rank_distance.addItems(['1','2','3','4'])
		self.hotel_rank_distance.setCurrentText('1')

		self.hotel_rank_wifi = QComboBox(self)
		self.hotel_rank_wifi.setToolTip("1 - Most Important, ..., 4 - Least Important")
		self.hotel_rank_wifi.addItems(['1','2','3','4'])
		self.hotel_rank_wifi.setCurrentText('1')

		self.hotel_rank_breakfast = QComboBox(self)
		self.hotel_rank_breakfast.setToolTip("1 - Most Important, ..., 4 - Least Important")
		self.hotel_rank_breakfast.addItems(['1','2','3','4'])
		self.hotel_rank_breakfast.setCurrentText('1')
		
		hotel_rank_layout_rating = QHBoxLayout()
		hotel_rank_layout_rating.addWidget(QLabel("Rating \t"))
		hotel_rank_layout_rating.addWidget(self.hotel_rank_rating)

		hotel_rank_layout_distance = QHBoxLayout()
		hotel_rank_layout_distance.addWidget(QLabel("Distance\t"))
		hotel_rank_layout_distance.addWidget(self.hotel_rank_distance)

		hotel_rank_layout_wifi = QHBoxLayout()
		hotel_rank_layout_wifi.addWidget(QLabel("Wi-fi \t"))
		hotel_rank_layout_wifi.addWidget(self.hotel_rank_wifi)

		hotel_rank_layout_breakfast = QHBoxLayout()
		hotel_rank_layout_breakfast.addWidget(QLabel("Breakfast"))
		hotel_rank_layout_breakfast.addWidget(self.hotel_rank_breakfast)

		hotel_rank_options_layout = QVBoxLayout()
		hotel_rank_options_layout.addLayout(hotel_rank_layout_rating)
		hotel_rank_options_layout.addLayout(hotel_rank_layout_distance)
		hotel_rank_options_layout.addLayout(hotel_rank_layout_wifi)
		hotel_rank_options_layout.addLayout(hotel_rank_layout_breakfast)

		self.hotel_rank_options_frame = QFrame(self)
		self.hotel_rank_options_frame.setLayout(hotel_rank_options_layout)
		self.hotel_rank_options_frame.setVisible(False)

		self.hotel_rank_button = QPushButton("Priorities")
		self.hotel_rank_button.setToolTip("Rank your filter priorities")
		self.hotel_rank_button.clicked.connect(lambda: self.hotel_rank_options_frame.setVisible(not self.hotel_rank_options_frame.isVisible()))

		hotel_rank_layout = QHBoxLayout()
		hotel_rank_layout.addWidget(self.hotel_rank_button)
		hotel_rank_layout.addWidget(self.hotel_rank_options_frame)	

		hotel_search_button = QPushButton("Search Hotels", self)
		hotel_search_button.clicked.connect(self.on_hotel_search_clicked)

		hotel_select_button = QPushButton("Select Hotel", self)
		hotel_select_button.clicked.connect(self.on_hotel_select_clicked)
		hotel_select_button.setFixedWidth(200)

		hotel_table_columns = ["Name", "Price per Night", "Total Price", "Rating", "Distance from Airport", "Amenities"]
		self.hotel_table_label = QLabel("Hotels")
		self.hotel_table = QTableWidget(self)
		self.hotel_table.setColumnCount(len(hotel_table_columns))
		self.hotel_table.setRowCount(1)
		for i in range(self.hotel_table.columnCount()):
			self.hotel_table.setItem(0 , i, QTableWidgetItem(hotel_table_columns[i]))
			self.hotel_table.item(0, i).setBackground(QColor(30,38,64))
		self.hotel_table.horizontalHeader().setVisible(False)
		self.hotel_table.verticalHeader().setVisible(False)
		self.hotel_table.cellClicked.connect(self.on_hotel_row_clicked)
		self.hotel_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.hotel_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.hotel_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
		self.hotel_table.setShowGrid(False)
		self.hotel_table.setWordWrap(True)

		hotel_table_layout = QVBoxLayout()
		hotel_table_layout.addWidget(self.hotel_table)
		hotel_table_layout.addWidget(self.hotel_table_label)

		hotel_details = \
		f'\
Name:\t\t\t \n\
Nightly Price:\t\t \n\
Total Price:\t\t \n\
Rating:\t\t\t \n\
Distance from Airport:\t\n\
Amenities:\t\t \
'

		self.hotel_table_details_label = QLabel("Hotel Details")
		self.hotel_table_details = QLabel(hotel_details)
		self.hotel_table_details.setStyleSheet("QLabel {text-align: left; qproperty-alignment: AlignLeft;}")
		self.hotel_table_details.setFixedWidth(500)

		hotel_table_details_layout = QVBoxLayout()
		hotel_table_details_layout.addWidget(self.hotel_table_details_label)
		hotel_table_details_layout.addWidget(self.hotel_table_details)

		hotel_left_panel_layout = QVBoxLayout()
		hotel_left_panel_layout.addLayout(hotel_rating_layout)
		hotel_left_panel_layout.addLayout(hotel_distance_layout)
		hotel_left_panel_layout.addLayout(hotel_amenities_layout)
		hotel_left_panel_layout.addLayout(hotel_rank_layout)

		self.hotel_left_panel = QFrame(self)
		self.hotel_left_panel.setLayout(hotel_left_panel_layout)
		self.hotel_left_panel.setFixedWidth(200)
		self.hotel_left_panel.setStyleSheet(QLABEL_LEFT)
		self.hotel_left_panel.setFixedHeight(LEFT_PANEL_HEIGHT)
		self.hotel_left_panel.setFixedWidth(LEFT_PANEL_WIDTH)

		hotel_main_panel_buttons_layout = QHBoxLayout()
		hotel_main_panel_buttons_layout.addWidget(hotel_search_button)
		hotel_main_panel_buttons_layout.addWidget(hotel_select_button)

		hotel_main_panel_info_layout = QVBoxLayout()
		hotel_main_panel_info_layout.addLayout(hotel_main_panel_buttons_layout)
		hotel_main_panel_info_layout.addLayout(hotel_table_layout)

		hotel_main_panel_details_layout = QHBoxLayout()
		hotel_main_panel_details_layout.addLayout(hotel_main_panel_info_layout)
		hotel_main_panel_details_layout.addLayout(hotel_table_details_layout)

		hotel_main_panel_layout = QVBoxLayout()
		hotel_main_panel_layout.addLayout(hotel_loc_and_date_layout)
		hotel_main_panel_layout.addLayout(hotel_main_panel_details_layout)

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
		#   BEGIN CONFIRMATION PAGE
		##############################################################################################################

		flight_details = \
			f'\
Airline:\t\t \n\
Price:\t\t \n\
Type:\t\t \n\
Departure:\t \n\
Arrival:\t\t \n\
Class:\t\t \n\
Layover Flights:\t \
'
	
		hotel_details = \
			f'\
Name:\t\t\t \n\
Nightly Price:\t\t \n\
Total Price:\t\t \n\
Rating:\t\t\t \n\
Distance from Airport:\t\n\
Amenities:\t\t \
'

		self.confirm_dep_flight_details = QLabel(flight_details)
		self.confirm_dep_flight_details.setStyleSheet("QLabel {text-align: left; qproperty-alignment: AlignLeft;}")


		confirm_dep_flight_panel_layout = QHBoxLayout()
		confirm_dep_flight_panel_layout.addWidget(QLabel("DEPARTURE FLIGHT"))
		confirm_dep_flight_panel_layout.addWidget(self.confirm_dep_flight_details)

		self.confirm_ret_flight_details = QLabel(flight_details)
		self.confirm_ret_flight_details.setStyleSheet("QLabel {text-align: left; qproperty-alignment: AlignLeft;}")


		confirm_ret_flight_panel_layout = QHBoxLayout()
		confirm_ret_flight_panel_layout.addWidget(QLabel("RETURN FLIGHT"))
		confirm_ret_flight_panel_layout.addWidget(self.confirm_ret_flight_details)

		self.confirm_hotel_details = QLabel(hotel_details)
		self.confirm_hotel_details.setStyleSheet("QLabel {text-align: left; qproperty-alignment: AlignLeft;}")


		confirm_hotel_panel_layout = QHBoxLayout()
		confirm_hotel_panel_layout.addWidget(QLabel("HOTEL"))
		confirm_hotel_panel_layout.addWidget(self.confirm_hotel_details)

		self.confirm_dep_flight_panel = QFrame(self)
		self.confirm_dep_flight_panel.setLayout(confirm_dep_flight_panel_layout)

		self.confirm_ret_flight_panel = QFrame(self)
		self.confirm_ret_flight_panel.setLayout(confirm_ret_flight_panel_layout)

		self.confirm_hotel_panel = QFrame(self)
		self.confirm_hotel_panel.setLayout(confirm_hotel_panel_layout)

		confirm_frame_layout = QVBoxLayout()
		confirm_frame_layout.addWidget(self.confirm_dep_flight_panel)
		confirm_frame_layout.addWidget(self.confirm_ret_flight_panel)
		confirm_frame_layout.addWidget(self.confirm_hotel_panel)
		confirm_frame_layout.addWidget(QLabel("\nThank you for using FairFare!\n"))

		self.confirm_frame = QFrame(self)
		self.confirm_frame.setLayout(confirm_frame_layout)
		self.confirm_frame.setVisible(False)


		##############################################################################################################
		#   END CONFIRMATION PAGE
		##############################################################################################################

		##############################################################################################################
		#   BEGIN PAGE INSERTION
		##############################################################################################################

		
		# self.flight_menu_button = QPushButton("<<< Flights")
		# self.flight_menu_button.clicked.connect(self.on_menu_button_clicked)
		# self.flight_menu_button.setVisible(False)
		# self.hotel_menu_button = QPushButton("Hotels >>>")
		# self.hotel_menu_button.clicked.connect(self.on_menu_button_clicked)
		# self.hotel_menu_button.setVisible(False)

		self.next_menu_button = QPushButton("Next >>>")
		self.next_menu_button.setVisible(False)
		self.next_menu_button.clicked.connect(self.on_menu_button_clicked)

		self.prev_menu_button = QPushButton("<<< Prev")
		self.prev_menu_button.setVisible(False)
		self.prev_menu_button.clicked.connect(self.on_menu_button_clicked)

		self.menu_spacer_label = QLabel(" " * ((GUI_WIDTH // 10 * 7) // 6))

		menu_frame_layout = QHBoxLayout()
		# menu_frame_layout.addWidget(self.flight_menu_button)
		menu_frame_layout.addWidget(self.prev_menu_button)
		menu_frame_layout.addWidget(self.menu_spacer_label)
		# menu_frame_layout.addWidget(self.hotel_menu_button)
		menu_frame_layout.addWidget(self.next_menu_button)

		self.menu_frame = QFrame(self)
		self.menu_frame.setLayout(menu_frame_layout)

		logo_label = QLabel(self)
		logo_label.setPixmap(QPixmap("logo.png")) #.scaled(10, 20, Qt.KeepAspectRatio))
		logo_label.setScaledContents(True)
		logo_label.setFixedWidth(50)
		logo_label.setFixedHeight(50)
		logo_label.setStyleSheet(QLABEL_ICON)

		logo_title = QLabel("FAIRFARE")
		logo_title.setStyleSheet(QLABEL_TITLE)

		logo_panel_layout = QHBoxLayout()
		logo_panel_layout.setAlignment(Qt.AlignCenter)
		# logo_panel_layout.addWidget(self.flight_menu_button)
		logo_panel_layout.addWidget(logo_label)
		logo_panel_layout.addWidget(logo_title)
		# logo_panel_layout.addWidget(self.hotel_menu_button)

		self.logo_panel = QFrame(self)
		self.logo_panel.setLayout(logo_panel_layout)

		welcome_layout = QVBoxLayout()
		welcome_layout.addWidget(self.welcome_start_button)
		welcome_layout.setAlignment(Qt.AlignCenter)

		self.welcome_panel = QFrame(self)
		self.welcome_panel.setLayout(welcome_layout)

		layout = QVBoxLayout()
		layout.addWidget(self.menu_frame)
		layout.addWidget(self.logo_panel)
		layout.addWidget(self.welcome_panel)
		layout.addWidget(self.flight_frame)
		layout.addWidget(self.hotel_frame)
		layout.addWidget(self.confirm_frame)

		# layout.addWidget(QLabel("THIS IS A TEST"))
		self.setLayout(layout)

	def on_start_button_clicked(self):
		self.welcome_start_button.setVisible(False)
		self.flight_frame.setVisible(True)
		self.next_menu_button.setVisible(True)

	def clear_departure_flight_table(self):
		flight_details = \
			f'\
Airline:\t\t \n\
Price:\t\t \n\
Type:\t\t \n\
Departure:\t \n\
Arrival:\t\t \n\
Class:\t\t \n\
Layover Flights:\t \
'
		self.confirm_dep_flight_details.setText(flight_details)
		for i in range(1, self.departure_flight_table.rowCount()):
			self.departure_flight_table.removeRow(1)


	def clear_return_flight_table(self):
		flight_details = \
			f'\
Airline:\t\t \n\
Price:\t\t \n\
Type:\t\t \n\
Departure:\t \n\
Arrival:\t\t \n\
Class:\t\t \n\
Layover Flights:\t \
'
		self.confirm_ret_flight_details.setText(flight_details)
		for i in range(1, self.return_flight_table.rowCount()):
			self.return_flight_table.removeRow(1)

	def on_search_clicked(self):
		# Clear previous search results
		# self.departure_flight_list.clear()
		# self.flight_departure_token_list = []
		self.departure_token = ""
		# self.flight_details.clear()

		self.clear_departure_flight_table()

		self.clear_return_flight_table()

		# if self.flight_trip_type == "Round Trip":
		# 	self.return_flight_table.setVisible(True)
		# 	self.return_flight_table_label.setVisible(True)
		# else:
		# 	self.return_flight_table.setVisible(False)
		# 	self.return_flight_table_label.setVisible(False)

		# Retrieve input values
		departure_id = self.flight_departure_entry.text().upper()
		arrival_id = self.flight_arrival_entry.text().upper()
		departure_date = self.flight_departure_date_entry.text()
		return_date = self.flight_return_date_entry.text()
		currency = self.flight_currency_entry.currentText()
		max_cost = None if self.flight_cost_max_entry.text() == "" else self.flight_cost_max_entry.text()  # Optional max cost input
		min_time = None if self.flight_time_min_entry.text() == "" else self.flight_time_min_entry.text() # Optional minimum time input
		max_time = None if self.flight_time_max_entry.text() == "" else self.flight_time_max_entry.text() # Optional maximum time input
			

		# Check for required fields
		if not all([departure_id, arrival_id, departure_date, return_date, currency]):
			QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
			return

		# Check date validity
		if self.flight_return_date_entry.dateTime() < self.flight_departure_date_entry.dateTime():
			QMessageBox.warning(self, "Input Error", "Please ensure return date is not before departure date.")
			return

		# Check date availbility
		if self.flight_return_date_entry.dateTime() < datetime.today() or self.flight_departure_date_entry.dateTime() < datetime.today():
			QMessageBox.warning(self, "Input Error", "Please ensure dates are not before current day.")
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

		# Convert flight_data to Dataframe ["Airline", "Price", "Type", "Departure", "Dpt Date", "Arrival", "Arr Date", "Travel Class"]
		# print(flight_data)
		self.current_dep_flight_data = pd.DataFrame([ [ flight['flights'][0]['airline'], "$" + str(flight['price']), flight['type'], \
					self.time_to_12(flight['flights'][0]['departure_time']), \
					self.date_to_mmm(flight['flights'][0]['departure_time']), \
					self.time_to_12(flight['flights'][-1]['arrival_time']), \
					self.date_to_mmm(flight['flights'][0]['arrival_time']), \
					flight['flights'][0]['travel_class'], \
					flight['departure_token'], \
					len(flight['flights'])] \
				for flight in flight_data \
				], columns = ["Airline", "Price", "Type", "Departure", "Dpt Date", "Arrival", "Arr Date", "Travel Class", "Departure Token", "numLegs"])

		# print(flight_data)
		self.calculate_departure_flight_table_data()
		# self.enter_departure_flight_table_data()
		

	def on_hotel_search_clicked(self):
		# Clear previous search results
		for i in range(1, self.hotel_table.rowCount()):
				self.hotel_table.removeRow(1)

		# Retrieve input values
		location = self.hotel_location_entry.text()
		check_in_date = self.hotel_in_date_entry.text()
		check_out_date = self.hotel_out_date_entry.text()
		currency = self.flight_currency_entry.currentText()
		max_price = None #if self.hotel_cost_max_entry.text() == "-" else self.hotel_cost_max_entry.text()  # Optional maximum price input
		min_price = None #if self.hotel_cost_min_entry.text() == "-" else self.hotel_cost_min_entry.text() # Optional minimum price input
		min_rating = None #if self.hotel_rating_min_entry.text() == "-" else self.hotel_rating_min_entry.text() # Optional minimum rating input
		amenities = None #if self.hotel_amenities == [] else self.hotel_amenities # Optional amenities input
		# airport_code = self.departure_entry.text()  # Assuming there's an entry for the airport code
		airport_code = self.flight_arrival_entry.text().upper()


		# Check for required fields
		if not all([location, check_in_date, check_out_date, currency]):
			QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
			return

		# Check date validity
		if self.hotel_in_date_entry.dateTime() > self.hotel_out_date_entry.dateTime():
			QMessageBox.warning(self, "Input Error", "Please ensure check-out date is not before check-in date.")
			return

		# Check date availbility
		if self.hotel_in_date_entry.dateTime() < datetime.today() or self.hotel_out_date_entry.dateTime() < datetime.today():
			QMessageBox.warning(self, "Input Error", "Please ensure dates are not before current day.")
			return

		

		#Get hotel data with optional parameters
		hotel_data = search_hotels(
			location, check_in_date, check_out_date, currency, 
			max_price= max_price if max_price else None, 
			min_price= min_price if min_price else None, 
			min_rating= min_rating if min_rating else None, 
			amenities=None
		)

		# Handle no results or errors
		if not hotel_data or isinstance(hotel_data, str):
			QMessageBox.information(self, "No Results", str(hotel_data) if hotel_data else "No hotels found.")
			return

		# Display flight options in the list

		distance_str_list = []
		for hotel in hotel_data:
			if "latitude" in hotel and "longitude" in hotel and hotel["latitude"] and hotel["longitude"]:
					hotel_lat = float(hotel["latitude"])
					hotel_lon = float(hotel["longitude"])
					
					#distance calculating
					try:
						distance = calculate_distance(airport_code, hotel_lat, hotel_lon)
						distance_str = f"{distance:.2f} miles"

					except ValueError as e:
						distance_str = "Distance unavailable."
			else:
				distance_str = "Distance unavailable."

			# if not airport_code:
			# 	distance_str = "Arrival airport undefined."
			distance_str_list.append(distance_str)

		# self.current_hotel_data = pd.DataFrame([ [ hotel['name'], hotel['price_per_night'], hotel['total_price'], \
		# 			round(hotel['rating'],1), \
		# 			distance_str_list[index], \
		# 			str(hotel['amenities'])] \
		# 		for index, hotel in enumerate(hotel_data) \
		# 		], columns = ["Name", "Price per Night", "Total Price", "Rating", "Distance from Airport", "Amenities"])

		hotel_adjusted_data = []

		for index, hotel in enumerate(hotel_data):
			name = hotel['name']
			ppn = hotel['price_per_night']
			tp = hotel['total_price']
			rating = round(hotel['rating'],1) if hotel['rating'] != None else 0
			dist = distance_str_list[index]
			amen = str(hotel['amenities'])
			hotel_adjusted_data.append([name, ppn, tp, rating, dist, amen])

		columnHeaders = ["Name", "Price per Night", "Total Price", "Rating", "Distance from Airport", "Amenities"]
		self.current_hotel_data = pd.DataFrame(hotel_adjusted_data, columns = columnHeaders)

		self.calculate_hotel_table_data()

	def on_hotel_select_clicked(self):
		if type(self.current_hotel) != type(None):
			hotel_amenities = self.current_hotel["Amenities"][1:-1].replace(", ", "\n\t\t\t")
			hotel_details = \
				f'\
Name:\t\t\t {self.current_hotel["Name"]}\n\
Nightly Price:\t\t {self.current_hotel["Price per Night"]}\n\
Total Price:\t\t {self.current_hotel["Total Price"]}\n\
Rating:\t\t\t {self.current_hotel["Rating"]}\n\
Distance from Airport:\t{self.current_hotel["Distance from Airport"]}\n\
Amenities:\t\t{hotel_amenities}\
'
			self.confirm_hotel_details.setText(hotel_details)
		

	def on_departure_flight_row_clicked(self, row, column):
		if row > 0:
			self.departure_flight_table.selectRow(row)
			self.current_dep_flight = self.current_dep_flight_data.loc[row - 1,:]

			flight_details = \
			f'\
Airline:\t\t {self.current_dep_flight["Airline"]}\n\
Price:\t\t {self.current_dep_flight["Price"]}\n\
Type:\t\t {self.current_dep_flight["Type"]}\n\
Departure:\t {self.current_dep_flight["Dpt Date"][:-4] + self.current_dep_flight["Departure"]}\n\
Arrival:\t\t {self.current_dep_flight["Arr Date"][:-4] + self.current_dep_flight["Arrival"]}\n\
Class:\t\t {self.current_dep_flight["Travel Class"]}\n\
Layover Flights:\t {str(self.current_dep_flight["numLegs"] - 1)}\
			'
			self.dep_flight_table_details.setText(flight_details)
			self.departure_token = self.current_dep_flight_data.loc[row - 1, 'Departure Token']


	def on_departure_flight_select_clicked(self):
		if type(self.current_dep_flight) != type(None):

			###################################################################################################################
			# RETURN FLIGHT INFORMATION
			###################################################################################################################
			if self.flight_trip_type == "Round Trip":
				# Clear previous search results
				self.clear_return_flight_table()

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
				self.return_flight_table.setShowGrid(False)

				# Check for required fields
				if not all([departure_id, arrival_id, departure_date, return_date, currency]):
					QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
					return
					
				# Check date validity
				if self.flight_return_date_entry.dateTime() < self.flight_departure_date_entry.dateTime():
					QMessageBox.warning(self, "Input Error", "Please ensure return date is not before departure date.")
					return

				# Check date availbility
				if self.flight_return_date_entry.dateTime() < datetime.today() or self.flight_departure_date_entry.dateTime() < datetime.today():
					QMessageBox.warning(self, "Input Error", "Please ensure dates are not before current day.")
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

				self.current_ret_flight_data = flight_data

				self.current_ret_flight_data = pd.DataFrame([ [ flight['flights'][0]['airline'], "$" + str(flight['price']), flight['type'], \
					self.time_to_12(flight['flights'][0]['departure_time']), \
					self.date_to_mmm(flight['flights'][0]['departure_time']), \
					self.time_to_12(flight['flights'][-1]['arrival_time']), \
					self.date_to_mmm(flight['flights'][0]['arrival_time']), \
					flight['flights'][0]['travel_class'], \
					flight['departure_token'], \
					len(flight['flights'])] \
				for flight in flight_data \
				], columns = ["Airline", "Price", "Type", "Departure", "Dpt Date", "Arrival", "Arr Date", "Travel Class", "Departure Token", "numLegs"])

				# print("falsdjf;lads")
				self.calculate_return_flight_table_data()


			flight_details = \
			f'\
Airline:\t\t {self.current_dep_flight["Airline"]}\n\
Price:\t\t {self.current_dep_flight["Price"]}\n\
Type:\t\t {self.current_dep_flight["Type"]}\n\
Departure:\t {self.current_dep_flight["Dpt Date"][:-4] + self.current_dep_flight["Departure"]}\n\
Arrival:\t\t {self.current_dep_flight["Arr Date"][:-4] + self.current_dep_flight["Arrival"]}\n\
Class:\t\t {self.current_dep_flight["Travel Class"]}\n\
Layover Flights:\t {str(self.current_dep_flight["numLegs"] - 1)}\
'
			self.confirm_dep_flight_details.setText(flight_details)

		###################################################################################################################
		###################################################################################################################

	def on_return_flight_row_clicked(self, row, column):
		if row > 0:
			self.return_flight_table.selectRow(row)
			self.current_ret_flight = self.current_ret_flight_data.loc[row - 1, :]
			# print("CURRENT RETURN FLIGHT:")
			# pprint(self.current_ret_flight)

			flight_details = \
			f'\
Airline:\t\t {self.current_ret_flight["Airline"]}\n\
Price:\t\t {self.current_ret_flight["Price"]}\n\
Type:\t\t {self.current_ret_flight["Type"]}\n\
Departure:\t {self.current_ret_flight["Dpt Date"][:-4] + self.current_ret_flight["Departure"]}\n\
Arrival:\t\t {self.current_ret_flight["Arr Date"][:-4] + self.current_ret_flight["Arrival"]}\n\
Class:\t\t {self.current_ret_flight["Travel Class"]}\n\
Layover Flights:\t {str(self.current_ret_flight["numLegs"] - 1)}\
			'
			self.ret_flight_table_details.setText(flight_details)

	def on_return_flight_select_clicked(self):
		if type(self.current_ret_flight) != type(None):
			flight_details = \
				f'\
Airline:\t\t {self.current_ret_flight["Airline"]}\n\
Price:\t\t {self.current_ret_flight["Price"]}\n\
Type:\t\t {self.current_ret_flight["Type"]}\n\
Departure:\t {self.current_ret_flight["Dpt Date"][:-4] + self.current_dep_flight["Departure"]}\n\
Arrival:\t\t {self.current_ret_flight["Arr Date"][:-4] + self.current_dep_flight["Arrival"]}\n\
Class:\t\t {self.current_ret_flight["Travel Class"]}\n\
Layover Flights:\t {str(self.current_ret_flight["numLegs"] - 1)}\
'
			self.confirm_ret_flight_details.setText(flight_details)

	def on_hotel_row_clicked(self, row, column):
		if row > 0:
			self.hotel_table.selectRow(row)
			self.current_hotel = self.current_hotel_data.loc[row - 1, :]

			hotel_amenities = self.current_hotel["Amenities"][1:-1].replace(", ", "\n\t\t\t")
			hotel_details = \
			f'\
Name:\t\t\t {self.current_hotel["Name"]}\n\
Nightly Price:\t\t {self.current_hotel["Price per Night"]}\n\
Total Price:\t\t {self.current_hotel["Total Price"]}\n\
Rating:\t\t\t {self.current_hotel["Rating"]}\n\
Distance from Airport:\t{self.current_hotel["Distance from Airport"]}\n\
Amenities:\t\t{hotel_amenities}\
'

			self.hotel_table_details.setText(hotel_details)

	def on_departure_date_calendar_date_changed(self):
		self.flight_return_date_entry.setDateTime(self.flight_departure_date_entry.dateTime())
		self.hotel_in_date_entry.setDateTime(self.flight_departure_date_entry.dateTime())

	def enter_departure_flight_table_data(self):

		self.clear_departure_flight_table()

		for row in range(len(self.current_dep_flight_data)):

			# Add flight information into the table ["Airline", "Price", "Type", "Departure", "Dpt Date", "Arrival", "Arr Date", "Travel Class"]
			rowPosition = self.departure_flight_table.rowCount()
			self.departure_flight_table.insertRow(rowPosition)
			self.departure_flight_table.setItem(rowPosition , 0, QTableWidgetItem(str(self.current_dep_flight_data.loc[row, "Airline"])))
			self.departure_flight_table.setItem(rowPosition , 1, QTableWidgetItem(str(self.current_dep_flight_data.loc[row, "Price"])))
			self.departure_flight_table.setItem(rowPosition , 2, QTableWidgetItem(str(self.current_dep_flight_data.loc[row, "Type"])))
			self.departure_flight_table.setItem(rowPosition , 3, QTableWidgetItem(str(self.current_dep_flight_data.loc[row, "Departure"])))
			self.departure_flight_table.setItem(rowPosition , 4, QTableWidgetItem(str(self.current_dep_flight_data.loc[row, "Dpt Date"])))
			self.departure_flight_table.setItem(rowPosition , 5, QTableWidgetItem(str(self.current_dep_flight_data.loc[row, "Arrival"])))
			self.departure_flight_table.setItem(rowPosition , 6, QTableWidgetItem(str(self.current_dep_flight_data.loc[row, "Arr Date"])))
			self.departure_flight_table.setItem(rowPosition , 7, QTableWidgetItem(str(self.current_dep_flight_data.loc[row, "Travel Class"])))

	def enter_return_flight_table_data(self):

		self.clear_return_flight_table()

		for row in range(len(self.current_ret_flight_data)):

			# Add flight information into the table ["Airline", "Price", "Type", "Departure", "Dpt Date", "Arrival", "Arr Date", "Travel Class"]
			rowPosition = self.return_flight_table.rowCount()
			self.return_flight_table.insertRow(rowPosition)
			self.return_flight_table.setItem(rowPosition , 0, QTableWidgetItem(str(self.current_ret_flight_data.loc[row, "Airline"])))
			self.return_flight_table.setItem(rowPosition , 1, QTableWidgetItem(str(self.current_ret_flight_data.loc[row, "Price"])))
			self.return_flight_table.setItem(rowPosition , 2, QTableWidgetItem(str(self.current_ret_flight_data.loc[row, "Type"])))
			self.return_flight_table.setItem(rowPosition , 3, QTableWidgetItem(str(self.current_ret_flight_data.loc[row, "Departure"])))
			self.return_flight_table.setItem(rowPosition , 4, QTableWidgetItem(str(self.current_ret_flight_data.loc[row, "Dpt Date"])))
			self.return_flight_table.setItem(rowPosition , 5, QTableWidgetItem(str(self.current_ret_flight_data.loc[row, "Arrival"])))
			self.return_flight_table.setItem(rowPosition , 6, QTableWidgetItem(str(self.current_ret_flight_data.loc[row, "Arr Date"])))
			self.return_flight_table.setItem(rowPosition , 7, QTableWidgetItem(str(self.current_ret_flight_data.loc[row, "Travel Class"])))

	def enter_hotel_table_data(self):

		for i in range(1, self.hotel_table.rowCount()):
			self.hotel_table.removeRow(1)

		for row in range(len(self.current_hotel_data)):

			# Add flight information into the table ["Name", "Price per Night", "Total Price", "Rating", "Distance from Airport", "Amenities"]

			rowPosition = self.hotel_table.rowCount()
			# print([rowPosition, row, self.current_hotel_data.loc[row, "Total Price"]])
			self.hotel_table.insertRow(rowPosition)
			self.hotel_table.setItem(rowPosition , 0, QTableWidgetItem(str(self.current_hotel_data.loc[row, "Name"])))
			self.hotel_table.setItem(rowPosition , 1, QTableWidgetItem(str(self.current_hotel_data.loc[row, "Price per Night"])))
			self.hotel_table.setItem(rowPosition , 2, QTableWidgetItem(str(self.current_hotel_data.loc[row, "Total Price"])))
			self.hotel_table.setItem(rowPosition , 3, QTableWidgetItem(str(self.current_hotel_data.loc[row, "Rating"])))
			self.hotel_table.setItem(rowPosition , 4, QTableWidgetItem(str(self.current_hotel_data.loc[row, "Distance from Airport"])))
			self.hotel_table.setItem(rowPosition , 5, QTableWidgetItem(str(self.current_hotel_data.loc[row, "Amenities"])))

		# print(self.current_hotel_data.loc[:, "totalRank":])

	def calculate_departure_flight_table_data(self):
		# Default Priority Order
		legPrio = 3 - int(self.flight_rank_leg.currentText())
		timePrio = 3 - int(self.flight_rank_time.currentText())

		if self.flight_leg_box_1.isChecked():
			self.current_dep_flight_data.loc[:, "legRank"] = np.where(self.current_dep_flight_data.loc[:, "numLegs"] == 1, 1, 0)
		elif self.flight_leg_box_2.isChecked():
			self.current_dep_flight_data.loc[:, "legRank"] = np.where(self.current_dep_flight_data.loc[:, "numLegs"] <= 2, 1, 0)
		elif self.flight_leg_box_3.isChecked():
			self.current_dep_flight_data.loc[:, "legRank"] = np.where(self.current_dep_flight_data.loc[:, "numLegs"] <= 3, 1, 0)
		else:
			self.current_dep_flight_data.loc[:, "legRank"] = 0

		if self.flight_time_box_1.isChecked():
			self.current_dep_flight_data.loc[:, "timeRank"] = np.where(self.current_dep_flight_data.loc[:, "Departure"].str.contains("AM") & self.current_dep_flight_data.loc[:, "Departure"].str.split(":", expand = True)[0].isin(["12", "1", "2", "3", "4", "5", "6", "7"]), 1, 0)
		elif self.flight_time_box_3.isChecked():
			self.current_dep_flight_data.loc[:, "timeRank"] = np.where(self.current_dep_flight_data.loc[:, "Departure"].str.contains("PM") & self.current_dep_flight_data.loc[:, "Departure"].str.split(":", expand = True)[0].isin(["4", "5", "6", "7", "8", "9", "10", "11"]), 1, 0)
		elif self.flight_time_box_2.isChecked():
			self.current_dep_flight_data.loc[:, "timeRank"] = np.where(self.current_dep_flight_data.loc[:, "Departure"].str.split(":", expand = True)[0].isin(["8", "9", "10", "11", "12", "1", "2", "3"]), 1, 0)
		else:
			self.current_dep_flight_data.loc[:, "timeRank"] = 0

		self.current_dep_flight_data.loc[:, "totalRank"] = self.current_dep_flight_data.loc[:, "legRank"] * legPrio + \
													self.current_dep_flight_data.loc[:, "timeRank"]	* timePrio

		self.current_dep_flight_data.loc[:, "totalPrice"] = self.current_dep_flight_data.loc[:, "Price"].str.replace('$', '').str.replace(',','').astype(int)

		self.current_dep_flight_data = self.current_dep_flight_data.sort_values(['totalRank', 'totalPrice'], ascending = [False, True]).reset_index()

		# print(self.current_dep_flight_data.loc[:, "legRank":])

		self.enter_departure_flight_table_data()

	def calculate_return_flight_table_data(self):

		# Default Priority Order
		legPrio = 3 - int(self.flight_rank_leg.currentText())
		timePrio = 3 - int(self.flight_rank_time.currentText())

		if self.flight_leg_box_1.isChecked():
			self.current_ret_flight_data.loc[:, "legRank"] = np.where(self.current_ret_flight_data.loc[:, "numLegs"] == 1, 1, 0)
		elif self.flight_leg_box_2.isChecked():
			self.current_ret_flight_data.loc[:, "legRank"] = np.where(self.current_ret_flight_data.loc[:, "numLegs"] <= 2, 1, 0)
		elif self.flight_leg_box_3.isChecked():
			self.current_ret_flight_data.loc[:, "legRank"] = np.where(self.current_ret_flight_data.loc[:, "numLegs"] <= 3, 1, 0)
		else:
			self.current_ret_flight_data.loc[:, "legRank"] = 0

		if self.flight_time_box_1.isChecked():
			self.current_ret_flight_data.loc[:, "timeRank"] = np.where(self.current_ret_flight_data.loc[:, "Departure"].str.contains("AM") & self.current_ret_flight_data.loc[:, "Departure"].str.split(":", expand = True)[0].isin(["12", "1", "2", "3", "4", "5", "6", "7"]), 1, 0)
		elif self.flight_time_box_3.isChecked():
			self.current_ret_flight_data.loc[:, "timeRank"] = np.where(self.current_ret_flight_data.loc[:, "Departure"].str.contains("PM") & self.current_ret_flight_data.loc[:, "Departure"].str.split(":", expand = True)[0].isin(["4", "5", "6", "7", "8", "9", "10", "11"]), 1, 0)
		elif self.flight_time_box_2.isChecked():
			self.current_ret_flight_data.loc[:, "timeRank"] = np.where(self.current_ret_flight_data.loc[:, "Departure"].str.split(":", expand = True)[0].isin(["8", "9", "10", "11", "12", "1", "2", "3"]), 1, 0)
		else:
			self.current_ret_flight_data.loc[:, "timeRank"] = 0

		self.current_ret_flight_data.loc[:, "totalRank"] = self.current_ret_flight_data.loc[:, "legRank"] * legPrio + \
													self.current_ret_flight_data.loc[:, "timeRank"]	* timePrio

		self.current_ret_flight_data.loc[:, "totalPrice"] = self.current_ret_flight_data.loc[:, "Price"].str.replace('$', '').str.replace(',','').astype(int)

		self.current_ret_flight_data = self.current_ret_flight_data.sort_values(['totalRank', 'totalPrice'], ascending = [False, True]).reset_index()

		# print(self.current_ret_flight_data.loc[:, "legRank":])

		self.enter_return_flight_table_data()

	def calculate_hotel_table_data(self):
		
		# Default Priority Order
		ratePrio = 5 - int(self.hotel_rank_rating.currentText())
		distPrio = 5 - int(self.hotel_rank_distance.currentText())
		wifiPrio = 5 - int(self.hotel_rank_wifi.currentText())
		breakfastPrio = 5 - int(self.hotel_rank_breakfast.currentText())

		# Rating Priority Calculation
		if self.hotel_rating_box_1.isChecked():
			self.current_hotel_data.loc[:, "rateRank"] = np.where(self.current_hotel_data.loc[:, "Rating"].astype(float) >= float(self.hotel_rating_box_1.text().split()[0]), 1, 0)
		elif self.hotel_rating_box_2.isChecked():
			self.current_hotel_data.loc[:, "rateRank"] = np.where(self.current_hotel_data.loc[:, "Rating"].astype(float) >= float(self.hotel_rating_box_2.text().split()[0]), 1, 0)
		elif self.hotel_rating_box_3.isChecked():
			self.current_hotel_data.loc[:, "rateRank"] = np.where(self.current_hotel_data.loc[:, "Rating"].astype(float) >= float(self.hotel_rating_box_3.text().split()[0]), 1, 0)
		else:
			self.current_hotel_data.loc[:, "rateRank"] = 0


		self.current_hotel_data.loc[:, "dist"] = np.where(self.current_hotel_data.loc[:, "Distance from Airport"].str.isnumeric(), self.current_hotel_data.loc[:, "Distance from Airport"].str.split(" ", expand = True)[0], "9999999999999")

		if self.hotel_distance_box_1.isChecked():
			self.current_hotel_data.loc[:, "distRank"] = np.where(self.current_hotel_data.loc[:, "dist"].astype(float) <= float(self.hotel_distance_box_1.text().split()[1]), 1, 0)
		elif self.hotel_distance_box_2.isChecked():
			self.current_hotel_data.loc[:, "distRank"] = np.where(self.current_hotel_data.loc[:, "dist"].astype(float) <= float(self.hotel_distance_box_2.text().split()[1]), 1, 0)
		elif self.hotel_distance_box_3.isChecked():
			self.current_hotel_data.loc[:, "distRank"] = np.where(self.current_hotel_data.loc[:, "dist"].astype(float) <= float(self.hotel_distance_box_3.text().split()[1]), 1, 0)
		else:
			self.current_hotel_data.loc[:, "distRank"] = 0

		if self.hotel_amenities_box_1.isChecked():
			self.current_hotel_data.loc[:, "wifiRank"] = np.where(self.current_hotel_data.loc[:, "Amenities"].str.contains("Free Wi-Fi"), 1, 0)
		else:
			self.current_hotel_data.loc[:, "wifiRank"] = 0

		if self.hotel_amenities_box_2.isChecked():
			self.current_hotel_data.loc[:, "breakfastRank"] = np.where(self.current_hotel_data.loc[:, "Amenities"].str.contains("Free breakfast"), 1, 0)
		else:
			self.current_hotel_data.loc[:, "breakfastRank"] = 0

		self.current_hotel_data.loc[:, "totalRank"] = self.current_hotel_data.loc[:, "rateRank"] * ratePrio + \
													self.current_hotel_data.loc[:, "distRank"]	* distPrio + \
													self.current_hotel_data.loc[:, "wifiRank"]	* wifiPrio + \
													self.current_hotel_data.loc[:, "breakfastRank"]	* breakfastPrio

		self.current_hotel_data.loc[:, "totalPrice"] = self.current_hotel_data.loc[:, "Total Price"].str.replace('$', '').str.replace(',','').astype(int)


		self.current_hotel_data = self.current_hotel_data.sort_values(['totalRank', 'totalPrice', 'dist'], ascending = [False, True, True]).reset_index()
		# print(self.current_hotel_data.loc[:, "rateRank":])
		# print(self.current_hotel_data.loc[:, "totalRank":])

		self.enter_hotel_table_data()



	def on_radio_button_toggled(self):
		radio_button = self.sender()

		self.clear_departure_flight_table()
		self.clear_return_flight_table()


		if radio_button == self.flight_trip_round:
			self.flight_return_date_entry.setEnabled(True)
			self.flight_return_date_entry.setVisible(True)
			self.flight_ret_date_label.setVisible(True)

			self.return_flight_table.setVisible(True)
			self.return_flight_table_label.setVisible(True)

			self.ret_flight_table_details.setVisible(True)
			self.ret_flight_table_details_label.setVisible(True)
			self.return_flight_table_button.setVisible(True)

			self.confirm_ret_flight_panel.setVisible(True)
		else:
			self.flight_return_date_entry.setEnabled(False)
			self.flight_return_date_entry.setVisible(False)
			self.flight_ret_date_label.setVisible(False)

			self.return_flight_table.setVisible(False)
			self.return_flight_table_label.setVisible(False)

			self.ret_flight_table_details.setVisible(False)
			self.ret_flight_table_details_label.setVisible(False)
			self.return_flight_table_button.setVisible(False)

			self.confirm_ret_flight_panel.setVisible(False)

		self.flight_trip_type = radio_button.text()

	def on_leg_box_button_toggled(self):
		box_button = self.sender()
		if self.flight_leg_box_1.isChecked() and box_button == self.flight_leg_box_1:
			self.flight_leg_box_2.setChecked(False)
			self.flight_leg_box_3.setChecked(False)

		if self.flight_leg_box_2.isChecked() and box_button == self.flight_leg_box_2:
			self.flight_leg_box_1.setChecked(False)
			self.flight_leg_box_3.setChecked(False)

		if self.flight_leg_box_3.isChecked() and box_button == self.flight_leg_box_3:
			self.flight_leg_box_1.setChecked(False)
			self.flight_leg_box_2.setChecked(False)

	def on_time_box_button_toggled(self):
		box_button = self.sender()
		if self.flight_time_box_1.isChecked() and box_button == self.flight_time_box_1:
			self.flight_time_box_2.setChecked(False)
			self.flight_time_box_3.setChecked(False)

		if self.flight_time_box_2.isChecked() and box_button == self.flight_time_box_2:
			self.flight_time_box_1.setChecked(False)
			self.flight_time_box_3.setChecked(False)

		if self.flight_time_box_3.isChecked() and box_button == self.flight_time_box_3:
			self.flight_time_box_1.setChecked(False)
			self.flight_time_box_2.setChecked(False)

	def on_rating_box_button_toggled(self):
		box_button = self.sender()
		if self.hotel_rating_box_1.isChecked() and box_button == self.hotel_rating_box_1:
			self.hotel_rating_box_2.setChecked(False)
			self.hotel_rating_box_3.setChecked(False)

		if self.hotel_rating_box_2.isChecked()and box_button == self.hotel_rating_box_2:
			self.hotel_rating_box_1.setChecked(False)
			self.hotel_rating_box_3.setChecked(False)

		if self.hotel_rating_box_3.isChecked()and box_button == self.hotel_rating_box_3:
			self.hotel_rating_box_1.setChecked(False)
			self.hotel_rating_box_2.setChecked(False)

	def on_distance_box_button_toggled(self):
		box_button = self.sender()
		if self.hotel_distance_box_1.isChecked() and box_button == self.hotel_distance_box_1:
			self.hotel_distance_box_2.setChecked(False)
			self.hotel_distance_box_3.setChecked(False)

		if self.hotel_distance_box_2.isChecked()and box_button == self.hotel_distance_box_2:
			self.hotel_distance_box_1.setChecked(False)
			self.hotel_distance_box_3.setChecked(False)

		if self.hotel_distance_box_3.isChecked()and box_button == self.hotel_distance_box_3:
			self.hotel_distance_box_1.setChecked(False)
			self.hotel_distance_box_2.setChecked(False)

	def on_menu_button_clicked(self):
		push_button = self.sender()
		page_order = ["Flights", "Hotels", "Confirmation"]

		self.flight_rank_options_frame.setVisible(False)
		self.hotel_rank_options_frame.setVisible(False)

		# Identify current page
		if self.flight_frame.isVisible():
			current_page = "Flights"
		elif self.hotel_frame.isVisible():
			current_page = "Hotels"
		else:
			current_page = "Confirmation"

		# Functionality for next page button
		if push_button == self.next_menu_button:
			new_page = page_order[page_order.index(current_page) + 1] if page_order.index(current_page) + 1 < len(page_order) else page_order[-1]
			next_page = page_order[page_order.index(current_page) + 2] if page_order.index(current_page) + 2 < len(page_order) else ""
			self.prev_menu_button.setText(current_page)
			self.next_menu_button.setText(next_page)
			# print(current_page)
			# print(new_page)
			# print(next_page)
			self.change_page(new_page)

			self.prev_menu_button.setVisible(True)
			if page_order.index(new_page) == len(page_order) - 1:
				self.next_menu_button.setVisible(False)

		# Functionality for prev page button
		if push_button == self.prev_menu_button:
			new_page = page_order[page_order.index(current_page) - 1] if page_order.index(current_page) - 1 >= 0 else page_order[0]
			prev_page = page_order[page_order.index(current_page) - 2] if page_order.index(current_page) - 2 >= 0 else ""
			self.next_menu_button.setText(current_page)
			self.prev_menu_button.setText(prev_page)
			# print(current_page)
			# print(new_page)
			# print(prev_page)
			self.change_page(new_page)

			self.next_menu_button.setVisible(True)
			if page_order.index(new_page) == 0:
				self.prev_menu_button.setVisible(False)

	def change_page(self, new_page):
		if new_page == "Flights":
			self.hotel_frame.setVisible(False)
			self.confirm_frame.setVisible(False)
			self.flight_frame.setVisible(True)
				
		if new_page == "Hotels":
			self.flight_frame.setVisible(False)
			self.confirm_frame.setVisible(False)
			self.hotel_frame.setVisible(True)

		if new_page == "Confirmation":
			self.flight_frame.setVisible(False)
			self.hotel_frame.setVisible(False) 
			self.confirm_frame.setVisible(True)

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


if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = FlightSearchApp()
	window.show()
	sys.exit(app.exec_())
