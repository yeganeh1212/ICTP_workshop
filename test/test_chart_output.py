import os
import pandas as pd
from proteins.bar_chart import create_bar_chart

def test_bar_chart_output():
    protdata = pd.read_csv('./test/test_minimum_modifications_dataset.csv')
    # I choose it likje this so its more flexible
    test_residue_barchart = create_bar_chart(protdata)
    test_residue_barchart.save('test_residue_bar_chart.html')
    assert os.path.isfile('./test_residue_bar_chart.html')
