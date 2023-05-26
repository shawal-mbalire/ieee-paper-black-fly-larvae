# import pyrebase
# import streamlit as st
# from datetime import datetime


# firebaseConfig = {
#   'apiKey'             : "AIzaSyAHDUls-v3DKM7q9X70OkXaMzIbNgWqHR4",
#   'authDomain'         : "ieeepaper.firebaseapp.com",
#   'databaseURL'        : "https://ieeepaper-default-rtdb.europe-west1.firebasedatabase.app",
#   'projectId'          : "ieeepaper",
#   'storageBucket'      : "ieeepaper.appspot.com",
#   'messagingSenderId'  : "296735563322",
#   'appId'              : "1:296735563322:web:8264b3da451df8ed881f03",
#   'measurementId'      : "G-295EPTTZ0W"
# }

# # Initialize Firebase
# firebase    = pyrebase.initialize_app(firebaseConfig)
# auth        = firebase.auth()
# db          = firebase.database()
# storage     = firebase.storage()

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

# # Main Page
# def main():
#     st.title("IEEE Paper")
#     st.subheader("Main")

#     # Get data from Firebase Realtime Database
#     lux          = db.child("BH1750"    ).child("lux"        ).get()
#     temperature  = db.child("DHT"       ).child("temperature").get()
#     humidity     = db.child("DHT"       ).child("humidity"   ).get()
#     onFog        = db.child("fogMachine").child("isOn"       ).get()
#     onShade      = db.child("shadeMotor").child("isOn"       ).get()
#     onBulb       = db.child("heaterBulb").child("isOn"       ).get()
#     setFog       = db.child("fogMachine").child("setOn"      ).get()
#     setShade     = db.child("shadeMotor").child("setOn"      ).get()
#     setBulb      = db.child("heaterBulb").child("setOn"      ).get()

#     # Display data
#     st.write("Lux: ",             lux.val())
#     st.write("Temperature: ",     temperature.val())
#     st.write("Humidity: ",        humidity.val())
#     st.write("Fog Machine: ",     onFog.val())
#     st.write("Shade Motor: ",     onShade.val())
#     st.write("Heater Bulb: ",     onBulb.val())
#     st.write("Set Fog Machine: ", setFog.val())
#     st.write("Set Shade Motor: ", setShade.val())
#     st.write("Set Heater Bulb: ", setBulb.val())


# if __name__ == "__main__":
#     main()
#     #st.sidebar.title("IEEE Paper")
#     #menu = st.sidebar.radio("Menu", ["Login", "SignUp"])
#     #if menu == "Login":
#     #    login()
#     #elif menu == "SignUp":
#     #    signup()

import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

firebaseConfig = {
  "type":           "service_account",
  "project_id":     "bsf-bradley",
  "private_key_id": "be10d041e30c2cb6cae1a389cc3ab90711e98c42",
  "private_key":    "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDTEThoNj6HIBEd\nEDszfB61wcA5D8h5fnLzWavByaBPntutxk/28AsM1oES+BWx+NIbIhn4GRDjPf0k\n+pAGuSle5JkFFa99uHvq9O7LSepIEEr63qBS2apU7+ujGW63dTVwilwMavqRSwSO\n/tmln42UcQ/QCfkVVzB6r97c+5v3wd16Gvo3rFk5Fg7qaBTzCwECOkEyqFBj9WhP\n/zt+OECmhQhuUrcJG//kCtl4fXXb+8aNyawT1dbCzcPviSuJe22dDRycXdM4oPqr\n9vlRWLd5wcwZm9ay/TfurFR4ukJgXCXuTppl4uh5/tSESyNQQs6aFit0RbFj5+qD\nMDOMLZOrAgMBAAECggEAS0FdklKc8sLtNyadZRsBPB8L8Yx+F0uNotS7F8pTHXBv\ntUL7KfmmhvpIZUINQjqMd14uUjZlvhBRHQk1pyAH7yyknpp/ytynWjvglJ0TKoSc\np1wPX9r6D3TH2Ixt3H2vAyRh84+FLZ7Izk9xvMrpyR6S28Nii0heIbBpTvNrRee0\n0RlWPC7MepuVW/8n92Y+0uIHCa6bMumj9OYPUtSOCpQYWz/9fHZR33wR/pY9oJqu\nkWxkFjHMIKBl/98hst2bNtDZqv3WOMwtgCYkAbeomG8ZnTLd2mwVz2VI4ExuhT+4\npUjFqGCOrzJ0E2TpQ8Wgg6wmpBJwjoZCgDmUFBh1SQKBgQDrRzOj1xDwdz1YhcGk\nD8xMBKVsXfTWwkj8eDsfmfLauadmiErivan9KpjuTAYGakT9rqDSmgiVHJL4Ttpx\nR9HGfl1MAJ8Z9XbACN06C1DpNDM4sIVRQlvpi2egNcaVqnmiQmrv9em2TEbTA7Uj\nf3vP7PhWXp2iCoIRt1Cead7eZQKBgQDlqCNZQMUIh4/bosu2X4MiI9cMSpkxou9n\nxbugelITQK+K9vQGP1SfvhRwplhifxDFsYTWmVgjJ7r1V/2UctxuZeL7uHF2WXSM\neNZ0vngkKarRopmHKvP5isuTaQIgiWyccSmhBl6tYJLA9uKHLPsj9HaUlh8H9yv3\n0UBwGLzAzwKBgBVLwJTX5qSdZmQY10ouU+OdmAuTBZJay5humYtmt+CsZUaWl5Cm\ncjiEHouTPghenhgIMm5dmuFEUNlA6ezO/2HkFjXG6J/E5BbFtqCGXbB+FRTQhYCx\nbPhaseqCc5MgdxoEwQEvVRQ3G0IGV+L6qw5K+L94mPQN13AbE6UDGDUxAoGAaxw+\nUFRbER1YxRFqfYaSfIvGsp7gUDwz+GxKlBA4023p8aA4M+m5qD9Y/Sk4M8gbpHil\nAgnHB65yDheZ13CyynKOqORfVtll+FYrf4uOMR+V4ew6OsaXv50yUXA6Y750f4pv\n5gA4jBhsmb8L7AvYne5Yl/hkRKzNPunDagS/lBUCgYAi6RheKp5Iu8lx5wlpbFNs\nUYva1EOqrcTDKprHXnva4zeEO9SXDjK2o61vdqqJSQR/CrvqKdWt2Vl37o7MXA5g\nbwl70bWznG/ODJgkaPaEgjzSrjgXf2SP+tabuq5lbbJtlEO4y6wResrbH/gMR4OP\n3UR1My6PRDwduhSVxMBHaw==\n-----END PRIVATE KEY-----\n",
  "client_email":   "firebase-adminsdk-snxpg@bsf-bradley.iam.gserviceaccount.com",
  "client_id":      "118392316616996417164",
  "auth_uri":       "https://accounts.google.com/o/oauth2/auth",
  "token_uri":      "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-snxpg%40bsf-bradley.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com",
  "databaseURL":     "https://bsf-bradley-default-rtdb.firebaseio.com/"
}
    
# Initialize the Firebase app
firebase_admin.initialize_app(firebaseConfig)

# Function to update the boolean value in Firebase
def update_boolean_value(value):
    ref = db.reference('/fogMachine/setOn')
    ref.set(value)

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

if _name_ == "_main_":
    main()
