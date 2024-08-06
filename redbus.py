import streamlit as st
import pandas as pd
import mysql.connector
from sqlalchemy  import create_engine


db_url = 'mysql+mysqlconnector://root:@localhost/redbus'

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
#1.route
route = st.sidebar.multiselect(
    'Select Route',
    options=df['route_name'].unique()
)

#2.bustype
bustype = st.sidebar.multiselect(
    'Select Bus Type',
    options=df['bustype'].unique()
)

#3.price range 
price_min = float(df['price'].min())
price_max = float(df['price'].max())
price_range = st.sidebar.slider(
    'Select Price Range',
    max_value=price_max,
    min_value=price_min,
    value=(price_max,price_min)
)

#4.star rating
star_max = float(df['star_rating'].max())
star_min = float(df['star_rating'].min())
star_rating = st.sidebar.slider(
    'Select Ratings',
    max_value=star_max,
    min_value=star_min,
    value=(star_max,star_min)
)

#5.Availability
availability = st.sidebar.selectbox(
    'Seats Availability',
    options=('All','Available Only')
)

#Apply filters

filter_df = df[
    (df['bustype'].isin(bustype)) &
    (df['route_name'].isin(route)) &
    (df['price'] >= price_range[0]) &
    (df['price'] <= price_range[1]) &
    (df['star_rating'] >= star_rating[0]) &
    (df['star_rating'] <= star_rating[1])
]

if availability == 'Available Only':
    filter_df = filter_df[filter_df['seats_available'] > 0]

st.dataframe(filter_df)

#analysis

st.header('Data Analysis')

avg_price_per_busroute = filter_df.groupby('route_name')['price'].mean()
st.bar_chart(avg_price_per_busroute)

avg_rating_per_bustype = filter_df.groupby('bustype')['star_rating'].mean()
st.bar_chart(avg_rating_per_bustype)