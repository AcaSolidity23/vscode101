import os
class OutlookImporter:
    def __init__(self, save_directory):
        self.save_directory = save_directory
        self.saved_attachments = []

    def import_attachments(self, email):
        largest_attachment = None
        largest_size = 0
        temp_files = []

        if email.Attachments:
            for attachment in email.Attachments:
                if (attachment.FileName.endswith(".pdf") and "504000-100007748" in attachment.FileName):
                    self.save_attachment(attachment)
                    break
                elif attachment.FileName.endswith(".png"):
                    # Save the attachment temporarily to check its size
                    temp_file_path = os.path.join(self.save_directory, attachment.FileName)
                    attachment.SaveAsFile(temp_file_path)
                    temp_files.append(temp_file_path)
                    file_size_kb = os.path.getsize(temp_file_path) / 1024  # Convert bytes to KB
                    print(f"{attachment.FileName} File size: {file_size_kb} KB")
                    if file_size_kb > largest_size:
                        largest_size = file_size_kb
                        largest_attachment = temp_file_path
        # Delete all other temporary files except the largest one
        for temp_file in temp_files:
            if temp_file != largest_attachment:
                os.remove(temp_file)
                print(f"Deleted temporary file: {temp_file}")

        if largest_attachment:
            self.saved_attachments.append(largest_attachment)
            print(f"Largest attachment saved to: {largest_attachment}")

    def save_attachment(self, attachment):
        file_path = f"{self.save_directory}/{attachment.FileName}"
        attachment.SaveAsFile(file_path)
        self.saved_attachments.append(file_path)
        print(f"Attachment saved to: {file_path}")

    def get_saved_attachments(self):
        return self.saved_attachments
