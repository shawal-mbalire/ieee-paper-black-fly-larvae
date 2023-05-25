# import pyrebase
# import streamlit as st
# from datetime import datetime


# firebaseConfig = {
#   'apiKey': "AIzaSyAtqKKRESq6bK8-2f4ypc4tb4zY5pDWXFs",
#   'authDomain': "bsf-bradley.firebaseapp.com",
#   'databaseURL': "https://bsf-bradley-default-rtdb.firebaseio.com",
#   'projectId': "bsf-bradley",
#   'storageBucket': "bsf-bradley.appspot.com",
#   'messagingSenderId': "584438088785",
#   'appId': "1:584438088785:web:6cfd98e025c04ce0212470",
#   'measurementId': "G-BMQN6WWJL1"
# }

# # Initialize Firebase
# firebase    = pyrebase.initialize_app(firebaseConfig)
# auth        = firebase.auth()
# db          = firebase.database()
# storage     = firebase.storage()

# # sign up
# def signup():
#     st.title("BSF SYSTEM")
#     st.subheader("Sign Up Page")
#     email = st.text_input("Email")
#     #check if email is valid email
#     if email:
#         if "@" not in email:
#             st.error("Invalid Email")
#         elif "." not in email:
#             st.error("Invalid Email")
#         elif " " in email:
#             st.error("Invalid Email")
#         elif len(email) < 5:
#             st.error("Invalid Email")
#         else:
#             st.success("Valid Email")
#     password = st.text_input("Password", type="password")
#     if st.button("Sign Up"):
#         try:
#             auth.create_user_with_email_and_password(email, password)
#             st.success("User Created")
#             st.balloons()
#             login()
#         except:
#             st.error("Email already exists")


# # Login Page
# def login():
#     st.title("BSF SYSTEM")
#     st.subheader("Login Page")
#     email    = st.text_input("Email")
#     password = st.text_input("Password", type="password")
#     if st.button("Login"):
#         try:
#             auth.sign_in_with_email_and_password(email, password)
#             st.success("Logged In")
#             main()
#         except:
#             st.error("Invalid Email or Password")
     
# # Main Page
# def main():
#     st.title("BSF System")
#     st.subheader("Parameters")

#     # Get data from Firebase Realtime Database
#     lux          = db.child("BH1750"    ).child("lux"        ).get()
#     temperature  = db.child("DHT"       ).child("temperature(celcius)").get()
#     humidity     = db.child("DHT"       ).child("humidity"   ).get()
    
#     # Display data
#     st.write("Lux: ",             lux.val())
#     st.write("Temperature: ",     temperature.val())
#     st.write("Humidity: ",        humidity.val())
    
#     def FogOn():
#       db.child("fogMachine").child("setOn").setValue(True)
      
#     def undoFogOn():
#       db.child("fogMachine").child("setOn").setValue(False)
      
#     def FogOff():
#       db.child("fogMachine").child("setOff").setValue(True)
    
#     def undoFogOff():
#       db.child("fogMachine").child("setOff").setValue(False)
      
      
#     st.button(
#       "Fog Machine On",
#       on_click = FogOn()
#     )
#     st.button(
#       "Undo Fog Machine On",
#       on_click = undoFogOn()
#     )
#     st.button(
#       "Fog Machine Off",
#       on_click = FogOff()
#     )
#     st.button(
#       "Undo Fog Machine Off",
#       on_click = undoFogOff()
#     )
    

# if __name__ == "__main__":
#   main()
#     st.sidebar.title("BSF System Monitoring")
#     menu = st.sidebar.radio("Menu", ["Login", "SignUp"])
#     if menu == "Login":
#         login()
#     elif menu == "SignUp":
#         signup()

import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Initialize the Firebase app
cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://bsf-bradley-default-rtdb.firebaseio.com'
})

# Function to update the boolean value in Firebase
def update_boolean_value(value):
    ref = db.reference('/path/to/your/boolean')
    ref.set(value)

# Streamlit app
def main():
    st.title("Firebase Realtime Database Example")
    
    # Button to update boolean value to True
    if st.button("Set Boolean to True"):
        update_boolean_value(True)
        st.success("Boolean value set to True")
    
    # Button to update boolean value to False
    if st.button("Set Boolean to False"):
        update_boolean_value(False)
        st.success("Boolean value set to False")

if _name_ == "_main_":
    main()
