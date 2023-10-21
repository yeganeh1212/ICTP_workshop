import pandas as pd

data = pd.read_csv("BioVis-challenge-test-data.csv")

data_human = data[data["Species"] == 'HUMAN']
print(len(data_human))
#filter Nan, artifact and chemical "classifications"

#mask = ('calssification' == 'Chemical derivative') | 
#    ('calssification' == 'Artefact') |
#    ('calssification' == nan)
#
#data_human = data_human[data_human[!mask]]

print(data_human['Gene'].unique())