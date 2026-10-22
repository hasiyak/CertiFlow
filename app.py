import streamlit as st
import pandas as pd
import os
import smtplib
from email.message import EmailMessage
import pymupdf as fitz
import tempfile
import zipfile
import io
import time

# --- UI Configuration ---
st.set_page_config(page_title="CertiFlow", layout="wide", page_icon="🎓")

# --- Custom CSS & Footer Styling ---
st.markdown("""
    <style>
    /* Button Styling */
    div.stButton > button:first-child {
        background-color: #150d57;
        color: white;
        border-radius: 8px;
        width: 100%;
        height: 50px;
        font-weight: bold;
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #281a9c;
        border-color: #281a9c;
    }
    
    /* Hide Streamlit Default Footer */
    footer {visibility: hidden;} 
    
    /* Custom Modern Footer Styling */
    .custom-footer {
        background-color: rgba(128, 128, 128, 0.12);
        border-radius: 8px;
        text-align: center;
        padding: 12px;
        margin-top: 50px;
        font-size: 14px;
        color: var(--text-color); 
        opacity: 0.55; 
        font-family: 'Segoe UI', sans-serif;
    }
    .custom-footer .brand {
        font-weight: 900;
    }
    .section-spacer {
        margin-top: 30px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Display Banner Image (Full width to fit app size) ---
try:
    st.image("banner.jpg", use_container_width=True)
except Exception:
    pass

st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
st.title("🎓 CertiFlow - Automated PDF Certificate Generator & Emailer")
st.write("Upload your details below to generate custom certificates and optionally email them to participants.")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

# --- 1. File Uploads (CSV/Excel & PDF) ---
st.header("📁 1. Upload Files")
col1, col2 = st.columns(2)
with col1:
    data_file = st.file_uploader("Upload Attendees List (CSV or Excel)", type=["csv", "xlsx", "xls"])
    st.caption("⚠️ Your file must have columns named **'name'** and **'email'**.")
with col2:
    template_file = st.file_uploader("Upload Certificate Template (PDF)", type=["pdf"])

font_file = st.file_uploader("Upload Custom Font (.otf / .ttf) [Optional]", type=["otf", "ttf"])

st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

# --- 2. Certificate Settings ---
st.header("⚙️ 2. Certificate Settings")
st.info("ℹ️ **Note:** Use the X and Y coordinates below to correctly position the participant's name exactly on the blank space of your certificate template.")

col3, col4, col5 = st.columns(3)
with col3:
    x_cord = st.number_input("Text X Coordinate", value=240)
with col4:
    y_cord = st.number_input("Text Y Coordinate", value=277)
with col5:
    font_size = st.slider("Font Size", min_value=10, max_value=100, value=40)

is_bold = st.checkbox("Make Text Bold (Applies only if no custom font is uploaded)")

st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

# --- 3. Email Settings (Optional) ---
st.header("📧 3. Email Settings")
send_emails = st.checkbox("Enable Automatic Email Sending")

if send_emails:
    with st.expander("ℹ️ How to get a Gmail App Password?"):
        st.markdown("""
        **English:**
        You cannot use your standard Gmail password here. Please create an App Password:
        1. Go to [Google Account Security](https://myaccount.google.com/security).
        2. Ensure **2-Step Verification** is turned ON.
        3. Search for **App passwords** in the top search bar.
        4. Enter 'CertiFlow' as the App name and click **Create**.
        5. Copy the **16-letter password** (without spaces) and paste it below.
        """)

    st.info("💡 You can use **{name}** in the Email Body. It will automatically be replaced by the participant's name.")
    e_col1, e_col2 = st.columns(2)
    with e_col1:
        sender_email = st.text_input("Your Gmail Address")
    with e_col2:
        sender_password = st.text_input("Your 16-digit App Password", type="password")
    
    email_subject = st.text_input("Email Subject", value="Your Certificate of Participation")
    
    default_body = """<html>
  <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333333;">
    <h2 style="color: #150d57;">Dear {name},</h2>
    <p>With great honor, please find attached your <b>Certificate of Achievement</b>.</p>
    <p>Best Regards,<br>Event Organizing Committee</p>
  </body>
</html>"""
    email_body = st.text_area("Email Body (HTML supported)", value=default_body, height=200)

st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

# --- 4. Process Execution ---
st.write("---")
if st.button("🚀 Process Certificates"):
    if not data_file or not template_file:
        st.error("⚠️ Please upload both the Data file (CSV/Excel) and the PDF Template!")
    elif send_emails and (not sender_email or not sender_password):
        st.error("⚠️ Please provide Email Credentials, or untick the Email Sending option.")
    else:
        try:
            if data_file.name.endswith('.csv'):
                df = pd.read_csv(data_file)
            elif data_file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(data_file)
        except Exception as e:
            st.error(f"Error reading the file: {e}")
            st.stop()

        if 'name' not in df.columns or 'email' not in df.columns:
            st.error("⚠️ The uploaded file MUST contain columns named 'name' and 'email'. Please check your file.")
            st.stop()

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_template_path = os.path.join(temp_dir, "template.pdf")
            with open(temp_template_path, "wb") as f:
                f.write(template_file.getbuffer())

            font_path = None
            if font_file:
                font_path = os.path.join(temp_dir, font_file.name)
                with open(font_path, "wb") as f:
                    f.write(font_file.getbuffer())

            total_users = len(df)
            success_count = 0
            zip_buffer = io.BytesIO()

            progress_bar = st.progress(0)
            
            # Professional Status Animation
            with st.status("⏳ Starting the process...", expanded=True) as status:
                with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                    for index, row in df.iterrows():
                        name = str(row['name']).strip()
                        email = str(row['email']).strip()
                        
                        status.update(label=f"⏳ Processing: {name} ({index + 1}/{total_users})", state="running")
                        
                        try:
                            # 1. PDF Generation
                            output_pdf = os.path.join(temp_dir, f"{name.replace(' ', '_')}.pdf")
                            doc = fitz.open(temp_template_path)
                            page = doc[0]
                            text_point = fitz.Point(x_cord, y_cord)
                            
                            if font_path:
                                page.insert_text(text_point, name, fontsize=font_size, fontfile=font_path, fontname="custom", color=(21/255, 13/255, 87/255))
                            else:
                                default_font = "hebo" if is_bold else "helv"
                                page.insert_text(text_point, name, fontsize=font_size, fontname=default_font, color=(21/255, 13/255, 87/255))
                            
                            doc.save(output_pdf)
                            doc.close()
                            zip_file.write(output_pdf, f"{name}_Certificate.pdf")
                            st.write(f"📄 Generated PDF for **{name}**")
                            
                            # 2. Email Dispatch
                            if send_emails:
                                msg = EmailMessage()
                                msg['Subject'] = email_subject
                                msg['From'] = sender_email
                                msg['To'] = email
                                
                                formatted_body = email_body.replace("{name}", name)
                                msg.set_content("Please enable HTML to view this email.") 
                                msg.add_alternative(formatted_body, subtype='html')
                                
                                with open(output_pdf, 'rb') as f:
                                    msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename=f"{name}_Certificate.pdf")
                                
                                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                                    smtp.login(sender_email, sender_password)
                                    smtp.send_message(msg)
                                
                                st.write(f"📧 Successfully sent email to **{email}**")
                                
                            success_count += 1
                            
                        except Exception as e:
                            st.error(f"❌ Failed for {name}: {e}")
                        
                        progress_bar.progress((index + 1) / total_users)
                        time.sleep(0.1)
                        
                # Finalizing the status box
                status.update(label=f"✅ Complete! Successfully processed {success_count} out of {total_users} records.", state="complete", expanded=False)
            
            st.toast("Process Completed Successfully!", icon="✅")
            
            st.download_button(
                label="📥 Download All Certificates (ZIP Archive)",
                data=zip_buffer.getvalue(),
                file_name="Certificates_Archive.zip",
                mime="application/zip",
                type="primary"
            )

# --- 5. Custom Footer Render ---
st.markdown("""
    <div class="custom-footer">
        <span class="brand">CertiFlow</span> Automated Certificate Generation System &nbsp; | &nbsp; Developed with ❤️ by <b>Hasindu Kaveeshwara</b> © 2026
    </div>
""", unsafe_allow_html=True)