import yfinance as yf
import pandas as pd
import datetime as dt
import traceback


def get_live_yfinance_option_chain(symbol: str, expiry_rank: int = 1) -> pd.DataFrame:
    """
    function which can obtain the live option chain for any symbol os users choice
    option chain data pulled from yahoo finance

    :param symbol:
        ticker symbol of the equity  user wants option data for (ex: "AAPL")
    :param expiry_rank:
        which  expiry  user wants option chain data for.
        expiry_rank == 1 corresponds to the nearest expiry
        expiry_rank == 2 corresponds to the subsequent expiry
        and so on for higher numbers

    :return:
        pandas dataframe of the option chain information requested by the user

        the output columns received are
        1. symbol: as passed by user
        2. tickdate: current tickdate options data has been pulled for in YYYY-MM-DD format
        3. expiry_rank: as passed by user
        4. strike: strike price of the CE and PE columns specified
        5. expiration: expiration date of the option chain requested in YYYY-MM-DD format
        6. CE_last: last traded price for CE against its strike price
        7. CE_bid: bid price for CE against its strike price
        8. CE_ask: ask price for CE against its strike price
        9. PE_last: last traded price for PE against its strike price
        10. PE_bid: bid price for PE against its strike price
        11. PE_ask: ask price for PE against its strike price
    """
    try:
        # log
        print("=" * 69)
        print(f"pulling option chain data for symbol: {symbol}, expiry_rank: {expiry_rank}")
        print("=" * 69)

        # get ticker
        t = yf.Ticker(symbol)

        # get option chain based on expiry rank
        expiration = t.options[expiry_rank - 1]
        chain = t.option_chain(expiration)

        # get call and puts option chain
        ce = chain.calls
        pe = chain.puts

        # rename and merge CE and PE dataframes
        ce = ce.loc[:, ['strike', 'lastPrice', 'bid', 'ask']] \
            .sort_values(['strike']) \
            .reset_index(drop=True) \
            .rename(columns={'lastPrice': 'CE_last', 'bid': 'CE_bid', 'ask': 'CE_ask'})
        pe = pe.loc[:, ['strike', 'lastPrice', 'bid', 'ask']] \
            .sort_values(['strike']) \
            .reset_index(drop=True) \
            .rename(columns={'lastPrice': 'PE_last', 'bid': 'PE_bid', 'ask': 'PE_ask'})

        # merge the 2 dataframes into one
        df = pd.merge(ce, pe, on=['strike'], how='outer')
        df.insert(1, "expiration", expiration)

        # compute DTE
        df['DTE'] = (pd.to_datetime(df['expiration']) -
                     pd.to_datetime(dt.datetime.now().strftime('%Y-%m-%d'))).dt.days

        # add in tickdate, expiry_rank and symbol as well
        df.insert(0, "symbol", symbol)
        df.insert(1, "tickdate", dt.datetime.now().strftime("%Y-%m-%d"))
        df.insert(2, "expiry_rank", expiry_rank)


    except:
        print(f"exception occurred for symbol: {symbol}, expiry_rank: {expiry_rank}")
        traceback.print_exc()
        df = pd.DataFrame()

    return df
