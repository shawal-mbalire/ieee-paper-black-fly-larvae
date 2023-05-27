import pyrebase
import streamlit as st
#from datetime import datetime


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

# # sign up
# def signup():
#     st.title("IEEE Paper")
#     st.subheader("Sign Up")
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
#     st.title("IEEE Paper")
#     st.subheader("Login")
#     email    = st.text_input("Email")
#     password = st.text_input("Password", type="password")
#     if st.button("Login"):
#         try:
#             auth.sign_in_with_email_and_password(email, password)
#             st.success("Logged In")
#             main()
#         except:
#             st.error("Invalid Email or Password")

def update_boolean_value(value):
    ref = db.reference('fogMachine/setOn')
    ref.set(value)
    st.write("Fog!!")
# Streamlit app
def main():
    st.title("Firebase Realtime Database Example")
    
    # Button to update boolean value to True
    if st.button("Set fogOn to True"):
        update_boolean_value(True)
        st.success("Boolean value set to True")
    
    # Button to update boolean value to False
    if st.button("Set fog On to False"):
        update_boolean_value(False)
        st.success("Boolean value set to False")

if __name__ == "__main__":
    main()
# # Main Page
# def main():
#     st.title("IEEE Paper")
#     st.subheader("Main")

#     # Get data from Firebase Realtime Database
#     lux          = db.child("BH1750"    ).child("lux"        ).get()
#     temperature  = db.child("DHT"       ).child("temperature").get()
#     humidity     = db.child("DHT"       ).child("humidity"   ).get()
# #     onFog        = db.child("fogMachine").child("isOn"       ).get()
# #     onShade      = db.child("shadeMotor").child("isOn"       ).get()
# #     onBulb       = db.child("heaterBulb").child("isOn"       ).get()
# #     setFog       = db.child("fogMachine").child("setOn"      ).get()
# #     setShade     = db.child("shadeMotor").child("setOn"      ).get()
# #     setBulb      = db.child("heaterBulb").child("setOn"      ).get()

#     # Display data
#     st.write("Lux: ",             lux.val())
#     st.write("Temperature: ",     temperature.val())
#     st.write("Humidity: ",        humidity.val())
# #     st.write("Fog Machine: ",     onFog.val())
# #     st.write("Shade Motor: ",     onShade.val())
# #     st.write("Heater Bulb: ",     onBulb.val())
# #     st.write("Set Fog Machine: ", setFog.val())
# #     st.write("Set Shade Motor: ", setShade.val())
# #     st.write("Set Heater Bulb: ", setBulb.val())


# if __name__ == "__main__":
#     main()
    #st.sidebar.title("IEEE Paper")
    #menu = st.sidebar.radio("Menu", ["Login", "SignUp"])
    #if menu == "Login":
    #    login()
    #elif menu == "SignUp":
    #    signup()

# import streamlit as st
# import firebase_admin
# #from firebase_admin import credentials
# from firebase_admin import db

# #cred = credentials.Certificate("C:\Users\asus\Downloads\key.json")

# # Initialize the Firebase app
# firebase_admin.initialize_app()


# # Function to update the boolean value in Firebase
# def update_boolean_value(value):
#     ref = db.reference('https://bsf-bradley-default-rtdb.firebaseio.com/fogMachine/setOn')
#     ref.set(value)

# # Streamlit app
# def main():
#     st.title("Firebase Realtime Database Example")
    
#     # Button to update boolean value to True
#     if st.button("Set fogOn to True"):
#         update_boolean_value(True)
#         st.success("Boolean value set to True")
    
#     # Button to update boolean value to False
#     if st.button("Set fog On to False"):
#         update_boolean_value(False)
#         st.success("Boolean value set to False")

# if __name__ == "__main__":
#     main()
