# FairFare - Affordable Travel Planning Made Simple

FairFare is a travel planning tool designed to help budget-conscious travelers find affordable flights and accommodations without the influence of paid promotions. Unlike platforms like Expedia or Kayak, FairFare prioritizes transparency and personalization. Using data from Google Flights and Hotels APIs, FairFare applies the **Skyline Extraction Method** to filter and rank results based on your preferences—such as price, layovers, and amenities.

With FairFare, users can:
- Find the most cost-effective options for flights and hotels.
- Personalize results by prioritizing key features.
- Enjoy an intuitive interface for streamlined trip planning.

FairFare ensures that travel planning experience is affordable and hassle-free.

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mei-ame/CX_4242_Project.git
   cd CX_4242_Project
   ```

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Execution

1. **Run the application**:
   ```bash
   python FairFare_GUI.py
   ```

2. **Local interaction**:
   - Once the application launches, a graphical user interface (GUI) will appear.
   - Follow the on-screen prompts to enter travel details such as dates, budget, and preferences

3. **Explore the Demo**:
   Follow these steps to interact with the application:
     1. **Flight Selection**:
         - Navigate to the *Flights Page* to view a table of flight options tailored to your criteria.
         - Columns include flight price, number of layovers, travel duration, and departure/arrival times.
         - Use sorting and filtering tools to refine your selection further.

      2. **Hotel Selection**:
         - Switch to the *Hotels Page* to browse a table of accommodation options.
         - The table provides details such as hotel name, price per night, distance from the airport, and included amenities.
         - Customize the ranking of features to prioritize options that match your preferences.

      3. **Review Your Selections**:
         - Proceed to the *Confirmation Page* to view a summary of your chosen flight and hotel.
         - Ensure all details align with your preferences before finalizing your trip plan.

---