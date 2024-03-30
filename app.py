
import streamlit as st
import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

st.title('Books recommender')

import streamlit as st
import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
html_temp = """
<div style = 'background_color:tomato ; padding;10px'>
<h2 style = "color : white; text-align :center;">Books recommender</h2>
</div>
"""
st.markdown(html_temp,unsafe_allow_html= True)
books1 = pd.read_csv("https://raw.githubusercontent.com/asaikiran1999/books-recommender/main/data/books1.csv")
books2 = pd.read_csv("https://raw.githubusercontent.com/asaikiran1999/books-recommender/main/data/books2.csv")
books3 = pd.read_csv("https://raw.githubusercontent.com/asaikiran1999/books-recommender/main/data/books3.csv")
books4 = pd.read_csv("https://raw.githubusercontent.com/asaikiran1999/books-recommender/main/data/books4.csv")
books1 = pd.concat([books1, books2], ignore_index=True)
books1 = pd.concat([books1, books3], ignore_index=True)
books1 = pd.concat([books1, books4], ignore_index=True)
books = books1.copy()
page = st.selectbox("Choose your page", ["Top 50 book recommendation", "selected book recommender"])
def paginator(label, items, items_per_page=10, on_sidebar=True):
	"""Lets the user paginate a set of items.
	Parameters
	----------
	label : str
	    The label to display over the pagination widget.
	items : Iterator[Any]
	    The items to display in the paginator.
	items_per_page: int
	    The number of items to display per page.
	on_sidebar: bool
	    Whether to display the paginator widget on the sidebar.
	    
	Returns
	-------
	Iterator[Tuple[int, Any]]
	    An iterator over *only the items on that page*, including
	    the item's index.
	Example
	-------
	This shows how to display a few pages of fruit.
	>>> fruit_list = [
	...     'Kiwifruit', 'Honeydew', 'Cherry', 'Honeyberry', 'Pear',
	...     'Apple', 'Nectarine', 'Soursop', 'Pineapple', 'Satsuma',
	...     'Fig', 'Huckleberry', 'Coconut', 'Plantain', 'Jujube',
	...     'Guava', 'Clementine', 'Grape', 'Tayberry', 'Salak',
	...     'Raspberry', 'Loquat', 'Nance', 'Peach', 'Akee'
	... ]
	...
	... for i, fruit in paginator("Select a fruit page", fruit_list):
	...     st.write('%s. **%s**' % (i, fruit))
	"""

	# Figure out where to display the paginator
	if on_sidebar:
	    location = st.sidebar.empty()
	else:
	    location = st.empty()

	# Display a pagination selectbox in the specified location.
	items = list(items)
	n_pages = len(items)
	n_pages = (len(items) - 1) // items_per_page + 1
	page_format_func = lambda i: "Page %s" % i
	page_number = location.selectbox(label, range(n_pages), format_func=page_format_func)

	# Iterate over the items in the page to let the user display them.
	min_index = page_number * items_per_page
	max_index = min_index + items_per_page
	import itertools
	return itertools.islice(enumerate(items), min_index, max_index)

if page == "Top 50 book recommendation":
    items2 = []
    items3 = []
    x = pd.read_csv("https://raw.githubusercontent.com/asaikiran1999/books-recommender/main/data/top50book.csv")
    for i in range(50):
        items2.append(x['Image-URL-M'][i])
        items3.append(x['Book-Title'][i])

    image_iterator = paginator("Select next page", zip(items2, items3))
    indices_on_page, images_and_titles_on_page = map(list, zip(*image_iterator))

    for image_url, book_title in images_and_titles_on_page:
        st.image(image_url, width=200)
        st.write(book_title)
	
elif page == "selected book recommender":
	users= pd.read_csv("https://raw.githubusercontent.com/asaikiran1999/books-recommender/main/data/Users.csv")
	ratings = pd.read_csv("https://raw.githubusercontent.com/asaikiran1999/books-recommender/main/data/Ratings.csv")
	ratings_and_books = ratings.merge(books,on='ISBN')
	x=ratings_and_books.groupby('User-ID').count()['Book-Rating']>200
	best_users=x[x].index
	filtered_ratings =ratings_and_books[ratings_and_books['User-ID'].isin(best_users)]
	y=filtered_ratings.groupby('Book-Title').count()['Book-Rating']>=50
	famous_books=y[y].index
	filtered_famous = filtered_ratings[filtered_ratings['Book-Title'].isin(famous_books)]
	pivot = filtered_famous.pivot_table(index ='Book-Title',columns='User-ID',values='Book-Rating')
	pivot.fillna(0,inplace=True)
	similarity_scores = cosine_similarity(pivot)

	def recommend(book_name):
	  index = np.where(pivot.index == book_name)[0][0]
	  similar_items =sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:6]
	  items=[]
	  for i in similar_items:
	    #print(pivot.index[i[0]])
	    temp_df = books[books['Book-Title']==pivot.index[i[0]]] 
	    items.append(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M']))
	  return items
	input = st.text_input("Book_Name","")
	st.text('most search books are :')
	st.text("Harry Potter and the Sorcerer's Stone (Book 1)")
	st.text('The Da Vinci Code')
	st.text('The Secret Life of Bees')
	st.text('Girl with a Pearl Earring')
	st.text('About a Boy')
        recommended_books = recommend(input)
if st.button('recommend'):
	for book_image_url in recommended_books:
		st.image(book_image_url, width=200)
		book_title = books[books['Image-URL-M'] == book_image_url]['Book-Title'].values[0]
		st.write(book_title)

