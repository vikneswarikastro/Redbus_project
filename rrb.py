import streamlit as st
import pandas as pd
import pymysql
from datetime import timedelta

st.title('Redbus Data Scraping and Filtering')

# Database connection
connection = pymysql.connect(host="localhost", port=3306, database="redbus", user="root", passwd="Prathiksha@123")
mycursor = connection.cursor()

# Fetch distinct states
q1 = "SELECT DISTINCT state FROM bus_routes1"
mycursor.execute(q1)
states = mycursor.fetchall()

state_list = [s[0] for s in states]  # Extracting states as a list of strings
selected_state = st.sidebar.selectbox('Select State', state_list)

# Fetch distinct route names
q2 = "SELECT DISTINCT route_name FROM bus_routes1"
mycursor.execute(q2)
route_names = mycursor.fetchall()

route_name_list = [r[0] for r in route_names]  # Extracting route names
selected_route = st.sidebar.selectbox('Select Route', route_name_list)

# Fetch distinct bus types
q3 = "SELECT DISTINCT bus_type FROM bus_routes1"
mycursor.execute(q3)
bus_types = mycursor.fetchall()
bus_type_list = [b[0] for b in bus_types]  # Extracting bus types
selected_bus_type = st.sidebar.selectbox("Select Bus Type", bus_type_list)

# Filters from the user
selected_star_rating = st.slider('Star Rating', min_value=1, max_value=5, value=3)
#selected_time = st.time_input('Enter Time', value=pd.to_datetime('12:00:00').time())  # Default 12:00 PM
selected_time = st.time_input('Enter Time')
selected_price = st.slider('Price Range', min_value=80.0, max_value=1000.0, value=500.0)
selected_seat_availability = st.number_input('Seat Availability', min_value=1, max_value=100, value=10)

# Construct the SQL query based on selected filters
query = """
    SELECT * FROM bus_routes1 
    WHERE state = %s 
    AND route_name = %s 
    AND bus_type = %s 
    AND star_rating >= %s 
    AND TIME(departing_time) >= %s    
    AND price <= %s 
    AND seat_availability >= %s
"""
 # Extract time from DATETIME and compare
# Convert the selected_time to the appropriate format (HH:MM:SS)

#selected_time_str = selected_time.strftime('%H:%M:%S')
#st.write(selected_time)

# Prepare the tuple to be passed to the query
params = (
    selected_state,
    selected_route,
    selected_bus_type,
    selected_star_rating,
    selected_time,  
    selected_price,
    selected_seat_availability
)

# Execute the query with user-selected values
mycursor.execute(query, params)

# Fetch the results from the query
results = mycursor.fetchall()

# Display results
if results:
    # Define column names based on your schema
    columns = ["id", "route_name", "route_link", "bus_name", "bus_type", "departing_time", "duration",
               "reaching_time", "price", "star_rating", "seat_availability", "state"]
    df = pd.DataFrame(results, columns=columns)
    
    df["departing_time"]=df["departing_time"].apply(lambda x:str(x).split(",")[-1]if isinstance(x,timedelta)else x)
    df["reaching_time"]=df["reaching_time"].apply(lambda x:str(x).split(",")[-1]if isinstance(x,timedelta)else x)
    #st.write(results)
    
    st.dataframe(df)
else:
    st.write("No buses match the selected criteria.")

# Display selected filters
st.write(f"Selected Filters:")
st.write(f"State: {selected_state}")
st.write(f"Route: {selected_route}")
st.write(f"Bus Type: {selected_bus_type}")
st.write(f"Star Rating: {selected_star_rating}")
st.write(f"Price Range: {selected_price}")
st.write(f"Seat Availability: {selected_seat_availability}")
st.write(f"Time: {selected_time}")

# Close the cursor and connection to the database
mycursor.close()
connection.close()

#df['event_time'] = df['event_time'].dt.strftime('%H:%M:%S')