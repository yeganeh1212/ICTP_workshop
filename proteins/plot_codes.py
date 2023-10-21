# heatmap example code

def F_to_C(temp_F):
    return round((temp_F - 32) * (5 / 9), 2)


import altair as alt
import pandas as pd

source = pd.read_csv("./basic_charts_data/bergen_weather.csv")


alt.Chart(
    source, title="2021-22 Daily High Temperature (C) in Bergen, Norway"
).mark_rect().encode(
    alt.X(
        "date(DATE):O",
    ),
    alt.Y(
        "month(DATE):O",
    ),
    alt.Color("TMAX:Q", scale=alt.Scale(scheme="inferno")),
    tooltip=[
        alt.Tooltip("monthdate(DATE):T", title="Date"),
        alt.Tooltip("TMAX:Q", title="Max Temp"),
    ],
).properties(
    width=550
).save(
    "./basic_charts_html_output/heatmap.html"
)


# bar plot example 
penguins_data = pd.read_json("./basic_charts_data/penguins.json")
print(penguins_data.head())

# how many of each species of penguin are there?
penguin_species_bar = (
    alt.Chart(penguins_data)
    .mark_bar()
    .encode(alt.Y("Species:N", sort="x"), alt.X("count()"), color="Species")
    .properties(title="Number of Penguins by Species")
)

penguin_species_bar.configure_title(fontSize=20, anchor="start").save(
    "./basic_charts_html_output/bar.html"
)
penguin_species_bar.show()
# how does beak depth distribution vary between penguin species?
penguin_species_beak_depth_histo = (
    alt.Chart(penguins_data)
    .mark_bar(opacity=0.3, binSpacing=0)
    .encode(
        alt.X("Beak Depth (mm)", bin=True),
        alt.Y("count()", stack=True),
        alt.Color("Species:N"),
    )
    .properties(title="Penguin Beak Depth by Species")
)
penguin_species_beak_depth_histo.configure_title(fontSize=20, anchor="start").save(
    "./basic_charts_html_output/histo.html"
)