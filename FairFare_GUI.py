import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from Google_Flights_Scraper import search_flights  # Import from Google_Flights_Scraper.py

class FlightSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up the main layout
        self.setWindowTitle("Flight Search")
        layout = QVBoxLayout()

        # Add input fields for each parameter
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
        self.max_price_entry = QLineEdit(self)
        self.max_price_entry.setPlaceholderText("Enter max price (optional)")
        layout.addWidget(QLabel("Max Price (optional):"))
        layout.addWidget(self.max_price_entry)

        self.min_time_entry = QLineEdit(self)
        self.min_time_entry.setPlaceholderText("Enter minimum departure time (optional, HH:MM)")
        layout.addWidget(QLabel("Min Departure Time (optional):"))
        layout.addWidget(self.min_time_entry)

        self.max_time_entry = QLineEdit(self)
        self.max_time_entry.setPlaceholderText("Enter maximum departure time (optional, HH:MM)")
        layout.addWidget(QLabel("Max Departure Time (optional):"))
        layout.addWidget(self.max_time_entry)

        # Search button
        search_button = QPushButton("Search Flights", self)
        search_button.clicked.connect(self.on_search_clicked)
        layout.addWidget(search_button)

        self.setLayout(layout)

    def on_search_clicked(self):
        # Retrieve values from the input fields
        departure_id = self.departure_entry.text()
        arrival_id = self.arrival_entry.text()
        outbound_date = self.outbound_date_entry.text()
        return_date = self.return_date_entry.text()
        currency = self.currency_entry.text()
        max_price = self.max_price_entry.text()
        min_time = self.min_time_entry.text()
        max_time = self.max_time_entry.text()

        # Ensure required fields are filled
        if not (departure_id and arrival_id and outbound_date and return_date and currency):
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return

        # Call the API function with collected inputs
        results = search_flights(departure_id, arrival_id, outbound_date, return_date, currency, max_price, min_time, max_time)

        # Display results in a message box
        QMessageBox.information(self, "Search Results", str(results))

# Main function to run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = FlightSearchApp()
    mainWin.show()
    sys.exit(app.exec_())
