import datetime
from data_storage.store_data import save_to_csv
from data_fetching.fetch_data import fetch_all_stock_close_price_by_date

def main():
    start_date = (datetime.date.today() - datetime.timedelta(days=366)).strftime("%Y-%m-%d")
    end_date = datetime.date.today().strftime("%Y-%m-%d")
    print(start_date, end_date)
    all_stock_close_price = fetch_all_stock_close_price_by_date(start_date, end_date)
    save_to_csv(all_stock_close_price, f"all_stock_close_price_from{start_date}to{end_date}.csv")

main()