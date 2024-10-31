import sys

from qrangeslider import QRangeSlider

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QListWidget, QTextEdit, QMessageBox, QDateTimeEdit, QComboBox, QHBoxLayout
)
from PyQt5.QtCore import (
    QDate, Qt
)
from PyQt5.QtGui import (
    QPixmap
)
from Google_Flights_Scraper import search_flights  # Import the flight search function

import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
from datetime import datetime

# Stylesheet information for GUI layout

QCOMBO_HEIGHT = 50

# QLABEL_BASE = "QLabel {{background: #{}; color: #00aeef; border: 3px inset #5252cc; font: 'Noto Serif';}}"
# # QLABEL_DEFAULT = "QLabel {background: #002050; color: #00aeef; border: 3px outset #5252cc; font: 'Noto Serif'; font-size: 50pt;}"
# QLABEL_DEFAULT = "QWidget {font: 'Noto Serif'; font-size: 16pt; text-align: center; background: #000000; color: #ffffff; border: 0px outset #696969;} \
                    # QLabel {font: 'Noto Serif'; font-size: 30pt; qproperty-alignment: AlignCenter; background: #000000; color: #ffffff; border: 3px outset #696969;}"
QLABEL_GUI = "QLabel {height: 40; font: 'Noto Serif'; font-size: 16pt; text-align: center; qproperty-alignment: AlignCenter; background: #343f62; color: #ffffff;} \
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
QLABEL_ICON = "QLabel {qproperty-alignment: AlignCenter; border: 0px outset #696969; width: 10; height: 10;}"
QLABEL_TITLE = "QLabel {width: 30; height: 40; font: 'Noto Serif'; font-size: 45pt; text-align: center; qproperty-alignment: AlignCenter; background: #343f62; color: #ffffff; font-weight: bold; font-style: italic;}"
    

GUI_HEIGHT = 750
GUI_WIDTH = 1000


# SERP_API_KEY = "b637153e8613b18fc81533dfbf72045c9b43cbdd25323736bc3009ee6c38435a"  
SERP_API_KEY = "8e3b97559f70aeb1a2d6f78da4ca024bab7525e316361ac1c955016a16136cf7"

#Font Code
# class Font(QFont):
#     def __init__(self, size):
#         super().__init__()
#         self.setFamily("Noto Serif")
#         self.setStyleHint(QFont.StyleHint.Times)
#         self.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
#         self.setPointSize(size)
#         self.setHintingPreference(QFont.HintingPreference.PreferFullHinting)

class FlightSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Flight Search")
        self.setGeometry(300, 100, GUI_WIDTH, GUI_HEIGHT)

        app.setStyleSheet(QLABEL_GUI)

        # Get list of all airport codes and locations

        self.get_all_airports()

        logo_label = QLabel(self)
        logo_label.setPixmap(QPixmap("logo.png")) #.scaled(10, 20, Qt.KeepAspectRatio))
        logo_label.setFixedWidth(100)
        logo_label.setFixedHeight(100)
        logo_label.setScaledContents(True)
        logo_label.setStyleSheet(QLABEL_ICON)

        logo_title = QLabel("FAIRFARE")
        logo_title.setStyleSheet(QLABEL_TITLE)

        logo_layout = QHBoxLayout()
        logo_layout.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(logo_label)
        logo_layout.addWidget(logo_title)

        # Input fields for search parameters

            # Departure Airport Code parameter
        self.departure_entry = QLineEdit(self)
        self.departure_entry.setPlaceholderText("Enter departure airport code (e.g., CDG)")
                # Parameter layout
        dep_airport_layout = QVBoxLayout()
        dep_airport_layout.addWidget(QLabel("Departure Airport Code:"))
        dep_airport_layout.addWidget(self.departure_entry)

            # Arrival Airport Code parameter
        self.arrival_entry = QLineEdit(self)
        self.arrival_entry.setPlaceholderText("Enter arrival airport code (e.g., AUS)")
                # Parameter layout
        arr_airport_layout = QVBoxLayout()
        arr_airport_layout.addWidget(QLabel("Arrival Airport Code:"))
        arr_airport_layout.addWidget(self.arrival_entry)

            # Outbound Date parameter
        self.outbound_date_entry = QDateTimeEdit(self)
        self.outbound_date_entry.setCalendarPopup(True)
        self.outbound_date_entry.setDate(QDate.currentDate())
        self.outbound_date_entry.setDisplayFormat('yyyy-MM-dd')

                # Parameter layout
        out_date_layout = QVBoxLayout()
        out_date_layout.addWidget(QLabel("Outbound Date:"))
        out_date_layout.addWidget(self.outbound_date_entry)

            # Return Date parameter
        self.return_date_entry = QDateTimeEdit(self)
        self.return_date_entry.setCalendarPopup(True)
        self.return_date_entry.setDate(QDate.currentDate())
        self.return_date_entry.setDisplayFormat('yyyy-MM-dd')

                # Parameter Layout
        ret_date_layout = QVBoxLayout()
        ret_date_layout.addWidget(QLabel("Return Date:"))
        ret_date_layout.addWidget(self.return_date_entry)

        self.get_all_currencies()
        self.currency_entry = QComboBox(self)
        self.currency_entry.addItems(self.all_currencies.keys())
        self.currency_entry.setCurrentText('USD')

        currency_entry_layout = QVBoxLayout()
        currency_entry_layout.addWidget(QLabel("Currency Code:"))
        currency_entry_layout.addWidget(self.currency_entry)

        self.currency_details = QLabel(self.all_currencies[self.currency_entry.currentText()])
        self.currency_entry.currentTextChanged.connect(lambda _: self.currency_details.setText(self.all_currencies[self.currency_entry.currentText()]))

        currency_layout = QHBoxLayout()
        currency_layout.addLayout(currency_entry_layout)
        currency_layout.addWidget(self.currency_details)


        # Optional fields

        self.max_cost_entry = QLineEdit(self)
        self.max_cost_entry.setPlaceholderText("Enter maximum cost (optional)")
        max_cost_layout = QVBoxLayout()
        max_cost_layout.addWidget(QLabel("Maximum Cost (Optional):"))
        max_cost_layout.addWidget(self.max_cost_entry)

        self.time_entry = QRangeSlider(self)
        self.time_entry.setFixedHeight(50)
        self.time_entry.setMin(0)
        self.time_entry.setMax(180)
        self.time_entry.setRange(0, 180)
        

        self.time_entry.handle.setStyleSheet('border: 0px; background-color:gray') 
        self.time_entry.head.setStyleSheet('border: 0px; background-color:#232b42')
        self.time_entry.tail.setStyleSheet('border: 0px; background-color:#232b42')

        print(self.time_entry.start())
        print(self.time_entry.end())
        self.time_entry.handle.setTextColor(255)

        # self.time_entry.setRange(500, 1253)
        

        # self.time_entry = QLineEdit(self)
        # self.time_entry.setPlaceholderText("Enter minimum flight time in minutes (optional)")
        time_layout = QVBoxLayout()
        time_layout.addWidget(QLabel("Minimum and Maximum Flight Time (Optional):"))
        time_layout.addWidget(self.time_entry)
        

        # self.max_time_entry = QLineEdit(self)
        # self.max_time_entry.setPlaceholderText("Enter maximum flight time in minutes (optional)")
        # max_time_layout = QVBoxLayout()
        # max_time_layout.addWidget(QLabel("Maximum Flight Time (Optional):"))
        # max_time_layout.addWidget(self.max_time_entry)
        

        # Search button
        search_button = QPushButton("Search Flights", self)
        search_button.clicked.connect(self.on_search_clicked)
        

        # List widget for displaying flights
        self.flight_list = QListWidget(self)
        self.flight_list.itemClicked.connect(self.display_flight_details)
        

        # Text edit for displaying flight details
        self.flight_details = QTextEdit(self)
        self.flight_details.setReadOnly(True)
        

        # Insert all data in layout
        airport_code_layout = QHBoxLayout()
        airport_code_layout.addLayout(dep_airport_layout)
        airport_code_layout.addLayout(arr_airport_layout)

        date_layout = QHBoxLayout()
        date_layout.addLayout(out_date_layout)
        date_layout.addLayout(ret_date_layout)

        other1_layout = QHBoxLayout()
        other1_layout.addLayout(currency_layout)
        other1_layout.addLayout(max_cost_layout)

        other2_layout = QHBoxLayout()
        other2_layout.addLayout(time_layout)
        # other2_layout.addLayout(max_time_layout)
        
        flight_info_layout = QHBoxLayout()
        flight_info_layout.addWidget(self.flight_list)
        flight_info_layout.addWidget(self.flight_details)

        layout = QVBoxLayout()
        layout.addLayout(logo_layout)
        layout.addLayout(airport_code_layout)
        layout.addLayout(date_layout)
        layout.addLayout(other1_layout)
        layout.addLayout(other2_layout)
        layout.addWidget(search_button)
        layout.addLayout(flight_info_layout)
        self.setLayout(layout)

    def on_outbound_date_calendar_clicked(self):
    # Toggle calendar widget once clicked
        self.outbound_date_entry.setText(self.outbound_date_calendar.selectedDate().toString())
        self.outbound_date_calendar.setVisible(False)

    def on_return_date_calendar_clicked(self):
    # Toggle calendar widget once clicked
        self.return_date_entry.setText(self.return_date_calendar.selectedDate().toString())
        self.return_date_calendar.setVisible(False)

    def get_all_currencies(self):
    # Get all currency abbreviations and names
        r = requests.get("https://developers.google.com/adsense/management/appendix/currencies")
        soup = BeautifulSoup(r.text, "html.parser")
        # table = soup.find('tbody')
        rows = soup.find_all('tr')
        self.all_currencies = {r.find_all('td')[0].text: r.find_all('td')[1].text for r in rows if "(" not in r.find_all('td')[1].text}

    def get_all_airports(self):
    # Get all airport abbreviations and names
        r = requests.get("https://www.bts.gov/topics/airlines-and-airports/world-airport-codes")
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find('tbody')
        rows = table.find_all('tr')
        self.all_airports = {i.find_all('td')[0].text : {'City':i.find_all('td')[1].text.split(': ')[0], 'Airport':i.find_all('td')[1].text.split(': ')[0]} for i in rows}


    def on_search_clicked(self):
        # Clear previous search results
        self.flight_list.clear()
        self.flight_details.clear()

        # Retrieve input values
        departure_id = self.departure_entry.text()
        arrival_id = self.arrival_entry.text()
        outbound_date = self.outbound_date_entry.text()
        return_date = self.return_date_entry.text()
        currency = self.currency_entry.currentText()
        max_cost = self.max_cost_entry.text()  # Optional max cost input
        min_time = self.time_entry.start()  # Optional minimum time input
        max_time = self.time_entry.end()  # Optional maximum time input

        # pprint([departure_id, arrival_id, outbound_date, return_date, currency, max_cost, min_time, max_time])
        # pprint([type(departure_id), type(arrival_id), type(outbound_date), type(return_date), type(currency), type(max_cost), type(min_time), type(max_time)])


        # Check for required fields
        if not all([departure_id, arrival_id, outbound_date, return_date, currency]):
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return

        # Get flight data with optional parameters
        flight_data = search_flights(
            departure_id, arrival_id, outbound_date, return_date, currency,
            max_price=max_cost if max_cost else None,
            min_time=min_time if min_time else None,
            max_time=max_time if max_time else None
        )

        # Handle no results or errors
        if not flight_data or isinstance(flight_data, str):
            QMessageBox.information(self, "No Results", str(flight_data) if flight_data else "No flights found.")
            return

        # Display flight options in the list
        for flight in flight_data:
            item_text = f"${flight['price']} | {flight['type']} | {flight['total_duration']} min"
            self.flight_list.addItem(item_text)

        # Save the flight data to display when an item is selected
        self.current_flight_data = flight_data

    def display_flight_details(self, item):
    # Get index of the selected item
        index = self.flight_list.row(item)

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
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlightSearchApp()
    window.show()
    sys.exit(app.exec_())
