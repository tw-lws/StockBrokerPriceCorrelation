import time
from FinMind.data import DataLoader
from config.config import FINMIND_API_KEY, API_BASE_URL
import pandas as pd
import datetime
from itertools import chain
import requests
from json.decoder import JSONDecodeError


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
        endpoint = 'taiwan_stock_trading_daily_report'
        url = f"{API_BASE_URL}/{endpoint}"
        print(url)
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


def fetch_taiwan_stcok_securities_trader_info():
    parameter = {
        "dataset": "TaiwanSecuritiesTraderInfo",
        "token": f"{FINMIND_API_KEY}" # 參考登入，獲取金鑰
    }
    response = requests.get(f"{API_BASE_URL}/data", params=parameter)
    data = response.json()
    data = pd.DataFrame(data["data"])
    return data

def fetch_taiwan_stock_trading_report_by_trader(trader_id, start_date, end_date, max_retries=2):
    if not trader_id:
        raise ValueError("請輸入券商代號")
    
    all_data = []
    current_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

    while current_date <= end_date:
        retries = 0
        success = False
        endpoint = 'taiwan_stock_trading_daily_report'
        url = f"{API_BASE_URL}/{endpoint}"
        print(url)
        parameters = {
            "securities_trader_id": trader_id,
            "date": current_date.strftime("%Y-%m-%d"),
            "token": FINMIND_API_KEY,
        }
        while retries <= max_retries and not success:
            try:
                response = requests.get(url, params=parameters)

                if response.status_code == 200:
                    data = response.json()
                    if data['status'] == 200:
                        all_data.append(data['data'])
                        success = True
                    else:
                        print(f"Error fetching data for {current_date}: {data['msg']}")
                        retries += 1
                        time.sleep(1)  # 等待 1 秒後重試
                else:
                    print(f"HTTP error {response.status_code} for {current_date}")
                    retries += 1
                    time.sleep(1)  # 等待 1 秒後重試

            except (JSONDecodeError, requests.RequestException) as e:
                print(f"Error fetching data for {current_date}: {e}")
                retries += 1
                time.sleep(1)  # 等待 1 秒後重試

        if not success:
            print(f"Failed to fetch data for {current_date} after {max_retries} retries.")

        current_date += datetime.timedelta(days=1)
    return pd.DataFrame(list(chain.from_iterable(all_data)))

def fetch_all_stock_close_price_by_date(start_date, end_date, max_retries=2):
    url = f"{API_BASE_URL}/data"
    all_data = []
    current_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

    while current_date <= end_date:
        retries = 0
        success = False
        parameters = {
            "dataset": "TaiwanStockPrice",
            "start_date": current_date.strftime("%Y-%m-%d"),
            "token": FINMIND_API_KEY,
        }
        while retries <= max_retries and not success:
            try:
                response = requests.get(url, params=parameters)

                if response.status_code == 200:
                    data = response.json()
                    if data['status'] == 200:
                        all_data.append(data['data'])
                        success = True
                    else:
                        print(f"Error fetching data for {current_date}: {data['msg']}")
                        retries += 1
                        time.sleep(1)  # 等待 1 秒後重試
                else:
                    print(f"HTTP error {response.status_code} for {current_date}")
                    retries += 1
                    time.sleep(1)  # 等待 1 秒後重試

            except (JSONDecodeError, requests.RequestException) as e:
                print(f"Error fetching data for {current_date}: {e}")
                retries += 1
                time.sleep(1)  # 等待 1 秒後重試

        if not success:
            print(f"Failed to fetch data for {current_date} after {max_retries} retries.")

        current_date += datetime.timedelta(days=1)
    
    return pd.DataFrame(list(chain.from_iterable(all_data)))