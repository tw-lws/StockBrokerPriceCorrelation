from FinMind.data import DataLoader
from config.config import FINMIND_API_KEY
import pandas as pd
import datetime
from itertools import chain
import requests

api = DataLoader()
api.login_by_token(api_token=FINMIND_API_KEY)
# # 使用 API 金鑰登入
# def login_by_token():
#     data_loader = DataLoader(api_token=FINMIND_API_KEY)
#     return data_loader

def fetch_stock_list():
    stock_list = api.taiwan_stock_info()
    return stock_list

def fetch_stock_data(stock_id, start_date, end_date):
    stock_price_data = pd.DataFrame()
    current_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

    while current_date <= end_date:
        daily_data = api.taiwan_stock_day_trading(
            stock_id=stock_id,
            start_date=current_date.strftime("%Y-%m-%d"),
            end_date=current_date.strftime("%Y-%m-%d")
        )
        stock_price_data = pd.concat([stock_price_data, daily_data])
        current_date += datetime.timedelta(days=1)

    return stock_price_data

def fetch_taiwan_stock_trading_daily_report(stock_id, start_date, end_date):
    all_data = []
    current_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

    while current_date <= end_date:
        url = 'https://api.finmindtrade.com/api/v4/taiwan_stock_trading_daily_report'
        parameters = {
            "data_id": stock_id,
            "date": current_date.strftime("%Y-%m-%d"),
            "token": FINMIND_API_KEY,
        }
        response = requests.get(url, params=parameters)
        data = response.json()
        if data['status'] == 200:
            all_data.append(data['data'])
        else:
            print(f"Error fetching data for {current_date}: {data['msg']}")
        current_date += datetime.timedelta(days=1)

    return pd.DataFrame(list(chain.from_iterable(all_data)))
