import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

from proteins import bar_chart

"""
This scrips plots the protein mutation data. It aims at covering two main goals:
- Identify where modifications are most likely to occur, and
- Identify and compare the frequencies of different modification types across individual sites.
We have a heatmap which shows the frequency of the different modifacations happening at 
each site within one protein. The other heatmap on the top shows the total number of mutatation at each site.
Note that if one site did not have any mutations, it was not shown. 

"""
path="./proteins/data_human.csv"
data=pd.read_csv(path)

st.set_page_config(layout="wide")

main_cont, r_sidebar = st.columns([10,2], gap="small")


with r_sidebar:
    selected_protein = st.selectbox(
        'Protein type',
        (data['Gene'].unique())
    )

    patho = st.radio(
        "Type of pathogenicity to show",
        ('All', 'Pathogenic_only'))







#function for heat map
#user should choose protein type : ['ALDOA', 'HNRNPA1', 'DDX3X', 'TGFB1']
#user should choose weather pathogenic modification or all modifications ,It is a boolean , True means pathogenic

def Heatmap_Data (data , protein_type , patho , length):
    if patho == 'All':
        pathogenic = False
    else:
        pathogenic = True

    data_protein = data[data['Gene']==protein_type]
    if pathogenic:
        data_protein=data_protein[data_protein['PathogenicMutation']==True]
    #counting modifications by position and classification
    data_protein_count = data_protein[(data_protein['POS'] >= length[0]) & (data_protein['POS'] <= length[1])]
    data_protein_count = data_protein_count.groupby(['POS' , 'classification' , 'RES'] , as_index=False).count()

    #for heatmap we need position , modification number
    residue = data_protein_count['RES'].values
    modification_frequency = data_protein_count['MOD'].values
    position = data_protein_count['POS'].values

    #add classification id for heatmap
    #{'Multiple': 0,'N-linked glycosylation': 1,'O-linked glycosylation': 2,'Other glycosylation': 3,'Post-translational': 4, 'Pre-translational': 5,'glyco': 6}
    classification = data_protein_count['classification'].values
    d = dict([(y,x) for x,y in enumerate(sorted(set(classification)))])
    classification_id = np.array([d[x] for x in classification])

    #creating dataframe for heatmap 
    heatmap_data = pd.DataFrame ({'position':position ,'res':residue,'classification':classification , 'classification_id':classification_id , 'modification_frequency':modification_frequency})
    heatmap_data = heatmap_data[(heatmap_data['position'] >= range_sites[0]) & (heatmap_data['position'] <= range_sites[1])]
    return heatmap_data
    

#function for sum classification in each position
#user should choose protein type : ['ALDOA', 'HNRNPA1', 'DDX3X', 'TGFB1']
#user should choose weather pathogenic modification or all modifications ,It is a boolean , True means pathogenic
def Sum_Classification_Data (data , protein_type , patho , length):
    if patho == 'All':
        pathogenic = False
    else:
        pathogenic = True
    data_protein = data[data['Gene']==protein_type]
    if pathogenic:
        data_protein=data_protein[data_protein['PathogenicMutation']==True]

    data_protein = data_protein[(data_protein['POS'] >= length[0]) & (data_protein['POS'] <= length[1])]
    
    #counting classification by position 
    sum_data = data_protein.groupby(['POS'] , as_index=False).count()
    sum_data = sum_data[(sum_data['POS'] >= range_sites[0]) & (sum_data['POS'] <= range_sites[1])]

    return sum_data



with main_cont:
    # add a slider to pick range of the data shown. range would give two values
    range_sites = st.slider(
        "range of sites shown",
        min(data[data['Gene']==selected_protein].POS),
        max(data[data['Gene']==selected_protein].POS), 
        (min(data[data['Gene']==selected_protein].POS),
        max(data[data['Gene']==selected_protein].POS)))


##    click = alt.selection_single()
    # click = alt.selection(type="interval")
    # add a summed heatmap on the top of the other heatmap

    summ = Sum_Classification_Data (data , selected_protein , patho , range_sites)
    # add a summed heatmap on the top of the other heatmap
    if len(summ) < 50:
        summed_heatmap_plot = (alt.Chart(
            Sum_Classification_Data (data , selected_protein , patho , range_sites),
            title="Total Frequency"
        ).mark_rect().encode(
            alt.X(
                "POS:O",
            ),
            # alt.Y(
            #     "classification:Q"#,sort='-x'
            # ),
            alt.Color("classification:Q", scale=alt.Scale(scheme='blues')),

        ).properties(height=120))#.add_selection(click))

    else :
          summed_heatmap_plot = (alt.Chart(
            Sum_Classification_Data (data , selected_protein , patho , range_sites),
            title="Total Frequency"
        ).mark_rect().encode(
            alt.X(
                "POS:O",bin=alt.Bin(maxbins=40)
            ),
            # alt.Y(
            #     "classification:Q"#,sort='-x'
            # ),
            alt.Color("classification:Q", scale=alt.Scale(scheme='blues')),

        ).properties(height=120))#.add_selection(click)) 

            # width='container' # in case we want to fit inside an html, different for each machine I guess
        
    heatmapp = Heatmap_Data (data , selected_protein , patho, range_sites)
    if len(heatmapp)< 50:
    # create heatmap plot
        heatmap_plot = alt.Chart(
            heatmapp,
            title="Protein mutations"
        ).mark_rect().encode(
            alt.X(
                "position:O",
            ),
            alt.Y(
                "classification:O",sort='-x'
            ),
            alt.Color("modification_frequency:Q", scale=alt.Scale(scheme='blues')),
            tooltip=[
                alt.Tooltip("position:O", title="Site Position"),
                alt.Tooltip("classification:N", title="Modification Class"),
                alt.Tooltip("res:N", title="Resude Type"),
                alt.Tooltip("modification_frequency:Q", title="Frequency"),
                
            ],
        )
    else :
        heatmap_plot = alt.Chart(
            heatmapp,
            title="Protein mutations"
        ).mark_rect().encode(
            alt.X(
                "position:O",bin=alt.Bin(maxbins=40)
            ),
            alt.Y(
                "classification:O",sort='-x'
            ),
            alt.Color("modification_frequency:Q", scale=alt.Scale(scheme='blues')),
            tooltip=[
    ##            alt.Tooltip("position:O", title="Site Position"),
                alt.Tooltip("classification:N", title="Modification Class"),
    ##            alt.Tooltip("res:N", title="Resude Type"),
                alt.Tooltip("modification_frequency:Q", title="Frequency"),
                
            ],
        )

    bar_chart = bar_chart.residue_bar_chart_random(heatmapp)
##    bar_chart = bar_chart.transform_filter(click)
                                            

    st.altair_chart(summed_heatmap_plot, use_container_width=True)
    st.altair_chart(heatmap_plot, use_container_width=True)
    st.altair_chart(bar_chart)
