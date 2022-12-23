import re
import PyPDF2

# Open the PDF file in read-binary mode
with open('Emmanuel Teye Nartey.pdf', 'rb') as file:
  # Create a PDF object
  pdf = PyPDF2.PdfFileReader(file)
  
  # Get the first page
  page = pdf.getPage(0)
  
  # Extract the text from the page
  text = page.extractText()
  print(text)
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
