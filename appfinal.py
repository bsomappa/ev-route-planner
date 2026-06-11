%%writefile app.py

import streamlit as st
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI-Based EV Route Planning System",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("AI-Based EV Route Planning System")

st.write("Intelligent electric vehicle route optimization considering:")
st.write("• Traffic conditions")
st.write("• Vehicle battery constraints")
st.write("• Energy consumption prediction")
st.write("• Route feasibility analysis")

# ---------------------------------------------------
# VEHICLE DATABASE
# ---------------------------------------------------

vehicle_data = {

    "Tata Nexon EV": {
        "battery": 40.5,
        "consumption": 0.14
    },

    "MG ZS EV": {
        "battery": 50.3,
        "consumption": 0.16
    },

    "Hyundai Kona EV": {
        "battery": 39.2,
        "consumption": 0.15
    },

    "Mahindra XUV400 EV": {
        "battery": 39.4,
        "consumption": 0.15
    },

    "Tata Tiago EV": {
        "battery": 24,
        "consumption": 0.11
    },

    "BYD Atto 3": {
        "battery": 60.5,
        "consumption": 0.17
    },

    "Ola S1 Pro": {
        "battery": 4,
        "consumption": 0.04
    },

    "Ather 450X": {
        "battery": 3.7,
        "consumption": 0.03
    },

    "TVS iQube": {
        "battery": 3.4,
        "consumption": 0.03
    },

    "Simple One": {
        "battery": 5,
        "consumption": 0.04
    }
}

# ---------------------------------------------------
# INPUT SECTION
# ---------------------------------------------------

st.header("Route Input Parameters")

col1, col2 = st.columns(2)

with col1:
   source = st.text_input(
    "Start Location",
    placeholder="Enter source city"
)

with col2:
    destination = st.text_input(
    "Destination Location",
    placeholder="Enter destination city"
)
# ---------------------------------------------------
# VEHICLE SELECTION
# ---------------------------------------------------

vehicle = st.selectbox(
    "Select Electric Vehicle",
    list(vehicle_data.keys())
)

# ---------------------------------------------------
# VEHICLE PARAMETERS
# ---------------------------------------------------

total_battery = vehicle_data[vehicle]["battery"]

consumption_factor = vehicle_data[vehicle]["consumption"]

# ---------------------------------------------------
# DISPLAY VEHICLE DETAILS
# ---------------------------------------------------

col3, col4 = st.columns(2)

with col3:
    st.info(
        f"Total Battery Capacity: "
        f"{total_battery} kWh"
    )

with col4:
    st.info(
        f"Energy Consumption: "
        f"{consumption_factor} kWh/km"
    )

# ---------------------------------------------------
# REMAINING BATTERY INPUT
# ---------------------------------------------------

available_battery = st.slider(
    "Available Remaining Battery (kWh)",
    1.0,
    float(total_battery),
    float(total_battery / 2)
)

# ---------------------------------------------------
# TRAFFIC CONDITION
# ---------------------------------------------------

traffic = st.selectbox(
    "Traffic Condition",
    ["Low", "Medium", "High"]
)

# ---------------------------------------------------
# BUTTON
# ---------------------------------------------------

if st.button("Find Optimal EV Route"):

    try:

        # ---------------------------------------------------
        # GEOLOCATION
        # ---------------------------------------------------

      geolocator = Nominatim(
            user_agent="ev_route_planner",
                          timeout=10
         )

source_location = geolocator.geocode(
source,
timeout=10
)

destination_location = geolocator.geocode(
destination,
timeout=10
)

if source_location is None or destination_location is None:

st.error(
    "Invalid source or destination location"
)

