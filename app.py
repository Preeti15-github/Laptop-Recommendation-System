import streamlit as st
import pandas as pd

def load_data():
    df = pd.read_csv("Laptop_Information.csv")
    df["Company_lower"] = df["Company"].str.lower()
    return df

def recommend_laptops(laptop_name):
    df = load_data()
    laptop_name_lower = laptop_name.lower()
    df_filtered = df[df["Company_lower"].str.contains(laptop_name_lower, na=False)]
    return df_filtered[['Company', 'Price', 'Rating', 'ImgURL']]

st.title("Laptop Recommendation System")
laptop_name = st.text_input("Enter Laptop Company Name:")
if laptop_name:
    recommendations = recommend_laptops(laptop_name)
    if recommendations.empty:
        st.write("No laptops found for the given company name.")
    else:
        for _, row in recommendations.iterrows():
            st.subheader(row['Company'])
            st.write(f"Price: {row['Price']}")
            st.write(f"Rating: {row['Rating']}")
            st.image(row['ImgURL'], width=300)
