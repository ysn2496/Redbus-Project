import streamlit as st
import pandas as pd
import mysql.connector
from sqlalchemy  import create_engine

#connect to sql
db_url = 'mysql+mysqlconnector://root:@localhost/redbus'

#Load data from sql to streamlit
engine = create_engine(db_url)
def load_data():
    
    query="SELECT * FROM redbus.busdata"
    df = pd.read_sql(query,engine)
    return df

df=load_data()

st.image('C:/Users/ADMIN/Downloads/redbus.jpg')

st.title("RedBus Data Viewer")
st.sidebar.header("Filter Options")
# Filters
# 1. Bus Name Filter
busname = st.sidebar.multiselect(
    'Select Bus Name',
    options=df['busname'].unique()
)
#2.route
route = st.sidebar.multiselect(
    'Select Route',
    options=df['route_name'].unique()
)

#3.bustype
bustype = st.sidebar.multiselect(
    'Select Bus Type',
    options=df['bustype'].unique()
)

#4.price range 
price_min = float(df['price'].min())
price_max = float(df['price'].max())
price_range = st.sidebar.slider(
    'Select Price Range',
    max_value=price_max,
    min_value=price_min,
    value=(price_max,price_min)
)

#5.star rating
star_max = float(df['star_rating'].max())
star_min = float(df['star_rating'].min())
star_rating = st.sidebar.slider(
    'Select Ratings',
    max_value=star_max,
    min_value=star_min,
    value=(star_max,star_min)
)

#6.Availability
availability = st.sidebar.selectbox(
    'Seats Availability',
    options=('All','Available Only')
)

# 7. Departure Time Filter
departure_time_start = st.sidebar.time_input('Select Departure Time Start', value=pd.to_datetime('00:00').time())
departure_time_end = st.sidebar.time_input('Select Departure Time End', value=pd.to_datetime('23:59').time())

# Function to convert a list to a format suitable for SQL IN clause
def format_for_sql_in(values):
    return ', '.join(f"'{value}'" for value in values)

# Construct the SQL query with filters
query = "SELECT * FROM redbus.busdata WHERE 1=1"  

# Add filters only if they are not empty
if bustype:
    query += f" AND bustype IN ({format_for_sql_in(bustype)})"
if route:
    query += f" AND route_name IN ({format_for_sql_in(route)})"
query += f" AND price BETWEEN {price_range[0]} AND {price_range[1]}"
query += f" AND star_rating BETWEEN {star_rating[0]} AND {star_rating[1]}"
if busname:
    query += f" AND busname IN ({format_for_sql_in(busname)})"
query += f" AND departing_time BETWEEN '{departure_time_start}' AND '{departure_time_end}'"

if availability == 'Available Only':
    query += " AND seats_available > 0"

# Execute the query
filter_df = pd.read_sql(query, engine)

# Display filtered data
st.dataframe(filter_df)

st.header('Data Analysis')

st.subheader("Route Vs Price")
#Data analysis=1
avg_price_query = "SELECT route_name, AVG(price) AS avg_price FROM redbus.busdata WHERE 1=1"

# Add filters only if they are not empty
if bustype:
    query += f" AND bustype IN ({format_for_sql_in(bustype)})"
if route:
    query += f" AND route_name IN ({format_for_sql_in(route)})"
query += f" AND price BETWEEN {price_range[0]} AND {price_range[1]}"
query += f" AND star_rating BETWEEN {star_rating[0]} AND {star_rating[1]}"
if busname:
    query += f" AND busname IN ({format_for_sql_in(busname)})"
query += f" AND departing_time BETWEEN '{departure_time_start}' AND '{departure_time_end}'"

if availability == 'Available Only':
    avg_price_query += " AND seats_available > 0"

avg_price_query += " GROUP BY route_name"

# Execute the query
avg_price_per_busroute = pd.read_sql(avg_price_query, engine)

# Display the result as a bar chart
st.bar_chart(avg_price_per_busroute.set_index('route_name'))


st.subheader("Bustype Vs Rating")
#Data analysis=2
avg_rating_query = "SELECT bustype, AVG(star_rating) AS avg_star_rating FROM redbus.busdata WHERE 1=1"

# Add filters only if they are not empty
if bustype:
    query += f" AND bustype IN ({format_for_sql_in(bustype)})"
if route:
    query += f" AND route_name IN ({format_for_sql_in(route)})"
query += f" AND price BETWEEN {price_range[0]} AND {price_range[1]}"
query += f" AND star_rating BETWEEN {star_rating[0]} AND {star_rating[1]}"
if busname:
    query += f" AND busname IN ({format_for_sql_in(busname)})"
query += f" AND departing_time BETWEEN '{departure_time_start}' AND '{departure_time_end}'"
if availability == 'Available Only':
    avg_rating_query += " AND seats_available > 0"

avg_rating_query += " GROUP BY bustype"

# Execute the query
avg_rating_per_bustype = pd.read_sql(avg_rating_query, engine)

# Display the result as a bar chart
st.bar_chart(avg_rating_per_bustype.set_index('bustype'))
