from backend.src.parser_prescription import PrescriptionParser
import pytest

@pytest.fixture()
def doc_1_maria():
    document = '''Dr John Smith, M.D
    2 Non-Important Street,
    New York, Phone (000)-111-2222

    Name: Marta Sharapova Date: 5/11/2022

    Address: 9 tennis court, new Russia, DC

    Prednisone 20 mg
    Lialda 2.4 gram

    Directions:

    Prednisone, Taper 5 mg every 3 days,
    Finish in 2.5 weeks a
    Lialda - take 2 pills everyday for 1 month

    Refill: 2 times'''
    return PrescriptionParser(document)

@pytest.fixture()
def doc_2_virat():
    document = '''Dr John Smith, M.D
    2 Non-Important street,
    New York, Phone (900)-323-2222

    Name: Virat Kohli Date: 2/05/2022

    Address: 2 cricket blvd, New Delhi

    Omeprazole 40 mg

    Directions: Use two tablets daily for three months

    Refill: 3 times'''
    return PrescriptionParser(document)

@pytest.fixture()
def doc_3_empty():
    return PrescriptionParser('')

def test_get_name(doc_1_maria, doc_2_virat,doc_3_empty):
    assert doc_1_maria.get_field('Patient_Name') == 'Marta Sharapova'
    assert doc_2_virat.get_field('Patient_Name') == 'Virat Kohli'
    assert doc_3_empty.get_field('Patient_Name') == None

def test_get_address(doc_1_maria, doc_2_virat,doc_3_empty):
    assert doc_1_maria.get_field('Patient_Address') == '9 tennis court, new Russia, DC'
    assert doc_2_virat.get_field('Patient_Address') == '2 cricket blvd, New Delhi'
    assert doc_3_empty.get_field('Patient_Address') == None
def test_get_medicine(doc_1_maria,doc_2_virat,doc_3_empty):
    assert doc_1_maria.get_field('Medicines') == 'Prednisone 20 mg\n    Lialda 2.4 gram'
    assert doc_2_virat.get_field('Medicines') == 'Omeprazole 40 mg'
    assert doc_3_empty.get_field('Medicines') == None

def test_get_direction(doc_1_maria,doc_2_virat,doc_3_empty):
    assert doc_1_maria.get_field('Directions') == 'Prednisone, Taper 5 mg every 3 days,\n    Finish in 2.5 weeks a\n    Lialda - take 2 pills everyday for 1 month'
    assert doc_2_virat.get_field('Directions') == 'Use two tablets daily for three months'
    assert doc_3_empty.get_field('Directions') == None

def test_get_refill(doc_1_maria,doc_2_virat,doc_3_empty):
    assert doc_1_maria.get_field('Refill') == '2'
    assert doc_2_virat.get_field('Refill') == '3'
    assert doc_3_empty.get_field('Refill') == None
def test_parse(doc_1_maria,doc_2_virat,doc_3_empty):

    record_virat = doc_2_virat.parse()
    assert record_virat == {
        'Patient_Name': 'Virat Kohli',
        'Patient_Address': '2 cricket blvd, New Delhi',
        'Medicines': 'Omeprazole 40 mg',
        'Directions': 'Use two tablets daily for three months',
        'Refill': '3'
    }

    record_empty = doc_3_empty.parse()
    assert record_empty == {
        'Patient_Name': None,
        'Patient_Address': None,
        'Medicines': None,
        'Directions': None,
        'Refill': None
    }