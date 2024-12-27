import PyPDF2
import re

file_nm = r'504000-100007748-20-SEP-2024.pdf'
file_path = r'C:\Users\alazarevic\Desktop\\'

obRezRegex = re.compile(r'([0-9]{1,3}(?:\,[0-9]{3})+(?:\.[0-9]+))')
obRezDtRegex = re.compile(r'(\d{2}\.\d{2}\.\d{4})')

pdfFIleObj = open(file_path + file_nm, 'rb')
pdfReader = PyPDF2.PdfReader(pdfFIleObj)
pageObj = pdfReader.pages[0]

obRez = obRezRegex.findall(pageObj.extract_text())
obRez = obRez[1:]

obRezDt = obRezDtRegex.search(pageObj.extract_text())

with open(file_path + 'PDF_output.txt', 'w', encoding="utf-8") as text_file:
    text_file.write('Datum:' + obRezDt.group() +'\n')
    text_file.write('Prethodno stanje:' + obRez[0]+'\n')
    text_file.write('Dnevne promene:' + obRez[1]+'\n')
    text_file.write('Saldo:' + obRez[2]+'\n')
