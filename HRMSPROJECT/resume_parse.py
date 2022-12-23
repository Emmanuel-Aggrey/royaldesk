import requests

# url = "https://docs.google.com/document/d/1PDInpw8dIwtELfz1pTFtsu-x0NoVHsf4/edit?usp=sharing&ouid=112142976742729723601&rtpof=true&sd=true"
url = 'http://127.0.0.1:8000/static/js/default_profile.jpg'
payload = {}
headers= {
  "apikey": "RC6V4CmviTUY40roSUNsQSGhBRY531gj"
}

response = requests.request("GET", url, headers=headers, data = payload)

status_code = response.status_code
result = response.text

print(result)


import docx2txt

# Read the contents of the CV into a string
cv_text = docx2txt.process("cv.docx")

# Use regular expressions to extract the email, date of birth, and phone
import re

email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
dob_pattern = r"\b(?:(?:0?[13578]|1[02])(?:0[1-9]|[12][0-9]|3[01]))(?:|-)(?:(?:19|20)\d\d)\b"
phone_pattern = r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"

email = re.search(email_pattern, cv_text).group()
dob = re.search(dob_pattern, cv_text).group()
phone = re.search(phone_pattern, cv_text).group()

# Populate the fields in a form or database
form = {"email": email, "dob": dob, "phone": phone}
database.add_record(form)


import re
import PyPDF2

# Open the PDF file in read-binary mode
with open('document.pdf', 'rb') as file:
  # Create a PDF object
  pdf = PyPDF2.PdfFileReader(file)
  
  # Get the first page
  page = pdf.getPage(0)
  
  # Extract the text from the page
  text = page.extractText()
  
  # Split the text into lines
  lines = text.split('\n')
  
  # Initialize variables to store the extracted information
  date_of_birth = ""
  name = ""
  email = ""
  phone = ""
  
  # Iterate over the lines
  for line in lines:
    # Use a regular expression to search for a pattern that matches the format of a date of birth
    match = re.search(r'\b(0?[1-9]|[12]\d|3[01])[- /.](0?[1-9]|1[012])[- /.](19|20)\d{2}\b', line)
    if match:
      # If a match is found, extract the date of birth
      date_of_birth = match.group()
      continue
      
    # Use a regular expression to search for a pattern that matches the format of a name
    match = re.search(r'[A-Z][a-z]+ [A-Z][a-z]+', line)
    if match:
      # If a match is found, extract the name
      name = match.group()
      continue
      
    # Use a regular expression to search for a pattern that matches the format of an email address
    match = re.search(r'[\w.-]+@[\w.-]+', line)
    if match:
      # If a match is found, extract the email
      email = match.group()
      continue
      
    # Use a regular expression to search for a pattern that matches the format of a phone number
    match = re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', line)
    if match:
      # If a match is found, extract the phone number
      phone = match.group()
      continue
      
  # Print the extracted information
  print("Date of birth:", date_of_birth)
  print("Name:", name)
  print("Email:", email)
  print("Phone:", phone)
