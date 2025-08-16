from pdf2image import convert_from_path
import pytesseract
from . import utlities  # Ensure this module exists and contains the required functions
from .parser_prescription import PrescriptionParser
from .parser_patient import PatientDetailsParser


# Set Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# This path for Poppler is correct, assuming you have extracted it there.
POPPLER_PATH = r"C:\poppler-24.02.0\Library\bin"

def extract(file_path, file_format):
    # Step 1 : Extract text from pdf file
    # Convert PDF to images
    pages = convert_from_path(file_path, poppler_path=POPPLER_PATH)

    document_text = ''
    if len(pages)>0:
        page = pages[0]
        # Preprocess the image
        processed_image = utlities.preprocess_image(page)

        # Extract text from the image
        text = pytesseract.image_to_string(processed_image, lang='eng')

        # --- ADD THESE LINES FOR DEBUGGING ---
        print("----------- OCR Text Output -----------")
        print(text)
        print("-------------------------------------")

        # Append the text to document_text
        document_text += '\n' + text



    # Step 2: Extract fields from text
    if file_format == 'prescription':
        extract_data = PrescriptionParser(document_text).parse() # Extract data from prescription
    elif file_format == 'patient_details':
        extract_data = PatientDetailsParser(document_text).parse()# Extract data from patient details
# ...
    else:
        raise Exception(f"Invalid Document Format: {file_format}")

# Add the full extracted text to the final dictionary
    extract_data['raw_text'] = document_text

    return extract_data

if __name__ == '__main__':
    data = extract(r'../resources/prescription/pre_1.pdf', 'prescription')
    print(data)
