#!/usr/bin/env python3
"""
testclient.py
tesing smart-on-fhir/client-py
"""
from fhirclient import client
from fhirclient import server
import uuid
import json


def getsmart():
    """
    set setting, and return smart server
    """
    settings = {
        'app_id': 'my_web_app',
        'api_base': 'http://fhirtest.b12x.org/baseDstu3'
    }
    smart = client.FHIRClient(settings=settings)
    return smart


def dosmart(smart):
    """
    do the smart thing
    """
    print(smart.ready)
    print(smart.prepare())
    print(smart.ready)
    print(smart.prepare())


def getpatient(smart):
    """
    get patient with Id 2342
    """
    import fhirclient.models.patient as p
    patient = p.Patient.read('2342', smart.server)
    print(patient.birthDate.isostring)
    # '1986-12-31'
    print(smart.human_name(patient.name[0]))
    # 'John Storm'
    print(json.dumps(patient.as_json(), indent=4))


def dosearch(smart):
    """
    searching for resources matching a particular set of criteria
    """
    import fhirclient.models.observation as o
    search = o.Observation.where(struct={'subject': '2342', 'status': 'final'})
    observations = search.perform_resources(smart.server)
    for observation in observations:
        # print(json.dumps(observation.as_json(), indent=4, sort_keys=True))
        print(observation.id)

    # to get the raw Bundle instead of resources only you can use:
    bundle = search.perform(smart.server)
    print(json.dumps(bundle.as_json(), indent=4))


def getpatientserv():
    '''
    uses FHIRServer class directly
    '''
    # You can work with the `FHIRServer` class directly, without using
    # `FHIRClient`, but this is not recommended:
    smart = server.FHIRServer(None, 'http://fhirtest.b12x.org/baseDstu3')
    import fhirclient.models.patient as p
    patient = p.Patient.read('2342', smart)
    print(patient.name[0].given)
    # ['John']


def mkpatient():
    """
    make a Patient resource using the data model
    """
    import fhirclient.models.patient as p
    import fhirclient.models.humanname as hn
    patient = p.Patient()
    # patient.id = 'patient-1'
    # print(patient.id)
    # prints `patient-1`
    name = hn.HumanName()
    name.given = ['Peter']
    name.family = 'Parker'
    patient.name = [name]
    # print(json.dumps(patient.as_json(), indent=4))
    patient.uuid = 'urn:uuid:'+str(uuid.uuid4())
    print(patient.uuid)
    return(patient)


def mksequence():
    """
    make a Sequence resource using the data model
    """
    import fhirclient.models.sequence as s
    sequence = s.Sequence({
        # 'id': 'seq-1',
        'coordinateSystem': 0
    })
    # adding uuid attribute to the sequence object
    # for later use in building bundles and referencing
    # resources with fullUrl
    sequence.uuid = 'urn:uuid:'+str(uuid.uuid4())

    import fhirclient.models.coding as c
    coding = c.Coding()
    coding.system = 'http://www.ebi.ac.uk/ipd/imgt/hla/'
    coding.version = '3.23'
    coding.display = 'HLA-A*01:01:01:01'
    coding.code = 'HLA00001'

    import fhirclient.models.codeableconcept as cc
    codecon = cc.CodeableConcept()
    codecon.coding = [coding]
    codecon.text = 'HLA-A*01:01:01:01'

    refseq = s.SequenceReferenceSeq()
    refseq.referenceSeqId = codecon
    refseq.windowStart = 503
    refseq.windowEnd = 773

    sequence.type = 'dna'
    sequence.referenceSeq = refseq
    sequence.observedSeq = (
        'GCTCCCACTCCATGAGGTATTTCTTCACATCCGTGTCCCGGCCCGGCCGCGGGGAGCCCC'
        'GCTTCATCGCCGTGGGCTACGTGGACGACACGCAGTTCGTGCGGTTCGACAGCGACGCCG'
        'CGAGCCAGAAGATGGAGCCGCGGGCGCCGTGGATAGAGCAGGAGGGGCCGGAGTATTGGG'
        'ACCAGGAGACACGGAATATGAAGGCCCACTCACAGACTGACCGAGCGAACCTGGGGACCC'
        'TGCGCGGCTACTACAACCAGAGCGAGGACG'
    )

    import fhirclient.models.narrative as n
    narrative = n.Narrative()
    narrative.div = (
        '<div xmlns="http://www.w3.org/1999/xhtml">'
        '<pre>HLA-A*01:01:01:01, exon 3</pre>'
        '</div>'
    )
    narrative.status = 'generated'
    sequence.text = narrative

    return sequence


def mkbundle(type, resources):
    """
    takes a list of resources and a bundle type and returns a bundle
    """
    import fhirclient.models.bundle as b
    bundle = b.Bundle({'type': type})
    bundle.entry = []
    for resource in resources:
        print(resource.uuid)
        entry = b.BundleEntry()
        entry.fullUrl = resource.uuid
        entry.resource = resource
        # print(json.dumps(resource.as_json(), indent=4))
        # print(resource.resource_type)
        # print(json.dumps(resource.referenceSeq.as_json(), indent=4))
        # print(dir(resource))
        if type == "transaction":
            request = b.BundleEntryRequest({
                'method': 'POST',
                'url': resource.resource_type
            })
            # print(request.as_json())
            entry.request = request
        bundle.entry.append(entry)
    # print(dir(entry))
    print(json.dumps(bundle.as_json(), indent=4))


def main():
    """
    some tests
    """
    resources = []
    # smart = getsmart()
    # dosmart(smart)
    # dosearch(smart)
    # getpatient(smart)
    # getpatientserv()
    resources.append(mkpatient())
    resources.append(mksequence())
    mkbundle('transaction', resources)


if __name__ == '__main__':
    main()
