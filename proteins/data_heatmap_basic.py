import pandas as pd
import numpy as np
import altair as alt

"""
A basic heatmap for part of the data
No specified width, to keep all the cell in square shape.
"""


data = pd.read_csv("data_human.csv")

#user should choose protein type
data_protein = data[data['Gene']=='ALDOA']

#counting modifications by position and classification
data_protein_count = data_protein.groupby(['POS' , 'classification'] , as_index=False).count()

#for heatmap we need position , modification number
modification_frequency = data_protein_count['MOD'].values
position = data_protein_count['POS'].values

#add classification id for heatmap
#{'Multiple': 0,'N-linked glycosylation': 1,'O-linked glycosylation': 2,'Other glycosylation': 3,'Post-translational': 4, 'Pre-translational': 5,'glyco': 6}
classification = data_protein_count['classification'].values
d = dict([(y,x) for x,y in enumerate(sorted(set(classification)))])
classification_id = np.array([d[x] for x in classification])

#creating dataframe for heatmap
heatmap_data = pd.DataFrame ({'position':position , 'classification':classification , 'classification_id':classification_id , 'modification_frequency':modification_frequency})
heatmap_data = heatmap_data[1:80]
alt.Chart(
    heatmap_data, title="Protein mutations"
).mark_rect().encode(
    alt.X(
        "position:O",
    ),
    alt.Y(
        "classification:O",
    ),
    alt.Color("modification_frequency:Q", scale=alt.Scale(scheme='blues')),
    # tooltip=[
    #     alt.Tooltip("monthdate(DATE):T", title="Date"),
    #     alt.Tooltip("TMAX:Q", title="Max Temp"),
    # ],
).properties(
    # width=800

    # width='container' # in case we want to fit inside an html, different for each machine I guess
).show()
