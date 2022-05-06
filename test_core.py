from decimal import Decimal

import pandas as pd

from core import get_gains_for_asset, to_decimal


def test_get_gains_for_asset():
    df = pd.DataFrame({
        'date': ['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-01-05'],
        'type': ['buy', 'sell', 'buy', 'sell', 'buy'],
        'amount': to_decimal([10., 20.5, 30.5, 40, 50]),
        'price': to_decimal([98, 99, 100, 101, 102]),
    })
    df['date'] = pd.to_datetime(df['date'])

    gain, left = get_gains_for_asset(df)
    assert gain['gain'].sum() == Decimal('38.28615')
    assert left == 30
