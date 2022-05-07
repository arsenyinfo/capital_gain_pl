from decimal import Decimal

import pandas as pd

from core import get_gains_for_asset, get_gains_for_multiple_assets, to_decimal


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


def test_get_gains_for_multiple_assets():
    df = pd.DataFrame({
        'date': ['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-01-05', '2020-01-06', '2020-01-07'],
        'type': ['buy', 'sell', 'buy', 'sell', 'buy', 'sell', 'buy'],
        'amount': to_decimal([10., 20.5, 30.5, 40, 50, 10, 10]),
        'price': to_decimal([98, 99, 100, 101, 102, 1000, 1001]),
        'asset': ['BTC', 'BTC', 'BTC', 'BTC', 'BTC', 'AAPL', 'AAPL'],
    })
    df['date'] = pd.to_datetime(df['date'])

    result = get_gains_for_multiple_assets(df).to_dict()
    assert result['gains']['BTC'] == Decimal('38.28615')
    assert result['gains']['AAPL'] == Decimal('-38.2130')
    assert result['leftover']['BTC'] == 30
    assert result['leftover']['AAPL'] == 0
