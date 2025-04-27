# Screenshot to PDF Converter

A Python utility that automatically captures screenshots of URLs from an Excel file and converts them to PDF documents.

## Features

- Takes full-page screenshots of websites listed in an Excel file
- Automatically converts screenshots to PDF format
- Organizes files in folders by brand name
- Implements human-like browsing behavior to avoid bot detection
- Handles CAPTCHA detection with retry mechanism
- Generates a detailed report of the process

## Requirements

- Python 3.7+
- Playwright
- pandas
- img2pdf
- Pillow

## Installation

1. Clone this repository:
```bash
git clone https://github.com/savhascelik/screenshot_to_pdf.git
cd screenshot_to_pdf
```

2. Install the required packages:
```bash
pip install playwright pandas img2pdf pillow
```

3. Install Playwright browsers:
```bash
playwright install
```

## Usage

1. Prepare an Excel file named `input.xlsx` with the following columns:
   - Column C (3rd column): URLs to capture
   - Column E (5th column): Brand names for organizing folders

2. Run the script:
```bash
python screenshot_to_pdf.py
```

3. The script will:
   - Create a directory called `screenshots_pdfs`
   - Process each URL in the Excel file
   - Take screenshots and convert them to PDFs
   - Save them in subfolders named after each brand
   - Generate a report file with statistics

## How It Works

The script performs these steps for each URL:
1. Opens a browser with stealth settings to mimic human behavior
2. Navigates to the URL with randomized scroll movements
3. Takes a full-page screenshot
4. Converts the screenshot to PDF
5. Deletes the original screenshot file
6. Organizes files in brand-specific folders

## Troubleshooting

If you encounter issues:
- Check the generated report file in the output directory
- Ensure your Excel file is formatted correctly
- Verify you have a stable internet connection
- Some websites may block automated access despite stealth measures

## License

This project is open-source and available for personal and commercial use. 