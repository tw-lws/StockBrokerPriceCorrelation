from data_fetching.fetch_data import fetch_taiwan_stcok_securities_trader_info
from data_storage.store_data import save_to_csv
def main():
    taiwan_stcok_securities_trader_info = fetch_taiwan_stcok_securities_trader_info()
    print(taiwan_stcok_securities_trader_info)
    save_to_csv(taiwan_stcok_securities_trader_info, "taiwan_stcok_securities_trader_info.csv")

if __name__ == "__main__":
    main()
    # 9217,凱基-松山,2009-12-21,台北市八德路4段678號3樓,02-27534567