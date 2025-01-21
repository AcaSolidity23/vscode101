import re
import pytesseract
import pyodbc
import os
import cv2
import json
from datetime import datetime, timedelta
from json_writer import JSONWriter

class ImageProcessor:
    def __init__(self, png_file_path, access_db_path, json_output_file):
        self.png_file_path = png_file_path
        self.access_db_path = access_db_path
        self.json_output_file = json_output_file

        # Set TESSDATA_PREFIX and tesseract_cmd
        tessdata_prefix = r"C:\Users\alazarevic\AppData\Local\Programs\Tesseract-OCR\tessdata"
        tesseract_cmd = r'C:\Users\alazarevic\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

        # Add TESSDATA_PREFIX to the system PATH
        os.environ['TESSDATA_PREFIX'] = tessdata_prefix
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

        # Set the Windows encoding to UTF-8
        os.environ['PYTHONIOENCODING'] = 'utf-8'

        # Load Serbian state holidays
        with open('Z:\\CRHVBaza\\RMD Reports\\MM and TBs rates\\M. M\\serbian_state_holidays.json', 'r') as file:
            self.serbian_holidays = json.load(file)

    def process_image(self):
        # Open the image file
        image = cv2.imread(self.png_file_path)
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

        # Extract row containing "Trenutno stanje"
        trenutnostanje_line  = None
        lines = text.split('\n')
        for line in lines:
            if "Trenutno stanje" in line:
                trenutnostanje_line = line
                break

        # Extract numbers and dates from the text
        numbers, StDt, next_working_day = self.__extract_numbers_and_dates(trenutnostanje_line, text)
        print(f"Next working day: {next_working_day} numbers: {numbers} stDt: {StDt}")
        # Connect to the Access database and update/insert data
        self.__update_database(next_working_day, numbers)

        # Write the extracted numbers to a JSON file
        JsonData = JSONWriter(self.json_output_file)
        JsonData.write_to_json(StDt, numbers, "ImageProcessor")

    def __extract_numbers_and_dates(self, trenutnostanje_line, text):
        # Define a regex to find numbers
        number_regex = re.compile(r'(?:\d{1,3}(?:,\d{3})+)(?:\.\d{2})')
        date_regex = re.compile(r'(\d{4}.\d{2}.\d{2})')

        # Find all numbers in the extracted text
        numbers = number_regex.findall(trenutnostanje_line)
        StDt = date_regex.findall(text)

        # Convert StDt[0] to a date format
        StDt[0] = StDt[0].replace('–', '-')
        date_value = datetime.strptime(StDt[0], '%Y-%m-%d').date()
        next_working_day = self.__find_next_working_day(date_value) # Find the next working day
        formatted_date = date_value.strftime('%d-%b-%Y')

        return numbers, formatted_date, next_working_day

    def __find_next_working_day(self, date):
        date += timedelta(days=1)
        while date.weekday() >= 5 or date.strftime('%d-%b-%Y') in self.serbian_holidays: # Check if the date is a weekend or a holiday
            date += timedelta(days=1)
        return date

    def __update_database(self, next_working_day, numbers):
        # Define the Access database connection string
        conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ=' + self.access_db_path + ';'
        )

        # Connect to the Access database
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Check if the record exists
        cursor.execute('SELECT COUNT(*) FROM AccStat WHERE AccStatDt = ?', next_working_day)
        record_exists = cursor.fetchone()[0]

        if record_exists:
            # Update the existing record
            cursor.execute('''
                UPDATE AccStat
                SET RSD = ?
                WHERE AccStatDt = ?
            ''', float(numbers[0].replace(',', '')), next_working_day)
        else:
            # Insert a new record
            cursor.execute('''
                INSERT INTO AccStat (AccStatDt, RSD)
                VALUES (?, ?)
            ''', next_working_day, float(numbers[0].replace(',', '')))

        # Commit the transaction
        conn.commit()

        # Close the connection
        cursor.close()
        conn.close()

        print("Data extracted and written to the Access database: {next_working_day}.")
