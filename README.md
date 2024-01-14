# Personal Project: Two-Factor Authentication

## Overview
This app simulates a two-factor authentication login system. The purpose of this personal object is to learn more about utilizing tkinter GUI for a frontend user experience and exploring the qrcode and pyotp libraries.

## Functionality
tkinter: The tkinter package (“Tk interface”) is the standard Python interface to the Tcl/Tk GUI toolkit. It was used to create the windows, labels, buttons and entry boxes that the user can see and interact with when running the applicaiton.

PyOTP: PyOTP is a Python library for generating and verifying one-time passwords. It can be used to implement two-factor (2FA) or multi-factor (MFA) authentication methods in web applications and in other systems that require users to log in. After the user enters their correct account information, this library is then utilized to generate a verification code that can be sent to the user via QR Code.

qrcode: QR Codes are 2D barcodes that can store data such as texts and links. For this application, the qrcode library is used to generate a QR code that contains the generated verifcation code. The user can then scan the QR Code with the Google Authenticator App to access the code and view its expiration time.

