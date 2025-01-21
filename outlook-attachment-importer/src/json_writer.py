import os
import json

class JSONWriter:
    def __init__(self, json_output_file_path):
        self.json_output_file_path = json_output_file_path

    def write_to_json(self, date, numbers, source):
        # Define the output file path
        output_file_path = self.json_output_file_path

        # Read the existing JSON file if it exists
        if os.path.exists(output_file_path):
            with open(output_file_path, 'r', encoding="utf-8") as json_file:
                existing_data = json.load(json_file)
        else:
            existing_data = {}

        # Update the dictionary based on the source class
        if source == "ImageProcessor":
            if date in existing_data:
                existing_data[date].update({
                    "Ukupno u NBS (RTGS)": numbers[0],
                    "Osnovni racun (RTGS)": numbers[1],
                    "RTGS-IPS (RTGS)": numbers[2]
                })
            else:
                existing_data[date] = {
                    "Ukupno u NBS (RTGS)": numbers[0],
                    "Osnovni racun (RTGS)": numbers[1],
                    "RTGS-IPS (RTGS)": numbers[2]
                }
        elif source == "PDFReader":
            if date in existing_data:
                existing_data[date].update({
                    "Prethodno stanje(EUR)": numbers[0],
                    "Dnevne promene(EUR)": numbers[1],
                    "Saldo(EUR)": numbers[2]
                })
            else:
                existing_data[date] = {
                    "Prethodno stanje(EUR)": numbers[0],
                    "Dnevne promene(EUR)": numbers[1],
                    "Saldo(EUR)": numbers[2]
                }

        # Write the updated dictionary to the JSON file
        with open(output_file_path, 'w', encoding="utf-8") as json_file:
            json.dump(existing_data, json_file, ensure_ascii=False, indent=4)

        print(f"Numbers extracted and written to {output_file_path}")
