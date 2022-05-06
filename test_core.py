import pandas as pd
import numpy as np
from core import get_gains_for_asset


def test_get_gains_for_asset():
    df = pd.DataFrame({
        'date': ['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-01-05'],
        'type': ['buy', 'sell', 'buy', 'sell', 'buy'],
        'amount': [10., 20.5, 30.5, 40, 50],
        'price': [98, 99, 100, 101, 102]
    })
    df['date'] = pd.to_datetime(df['date'])

    gain, left = get_gains_for_asset(df)
    assert np.isclose(gain['gain'].sum(), 38.28615, rtol=0., atol=1e-5)
    assert left == 30
