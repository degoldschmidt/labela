import pandas as pd

def load_data():
    out_dict = {
        "genotype": [],
        "date": [],
        "owner": [],
        "comments": [],
    }

    out_dict['genotype'] = ['nsyb-Gal4', 'UAS-TrpA1', 'Canton S', 'W;UAS-Chrimson/cyo;+']
    out_dict['date'] = ['04.05.2016', '04.05.2016', '04.05.2016', '27.12.2015']
    out_dict['owner'] = ['Dennis', 'Dennis', 'Dennis', 'Dennis']
    out_dict['comments'] = ['-', 'weak expression', '-', 'few flies']

    return pd.DataFrame(out_dict)
