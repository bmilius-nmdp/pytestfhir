"""
Read a csv file containing example data for FHIR Observations
"""

import json
import pandas as pd
# import fhirclient.r3.models.patient as p
# import fhirclient.r3.models.humanname as hn
# from fhirclient.r3 import client

file = "loinc.csv"

df = pd.read_csv(file)
print(df)
