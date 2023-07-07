import pyrebase
import streamlit as st
from datetime import datetime


firebaseConfig = {
<<<<<<< Updated upstream
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
  current_value = db.child("heaterBulb").child("setOn").get().val()  # Fetch current value from the database
  new_value = not current_value  # Toggle the value
  db.child("heaterBulb").child("setOn").set(new_value)
  if new_value == True:
    st.success("Manual ON activated")
  elif new_value == False:
    st.success("Manual ON deavtivated")
#     ref = db.child("heaterBulb").child('setOn')
#     if ref == True:
#       ref.set(False)
#       st.success("Manual ON deactivated")
#     elif ref == False:
#       ref.set(True)
#       st.success("Manual ON activated")
    #st.write("Bulb!!")
def update_bulbOff():
  current_value = db.child("heaterBulb").child("setOff").get().val()  # Fetch current value from the database
  new_value = not current_value  # Toggle the value
  db.child("heaterBulb").child("setOff").set(new_value)
  if new_value == True:
    st.success("Manual OFF activated")
  elif new_value == False:
    st.success("Manual OFF deavtivated")
#     ref = db.child("heaterBulb").child('setOff')
#     ref.set(value)
#     ref = db.child("heaterBulb").child('setOff')
#     if ref == True:
#       ref.set(False)
#       st.success("Manual OFF deactivated")
#     elif ref == False:
#       ref.set(True)
#       st.success("Manual OFF activated")
=======
  'apiKey'             : "AIzaSyAHDUls-v3DKM7q9X70OkXaMzIbNgWqHR4",
  'authDomain'         : "ieeepaper.firebaseapp.com",
  'databaseURL'        : "https://ieeepaper-default-rtdb.europe-west1.firebasedatabase.app",
  'projectId'          : "ieeepaper",
  'storageBucket'      : "ieeepaper.appspot.com",
  'messagingSenderId'  : "296735563322",
  'appId'              : "1:296735563322:web:8264b3da451df8ed881f03",
  'measurementId'      : "G-295EPTTZ0W"
}
>>>>>>> Stashed changes

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

# Main Page
def main():
<<<<<<< Updated upstream
    st.title("BSF SYSTEM MONITORING")
    st.subheader("Parameters")
    lux          = db.child("BH1750"    ).child("lux"        ).get()
    temperature  = db.child("DHT"       ).child("temperature").get()
    humidity     = db.child("DHT"       ).child("humidity"   ).get()
    bulbOn       = db.child("heaterBulb").child("setOn").get()
    bulbOff      = db.child("heaterBulb").child("setOff").get()
    
=======
    st.title("IEEE Paper")
    st.subheader("Main")

    # Get data from Firebase Realtime Database
    lux          = db.child("BH1750"    ).child("lux"        ).get()
    temperature  = db.child("DHT"       ).child("temperature").get()
    humidity     = db.child("DHT"       ).child("humidity"   ).get()
    onFog        = db.child("fogMachine").child("isOn"       ).get()
    onShade      = db.child("shadeMotor").child("isOn"       ).get()
    onBulb       = db.child("heaterBulb").child("isOn"       ).get()
    setFog       = db.child("fogMachine").child("setOn"      ).get()
    setShade     = db.child("shadeMotor").child("setOn"      ).get()
    setBulb      = db.child("heaterBulb").child("setOn"      ).get()

>>>>>>> Stashed changes
    # Display data
    st.write("Lux: ",             lux.val())
    st.write("Temperature: ",     temperature.val())
    st.write("Humidity: ",        humidity.val())
<<<<<<< Updated upstream
    
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
    
   


=======
    st.write("Fog Machine: ",     onFog.val())
    st.write("Shade Motor: ",     onShade.val())
    st.write("Heater Bulb: ",     onBulb.val())
    st.write("Set Fog Machine: ", setFog.val())
    st.write("Set Shade Motor: ", setShade.val())
    st.write("Set Heater Bulb: ", setBulb.val())


if __name__ == "__main__":
    main()
    #st.sidebar.title("IEEE Paper")
    #menu = st.sidebar.radio("Menu", ["Login", "SignUp"])
    #if menu == "Login":
    #    login()
    #elif menu == "SignUp":
    #    signup()

# import streamlit as st
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db

# # Initialize the Firebase app
# cred = credentials.Certificate("https://bsf-bradley-default-rtdb.firebaseio.com/webapp/private_key.json")
# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://bsf-bradley-default-rtdb.firebaseio.com/'
# })

# # Function to update the boolean value in Firebase
# def update_boolean_value(value):
#     ref = db.reference('/fogMachine/setOn')
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

# if _name_ == "_main_":
#     main()
>>>>>>> Stashed changes
