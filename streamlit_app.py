import streamlit
import pandas

streamlit.title('My Marents New Healthy Dinner')


streamlit.header('Breakfast favorites')
streamlit.text('🥣 Omega 3 and Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinnach and Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Advocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

# new section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
fruit_choice = streamlit.text_input('What fruit would you like information about ?','Kiwi')
streamlit.write('The user entered', fruit_choice)

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# normalize json
fruityvice_normalized =pandas.json_normalize(fruityvice_response.json())
# output in the screen as a table
streamlit.dataframe(fruityvice_normalized)

import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from FRUIT_LOAD_LIST")
my_data_row = my_cur.fetchone()
streamlit.text("The fruit list contains :")
streamlit.dataframe(my_data_row)


