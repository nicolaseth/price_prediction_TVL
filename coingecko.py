import requests
import pandas as pd
import datetime
import json

# coingecko starting date
fromDate = "1546034556"  # 12-28-2018
# coingecko to date
toDate = "1641213572"  # 01-02-2022

# list of cryptos
coin_gecko_list = ["ethereum", "terra-luna", "oec-binance-coin", "solana", "avalanche-2", "fantom", "matic-network",
                   "crypto-com-chain", "tron"]

defillama_list = ["Ethereum", "Terra", "BSC", "Solana", "Avalanche", "Fantom", "Polygon", "Cronos", "Tron"]


zip_object = zip(coin_gecko_list, defillama_list)
for crypto_curr, coin_lama in zip_object:

    df = pd.DataFrame()
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_curr}/market_chart/range?vs_currency=usd&from={fromDate}" \
          f"&to={toDate}"

    response = requests.get(url)
    data = json.loads(response.text)
    data = data["prices"]
    df = pd.DataFrame(data)
    df.columns = ["date", "price"]
    df.date = df.date / 1000
    df.date = df.date.apply(lambda d: datetime.datetime.fromtimestamp(int(d)).strftime('%Y-%m-%d'))
    df["date"] = df["date"].apply(pd.to_datetime)
    df.reset_index(drop=True, inplace=True)
    df.set_index('date')
    # print(df)
    # df.to_csv(f"{crypto_curr}.csv")
    response = requests.get(f"https://api.llama.fi/charts/{coin_lama}").json()

    df_dl = pd.DataFrame(response)
    df_dl.reset_index(drop=True, inplace=True)
    df_dl.set_index('date')
    df_dl.date = df_dl.date.apply(lambda d: datetime.datetime.fromtimestamp(int(d)).strftime('%Y-%m-%d'))
    df_dl["date"] = df_dl["date"].apply(pd.to_datetime)
    print(f"working on defi {coin_lama}")
    merged_df = df_dl.merge(df, on="date", how="inner")
    merged_df.totalLiquidityUSD = merged_df.totalLiquidityUSD/1000000
    merged_df.rename(columns={"totalLiquidityUSD": "TVL_in_Millions"}, inplace=True)
    merged_df.reset_index(drop=True, inplace=True)
    merged_df.to_csv(f"{crypto_curr}.csv")
    print(merged_df)
    df_dl = pd.DataFrame()
    merged_df = pd.DataFrame()

