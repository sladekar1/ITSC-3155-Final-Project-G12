import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import altair as alt
import numpy as np



st.title('Movie Finder')
st.subheader("Sort through your favorite Oscar Winners and Nominees!")

# add picture
from PIL import Image
image=Image.open("Oscar.png")
st.image(image, use_column_width=True)


# read the data and save it into cash 
@st.cache
def load_data():
    df = pd.read_csv('oscar_clean.csv', index_col='Film')
    return df

# load the data
df = load_data()


#login fields
def main():
    menu=["Sign In", "Sign Up"]
    choice=st.sidebar.selectbox("Log into your Account", menu)

    if choice=="Sign In":
        #st.subheader("Login")
        username=st.sidebar.text_input("User Name")
        password=st.sidebar.text_input("Password", type="password")
        if st.sidebar.checkbox("Log In"):
            st.success("Logged In as {}".format (username))
            dosmth=st.selectbox("What would you like to do?", ["Check My Movies", "Change password"])
            
    elif choice=="Sign Up":
        st.subheader("Create New Account")
        new_user=st.text_input("Username")
        new_password=st.text_input("Password", type="password")
        if st.button ("Sign Up"):
            st.success("You created a new account!")
main() 
   
  #create button
award = st.sidebar.radio("Choose Award Type", ("All", 'Nominee', 'Winner'))
placeholder=st.empty()

if st.sidebar.checkbox("Sort List via Award Type"):
    if award == 'Nominee':
        n= df.loc[df['Award']=="Nominee"]
        placeholder.dataframe(n)
    elif award=="Winner":
        n= df.loc[df['Award']=="Winner"]
        placeholder.dataframe(n)   
    elif award == "All":    
        placeholder.dataframe(df)

   # create side bar for genres
df=df.rename(columns={'Movie Genre': 'Genre'})   
genre = [" ", "Action", "Adventure", "Biography", "Comedy", "Crime", "Drama", "Fantasy", "History", "Horror", 
         "Mystery","Sci-Fi","Thriller", "Western", "Music", "Romance"]
g=st.selectbox("Select Genre", genre)
placeholder = st.empty()
if st.checkbox ("Show Movie List With Chosen Genre"):
    for i in genre:
        i=g
        gshow = df[df['Genre'].str.contains(i)]
    placeholder.dataframe(gshow)
    
    # create slider for IMDB
    maxValue = gshow['IMDB Rating'].max()
    minValue = gshow['IMDB Rating'].min()
    val=[minValue, maxValue]
    slider=st.slider ("Choose a rank", min_value= minValue , max_value=maxValue , step=0.1)
    r=gshow[gshow["IMDB Rating"] == slider]
    st.write("### Movies of ", slider, "rank", r)

   

    # create slider for years
placeholder = st.empty()
years = list(df['Year of Release'].unique())
slider=st.sidebar.select_slider ("Choose a Year", options= years)
if st.sidebar.checkbox ("Show Movie List According to Chosen Year"):
    df1=df[df["Year of Release"] == slider]
    st.write("### Movies of ", slider, "year", df1)
        

    
    
    # choose the rank to compare
cols = ['IMDB Rating', 'Tomatometer Rating', 'Audience Rating']

if st.sidebar.checkbox('Compare Ratings'):
    option = st.multiselect('Rank Movies of Chosen Years', cols, cols[0])
    df = df1[option].reset_index()
    alt_fig = alt.Chart(df).transform_fold(
    cols,
    ).mark_line().encode(
    x='Film',
    y=alt.Y('value:Q', title='Rating'),
    color='key:N' 
    ).properties(
    title='Comparisons Between Films',
    width=800,
    height=400
    ).interactive()
    # Show 
    st.write(alt_fig)
    
    
    

# fig, ax = plt.subplots()
# arr=df.loc[:, "IMDB Rating"]
# ax.hist(arr, bins=20)
# st.pyplot(fig)