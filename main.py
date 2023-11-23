from bs4 import BeautifulSoup

import json
import random
import string

def generate(manifest_file='manifest.json'):
    with open(manifest_file) as f:
        manifest = json.load(f)

    with open(manifest['basePath'], 'r') as f:
        xml_file = f.read()

    xml_structure = BeautifulSoup(xml_file, "xml")
    
    for number in range(manifest['quantity']):
        for replaceable in manifest['changes']['replace']:
            if replaceable['multiple']: 
                value =  get_value_to_replace(replaceable) if replaceable['differentValue'] is False else None
                for field in xml_structure.find_all(replaceable['field']):
                    field.string = value or get_value_to_replace(replaceable)
            else:
                field_to_change = xml_structure.find(replaceable['field'])
                field_to_change.string = get_value_to_replace(replaceable)
        with open(f"{manifest['outputBaseName']}{number}.xml", 'w') as file:
            file.write(str(xml_structure))

def random_digits_and_letters(length:int):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def random_in_values(values:list[str]):
    return random.choice(values)

def get_value_to_replace(replaceable):
    field_rule = replaceable['rule']
    if field_rule == 'random_digit_letter':
        field_length = replaceable['length']
        return random_digits_and_letters(field_length)
    if field_rule == 'random_in_values':
        values = replaceable['values']
        return random_in_values(values)
    
generate()