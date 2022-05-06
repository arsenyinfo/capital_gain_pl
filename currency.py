import os
import tempfile
from functools import lru_cache

import pandas as pd
import requests


@lru_cache(1)
def download_rates():
    currency = {}
    for year in range(2019, 2023):
        _, name = tempfile.mkstemp(suffix='csv')
        url = f'https://www.nbp.pl/kursy/Archiwum/archiwum_tab_a_{year}.csv'
        r = requests.get(url)
        with open(name, 'wb') as fd:
            fd.write(r.content)
        df = pd.read_csv(name, sep=';', encoding_errors='ignore')
        os.remove(name)

        dates = df['data'].values[1:-3]
        values = df['1USD'].values[1:-3]
        year_parsed = {k: float(v.replace(',', '.')) for k, v in zip(dates, values)}

        for k, v in year_parsed.items():
            currency[k] = v

    return currency
