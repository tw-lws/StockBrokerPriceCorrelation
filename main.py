from data_fetching.fetch_data import fetch_stock_list, fetch_stock_data, fetch_taiwan_stock_trading_daily_report
from data_storage.store_data import save_to_csv
import datetime

def main():
    stock_list = fetch_stock_list()
    save_to_csv(stock_list, "stock_list.csv")
    # 先取得第一筆股票代碼 用來當作範例 這邊取得的是 0050
    example_stock_id = stock_list["stock_id"][0]
    # 取得今天日期的前十天
    start_date = (datetime.date.today() - datetime.timedelta(days=10)).strftime("%Y-%m-%d")
    end_date = datetime.date.today().strftime("%Y-%m-%d")
    print(example_stock_id, start_date, end_date)

    stock_price_data = fetch_stock_data(example_stock_id, start_date, end_date)
    save_to_csv(stock_price_data, f"{example_stock_id}_stock_price.csv")

    broker_trading_data = fetch_taiwan_stock_trading_daily_report(example_stock_id, start_date, end_date)
    save_to_csv(broker_trading_data, f"{example_stock_id}_broker_trading.csv")

if __name__ == "__main__":
    main()

