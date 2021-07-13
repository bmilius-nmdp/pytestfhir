#!/usr/bin/env python3
"""
Make a transaction bundle resource with random Patient and Observation
using LOINC codes from spreadsheet,
and write it to a file
"""

import json
import math
import uuid
import random
# import pprint
import pandas as pd
from datetime import datetime
from dateutil import tz
from dateutil import parser as dateparser
from faker import Faker
from fhirclient.r3 import client
import fhirclient.r3.models.patient as p
import fhirclient.r3.models.humanname as hn
import fhirclient.r3.models.observation as o
import fhirclient.r3.models.quantity as q
import fhirclient.r3.models.coding as c

import fhirclient.r3.models.codeableconcept as cc
import fhirclient.r3.models.fhirdate as dt
import fhirclient.r3.models.bundle as b
import fhirclient.r3.models.fhirreference as fr
import fhirclient.r3.models.identifier as iden


def mkname(**keywords):
    '''
    takes parts of a name, and builds a nam to be used in a Patient resource
    '''
    name = hn.HumanName()
    for key in keywords:
        setattr(name, key, keywords[key])
    print(json.dumps(name.as_json(), indent=4))
    return name


def mkpatient():
    '''
    returns a random patient with a name, gender, birthdate, identifer,
    and uuid for bundle use
    '''

    # initialize fake
    fake = Faker()

    # set age range for creating birthdate
    # oldest = "-80y"
    # youngest = "-5"

    patient = p.Patient()

    # gender
    gender = random.choice(['male', 'female'])
    patient.gender = gender

    # name
    name = hn.HumanName()
    if gender == 'male':
        given_name = fake.first_name_male()
    elif gender == 'female':
        given_name = fake.first_name_female()
    family_name = fake.last_name()
    name.family = family_name
    # use 'Dash' as middle name so we can find it via search
    name.given = [given_name, "Dash"]
    name.text = given_name + " Dash " + family_name
    name.use = 'official'
    patient.name = [name]

    # birthdate
    birthdate = dt.FHIRDate()
    birthdate.date = fake.date_between(start_date='-80y', end_date='-5y')
    patient.birthDate = birthdate

    # identifier
    identifier = iden.Identifier()
    identifier.system = "http://example.org"
    identifier.value = uuid.uuid4().hex
    typecoding = c.Coding()
    typecoding.system = 'http://hl7.org/fhir/v2/0203'
    typecoding.code = 'MR'
    typecoding.display = 'Medical record number'
    identifiertype = cc.CodeableConcept()
    identifiertype.coding = [typecoding]
    identifier.type = identifiertype
    patient.identifier = [identifier]

    # add a uuid to be used in bundle fullUrls
    patient.uuid = uuid.uuid4().urn

    # print(json.dumps(patient.as_json(), indent=2))

    return patient


def writepatient(patient):
    '''
    takes a patient resource and writes it in json to a file
    '''
    fname = 'patient-r3.json'
    with open(fname, 'w') as outfile:
        json.dump(patient.as_json(), outfile, indent=4)
    print("patient json written to file {fn}".format(fn=fname))


def postpatient(patient):
    '''
    '''
    settings = {
        'app_id': 'my_web_app',
        'api_base': 'http://fhirtest.b12x.org/r3'
    }
    smart = client.FHIRClient(settings=settings)
    response = patient.create(smart.server)
    print(json.dumps(response.json(), indent=4))
    print(response.headers['location'])


def mkbundle(patient):
    '''
    returns a transaction bundle containing a single Patient resource
    '''
    bundle = b.Bundle()
    bundle.type = 'transaction'
    bundleEntry = b.BundleEntry()
    bundleEntry.fullUrl = patient.uuid
    bundleEntry.resource = patient
    bundleEntryRequest = b.BundleEntryRequest()
    bundleEntryRequest.method = "POST"
    bundleEntryRequest.url = "Patient"
    bundleEntryRequest.ifNoneExist = "identifier="+patient.identifier[0].system+"|"+patient.identifier[0].value
    bundleEntry.request = bundleEntryRequest
    bundle.entry = [bundleEntry]
    # print(json.dumps(bundle.as_json(), indent=2))
    return bundle


