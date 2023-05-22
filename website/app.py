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
  
def fogMachine():
  st.title("Fog Machine Control")
  menu = st.radio("Menu", ["Turn On Inactive","Turn On ",,"Turn Off Inactive","Turn Off"])
  if menu == "Turn On":
    db.child("fogMachine").update({"setOn":True})
    st.success("Fog machine turned on")
  elif menu == "Undo Turn On":
    db.child("fogMachine").update({"setOn":False})
    st.success("Action Undone")
  elif menu == "Turn Off":
    db.child("fogMachine").update({"setOff":True})
    st.success("Fog machine turned off")
  elif menu == "Undo Turn Off":
    db.child("fogMachine").update({"setOff":False})
    st.success("Action Undone")
 
def heater():
  st.title("Heater Bulb Control")
  menu = st.radio("Menu", ["Turn On Inactive","Turn On ",,"Turn Off Inactive","Turn Off"])
  if menu == "Turn On":
    db.child("heaterBulb").update({"setOn":True})
    st.success("Fog machine turned on")
  elif menu == "Turn On Inactive":
    db.child("heaterBulb").update({"setOn":False})
    st.success("Action Undone")
  elif menu == "Turn Off":
    db.child("heaterBulb").update({"setOff":True})
    st.success("Fog machine turned off")
  elif menu == "Turn Off Inactive":
    db.child("heaterBulb").update({"setOff":False})
    st.success("Action Undone")    
    
def shade():
  st.title("Shade Motor Control")
  menu = st.radio("Menu", ["Turn On Inactive","Turn On ",,"Turn Off Inactive","Turn Off"])
  if menu == "Turn On":
    db.child("shadeMotor").update({"setOn":True})
    st.success("Fog machine turned on")
  elif menu == "Turn On Inactive":
    db.child("shadeMotor").update({"setOn":False})
    st.success("Action Undone")
  elif menu == "Turn Off":
    db.child("shadeMotor").update({"setOff":True})
    st.success("Fog machine turned off")
  elif menu == "Turn Off Inactive":
    db.child("shadeMotor").update({"setOff":False})
    st.success("Action Undone")
    
    
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
    
    menu = st.sidebar.radio("Menu",["Heater Bulb","Fog Machine","Shade Motor"])
    if menu == "Heater Bulb":
      heater()
    elif menu == "Fog Machine":
      fogMachine()
    elif menu == "Shade Motor":
      shade()
    
    
#       try:
#           db.child("fogMachine").update({"setOn":True})
#           st.success("Fog Machine On")
#           st.write("Hello Fog Machine")
#           main()
#       except:
#           st.write("Failed")
      
      
#         try:
#             db.child("fogMachine").update({"setOn":True})
#             st.success("Fog Machine On")
#         except:
#             pass
#     elif st.button("Undo Fog Machine"):
#         try:
#             db.child("fogMachine").update({"setOn":False})
#             st.success("Task undone")
#         except:
#             pass
    
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
    st.sidebar.title("BSF System Monitoring")
    menu = st.sidebar.radio("Menu", ["Login", "SignUp"])
    if menu == "Login":
        login()
    elif menu == "SignUp":
        signup()

#I hope this helps you to get started with Firebase and Streamlit. If you have any questions, please let me know in the comments below.
