import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from sklearn.datasets import load_iris

conn = sqlite3.connect('data.db')
cur = conn.cursor()

def create_table():
    cur.execute('CREATE TABLE IF NOT EXISTS blogtable(author TEXT, title TEXT, article TEXT, postdate DATE)')

def add_data(author, title, article, postdate):
    cur.execute('INSERT INTO blogtable(author, title, article, postdate) VALUES (?, ?, ?, ?)', (author, title, article, postdate))
    conn.commit()

def view_all_notes():
    cur.execute('SELECT * FROM blogtable')
    data = cur.fetchall()
    return data

# Layout Templates
title_temp = """
<div style="background-color:#464e5f; padding:10px; margin:10px;">
    <h4 style="color:white; text-align:center;">{}</h4>
    <img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align:middle; float:left; width:50px; height:50px;">
    <h4 style="color:white; text-align:center;">Author:{}</h4>
    <p>{}</p>
    <h6 style="color:white; text-align:center;">Post Date:{}</h6>
</div>
"""

def main():

    st.title("Simple Blog")

    menu = ["Home", "View Posts", "Add Posts", "Search", "Manage Blog"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        result = view_all_notes()
        # st.write(result)
        x = np.linspace(0, 10, 100)
        y = np.sin(x)

        fig, ax = plt.subplots(1, 1, figsize=(8, 4))
        ax.plot(x, y)
        st.pyplot(fig)
        iris = load_iris()
        st.dataframe(iris['data'])

        for i in result:
            b_author = i[0]
            b_title = i[1]
            b_article = i[2]
            b_post_date = i[3]
            st.markdown(title_temp.format(b_author, b_title, b_article, b_post_date), unsafe_allow_html=True)
    
    elif choice == "View Posts":
        st.subheader("View Articles")
    
    elif choice == "Add Posts":
        st.subheader("Add Articles")
        create_table()
        blog_author = st.text_input("Enter Author Name", max_chars=50)
        blog_title = st.text_input("Enter Post Title")
        blog_article = st.text_area("Enter Article Here", height=200)
        blog_post_date = st.date_input("Date")
        if st.button("Add"):
            add_data(blog_author, blog_title, blog_article, blog_post_date)
            st.success(f"Post: {blog_title} saved")


    elif choice == "Search":
        st.subheader("Search")

    elif choice == "Manage Blog":
        st.subheader("Manage Blog")

if __name__ == '__main__':
    main()