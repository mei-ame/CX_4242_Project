import sys

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

import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
from datetime import datetime

# Stylesheet information for GUI layout

GUI_HEIGHT = 750
GUI_WIDTH = 1500
GUI_PANEL_WIDTH = 300

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
        #Connect itemClicked here
    #     self.itemClicked.connect(self.onItemClicked)                                            #BUILD
    
    # def onItemClicked(self, item):
    #     choice = item.text()
    #     board = self.window().board
    #     if board.tries < board.numOfGuesses:
    #         board.guess = list(choice)
    #         for i, l in zip(range(5), choice):
    #             board.grid.itemAtPosition(board.tries, i).widget().setText(l)
    #         board.evaluate()

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

        ############################################################################################################
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

            # Departure Date parameter
        self.departure_date_entry = QDateTimeEdit(self)
        self.departure_date_entry.setCalendarPopup(True)
        self.departure_date_entry.setDate(QDate.currentDate())
        self.departure_date_entry.setDisplayFormat('yyyy-MM-dd')

                # Parameter layout
        out_date_layout = QVBoxLayout()
        out_date_layout.addWidget(QLabel("Departure Date:"))
        out_date_layout.addWidget(self.departure_date_entry)

            # Return Date parameter
        self.return_date_entry = QDateTimeEdit(self)
        self.return_date_entry.setCalendarPopup(True)
        self.return_date_entry.setDate(QDate.currentDate())
        self.return_date_entry.setDisplayFormat('yyyy-MM-dd')
        self.return_date_entry.setEnabled(False)

                # Parameter Layout
        ret_date_layout = QVBoxLayout()
        self.ret_date_label = QLabel("Return Date:")
        ret_date_layout.addWidget(self.ret_date_label)
        ret_date_layout.addWidget(self.return_date_entry)

        self.get_all_currencies()
        self.currency_entry = QComboBox(self)
        self.currency_entry.addItems(self.all_currencies.keys())
        self.currency_entry.setCurrentText('USD')

        currency_entry_layout = QVBoxLayout()
        currency_entry_layout.addWidget(QLabel("Currency:"))
        currency_entry_layout.addWidget(self.currency_entry)

        self.currency_details = QLabel(self.all_currencies[self.currency_entry.currentText()])
        self.currency_entry.currentTextChanged.connect(lambda _: self.currency_details.setText(self.all_currencies[self.currency_entry.currentText()]))

        currency_layout = QHBoxLayout()
        currency_layout.addLayout(currency_entry_layout)
        # currency_layout.addWidget(self.currency_details)

        ############################################################################################################
        # OPTIONAL FIELDS 

        # Trip Type
        
        self.trip_round = QRadioButton("Round Trip")
        self.trip_one = QRadioButton("One Way")
        self.trip_multi = QRadioButton("Multi-city")

        self.trip_round.toggled.connect(self.on_radio_button_toggled)
        self.trip_one.toggled.connect(self.on_radio_button_toggled)
        self.trip_multi.toggled.connect(self.on_radio_button_toggled)
        self.trip_round.setChecked(True)

        trip_layout = QVBoxLayout()
        trip_layout.addWidget(QLabel("Trip Type"))
        trip_layout.addWidget(self.trip_round)
        trip_layout.addWidget(self.trip_one)
        trip_layout.addWidget(self.trip_multi)

        # Min and Max Time

        self.time_min_entry = QLineEdit(self)
        self.time_min_entry.setPlaceholderText("-")

        time_min_layout = QVBoxLayout()
        time_min_layout.addWidget(QLabel("Min"))
        time_min_layout.addWidget(self.time_min_entry)

        self.time_max_entry = QLineEdit(self)
        self.time_max_entry.setPlaceholderText("-")

        time_max_layout = QVBoxLayout()
        time_max_layout.addWidget(QLabel("Max"))
        time_max_layout.addWidget(self.time_max_entry)

        time_range_layout = QHBoxLayout()
        time_range_layout.addLayout(time_min_layout)
        time_range_layout.addWidget(QLabel(" - "))
        time_range_layout.addLayout(time_max_layout)

        time_layout = QVBoxLayout()
        time_layout.addWidget(QLabel("Flight Time (min)"))
        time_layout.addLayout(time_range_layout)

        # Min and Max Cost

        self.cost_min_entry = QLineEdit(self)
        self.cost_min_entry.setPlaceholderText("-")

        cost_min_layout = QVBoxLayout()
        cost_min_layout.addWidget(QLabel("Min"))
        cost_min_layout.addWidget(self.cost_min_entry)

        self.cost_max_entry = QLineEdit(self)
        self.cost_max_entry.setPlaceholderText("-")

        cost_max_layout = QVBoxLayout()
        cost_max_layout.addWidget(QLabel("Max"))
        cost_max_layout.addWidget(self.cost_max_entry)

        cost_range_layout = QHBoxLayout()
        cost_range_layout.addLayout(cost_min_layout)
        cost_range_layout.addWidget(QLabel(" - "))
        cost_range_layout.addLayout(cost_max_layout)

        cost_layout = QVBoxLayout()
        cost_layout.addWidget(QLabel("Cost ($)"))
        cost_layout.addLayout(cost_range_layout)
        

        # Search button
        search_button = QPushButton("Search Flights", self)
        search_button.clicked.connect(self.on_search_clicked)
        

        # List widget for displaying flights
        self.flight_list = QListWidget(self)
        self.flight_list.itemClicked.connect(self.display_flight_details)
        

        # Text edit for displaying flight details
        self.flight_details = QTextEdit(self)
        self.flight_details.setReadOnly(True)

        # Table widget for flight information
        self.flight_table = QTableWidget(self)
        self.flight_table.setColumnCount(7)
        self.flight_table.setRowCount(1)
        flight_table_columns = ["Airline", "Price", "Type", "Departure", "Arrival", "Arrival Date", "Travel Class"]
        for i in range(self.flight_table.columnCount()):
            self.flight_table.setItem(0 , i, QTableWidgetItem(flight_table_columns[i]))
            self.flight_table.item(0, i).setBackground(QColor(30,38,64))
        self.flight_table.horizontalHeader().setVisible(False)
        self.flight_table.verticalHeader().setVisible(False)
        self.flight_table.cellClicked.connect(self.flights_select_row)
        self.flight_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.flight_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.flight_table.setShowGrid(False)
        
        ############################################################################################################
        # Insert all data in layout

        airport_code_layout = QHBoxLayout()
        airport_code_layout.addLayout(dep_airport_layout)
        airport_code_layout.addLayout(arr_airport_layout)

        date_layout = QHBoxLayout()
        date_layout.addLayout(out_date_layout)
        date_layout.addLayout(ret_date_layout)

        code_and_date_layout = QHBoxLayout()
        code_and_date_layout.addLayout(airport_code_layout)
        code_and_date_layout.addLayout(date_layout)
        
        flight_info_layout = QHBoxLayout()
        flight_info_layout.addWidget(self.flight_list)
        flight_info_layout.addWidget(self.flight_details)
        self.flight_list.setVisible(False)
        self.flight_details.setVisible(False)

        left_panel_layout = QVBoxLayout()
        left_panel_layout.addLayout(trip_layout)
        left_panel_layout.addWidget(QLabel(" "))
        left_panel_layout.addLayout(time_layout)
        left_panel_layout.addWidget(QLabel(" "))
        left_panel_layout.addLayout(cost_layout)
        left_panel_layout.addWidget(QLabel(" "))
        left_panel_layout.addLayout(currency_layout)
        left_panel_layout.setSpacing(0)

        self.left_panel = QFrame(self)
        self.left_panel.setLayout(left_panel_layout)
        self.left_panel.setFixedWidth(200)
        self.left_panel.setStyleSheet(QLABEL_LEFT)
        self.left_panel.setFixedHeight(500)


        main_panel = QVBoxLayout()
        main_panel.addLayout(code_and_date_layout)
        main_panel.addWidget(search_button)
        main_panel.addLayout(flight_info_layout)
        main_panel.addWidget(self.flight_table)

        panel_layout = QHBoxLayout()
        panel_layout.addWidget(self.left_panel)
        panel_layout.addLayout(main_panel)

        layout = QVBoxLayout()
        layout.addLayout(logo_layout)
        layout.addLayout(panel_layout)
        self.setLayout(layout)

    def on_departure_date_calendar_clicked(self):
    # Toggle calendar widget once clicked
        self.departure_date_entry.setText(self.departure_date_calendar.selectedDate().toString())
        self.departure_date_calendar.setVisible(False)

    def on_return_date_calendar_clicked(self):
    # Toggle calendar widget once clicked
        self.return_date_entry.setText(self.return_date_calendar.selectedDate().toString())
        self.return_date_calendar.setVisible(False)

    def on_radio_button_toggled(self):
        radio_button = self.sender()
        if radio_button == self.trip_round:
            self.return_date_entry.setEnabled(True)
            self.return_date_entry.setVisible(True)
            self.ret_date_label.setVisible(True)
        else:
            self.return_date_entry.setEnabled(False)
            self.return_date_entry.setVisible(False)
            self.ret_date_label.setVisible(False)

    def flights_select_row(self, row, column):
            self.flight_table.selectRow(row)

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
        departure_id = self.departure_entry.text().upper()
        arrival_id = self.arrival_entry.text().upper()
        departure_date = self.departure_date_entry.text()
        return_date = self.return_date_entry.text()
        # return_date = self.departure_date_entry.text()
        # return_date_2 = self.departure_date_entry.date().addDays(1).toString('yyyy-MM-dd')
        currency = self.currency_entry.currentText()
        max_cost = None if self.cost_max_entry.text() == "-" else self.cost_max_entry.text()  # Optional max cost input
        min_time = None if self.time_min_entry.text() == "-" else self.time_min_entry.text() # Optional minimum time input
        max_time = None if self.time_max_entry.text() == "-" else self.time_max_entry.text() # Optional maximum time input

        # pprint([departure_id, arrival_id, departure_date, return_date, currency, max_cost, min_time, max_time])
        # pprint([type(departure_id), type(arrival_id), type(departure_date), type(return_date), type(currency), type(max_cost), type(min_time), type(max_time)])


        # Check for required fields
        if not all([departure_id, arrival_id, departure_date, return_date, currency]):
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return

        # Get flight data with optional parameters
        flight_data = search_flights(
            departure_id, arrival_id, departure_date, return_date, currency,
            max_price=max_cost if max_cost else None,
            min_time=min_time if min_time else None,
            max_time=max_time if max_time else None
        )
        
        # flight_data.extend(search_flights(
        #     departure_id, arrival_id, departure_date, return_date_2, currency,
        #     max_price=max_cost if max_cost else None,
        #     min_time=min_time if min_time else None,
        #     max_time=max_time if max_time else None
        # ))

        # Handle no results or errors
        if not flight_data or isinstance(flight_data, str):
            QMessageBox.information(self, "No Results", str(flight_data) if flight_data else "No flights found.")
            return

        # Display flight options in the list
        flight_list_headers = ["Airline", "Price", "Type", "Departure", "Arrival", "Travel Class"]
        self.flight_list.addItem("\t".join(flight_list_headers))

        for flight in flight_data:
            pprint(flight)
            # item_text = f"${flight['price']} \t {flight['type']} \t {flight['total_duration']} min"
            item_list = [flight['flights'][0]['airline'], "$" + str(flight['price']), flight['type'], \
                self.time_to_12(flight['flights'][0]['departure_time']), self.time_to_12(flight['flights'][-1]['arrival_time']), \
                flight['flights'][0]['travel_class']  ]
            item_text = "\t".join(item_list)
            self.flight_list.addItem(item_text)

            # Add flight information into the table ["Airline", "Price", "Type", "Departure", "Arrival", "Travel Class"]
            format_string = "%Y-%m-%d %H:%M"
            rowPosition = self.flight_table.rowCount()
            self.flight_table.insertRow(rowPosition)
            self.flight_table.setItem(rowPosition , 0, QTableWidgetItem(flight['flights'][0]['airline']))
            self.flight_table.setItem(rowPosition , 1, QTableWidgetItem("$" + str(flight['price'])))
            self.flight_table.setItem(rowPosition , 2, QTableWidgetItem(flight['type']))
            self.flight_table.setItem(rowPosition , 3, QTableWidgetItem(self.time_to_12(flight['flights'][0]['departure_time'])))
            self.flight_table.setItem(rowPosition , 4, QTableWidgetItem(self.time_to_12(flight['flights'][-1]['arrival_time'])))
            self.flight_table.setItem(rowPosition , 5, QTableWidgetItem(flight['flights'][0]['arrival_time'].split(" ")[0]))
            self.flight_table.setItem(rowPosition , 6, QTableWidgetItem(flight['flights'][0]['travel_class']))

        # Save the flight data to display when an item is selected
        self.current_flight_data = flight_data

    def time_to_12(self, time):
        return "12:" + time.split(" ")[-1].split(":")[1] + " PM" \
            if int(time.split(" ")[-1].split(":")[0]) == 12 \
            else "12:" + time.split(" ")[-1].split(":")[1] + " AM" \
            if int(time.split(" ")[-1].split(":")[0]) == 24 \
            else time.split(" ")[-1].split(":")[0].lstrip("0") + ":" + time.split(" ")[-1].split(":")[1] + " AM" \
            if int(time.split(" ")[-1].split(":")[0]) < 12 \
            else str(int(time.split(" ")[-1].split(":")[0]) % 12).lstrip("0") + ":" + time.split(" ")[-1].split(":")[1] + " PM" \

    def display_flight_details(self, item):
    # Get index of the selected item
        index = self.flight_list.row(item)

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
