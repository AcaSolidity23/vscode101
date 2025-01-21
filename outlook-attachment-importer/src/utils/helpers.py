def check_subject(subject, keywords):
    """Check if the subject contains any of the specified keywords."""
    return any(keyword.lower() in subject.lower() for keyword in keywords)

def save_attachment(attachment, save_path):
    """Save the given attachment to the specified path."""
    with open(save_path, 'wb') as f:
        f.write(attachment.content)  # Assuming attachment.content contains the binary data of the file

def create_save_path(attachment_name, directory):
    """Create a full save path for the attachment."""
    import os
    return os.path.join(directory, attachment_name)