import pandas as pd
data=pd.read_csv("./Desktop/data/BioVis-challenge-test-data.csv")

data_human=data[data['Species']=='HUMAN']

data_human_clean=data_human[ (data_human['classification'] != 'Chemical derivative') & (data_human['classification'] != 'Artefact') ]
data_human_clean=data_human_clean.dropna()
data_human_clean=data_human_clean.drop(columns=['Entry','UniAcc'])
data_human_clean=data_human_clean.reset_index()
data_human_clean.to_csv('protein_data_human_clean.csv')