st.stop()
        source_coords = (
            source_location.latitude,
            source_location.longitude
        )

        destination_coords = (
            destination_location.latitude,
            destination_location.longitude
        )

        # ---------------------------------------------------
        # DISTANCE CALCULATION
        # ---------------------------------------------------

        distance = geodesic(
            source_coords,
            destination_coords
        ).km

        # ---------------------------------------------------
        # TRAFFIC CONDITIONS
        # ---------------------------------------------------

        if traffic == "Low":

            speed = 48
            traffic_factor = 1.0

        elif traffic == "Medium":

            speed = 35
            traffic_factor = 1.3

        else:

            speed = 25
            traffic_factor = 1.6

        # ---------------------------------------------------
        # TRAVEL TIME
        # ---------------------------------------------------

        travel_time_hours = distance / speed

        travel_time_minutes = (
            travel_time_hours * 60
        )

        # ---------------------------------------------------
        # ENERGY CALCULATION
        # ---------------------------------------------------

        base_energy = (
            distance * consumption_factor
        )

        energy_required = (
            base_energy * traffic_factor
        )

        # ---------------------------------------------------
        # BATTERY ANALYSIS
        # ---------------------------------------------------

        remaining_battery = (
            available_battery - energy_required
        )

        battery_usage = (
            energy_required / available_battery
        ) * 100

        # ---------------------------------------------------
        # ROUTE STATUS
        # ---------------------------------------------------

        if remaining_battery > 0:

            route_status = "APPROVED"

        else:

            route_status = "CHARGING REQUIRED"

        # ---------------------------------------------------
        # RESULTS
        # ---------------------------------------------------

        st.header("Route Analysis Results")

        r1, r2, r3 = st.columns(3)

        with r1:

            st.metric(
                "Distance",
                f"{distance:.2f} km"
            )

        with r2:

            st.metric(
                "Travel Time",
                f"{travel_time_minutes:.2f} mins"
            )

        with r3:

            st.metric(
                "Energy Required",
                f"{energy_required:.2f} kWh"
            )

        # ---------------------------------------------------
        # BATTERY ANALYTICS
        # ---------------------------------------------------

        st.header("Battery Analytics")

        b1, b2, b3 = st.columns(3)

        with b1:

            st.metric(
                "Remaining Battery",
                f"{remaining_battery:.2f} kWh"
            )

        with b2:

            st.metric(
                "Battery Usage",
                f"{battery_usage:.2f} %"
            )

        with b3:

            st.metric(
                "Route Status",
                route_status
            )

        # ---------------------------------------------------
        # BATTERY UTILIZATION BAR
        # ---------------------------------------------------

        st.subheader("Battery Utilization")

        battery_percentage = max(
            0,
            min(100, 100 - battery_usage)
        )

        st.progress(
            int(battery_percentage)
        )

        st.write(
            f"Remaining Battery Capacity: "
            f"{remaining_battery:.2f} kWh"
        )

        # ---------------------------------------------------
        # SYSTEM STATUS
        # ---------------------------------------------------

        st.header("System Status")

        if remaining_battery > 0:

            st.success(
                f"Route Feasibility Status: "
                f"{route_status}"
            )

        else:

            st.error(
                f"Route Feasibility Status: "
                f"{route_status}"
            )

        # ---------------------------------------------------
        # VEHICLE DETAILS OUTPUT
        # ---------------------------------------------------

        st.header("Selected Vehicle Details")

        v1, v2, v3 = st.columns(3)

        with v1:

            st.metric(
                "Vehicle",
                vehicle
            )

        with v2:

            st.metric(
                "Battery Capacity",
                f"{total_battery} kWh"
            )

        with v3:

            st.metric(
                "Consumption",
                f"{consumption_factor} kWh/km"
            )

        # ---------------------------------------------------
        # GOOGLE MAPS
        # ---------------------------------------------------

        st.header("Google Maps Navigation")

        google_maps_url = (
            f"https://www.google.com/maps/dir/"
            f"{source}/{destination}"
        )

        st.markdown(
            f'''
            <a href="{google_maps_url}" target="_blank">
                <button style="
                    background-color:#0b1a3c;
                    color:white;
                    padding:12px;
                    border:none;
                    border-radius:5px;
                    cursor:pointer;">
                    Open Full Route in Google Maps
                </button>
            </a>
            ''',
            unsafe_allow_html=True
        )

    except Exception as e:

        st.error(f"Error: {e}")
