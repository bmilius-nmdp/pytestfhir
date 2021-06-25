#!/usr/bin/env python3
"""
make a patient resource and write it to a file
"""


import json
import uuid
import fhirclient.models.patient as patient
import fhirclient.models.specimen as specimen
import fhirclient.models.codeableconcept as codeableconcept
import fhirclient.models.coding as coding
import fhirclient.models.fhirreference as fhirreference
from fhirclient import client


def writepatient(mypatient):
    '''
    takes a patient resource and writes it in json to a file
    '''
    fname = 'patient-1.json'
    with open(fname, 'w') as outfile:
        json.dump(mypatient.as_json(), outfile, indent=4)
    print("patient json written to file {fn}".format(fn=fname))


def postpatient(mypatient, smart):
    '''
    '''
    response = mypatient.create(smart.server)
    print(json.dumps(response(), indent=4))


def getsmart():
    '''
    set setting, and return smart server
    '''
    settings = {
        'app_id': 'my_web_app',
        'api_base': 'http://fhirtest.b12x.org/r3'
    }
    smart = client.FHIRClient(settings=settings)
    return smart


def readpatient(fname):
    '''
    '''
    with open(fname, 'r') as patientfile:
        pjson = json.load(patientfile)
    mypatient = patient.Patient(pjson)
    return mypatient


def getpatient(iden, smart):
    '''
    get patient with Id
    '''
    mypatient = patient.Patient.read(iden, smart.server)
    return mypatient


def mkspecimen(mypatient):
    '''
    '''
    myspecimen = specimen.Specimen()
    mypatient.uuid = uuid.uuid4().urn
    reference = fhirreference.FHIRReference()
    if mypatient.id:
        reference.id = 'Patient/' + mypatient.id
    else:
        reference.id = mypatient.uuid
    myspecimen.subject = reference
    myspecimen.collection = mkCollection()
    myspecimen.uuid = uuid.uuid4().urn
    return myspecimen


def mkCollection():
    '''
    '''
    collection = specimen.SpecimenCollection()
    collection.bodySite = mkCollectionBodySite()
    collection.method = mkCollectionMethod()
    return collection

def mkCollectionBodySite():
    '''
    '''
    bodySite = codeableconcept.CodeableConcept()
    bodySiteCoding = mkCoding(system='http://snomed.info/sct',
                              code='261063000',
                              display='Buccal space')
    bodySite.coding = [bodySiteCoding]
    return bodySite


def mkCollectionMethod():
    '''
    '''
    method = codeableconcept.CodeableConcept()
    methodCoding = mkCoding(system='http://hl7.org/fhir/v2/0488',
                            code='SWA',
                            display='Swab')
    method.coding = [methodCoding]
    return method


def mkCoding(**keywords):
    '''
    returns a Coding using keyword/values
    '''
    c = coding.Coding()
    for key in keywords:
        setattr(c, key, keywords[key])
    return c


def main():
    '''
    doing the main thing
    '''
    # mypatient = readpatient('patient-1.json')
    mypatient = getpatient('3002', getsmart())
    myspecimen = mkspecimen(mypatient)
    print(json.dumps(myspecimen.as_json(), indent=4))
    # print(json.dumps(mypatient.as_json(), indent=4))


if __name__ == '__main__':
    main()

