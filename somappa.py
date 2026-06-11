import streamlit as st
import openrouteservice

# ---------------------------------------------------
# OPENROUTESERVICE API
# ---------------------------------------------------

API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjkxOWRmM2U4MTk5YzQ3NzU5NzFhYzU0OWNkOTFkOGQ3IiwiaCI6Im11cm11cjY0In0="

client = openrouteservice.Client(
    key=API_KEY
)

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

st.title("AI-Based Multi-Vehicle EV Route Planning System")

st.write("AI-powered electric vehicle route optimization considering:")
st.write("• Real road distance")
st.write("• Real travel time")
st.write("• Traffic conditions")
st.write("• Battery constraints")
st.write("• Energy consumption prediction")

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
        "battery": 24.0,
        "consumption": 0.11
    },

    "BYD Atto 3": {
        "battery": 60.5,
        "consumption": 0.17
    },

    "Ola S1 Pro": {
        "battery": 4.0,
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
        "battery": 5.0,
        "consumption": 0.04
    }
}

# ---------------------------------------------------
# INPUT PARAMETERS
# ---------------------------------------------------

st.header("Route Input Parameters")

col1, col2 = st.columns(2)

with col1:

    source = st.text_input(
        "Start Location",
        placeholder="Enter source city, state, country"
    )

with col2:

    destination = st.text_input(
        "Destination Location",
        placeholder="Enter destination city, state, country"
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
        f"Battery Capacity: "
        f"{total_battery} kWh"
    )

with col4:

    st.info(
        f"Energy Consumption: "
        f"{consumption_factor} kWh/km"
    )

# ---------------------------------------------------
# REMAINING BATTERY
# ---------------------------------------------------

available_battery = st.slider(
    "Available Remaining Battery (kWh)",
    1.0,
    float(total_battery),
    float(total_battery / 2)
)

# ---------------------------------------------------
# TRAFFIC CONDITIONS
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
        # GEOCODING USING OPENROUTESERVICE
        # ---------------------------------------------------

        source_location = client.pelias_search(
            text=source
        )

        destination_location = client.pelias_search(
            text=destination
        )

        # ---------------------------------------------------
        # COORDINATES
        # ---------------------------------------------------

        source_coords = (
            source_location['features'][0]
            ['geometry']['coordinates']
        )

        destination_coords = (
            destination_location['features'][0]
            ['geometry']['coordinates']
        )

        coordinates = [
            source_coords,
            destination_coords
        ]

        # ---------------------------------------------------
        # ROUTE API
        # ---------------------------------------------------

        try:

            route = client.directions(
                coordinates=coordinates,
                profile='driving-car',
                format='geojson'
            )

        except:

            st.error(
                "Unable to find valid road route. "
                "Please enter proper city names "
                "with state and country."
            )

            st.stop()

        # ---------------------------------------------------
        # EXACT ROAD DISTANCE
        # ---------------------------------------------------

        distance = (
            route['features'][0]
            ['properties']['summary']
            ['distance']
        ) / 1000

        # ---------------------------------------------------
        # EXACT TRAVEL TIME
        # ---------------------------------------------------

        duration = (
            route['features'][0]
            ['properties']['summary']
            ['duration']
        ) / 60

        # ---------------------------------------------------
        # TRAFFIC FACTOR
        # ---------------------------------------------------

        if traffic == "Low":

             traffic_factor = 1.25

        elif traffic == "Medium":

           traffic_factor = 1.45

        else:

                traffic_factor = 1.75

        # ---------------------------------------------------
        # TRAFFIC ADJUSTED TIME
        # ---------------------------------------------------

        adjusted_duration = (
            duration * traffic_factor
        )

        # ---------------------------------------------------
        # ENERGY CALCULATION
        # ---------------------------------------------------

        energy_required = (
            distance *
            consumption_factor *
            traffic_factor
        )

        # ---------------------------------------------------
        # BATTERY ANALYSIS
        # ---------------------------------------------------

        remaining_battery = (
            available_battery -
            energy_required
        )

        battery_usage = (
            energy_required /
            available_battery
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
                "Road Distance",
                f"{distance:.2f} km"
            )

        with r2:

            st.metric(
                "Travel Time",
                f"{adjusted_duration:.2f} mins"
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
        # BATTERY BAR
        # ---------------------------------------------------

        st.subheader("Battery Utilization")

        battery_percentage = max(
            0,
            min(100, 100 - battery_usage)
        )

        st.progress(
            int(battery_percentage)
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
        # GOOGLE MAPS
        # ---------------------------------------------------

        st.header("Google Maps Navigation")

        google_maps_url = (
            f"https://www.google.com/maps/dir/"
            f"{source}/{destination}"
        )

        st.markdown(
            f"""
            <a href="{google_maps_url}" target="_blank">
                <button style="
                    background-color:#0b1a3c;
                    color:white;
                    padding:12px;
                    border:none;
                    border-radius:5px;
                    cursor:pointer;">
                    Open Route in Google Maps
                </button>
            </a>
            """,
            unsafe_allow_html=True
        )

    except Exception as e:

        st.error(f"Error: {e}")
