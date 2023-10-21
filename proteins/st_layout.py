import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

df = pd.DataFrame({
    'protein': ['ALDOA', 'prot1', 'prot2'],
    'count': [10, 15, 7]
    })

mut = []
index = []
freq = []

for mutation in 'mut1 mut2 mut3 mut4 mut5'.split():
    for i in range(50):
        mut.append(mutation)
        index.append(i)
        freq.append(np.random.uniform())
    
df_heat = pd.DataFrame({
    'mut': mut,
    'index' : index,
    'freq' : freq,
    }
    )
    

bar_graph = alt.Chart(df).mark_bar().encode(
    x='count:Q',
    y='protein:N',
    color='protein:N')

# create heatmap plot
heatmap_plot = alt.Chart(
    df_heat,
    title="Protein mutations"
).mark_rect().encode(
    alt.X(
        "index:O",
    ),
    alt.Y(
        "mut:N",sort='-x'
    ),
    alt.Color("freq:Q", scale=alt.Scale(scheme='blues')),
    tooltip=[
        alt.Tooltip("index:O", title="Site Position"),
        alt.Tooltip("mutation:N", title="Modification Class"),        
    ],
).properties()

main_heatmap_plot = alt.Chart(
    df_heat,
    title="Protein mutations"
).mark_rect().encode(
    alt.X(
        "index:O",
    ),
    alt.Y('total:N'),
    alt.Color("sum(freq):Q", scale=alt.Scale(scheme='blues')),
    tooltip=[
        alt.Tooltip("index:O", title="Site Position"),
        alt.Tooltip("mut:N", title="Modification Class"),        
    ],
).properties()


main_cont, r_sidebar = st.columns([10,2], gap="small")


with main_cont:
    with st.container():
        st.header("Distribution of modifications.")
    with st.container():
        st.altair_chart(main_heatmap_plot, use_container_width=True)
    with st.container():
        st.altair_chart(heatmap_plot, use_container_width=True)

# Add a slider to the sidebar:
add_slider = st.slider(
    'Residue',
    min_value=1,
    max_value=300,
    step=1,
)

##st.bar_chart(np.random.randn(50, 3))
st.altair_chart(bar_graph)

with r_sidebar:
    st.header("Options")
    # Add a selectbox to the sidebar:
    add_selectbox = st.selectbox(
        'Protein',
        df.protein
    )

    # Add a radio to the sidebar:
    add_slider = st.radio(
        'Pathogenicity',
        options=['All', 'Yes', 'No']
    )

