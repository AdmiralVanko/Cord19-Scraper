import pandas as pd
import numpy as np
import csv
from collections import defaultdict
import spacy

filename = "metadata.csv"
parser = spacy.load("en_core_web_lg")
terms = ["registry", "registries", "database", "databases", "platform", "platforms", "repository", "repositories",
        "ipd-ma", "data dashboard", "individual participant data meta-analysis", "multicenter cohort",
         "multi-centre cohort", "patent level", "patient-level", "participant level", "participant-level",
         "individual participant data", "meta-analysis"]

lines_seen = set() # prevents duplicate titles
output_appos = open('output_appos.txt', 'w', encoding="utf-8")
output_pnoun = open('output_pnoun.txt', 'w', encoding="utf-8")

cord_uid_to_text = defaultdict(list)
with open("metadata.csv", encoding="utf-8") as f_in:
    reader = csv.DictReader(f_in)
    for column in reader:
        title = column['title']
        cord_uid = column['cord_uid']
        pdoc = parser(title)
        for token in pdoc:
            if token not in lines_seen:
                lines_seen.add(token)
                if token.dep_ == "appos" and token.orth_ in terms:
                    output_appos.write(str(title) + '\n')
                elif token.pos_ == "PROPN" and token.dep_ == "ROOT":
                    output_pnoun.write(str(title) + '\n')

output_appos.close()
output_pnoun.close()