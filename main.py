import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import time

st.set_page_config(layout="wide")
# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data

with st.sidebar:
    selected=option_menu(
        menu_title="Start Here!",
        options=["Signup","Login","Average OrdDetail","Fraud Count","Dashboard","Fraud Rate","Daily Subscription"],
        icons=["box-seam-fill","box-seam-fill"],
        menu_icon="home",
        default_index=0
    )

if selected=="Signup" :

    st.subheader("Create New Account")
    new_user = st.text_input("Username")
    new_password = st.text_input("Password",type='password')
    if st.button("Signup"):
        create_usertable()
        add_userdata(new_user,make_hashes(new_password))
        st.success("You have successfully created a valid Account")
        st.info("Go to Login Menu to login")


elif selected=="Login" :
    st.subheader("Login Section")
    username = st.text_input("User Name")
    password = st.text_input("Password",type='password')
    if st.sidebar.checkbox("Login"):
			# if password == '12345':
        create_usertable()
        hashed_pswd = make_hashes(password)
        result = login_user(username,check_hashes(password,hashed_pswd))
        prog=st.progress(0)
        for per_comp in range(100):
            time.sleep(0.05)
            prog.progress(per_comp+1)
        if result:
            st.success("Logged In as {}".format(username))
            st.warning("Go to Dashboard!")
        else:
            st.warning("Incorrect Username/Password")

elif selected=="Average OrdDetail":
    
    st.markdown("# Average subscription on networks")
    fb_check=st.checkbox("Facebook ")
    mb_check=st.checkbox("Mobaeneu")
    ads_check=st.checkbox("Smart Connect")
    if fb_check:
        image = Image.open('AVERAGEFACEBBOK.jpg')
        st.image(image, caption='')
    else:
        st.warning(f"Sorry the data not analysed yet")
    
elif selected=="Daily Subscription": 
    st.header("Sales for 599 & 899 Subscription Plans ")
  
    c1,c2,c3=st.columns([6,6,6])
    c1.header("Day 19 August")
    image1=Image.open("day19_599_899_average.JPG")
    c1.image(image1, caption='')
    c2.header("Day 20August")
    image2=Image.open("day20.JPG")
    c2.image(image2,caption="")
    c3.header("Day 21August")
    image3=Image.open("day21.JPG")
    c3.image(image3,caption="")
    st.markdown("# In total SaleRevenue from the Plans")
    st.spinner(text="In progress...")
    with st.spinner('Please wait ..'):
        time.sleep(5)
    img=Image.open("3 days sum of 599 & 899 and average.JPG")
    st.image(img,caption="")
elif selected=="Fraud Count":
    st.header("Select networks from below to get count:")
    genre = st.radio(
    "Network_Name:--",
    ('ADsFlourish', 'Facebook', 'Mobaveun','Smart Connect'))
    with st.spinner('Please wait ..'):
        time.sleep(5)
    if genre == "ADsFlourish":
        img=Image.open("fraud data of adsflourish.JPG")
    elif genre == "Facebook":
        img=Image.open("fraud data of facebook.JPG")
    elif genre=="Mobaveun":
        img=Image.open("fraud data of mobavenue.JPG")
    elif genre=="Smart Connect":
        img=Image.open("fraud data of smart connect.JPG")
    st.image(img,caption=f" # {genre} detail")
    time.sleep(0.5)
    st.header("Fraud caused due to UUID Duplication:")
    with st.expander("See Explanation"):
        st.write("Universal Unique identifier should be different for every subscription instances but analysis shows:-")
        im=Image.open("UUID_duplicate_network.JPG")
        st.image(im)
elif selected=="Fraud Rate":
    st.warning("Total detected fraud depending upon companies ")
    c1,c2=st.columns([5,5])
    im=Image.open("total fraud rate.JPG")
    c1.image(im,caption="")
    im2=Image.open("Pictorial fraud rate.JPG")
    c2.image(im2,caption="")

    with st.expander("See explanation"):
        st.write("""
        Code snippet of fraud calculation:-
    """)
        img=Image.open("fraud rate.png")
        st.image(img,caption="")
    
elif selected =="Dashboard":
    import pandas as pd
    import plotly.express as px
    st.header("Let's Analyse the subscription on given dates")
    df=pd.read_csv("Transaction Data_19th to 21st August 2022.csv")
    st.write("Data set loaded for transaction , kindly apply filters to show")
    df=df[df.duplicated("Phone")]
    df["Date"]=pd.to_datetime(df["Date"]).dt.strftime('%Y-%m-%d')
    df=df[df.duplicated("Date")]
    date_options=df["Date"].unique().tolist()
    select_date=st.multiselect("Which dates you want to see?",date_options)
    df_up=df[df["Date"].isin(select_date)]
    sub_opt=df_up["Requested Amount"].unique().tolist()
    select_sub=st.multiselect("Which plan you want to select?",sub_opt)
    df_up_sub=df_up[df_up["Requested Amount"].isin(select_sub)]
    with st.expander("See the plot"):
        st.write("""
        Code snippet of fraud calculation:-
    """)
        fig=px.bar(df_up_sub,x="Requested Amount",color="Date",)
        fig.update_layout(width=400)
        st.write(fig)
    
    


