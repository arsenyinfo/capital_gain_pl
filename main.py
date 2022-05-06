import datetime
from decimal import Decimal

import streamlit as st

from core import estimate_gain

TAX_RATE = Decimal(0.19)


def main():
    st.title("Capital gain calculator 🇵🇱")

    st.sidebar.header("FAQ")
    st.sidebar.markdown("""
    * What is this app?
    It's a capital gain calculator for Poland 🇵🇱 residents. 
    
    * What's capital gain?
    Capital gain is the amount of money you get from selling your property (e.g. stock, bonds, etc.). 
    You pay capital gain tax on it; currently 19% in Poland.
    
    * I don't own stocks or bonds for now, how can I start? 
    
    There will be a broker advertisement. 

    * I want to learn more before investing, would you suggest a crash course on finance and investments? 
    
    There will be an education advertisement. 
        
    * I want to get more information about it! 
    
    You need to contact the accountant or tax advisor. There will be an advertisement.
    
    * I have a question for the app developer!
    
    Contact me at: `me@arseny.info`.  
    """)

    selection = st.radio("Calculate for a ", ["single deal", "many deals"])

    if selection == "single deal":
        st.subheader("Estimate your capital gain for a single deal")
        buy_date = st.date_input("Buy date", datetime.date.today() - datetime.timedelta(days=365))
        sell_date = st.date_input("Sell date")
        buy_price = Decimal(st.number_input("Buy price in $", value=1000.0))
        sell_price = Decimal(st.number_input("Sell price in $", value=1000.0))

        if st.button("Calculate"):
            profit = estimate_gain(buy_price, sell_price, buy_date, sell_date, )
            st.write(f'Profit: {profit:.2f} PLN, taxes: {profit * TAX_RATE:.2f} PLN')
            st.write(f'Your deadline is: April 30, {(sell_date + datetime.timedelta(days=365)).year}')

    else:
        st.subheader("Estimate your capital gain for a list of deals")

        description = "Upload a file with deals. " \
                      "\nExpected format: csv with columns name, date, price, amount, type (buy/sell)"
        st.file_uploader(description, accept_multiple_files=True, type=["csv"])
        if st.button("Calculate"):
            st.warning("Not implemented yet!")

    st.info("Donations are welcome and will be spent entirely for :beer:")


if __name__ == "__main__":
    main()
