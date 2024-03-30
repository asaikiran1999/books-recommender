import streamlit as st
import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

st.title('Books recommender')

html_temp = """<div style='background_color: tomato; padding: 10px'><h2 style='color: white; text-align: center;'>Books recommender</h2></div>"""
st.markdown(html_temp, unsafe_allow_html=True)
page = st.selectbox("Choose your page", ["Top 50 book recommendation", "selected book recommender"])
# Load data
books1 = pd.read_csv("https://raw.githubusercontent.com/asaikiran1999/books-recommender/main/data/books1.csv")
books2 = pd.read_csv("https://raw.githubusercontent.com/asaikiran1999/books-recommender/main/data/books2.csv")
books3 = pd.read_csv("https://raw.githubusercontent.com/asaikiran1999/books-recommender/main/data/books3.csv")
books4 = pd.read_csv("https://raw.githubusercontent.com/asaikiran1999/books-recommender/main/data/books4.csv")
books = pd.concat([books1, books2, books3, books4], ignore_index=True)
# Function to recommend books
def recommend(book_name, pivot):
    index = np.where(pivot.index == book_name)[0][0]
    similarity_scores = cosine_similarity(pivot)
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]
    items = []
    for i in similar_items:
        temp_df = books[books['Book-Title'] == pivot.index[i[0]]]
        items.append(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M']))
    return items

# Load data for selected book recommender
users = pd.read_csv("https://raw.githubusercontent.com/asaikiran1999/books-recommender/main/data/Users.csv")
ratings = pd.read_csv("https://raw.githubusercontent.com/asaikiran1999/books-recommender/main/data/Ratings.csv")
ratings_and_books = ratings.merge(books, on='ISBN')
x = ratings_and_books.groupby('User-ID').count()['Book-Rating'] > 200
best_users = x[x].index
filtered_ratings = ratings_and_books[ratings_and_books['User-ID'].isin(best_users)]
y = filtered_ratings.groupby('Book-Title').count()['Book-Rating'] >= 50
famous_books = y[y].index
filtered_famous = filtered_ratings[filtered_ratings['Book-Title'].isin(famous_books)]
pivot = filtered_famous.pivot_table(index='Book-Title', columns='User-ID', values='Book-Rating')
pivot.fillna(0, inplace=True)

# User input and recommendation
user_input = st.text_input("Book Name", "")
st.text('Most searched books are:')
st.text("Harry Potter and the Sorcerer's Stone (Book 1)")
st.text('The Da Vinci Code')
st.text('The Secret Life of Bees')
st.text('Girl with a Pearl Earring')
st.text('About a Boy')

if st.button('Recommend'):
    recommended_books = recommend(user_input, pivot)
    for book_image_url in recommended_books:
        st.image(book_image_url, width=200)
        book_title = books[books['Image-URL-M'] == book_image_url]['Book-Title'].values[0]
        st.write(book_title)
