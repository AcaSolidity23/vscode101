import re
import pytesseract
import pyodbc
import os
import subprocess
import cv2
from datetime import datetime, timedelta

# Set TESSDATA_PREFIX and tesseract_cmd
tessdata_prefix = r"C:\Users\alazarevic\AppData\Local\Programs\Tesseract-OCR\tessdata"
tesseract_cmd = r'C:\Users\alazarevic\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
# tessdata_dir_config = "--tessdata-dir C:\\Users\\alazarevic\\AppData\\Local\\Programs\\Tesseract-OCR\\tessdata\\"

# Add TESSDATA_PREFIX to the system PATH
os.environ['TESSDATA_PREFIX'] = tessdata_prefix
pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
# print('TESSDATA_PREFIX: ' + os.environ['TESSDATA_PREFIX'])

# Set the Windows encoding to UTF-8
os.environ['PYTHONIOENCODING'] = 'utf-8'

def list_tesseract_languages():
    try:
        # Run the tesseract command to list languages
        result = subprocess.run([tesseract_cmd, '--list-langs'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check if the command was successful
        if result.returncode == 0:
            languages = result.stdout.splitlines()[1:]  # Skip the first line which is not a language
            print("Installed Tesseract languages:")
            for lang in languages:
                print(lang)
        else:
            print("Error listing Tesseract languages:")
            print(result.stderr)
    except FileNotFoundError:
        print("Tesseract is not installed or not found in the system PATH.")

# list_tesseract_languages()

# Define the file path
jpeg_file_path = r'C:\Users\alazarevic\Desktop\RSD_izvod.jpg'

# Open the image file
image = cv2.imread(jpeg_file_path)
# resize image
(image_height, image_width) = image.shape[:2]
image = cv2.resize(image, (image_width*5, image_height*5), interpolation = cv2.INTER_CUBIC)

# Grayscale, Gaussian blur, Otsu's threshold
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (11, 11), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Morph open to remove noise and invert image
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
invert = 255 - opening

# Use pytesseract to do OCR on the image
text = pytesseract.image_to_string(invert, lang='srp_latn',config='--psm 6')
print(text)

# Extract row containing "Trenutno stanje"
lines = text.split('\n')
for line in lines:
    if "Trenutno stanje" in line:
        trenutnostanje_line = line
        break

# cv2.imshow('thresh', thresh)
# cv2.imshow('opening', opening)
# cv2.imshow('invert', invert)
# cv2.waitKey()

# Define a regex to find numbers
number_regex = re.compile(r'(?:\d{1,3}(?:,\d{3})+)(?:\.\d{2})')
date_regex = re.compile(r'(\d{4}.\d{2}.\d{2})')

# Find all numbers in the extracted text
numbers = number_regex.findall(trenutnostanje_line)
StDt = date_regex.findall(text)

# Convert StDt[0] to a date format
StDt[0] = StDt[0].replace('–', '-')
date_value = datetime.strptime(StDt[0], '%Y-%m-%d').date()
formatted_date = date_value.strftime('%d-%b-%y')

# Add one working day to the date
def add_working_days(date, days):
    while days > 0:
        date += timedelta(days=1)
        if date.weekday() < 5:  # Monday to Friday are considered working days
            days -= 1
    return date

new_date_value = add_working_days(date_value, 1)
new_formatted_date = new_date_value.strftime('%d-%b-%y')
print(f"New Formatted Date (after adding one working day): {new_formatted_date}")

# Define the Access database connection string
access_db_path = r'Z:\CRHVBaza\RMD Reports\MM and TBs rates\M. M\DStorage.mdb'
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=' + access_db_path + ';'
)
# Connect to the Access database
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Check if the record exists
cursor.execute('SELECT COUNT(*) FROM AccStat WHERE AccStatDt = ?', new_formatted_date)
record_exists = cursor.fetchone()[0]

if record_exists:
    # Update the existing record
    cursor.execute('''
        UPDATE AccStat
        SET RSD = ?
        WHERE AccStatDt = ?
    ''', float(numbers[0].replace(',', '')), new_formatted_date)
else:
    # Insert a new record
    cursor.execute('''
        INSERT INTO AccStat (AccStatDt, RSD)
        VALUES (?, ?)
    ''', new_formatted_date, float(numbers[0].replace(',', '')))
# Commit the transaction
conn.commit()

# Close the connection
cursor.close()
conn.close()

print("Data extracted and written to the Access database")

# Define the output file path
output_file_path = r'C:\Users\alazarevic\Desktop\JPEG_output.txt'

# Write the extracted numbers to a text file
with open(output_file_path, 'w', encoding="utf-8") as text_file:
    text_file.write('Izvod za datum: ' + StDt[0] + '\n')
    text_file.write('Ukupno u NBS (RTGS): ' + numbers[0] + '\n')
    text_file.write('Osnovni racun (RTGS): ' + numbers[1] + '\n')
    text_file.write('RTGS-IPS (RTGS): ' + numbers[2] + '\n')

print(f"Numbers extracted and written to {output_file_path}")
