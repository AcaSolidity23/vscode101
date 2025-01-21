import PyPDF2
import re
from json_writer import JSONWriter
from datetime import datetime, timedelta
import pyodbc
import json

class PDFReader:
    def __init__(self, full_file_path, access_db_path, json_output_file):
        self.full_file_path = full_file_path
        self.json_output_file = json_output_file
        self.access_db_path = access_db_path

    def read_pdf(self):
        # Define regex patterns
        obRezRegex = re.compile(r'([0-9]{1,3}(?:\,[0-9]{3})+(?:\.[0-9]+))')
        obRezDtRegex = re.compile(r'(\d{2}\.\d{2}\.\d{4})')

        # Load Serbian state holidays
        with open('Z:\\CRHVBaza\\RMD Reports\\MM and TBs rates\\M. M\\serbian_state_holidays.json', 'r') as file:
            self.serbian_holidays = json.load(file)

        # Open the PDF file
        pdf_file_obj = open(self.full_file_path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
        page_obj = pdf_reader.pages[0]

        # Extract text from the PDF
        text = page_obj.extract_text()

        # Find matches using regex
        ob_rez = obRezRegex.findall(text)
        ob_rez = ob_rez[-3:]
        ob_rez_dt = obRezDtRegex.findall(text)

        # Convert ob_rez_dt to a date format and format it to '%d-%m-%Y'
        date_value = datetime.strptime(ob_rez_dt[1], '%d.%m.%Y').date()
        next_working_day = self.__find_next_working_day(date_value) # Find the next working day
        next_working_day = next_working_day.strftime('%d-%b-%Y')
        formatted_date = date_value.strftime('%d-%b-%Y')

        self.__write_to_json(formatted_date, ob_rez)
        self.__update_database(next_working_day, ob_rez[2])

    def __write_to_json(self, RRDate, numbers):
        # Extract numbers and dates from the text

        # Write the extracted numbers to a JSON file
        JsonData = JSONWriter(self.json_output_file)
        JsonData.write_to_json(RRDate, numbers, "PDFReader")

    def __update_database(self, RRDate, obRez_saldo):
        # Define the Access database connection string
        conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ=' + self.access_db_path + ';'
        )

        # Connect to the Access database
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Check if the record exists
        cursor.execute('SELECT COUNT(*) FROM AccStat WHERE AccStatDt = ?', RRDate)
        record_exists = cursor.fetchone()[0]

        if record_exists:
            # Update the existing record
            cursor.execute('''
                UPDATE AccStat
                SET RR_EUR= ?
                WHERE AccStatDt = ?
            ''', float(obRez_saldo.replace(',', '')), RRDate)
            print(f"Access database - Record updated: {RRDate} / {obRez_saldo}")
        else:
            # Insert a new record
            cursor.execute('''
                INSERT INTO AccStat (AccStatDt, RR_EUR)
                VALUES (?, ?)
            ''', RRDate, float(obRez_saldo.replace(',', '')))
            print(f"Access database - Record inserted: {RRDate} / {obRez_saldo}")
        # Commit the transaction
        conn.commit()

        # Close the connection
        cursor.close()
        conn.close()

    def __find_next_working_day(self, date):
        date += timedelta(days=1)
        while date.weekday() >= 5 or date.strftime('%d-%b-%Y') in self.serbian_holidays: # Check if the date is a weekend or a holiday
            date += timedelta(days=1)
        return date
