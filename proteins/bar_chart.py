import altair as alt
import random

def filter_by_residue(df, pos):
    """Filter mutations dataframe to get mutations on given residue"""

    residue_df = df[df['position'] == pos]
    return residue_df

def create_bar_chart(residue_df):
    """Create a bar chart showing the count of classifications within a residue

    Parameters
    ----------
    position_df : pd.DataFrame
        Dataframe containing all mutations for a specific site.
    """
    bar_chart = alt.Chart(residue_df).mark_bar().encode(
        x=alt.X('count(classification):Q',
                axis=alt.Axis(title='Count')),
        y=alt.Y('classification:N',
                axis=alt.Axis(title='Classification')),
        color=alt.Color('classification:N', legend=None),
        tooltip=[
            alt.Tooltip('count(classification):Q'),
            ]
        )

    return bar_chart


def residue_bar_chart(df, pos):
    """Return a classifications bar graph for a given filtered dataframe and position"""
    residue_df = filter_by_residue(df, pos)
    return create_bar_chart(residue_df).properties(title=f"Position {pos}")

def residue_bar_chart_first(df):
    """Return a classifications bar graph for the first residue on the dataframe"""
    first_residue = df['position'].iloc[0]
    return residue_bar_chart(df, first_residue)

def residue_bar_chart_random(df):
    """Return a classifications bar graph for the first residue on the dataframe"""
    random_residue = random.choice(df['position'].unique())
    return residue_bar_chart(df, random_residue)
