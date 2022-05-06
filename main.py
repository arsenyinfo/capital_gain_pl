import streamlit as st

from core import estimate_gain

TAX_RATE = 0.19


def main():
    st.title("Capital gain calculator")
    buy_date = st.date_input("Buy date")
    sell_date = st.date_input("Sell date")
    buy_price = st.number_input("Buy price", value=1.0)
    sell_price = st.number_input("Sell price", value=1.0)

    if st.button("Calculate"):
        profit = estimate_gain(buy_price, sell_price, buy_date, sell_date, )
        st.write(f'Profit: {profit:.2f} PLN, taxes: {profit * TAX_RATE:.2f} PLN')


if __name__ == "__main__":
    main()
