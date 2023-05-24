import pyrebase
import streamlit as st
from datetime import datetime


firebaseConfig = {
  'apiKey': "AIzaSyAtqKKRESq6bK8-2f4ypc4tb4zY5pDWXFs",
  'authDomain': "bsf-bradley.firebaseapp.com",
  'databaseURL': "https://bsf-bradley-default-rtdb.firebaseio.com",
  'projectId': "bsf-bradley",
  'storageBucket': "bsf-bradley.appspot.com",
  'messagingSenderId': "584438088785",
  'appId': "1:584438088785:web:6cfd98e025c04ce0212470",
  'measurementId': "G-BMQN6WWJL1"
}

# Initialize Firebase
firebase    = pyrebase.initialize_app(firebaseConfig)
auth        = firebase.auth()
db          = firebase.database()
storage     = firebase.storage()

# sign up
def signup():
    st.title("BSF SYSTEM")
    st.subheader("Sign Up Page")
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
    st.title("BSF SYSTEM")
    st.subheader("Login Page")
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
    st.title("BSF System")
    st.subheader("Parameters")

    # Get data from Firebase Realtime Database
    lux          = db.child("BH1750"    ).child("lux"        ).get()
    temperature  = db.child("DHT"       ).child("temperature(celcius)").get()
    humidity     = db.child("DHT"       ).child("humidity"   ).get()
    
    # Display data
    st.write("Lux: ",             lux.val())
    st.write("Temperature: ",     temperature.val())
    st.write("Humidity: ",        humidity.val())
    
    def FogOn():
      db.child("fogMachine").child("setOn").set(True)
      
    def undoFogOn():
      db.child("fogMachine").child("setOn").set(False)
      
    def FogOff():
      db.child("fogMachine").child("setOff").set(True)
    
    def undoFogOff():
      db.child("fogMachine").child("setOff").set(False)
      
      
    st.button(
      "Fog Machine On",
      on_click = FogOn()
    )
    st.button(
      "Undo Fog Machine On",
      on_click = undoFogOn()
    )
    st.button(
      "Fog Machine Off",
      on_click = FogOff()
    )
    st.button(
      "Undo Fog Machine Off",
      on_click = undoFogOff()
    )
    
#     onFog        = db.child("fogMachine").child("isOn"       ).get()
#     offFog       = db.child("fogMachine").child("isOff"      ).get()
#     onShade      = db.child("shadeMotor").child("isOn"       ).get()
#     offShade     = db.child("shadeMotor").child("isOff"      ).get()
#     onBulb       = db.child("heaterBulb").child("isOn"       ).get()
#     offBulb      = db.child("heaterBulb").child("isOff"      ).get()
#     setFogOn     = db.child("fogMachine").child("setOn"      ).get()
#     setFogOff    = db.child("fogMachine").child("setOff"     ).get()
#     setShadeOn   = db.child("shadeMotor").child("setOn"      ).get()
#     setShadeOff  = db.child("shadeMotor").child("setOff"     ).get()
#     setBulbOn    = db.child("heaterBulb").child("setOn"      ).get()
#     setBulbOff   = db.child("heaterBulb").child("setOff"     ).get()

#     st.write("Fog Machine manual on: ",     onFog.val())
#     st.write("Fog Machine manual off: ",     offFog.val())
#     st.write("Shade Motor: ",     onShade.val())
#     st.write("Heater Bulb: ",     onBulb.val())
#     st.write("Set Fog Machine Off: ", setFogOn.val())
#     st.write("Set Fog Machine : ", setFogOff.val())
#     st.write("Set Shade Motor: ", setShade.val())
#     st.write("Set Shade Motor: ", setShade.val())
#     st.write("Set Heater Bulb: ", setBulbOn.val())
#     st.write("Set Heater Bulb: ", setBulbOn.val())


if __name__ == "__main__":
  main()
#     st.sidebar.title("BSF System Monitoring")
#     menu = st.sidebar.radio("Menu", ["Login", "SignUp"])
#     if menu == "Login":
#         login()
#     elif menu == "SignUp":
#         signup()

#I hope this helps you to get started with Firebase and Streamlit. If you have any questions, please let me know in the comments below.
