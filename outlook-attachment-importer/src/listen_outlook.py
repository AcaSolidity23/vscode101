import win32com.client
import pythoncom  # Import pythoncom module
import os
import threading
from outlook_importer import OutlookImporter
from import_text_jpg import ImageProcessor
from pdf_reader import PDFReader

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
desktop_path = desktop_path + "\\Outlook_import"
json_output_file_path = r'Z:\CRHVBaza\RMD Reports\MM and TBs rates\M. M\RR_statements.json'
access_db_path = r'Z:\CRHVBaza\RMD Reports\MM and TBs rates\M. M\DStorage.mdb'
#json_output_file_path = r'C:\Users\alazarevic\Desktop\Outlook_import\RR_statements.json'

print(f"Desktop path: {desktop_path}")
class OutlookEvents:
    def OnNewMailEx(self, receivedItemsIDs):
        try:
            outlook = win32com.client.Dispatch("Outlook.Application")
            namespace = outlook.GetNamespace("MAPI")
            inbox = namespace.GetDefaultFolder(6)  # 6 refers to the inbox folder

            for ID in receivedItemsIDs.split(","):
                mail = namespace.GetItemFromID(ID)
                print(f"New email received: {mail.Subject}")
                print(f"MailClass: {mail.Class}")
                print(f"Unread: {mail.UnRead}")
                print(f"ReceivedTime: {mail.ReceivedTime}")
                if mail.Class == 43:  # 43 corresponds to the MailItem class
                    if hasattr(mail, 'UnRead') and mail.UnRead:  # Check if the email is unread
                        subject = mail.Subject
                        if "IZVOD MT 940" in subject:
                            importer = OutlookImporter(desktop_path)
                            importer.import_attachments(mail)
                            mail.UnRead = False  # Mark the message as read

                            # Process the saved attachment using ImageProcessor
                            png_file_path = importer.get_saved_attachments()[0]
                            print(f"PNG file path: {png_file_path}")

                            processor = ImageProcessor(png_file_path, access_db_path, json_output_file_path)
                            processor.process_image()

                        elif "IZVOD NBS" in subject:
                            importer = OutlookImporter(desktop_path)
                            importer.import_attachments(mail)
                            mail.UnRead = False

                            # Process the saved attachment using PDFReader
                            pdf_file_path = importer.get_saved_attachments()[0]
                            print(f"PDF file path: {pdf_file_path}")
                            pdf_reader = PDFReader(pdf_file_path, access_db_path, json_output_file_path)
                            pdf_reader.read_pdf()

        except Exception as e:
            print(f"Error processing email: {e}")

def check_inbox():
    pythoncom.CoInitialize()  # Initialize COM library
    try:
        outlook = win32com.client.DispatchWithEvents("Outlook.Application", OutlookEvents)
        pythoncom.PumpMessages()  # Keep the message pump running
    except Exception as e:
        print(f"Error initializing Outlook event handler: {e}")
    finally:
        pythoncom.CoUninitialize()  # Uninitialize COM library

def main():
    # Create a thread to run the check_inbox function
    inbox_thread = threading.Thread(target=check_inbox)
    inbox_thread.daemon = True  # Set as a daemon thread to exit when the main program exits
    inbox_thread.start()

    # Keep the main thread running
    while True:
        pass

if __name__ == "__main__":
    main()
