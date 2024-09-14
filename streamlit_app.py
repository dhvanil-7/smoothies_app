# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie !!!
    """
)

cnx = st.connection("snowflake")
session = cnx.session()
customer_name = st.text_input(label="Enter Your Name:",
                             placeholder="Name")
my_dataframe = session.table("smoothies.public.fruit_options").select("fruit_name")

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients: ",
    my_dataframe,
    max_selections=5
    
)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response)

if ingredients_list:

    ingredients_string= ", ".join(ingredients_list)

    my_insert_stmt = f""" insert into smoothies.public.orders(ingredients, name_on_order)
    values ('{ingredients_string}', '{customer_name}')
    """

    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered!, {customer_name}', icon="✅")
