import pyrebase
import streamlit as st
from datetime import datetime


firebaseConfig = {
  "apiKey": "AIzaSyAtqKKRESq6bK8-2f4ypc4tb4zY5pDWXFs",
  "authDomain": "bsf-bradley.firebaseapp.com",
  "databaseURL": "https://bsf-bradley-default-rtdb.firebaseio.com",
  "projectId": "bsf-bradley",
  "storageBucket": "bsf-bradley.appspot.com",
  "messagingSenderId": "584438088785",
  "appId": "1:584438088785:web:6cfd98e025c04ce0212470",
  "measurementId": "G-BMQN6WWJL1"
}

# Initialize Firebase
firebase    = pyrebase.initialize_app(firebaseConfig)
auth        = firebase.auth()
db          = firebase.database()
storage     = firebase.storage()

# sign up
def signup():
    st.title("IEEE Paper")
    st.subheader("Sign Up")
    email = st.text_input("Email")
    #check if email is valid email
    if email:
        if "@" not in email:
            st.error("Invalid Email")
        elif "." not in email:
            st.error("Invalid Email")
        elif " " in email:
            st.error("Invalid Email")
        elif len(email) < 5:
            st.error("Invalid Email")
        else:
            st.success("Valid Email")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        try:
            auth.create_user_with_email_and_password(email, password)
            st.success("User Created")
            st.balloons()
            login()
        except:
            st.error("Email already exists")


# Login Page
def login():
    st.title("IEEE Paper")
    st.subheader("Login")
    email    = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            auth.sign_in_with_email_and_password(email, password)
            st.success("Logged In")
            main()
        except:
            st.error("Invalid Email or Password")
   
def update_bulbOn():
    ref = db.child("heaterBulb").child('setOn')
    if ref == True:
      ref.set(False)
      st.success("Manual ON deactivated")
    elif ref == False:
      ref.set(True)
      st.success("Manual ON activated")
    #st.write("Bulb!!")
def update_bulbOff():
#     ref = db.child("heaterBulb").child('setOff')
#     ref.set(value)
    ref = db.child("heaterBulb").child('setOff')
    if ref == True:
      ref.set(False)
      st.success("Manual OFF deactivated")
    elif ref == False:
      ref.set(True)
      st.success("Manual OFF activated")

# Streamlit app
def main():
    st.title("BSF SYSTEM MONITORING")
    st.subheader("Parameters")
    lux          = db.child("BH1750"    ).child("lux"        ).get()
    temperature  = db.child("DHT"       ).child("temperature").get()
    humidity     = db.child("DHT"       ).child("humidity"   ).get()
    bulbOn       = db.child("heaterBulb").child("setOn").get()
    bulbOff      = db.child("heaterBulb").child("setOff").get()
    
    # Display data
    st.write("Lux: ",             lux.val())
    st.write("Temperature: ",     temperature.val())
    st.write("Humidity: ",        humidity.val())
    
    st.subheader("Heater Bulb")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("BULB ON"):
          update_bulbOn()
#           if bulbOn == False:
#             update_bulbOn(True)
#             st.success("Manual heater ON  activated")
#           elif bulbOn == True:
#             update_bulbOn(False)
#             st.success("Manual heater ON  deactivated")
            
    with col2:
        if st.button("BULB OFF"):
          update_bulbOff()
#           if bulbOff == False:
#             update_bulbOff(True)
#             st.success("Manual heater OFF  activated")
#           elif bulbOff == True:
#             update_bulbOff(False)
#             st.success("Manual heater OFF  deactivated")
        
if __name__ == "__main__":
    main()
#     st.sidebar.title("IEEE Paper")
#     menu = st.sidebar.radio("Menu", ["Login", "SignUp"])
#     if menu == "Login":
#        login()
#     elif menu == "SignUp":
#        signup()
    
   


