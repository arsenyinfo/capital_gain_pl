from datetime import datetime
from decimal import Decimal
from logging import getLogger
from typing import Collection, List

import coloredlogs
import pandas as pd

from currency import download_rates

logger = getLogger(__name__)

coloredlogs.install(level='INFO')


def to_decimal(collection: Collection) -> List[Decimal]:
    return [Decimal(x) for x in collection]


def convert_usd_to_pln(value: float, date: datetime, offset=1):
    currency = download_rates()
    if isinstance(value, str):
        value = float(value.replace(',', '.'))
    if offset > 10:
        raise ValueError('Offset is too big')
    try:
        return value * currency[(date - pd.Timedelta(days=offset)).strftime('%Y%m%d')]
    except KeyError:
        return convert_usd_to_pln(value, date, offset + 1)


def get_gains_for_asset(group: pd.DataFrame):
    """
    Expected dataframe of single asset deals, with columns: date, price, amount, type (buy/sell).
    """
    for k in ('type', 'date', 'price', 'amount'):
        if k not in group.columns:
            raise ValueError(f'{k} not in group')

    have = []
    debt = []
    group = group.sort_values('date')

    gains = []
    for _, row in group.iterrows():
        deal = [row['amount'], row['date'], row['price']]
        if row['type'] == 'buy':
            have.append(deal)
        elif row['type'] == 'sell':
            debt.append(deal)
        else:
            raise ValueError(f'Unknown deal type: {row["type"]}')

    have_idx, debt_idx = 0, 0

    while have_idx < len(have) and debt_idx < len(debt):
        have_amount, have_date, have_price = have[have_idx]
        debt_amount, debt_date, debt_price = debt[debt_idx]
        if have_amount == debt_amount:
            amount = have_amount
            have_idx += 1
            debt_idx += 1
        elif have_amount < debt_amount:
            amount = have_amount
            have_idx += 1
            debt[debt_idx][0] -= amount
        elif have_amount > debt_amount:
            amount = debt_amount
            debt_idx += 1
            have[have_idx][0] -= amount

        logger.info(f'Bought for {have_price * amount}, sold for {debt_price * amount}')
        gained = estimate_gain(buy_usd=have_price * amount,
                               sell_usd=debt_price * amount,
                               buy_date=have_date,
                               sell_date=debt_date)
        gains.append({'date': have_date, 'gain': gained})

    leftover_have = have[have_idx:]
    leftover_debt = debt[debt_idx:]

    have_left = sum(a for a, d, p in leftover_have)
    debt_left = sum(a for a, d, p in leftover_debt)
    logger.info(f'Leftover: have {have_left}, debt {debt_left}')
    assert have_left == 0 or debt_left == 0

    return pd.DataFrame(gains), have_left - debt_left


def estimate_gain(buy_usd, sell_usd, buy_date, sell_date) -> float:
    buy_price_pln = convert_usd_to_pln(buy_usd, buy_date, offset=1)
    sell_price_pln = convert_usd_to_pln(sell_usd, sell_date, offset=1)
    return sell_price_pln - buy_price_pln