def mksubjectref(patient):
    '''
    Takes a patient resource containing a uuid, and returns a
    subject reference that can be reused in bundle resources
    '''
    subject = fr.FHIRReference()
    subject.reference = patient.uuid
    # print(json.dumps(subject.as_json(), indent=2))
    return subject


def getpatient(bundle):
    bundlejson = json.dumps(bundle.as_json())
    bundledict = json.loads(bundlejson)
    patient = p.Patient()
    for i in bundledict['entry']:
        if i['resource']['resourceType'] == "Patient":
            patient = p.Patient(i['resource'])
            patient.uuid = i['fullUrl']
    # print(json.dumps(newpatient.as_json(), indent=2))
    # print(newpatient.uuid)
    return(patient)


def mkobservations(bundle):
    '''
    '''
    patient = getpatient(bundle)
    csvfile = "loinc_2.csv"
    df = pd.read_csv(csvfile)
    for index, row in df.iterrows():
        if row['Value[x]'] == 'Quantity':
            # for each LOINC code, make between 1 and 10 observations
            for i in range(random.randint(1, 15)):
                fake = Faker()

                # create instance of observation
                observation = o.Observation()

                # status (required)
                observation.status = "final"

                # code (required)
                code = cc.CodeableConcept()
                codecode = c.Coding()
                codecode.system = 'http://loinc.org'
                codecode.code = row['LOINC Code']
                codecode.display = row['LOINC Concept Name']
                code.text = row['LOINC Concept Name']
                code.coding = [codecode]
                observation.code = code

                # category
                category = cc.CodeableConcept()
                categorycoding = c.Coding()
                categorycoding.system = "http://loinc.org"
                categorycoding.code = "laboratory"
                categorycoding.display = "Laboratory"
                category.coding = [categorycoding]
                observation.category = [category]

                # subject
                observation.subject = mksubjectref(patient)

                # date, sometime between birthdate and now
                effectiveDateTime = dt.FHIRDate()
                effectiveDateTime.date = fake.date_time_between(
                    start_date=patient.birthDate.date, end_date='now', tzinfo=tz.UTC)
                observation.effectiveDateTime = effectiveDateTime

                # value
                low = row['q.low']
                high = row['q.high']
                value = math.ceil(random.uniform(low, high) * 10) / 10
                valuequantity = q.Quantity()
                valuequantity.value = value
                valuequantity.unit = row['q.unit']
                valuequantity.system = row['q.system']
                valuequantity.code = row['q.code']
                observation.valueQuantity = valuequantity

                # put observation into bundle entry
                bundleEntry = b.BundleEntry()
                bundleEntryRequest = b.BundleEntryRequest()
                bundleEntryRequest.method = "POST"
                bundleEntryRequest.url = "Observation"

                bundleEntry.request = bundleEntryRequest
                bundleEntry.resource = observation
                bundleEntry.fullUrl = uuid.uuid4().urn
                bundle.entry.append(bundleEntry)

    return bundle


def main():
    '''
    doing the main thing
    '''
    # make a random patient
    patient = mkpatient()
    numofbundles = 3
    for i in range(1, numofbundles+1):
        # make a transaction bundle containing the patient
        bundle = mkbundle(patient)

        # create a list of randcom observation using the loinc spreadsheet
        # add them to the bundle
        bundle = mkobservations(bundle)
        filename = "bundle_"+str(i)+"of"+str(numofbundles)+".json"
        with open(filename, 'w') as outfile:
            json.dump(bundle.as_json(), outfile, indent=2)

    # writepatient(patient)
    # postpatient(patient)


if __name__ == '__main__':
    main()
