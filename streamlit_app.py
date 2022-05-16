import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

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

# function
def get_fruityvice_data(this_fruit_choice):
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
      # normalize json
      fruityvice_normalized =pandas.json_normalize(fruityvice_response.json())
      # output in the screen as a table
      return fruityvice_normalized

# new section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about ?')
   if not fruit_choice:
      streamlit.error("Please choose a fruit !")
   else:
      back_from_function=get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()

# streamlit.stop()

# function load fruits to load
def get_fruits_load_list():
      with my_cnx.cursor() as my_cur:
            my_cur.execute("SELECT * from FRUIT_LOAD_LIST")
            return my_cur.fetchall()
      
if streamlit.button('View our fruit list - add your favorites'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      my_data_row = get_fruits_load_list()
      my_cnx.close()
      streamlit.dataframe(my_data_row)

# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT * from FRUIT_LOAD_LIST")
# my_data_row = my_cur.fetchall()
# streamlit.text("The fruit list contains :")
# streamlit.dataframe(my_data_row)

# add_fruit = streamlit.text_input('What fruit do you want to add ?','Kiwi')
# my_data_row.extend(add_fruit)
# streamlit.write('The user entered', add_fruit)
# my_cur.execute("INSERT INTO FRUIT_LOAD_LIST VALUES ('"+ add_fruit +"')")

def insert_row_snowflake(new_fruit):
      with my_cnx.cursor() as my_cur:
            my_cur.execute("INSERT INTO FRUIT_LOAD_LIST VALUES ('"+ new_fruit +"')")
            return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit do you want to add ?','Kiwi')
if streamlit.button('Add fruit to list'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      back_from_function = insert_row_snowflake(add_my_fruit)
      my_cnx.close()
      streamlit.text(back_from_function)


