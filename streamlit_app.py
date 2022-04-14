import pandas as pd
import requests
import snowflake.connector
import streamlit
from urllib.error import URLError



my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index("Fruit")

streamlit.title("My Parents New Healthy Diner")

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_ti_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_ti_show)

def get_fruityvice_data(this_fruit_choice):
  fruity_vice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
  fruitvice_normalized = pd.json_normalize(fruity_vice_response.json())
  return fruitvice_normalize


streamlit.header('Fruityvice Fruit Advice')
try:
  fruit_choice = streamlit.text_input("What fruit would you like information about?")
  if not fruit_choice:
    streamlit.error("Please select a fruit")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()

streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)
fruit_choice2 = streamlit.text_input("What fruit would you like to add")
streamlit.write("Thanks for add", fruit_choice2)
my_cur.execute("insert into fruit_load_list values ('from streamlit')")




