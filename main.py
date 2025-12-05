from utils.option_chain import get_live_yfinance_option_chain

if __name__ == '__main__':
    # sample run for Apple equity options data for the nearest week
    symbol = "AAPL"
    expiry_rank = 1

    # calling the option pulling function
    df = get_live_yfinance_option_chain(
        symbol=symbol,
        expiry_rank=expiry_rank
    )
    print(df.head())
