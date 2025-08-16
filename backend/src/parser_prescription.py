import re
from .parser_generic import MedicalDocParser

class PrescriptionParser(MedicalDocParser):
    def __init__(self, text):
        super().__init__(text)

    def parse(self):
        return {
            'Patient_Name': self.get_field('Patient_Name'),
            'Patient_Address': self.get_field('Patient_Address'),
            'Medicines': self.get_field('Medicines'),
            'Directions': self.get_field('Directions'),
            'Refill': self.get_field('Refill'),
        }

    def get_field(self, field_name):
        pattern_dict = {
            'Patient_Name': {'pattern': r'Name:(.*?)Date', 'flags': re.DOTALL},
            'Patient_Address': {'pattern': r'Address:(.*)', 'flags': 0},
            'Medicines': {'pattern': r'Address:.*\n(.*?)Directions:', 'flags': re.DOTALL},
            'Directions': {'pattern': r'Directions:(.*?)Refill:', 'flags': re.DOTALL},
            'Refill': {'pattern': r'Refill:\s*(\d+)\s*times', 'flags': 0},
        }

        pattern_object = pattern_dict.get(field_name)
        if pattern_object:
            matches = re.findall(pattern_object['pattern'], self.text, flags=pattern_object['flags'])
            if matches:
                # For medicines, we might get extra unwanted characters. Clean it up.
                if field_name == 'Medicines':
                    return matches[0].replace('K', '').strip()
                return matches[0].strip()

if __name__ == '__main__':
    document_text = '''Dr John Smith, M.D
2 Non-Important Street,
New York, Phone (000)-111-2222

Name: Marta Sharapova Date: 5/11/2022

Address: 9 tennis court, new Russia, DC

K

Prednisone 20 mg
Lialda 2.4 gram

Directions:

Prednisone, Taper 5 mig every 3 days,
Finish in 2.5 weeks a
Lialda - take 2 pill everyday for 1 month

Refill: 2 times'''

    pp = PrescriptionParser(document_text)
    print(pp.parse())