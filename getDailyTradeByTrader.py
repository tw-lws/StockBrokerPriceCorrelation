from data_storage.store_data import save_to_csv
from data_fetching.fetch_data import fetch_taiwan_stock_trading_report_by_trader
import datetime

def main():
    start_date = (datetime.date.today() - datetime.timedelta(days=366)).strftime("%Y-%m-%d")
    end_date = datetime.date.today().strftime("%Y-%m-%d")
    trader_id = "9217" # 凱基-松山
    print(trader_id, start_date, end_date)
    trader_trading_data = fetch_taiwan_stock_trading_report_by_trader(trader_id, start_date, end_date)
    save_to_csv(trader_trading_data, f"{trader_id}_from{start_date}to{end_date}_trader_trading.csv")


# securities_trader,price,buy,sell,securities_trader_id,stock_id,date
# 凱基松山,130.25,0,896,9217,0050,2023-11-15
# 凱基松山,130.3,0,1000,9217,0050,2023-11-15
# 凱基松山,130.45,0,365,9217,0050,2023-11-15
# 凱基松山,130.5,0,1000,9217,0050,2023-11-15
# 凱基松山,130.55,183,2000,9217,0050,2023-11-15
# 凱基松山,130.6,0,204,9217,0050,2023-11-15
# 凱基松山,130.8,0,1000,9217,0050,2023-11-15
# 凱基松山,71.1,0,5000,9217,0051,2023-11-15
# 凱基松山,23.87,0,2000,9217,0055,2023-11-15
# 凱基松山,34.8,0,500,9217,0056,2023-11-15
# 凱基松山,34.9,100,0,9217,0056,2023-11-15
# 凱基松山,34.92,3000,0,9217,0056,2023-11-15
# 凱基松山,35.05,0,6000,9217,0056,2023-11-15
# 凱基松山,35.09,0,15000,9217,0056,2023-11-15
# 凱基松山,35.1,1000,0,9217,0056,2023-11-15
# 凱基松山,35.12,0,10000,9217,0056,2023-11-15
# 凱基松山,35.14,0,1000,9217,0056,2023-11-15
def aggreate_by_stock_id_and_calculate_average_price(data):
    pass



if __name__ == "__main__":
    main()