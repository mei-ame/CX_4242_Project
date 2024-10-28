import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QListWidget, QTextEdit, QMessageBox
)
from Google_Flights_Scraper import search_flights  # Import the flight search function

class FlightSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Flight Search")
        self.setGeometry(300, 100, 800, 700)
        layout = QVBoxLayout()

        # Input fields for search parameters
        self.departure_entry = QLineEdit(self)
        self.departure_entry.setPlaceholderText("Enter departure airport code (e.g., CDG)")
        layout.addWidget(QLabel("Departure Airport Code:"))
        layout.addWidget(self.departure_entry)

        self.arrival_entry = QLineEdit(self)
        self.arrival_entry.setPlaceholderText("Enter arrival airport code (e.g., AUS)")
        layout.addWidget(QLabel("Arrival Airport Code:"))
        layout.addWidget(self.arrival_entry)

        self.outbound_date_entry = QLineEdit(self)
        self.outbound_date_entry.setPlaceholderText("Enter outbound date (YYYY-MM-DD)")
        layout.addWidget(QLabel("Outbound Date:"))
        layout.addWidget(self.outbound_date_entry)

        self.return_date_entry = QLineEdit(self)
        self.return_date_entry.setPlaceholderText("Enter return date (YYYY-MM-DD)")
        layout.addWidget(QLabel("Return Date:"))
        layout.addWidget(self.return_date_entry)

        self.currency_entry = QLineEdit(self)
        self.currency_entry.setPlaceholderText("Enter currency code (e.g., USD)")
        layout.addWidget(QLabel("Currency Code:"))
        layout.addWidget(self.currency_entry)

        # Optional fields
        self.max_cost_entry = QLineEdit(self)
        self.max_cost_entry.setPlaceholderText("Enter maximum cost (optional)")
        layout.addWidget(QLabel("Maximum Cost (Optional):"))
        layout.addWidget(self.max_cost_entry)

        self.min_time_entry = QLineEdit(self)
        self.min_time_entry.setPlaceholderText("Enter minimum flight time in minutes (optional)")
        layout.addWidget(QLabel("Minimum Flight Time (Optional):"))
        layout.addWidget(self.min_time_entry)

        self.max_time_entry = QLineEdit(self)
        self.max_time_entry.setPlaceholderText("Enter maximum flight time in minutes (optional)")
        layout.addWidget(QLabel("Maximum Flight Time (Optional):"))
        layout.addWidget(self.max_time_entry)

        # Search button
        search_button = QPushButton("Search Flights", self)
        search_button.clicked.connect(self.on_search_clicked)
        layout.addWidget(search_button)

        # List widget for displaying flights
        self.flight_list = QListWidget(self)
        self.flight_list.itemClicked.connect(self.display_flight_details)
        layout.addWidget(self.flight_list)

        # Text edit for displaying flight details
        self.flight_details = QTextEdit(self)
        self.flight_details.setReadOnly(True)
        layout.addWidget(self.flight_details)

        self.setLayout(layout)

    def on_search_clicked(self):
        # Clear previous search results
        self.flight_list.clear()
        self.flight_details.clear()

        # Retrieve input values
        departure_id = self.departure_entry.text()
        arrival_id = self.arrival_entry.text()
        outbound_date = self.outbound_date_entry.text()
        return_date = self.return_date_entry.text()
        currency = self.currency_entry.text()
        max_cost = self.max_cost_entry.text()  # Optional max cost input
        min_time = self.min_time_entry.text()  # Optional minimum time input
        max_time = self.max_time_entry.text()  # Optional maximum time input

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
