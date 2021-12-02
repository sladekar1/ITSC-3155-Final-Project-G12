import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import altair as alt
import numpy as np



st.title('Movie bla-bla-bla')
st.subheader("Something about what going on on this app")

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
    menu=["SignIn", "SignUp"]
    choice=st.sidebar.selectbox("Log in your Account", menu)

    if choice=="SignIn":
        #st.subheader("Login")
        username=st.sidebar.text_input("User Name")
        password=st.sidebar.text_input("Password", type="password")
        if st.sidebar.checkbox("LogIn"):
            st.success("Logged In as {}".format (username))
            dosmth=st.selectbox("What are you want to do", ["Check My Movies", "Change password"])
            
    elif choice=="SignUp":
        st.subheader("Create new account")
        new_user=st.text_input("Username")
        new_password=st.text_input("Password", type="password")
        if st.button ("SignUp"):
            st.success("You create a new account") 
main() 
   
  #create button
award = st.sidebar.radio("Choose award", ('Nominee', 'Winner', "All"))
placeholder=st.empty()

if st.sidebar.checkbox("Show Initial List"):
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
if st.checkbox ("Show list movies with chosen gener"):
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
slider=st.sidebar.select_slider ("Choose a year", options= years)
if st.sidebar.checkbox ("Show list movies of chosen years"):
    df1=df[df["Year of Release"] == slider]
    st.write("### Movies of ", slider, "year", df1)
        

    
    
    # choose the rank to compare
cols = ['IMDB Rating', 'Tomatometer Rating', 'Audience Rating']

if st.sidebar.checkbox('Compare ratings'):
    option = st.multiselect('Rank movies of chosen years', cols, cols[0])
    df = df1[option].reset_index()
    alt_fig = alt.Chart(df).transform_fold(
    cols,
    ).mark_line().encode(
    x='Film',
    y=alt.Y('value:Q', title='Rating'),
    color='key:N' 
    ).properties(
    title='SOme title...',
    width=800,
    height=400
    ).interactive()
    # Show 
    st.write(alt_fig)
    
    
    

# fig, ax = plt.subplots()
# arr=df.loc[:, "IMDB Rating"]
# ax.hist(arr, bins=20)
# st.pyplot(fig)