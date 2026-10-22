# \# 🎓 CertiFlow

# 

# \*\*Automated Certificate Generation \& Email Dispatch System\*\*

# 

# CertiFlow is a fully-featured, user-friendly Web Application built with Python and Streamlit. It automates the tedious process of generating personalized event certificates and emailing them directly to participants. Designed for event organizers, universities, and student chapters, CertiFlow eliminates manual graphic editing and bulk emailing workflows.

# 

# Developed as a final project for CS50P, this application has evolved into a robust production-ready web tool.

# 

# \---

# 

# \## ✨ Key Features

# 

# \* \*\*Flexible Data Input:\*\* Upload participant details using standard CSV or Excel (`.xlsx`, `.xls`) files.

# \* \*\*Precision Placement:\*\* Dynamically adjust the X and Y coordinates via the UI to place the participant's name exactly on your blank PDF certificate template.

# \* \*\*Custom Typography:\*\* Upload your own custom fonts (`.otf` or `.ttf`) or use the built-in bold formatting to match your event's branding.

# \* \*\*Automated Email Dispatch:\*\* Seamlessly send customized emails to all participants using standard Gmail App Passwords.

# \* \*\*Dynamic HTML Emails:\*\* Write custom email bodies with `{name}` placeholders that automatically personalize the message for each recipient.

# \* \*\*Real-time Status Tracking:\*\* Monitor the generation and emailing process with a sleek, real-time progress bar and step-by-step status animations.

# \* \*\*Bulk Download:\*\* Generates an in-memory ZIP archive of all personalized PDF certificates for easy one-click downloading, automatically cleaning up temporary server files afterward.

# 

# \---

# 

# \## 🛠️ Tech Stack

# 

# \* \*\*Frontend \& UI:\*\* \[Streamlit](https://streamlit.io/)

# \* \*\*PDF Processing:\*\* \[PyMuPDF (fitz)](https://pymupdf.readthedocs.io/)

# \* \*\*Data Handling:\*\* \[Pandas](https://pandas.pydata.org/), \[Openpyxl](https://openpyxl.readthedocs.io/)

# \* \*\*Email Automation:\*\* Python `smtplib`, `email.message.EmailMessage`

# \* \*\*File Management:\*\* `tempfile`, `zipfile`, `io`

# 

# \---

# 

# \## 🚀 How to Run Locally

# 

# \### 1. Clone the Repository

# ```bash

# git clone \[https://github.com/HasinduK/CertiFlow.git](https://github.com/HasinduK/CertiFlow.git)

# cd CertiFlow





2\. Install Dependencies

Ensure you have Python 3 installed, then install the required libraries:

Bash
pip install -r requirements.txt

3\. Launch the Web App

Bash
streamlit run app.py
The application will automatically open in your default web browser.



📖 Usage Guide

Upload Files: Upload your Excel/CSV file (must contain name and email columns) and your blank Certificate Template (PDF). Optional: Upload a custom font file.
Configure Placement: Use the numerical steppers to adjust the X and Y coordinates. Adjust the font size as needed.
Setup Email (Optional): Check the "Enable Automatic Email Sending" box. Enter your Gmail address and a 16-digit Google App Password. Customize your subject and HTML body.
Process: Click 🚀 Process Certificates.
Download: Once the progress completes, click the download button to save a ZIP file containing all the generated PDFs.



👨‍💻 Author

Hasindu Kaveeshwara
Undergraduate, BSc in Computer Science
Faculty of Computing and Technology, University of Kelaniya
This project was developed for Harvard University's CS50P (Introduction to Programming with Python).

