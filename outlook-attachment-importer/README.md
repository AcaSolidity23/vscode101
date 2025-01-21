# Outlook Attachment Importer

This project is designed to import attachments from Microsoft Outlook based on specific text in the email subject. It listens for incoming emails and triggers the import of attachments when the criteria are met.

## Project Structure

```
outlook-attachment-importer
├── src
│   ├── listen_outlook.py       # Main event listener for incoming emails
│   ├── outlook_importer.py      # Logic for importing attachments
│   └── utils
│       └── helpers.py          # Utility functions for the project
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd outlook-attachment-importer
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Configure your Outlook settings as needed in the `listen_outlook.py` file.
2. Run the event listener:
   ```
   python src/listen_outlook.py
   ```

3. The program will listen for incoming emails and import attachments based on the specified subject criteria.

## Configuration

Make sure to set up the necessary permissions and configurations in your Outlook account to allow the application to access your emails and attachments.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.