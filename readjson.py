#!/usr/bin/env python3
"""
read a json file containig a Patient resource, print it
"""

import json
import fhirclient.models.patient as p

def main():
    with open('patient.json', 'r') as h:
        pjs = json.load(h)
    patient = p.Patient(pjs)
    print(patient.name[0].given)
    # prints patient's given name array in the first `name` property
    print(json.dumps(patient.as_json(), indent=4))

if __name__ == '__main__':
    main()
