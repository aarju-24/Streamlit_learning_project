import streamlit as st
import pandas as pd
import numpy as np

st.title("Uber pickups in NYC")

# fetch data
date_column = "date/time"

data_url = (
    "https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz"
)

@st.cache_data
def load_data(nrows):

    data = pd.read_csv(data_url, nrows=nrows)

    lowercase = lambda x: str(x).lower()

    data.rename(lowercase, axis="columns", inplace=True)

    data[date_column] = pd.to_datetime(data[date_column])

    return data


# load the data and check

# create a text element and let the reader know the data is loading
data_load_state = st.text("Loading data...")

# load 10,000 rows of data into the dataframe
data = load_data(10000)

# notify the reader that the data was successfully loaded
data_load_state.text("Loading data...done! (using st.cache_data)")

# display the dataframe in the app

# inspect the raw data
st.subheader("Raw data")

st.write(data)


# draw a histogram
st.subheader("Number of pickups by hour")

# use numpy to generate histogram data
hist_values = np.histogram(
    data[date_column].dt.hour,
    bins=24,
    range=(0, 24)
)[0]

st.bar_chart(hist_values)


# create slider for hour selection
hour_to_filter = st.slider(
    "Hour",
    0,
    23,
    17
)

# filter data for pickups that happened during selected hour
filtered_data = data[
    data[date_column].dt.hour == hour_to_filter
]

# plot filtered data on map
st.subheader(f"Map of pickups at {hour_to_filter}:00")

st.map(filtered_data[['lat', 'lon']])


# use a checkbox to show raw filtered data
if st.checkbox("Show raw data"):

    st.subheader("Filtered raw data")

    st.write(filtered_data)