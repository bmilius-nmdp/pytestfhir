#!/usr/bin/env python3
"""
make a patient resource and write it to a file
"""

import json
import fhirclient.models.patient as p
import fhirclient.models.humanname as hn
from fhirclient import client


def mkname(**keywords):
    '''
    takes parts of a name, and builds a nam to be used in a Patient resource
    '''
    name =  hn.HumanName()
    for key in keywords:
        setattr(name, key, keywords[key])
    print(json.dumps(name.as_json(), indent=4))
    return name


def mkpatient():
    '''
    makes a patient with a name, and returns it
    '''
    patient = p.Patient()
    name1 = mkname(given=['Jonathon', 'Lowell'],
                   family='Storm',
                   text='Jonathon Storm',
                   use='official')
    name2 = mkname(given=['Johnny'],
                   family='Storm',
                   text='Johnny Storm',
                   use='nickname')
    name3 = mkname(text='Human Torch',
                   use='nickname')
    patient.name =[name1, name2, name3]
    # print(json.dumps(patient.as_json(), indent=4))
    return patient


def writepatient(patient):
    '''
    takes a patient resource and writes it in json to a file
    '''
    fname = 'patient-1.json'
    with open(fname, 'w') as outfile:
        json.dump(patient.as_json(), outfile, indent=4)
    print("patient json written to file {fn}".format(fn=fname))


def postpatient(patient):
    '''
    '''
    settings = {
        'app_id': 'my_web_app',
        'api_base': 'http://fhirtest.b12x.org/baseDstu3'
    }
    smart = client.FHIRClient(settings=settings)
    response = patient.create(smart.server)
    print(json.dumps(response.json(), indent=4))
    print(response.headers['location'])


def main():
    '''
    doing the main thing
    '''
    patient = mkpatient()
    # print(json.dumps(patient.as_json(), indent=4))
    writepatient(patient)
    postpatient(patient)


if __name__ == '__main__':
    main()
