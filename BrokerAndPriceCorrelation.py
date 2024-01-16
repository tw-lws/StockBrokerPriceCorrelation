# -*- coding: utf-8 -*-
"""劉岳樺_劉緯軒_財金所學分班_統計學期末報告.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EXgX96hCyUnJPUcVNC5o-M2NoZ28ivBC
"""

# from google.colab import drive
# drive.mount('/content/drive')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy import stats
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import gdown

# folder_path = '/content/drive/My Drive/交大學分班/112-1統計學/期末報告/資料集/'

def create_download_link(shared_link):
    file_id = shared_link.split('/')[-2]
    return f"https://drive.google.com/uc?export=download&id={file_id}&confirm=t"

    

# 股票列表數據
stk_list_url = 'https://drive.google.com/file/d/1vqT8-o3uR7NWtS_nemH711elS-V8tg5w/view?usp=drive_link'
stk_list_path = create_download_link(stk_list_url)
stk_list = pd.read_csv(stk_list_path)
print(stk_list.head())

# 交易數據
#df_trading_url = 'https://drive.google.com/file/d/1SA112l0qsN8L_vn3SEhk0xiRaWmowoVl/view?usp=drive_link'
#df_trading_path = create_download_link(df_trading_url)
#df_trading = pd.read_csv(df_trading_path)
#print(df_trading.head())

# 20240116 update 使用 gdown 下載資料
df_trading_url = 'https://drive.google.com/uc?id=1SA112l0qsN8L_vn3SEhk0xiRaWmowoVl&confirm=t'
df_trading_output = 'all_stock_close_price_from2022-12-23to2023-12-24.csv'
gdown.download(df_trading_url, df_trading_output, quiet=False)
df_trading = pd.read_csv(df_trading_output)
print(df_trading.head())

# 券商數據
df_broker_url = 'https://drive.google.com/file/d/1nl8vMQrRCVd0I-UmT_uop07s2OIxR_K3/view?usp=drive_link'
df_broker_path = create_download_link(df_broker_url)
df_broker = pd.read_csv(df_broker_path)


# 先整理股票清單（排除ETF等不列入樣本的資料)
stk_list = stk_list[~stk_list['industry_category'].isin(['ETF','ETN','上櫃指數股票型基金(ETF)','受益證券','指數投資證券(ETN)','其他','所有證券','創新板股票','存託憑證', 'Index', '大盤'])]
stk_list = stk_list[stk_list['type'].isin(['twse'])]
stk_list = stk_list[stk_list['stock_id'].apply(lambda x: len(x) == 4)]

stock_ids = stk_list['stock_id'].unique()

# 過濾出要分析的股票 而不是ETF等等
df_broker = df_broker[df_broker['stock_id'].isin(stock_ids)]

# 按日期分組，選取每天買進量前二十的股票
# top20_buys_daily = df_broker.groupby('date').apply(lambda x: x.sort_values('buy', ascending=False).head(20)).reset_index(drop=True)

buys_daily = df_broker.groupby('date').apply(lambda x: x.sort_values('buy', ascending=False)).reset_index(drop=True)

# 計算每支股票每天的總買進量
broker_buy_sum = buys_daily.groupby(['stock_id', 'date'])['buy'].sum().reset_index()

# 合併到每日成交資料中
df_combined = pd.merge(df_trading, broker_buy_sum, on=['stock_id', 'date'], how='left')

# 計算買進比例
df_combined['buy_ratio'] = df_combined['buy'] / df_combined['Trading_Volume']

# 對日期進行排序，以便計算隔天價格
df_combined.sort_values(by=['stock_id', 'date'], inplace=True)
print(len(df_combined))
# ----------
df_combined['next_day_close'] = df_combined.groupby('stock_id')['close'].shift(-1)
df_combined['price_change'] = df_combined['next_day_close'] - df_combined['close']
df_combined['price_change_percentage'] = (df_combined['price_change'] / df_combined['close']) * 100

#list the next_day_price_change > +- 10%
# filter out the outlier
df_combined = df_combined[df_combined['price_change_percentage'].apply(lambda x: abs(x) < 10)]
print(len(df_combined))


df_combined['date'] = pd.to_datetime(df_combined['date'])
df_combined.sort_values(by=['stock_id', 'date'], inplace=True)
df_combined = df_combined.dropna(subset=['buy_ratio'])

print(len(df_combined))

for i in range(1, 6):
    # 先計算值
    next_day_close = df_combined.groupby('stock_id')['close'].shift(-i)
    price_change = (next_day_close - df_combined['close']) / df_combined['close'] * 100

    # 使用 .loc 来安全地修改 df_combined
    df_combined.loc[:, f'next_day_{i}_close'] = next_day_close
    df_combined.loc[:, f'price_change_day_{i}'] = price_change


df_combined = df_combined[df_combined['price_change_day_1'].abs() <= 10]
df_combined = df_combined[df_combined['price_change_day_2'].abs() <= 10 * 1.1]
df_combined = df_combined[df_combined['price_change_day_3'].abs() <= 10 * 1.1 ** 2]
df_combined = df_combined[df_combined['price_change_day_4'].abs() <= 10 * 1.1 ** 3]
df_combined = df_combined[df_combined['price_change_day_5'].abs() <= 10 * 1.1 ** 4]

# 移除NaN值
df_combined = df_combined.dropna(subset=['buy_ratio','price_change_day_1','price_change_day_2','price_change_day_3','price_change_day_4', 'price_change_day_5'])
print(len(df_combined))
df_combined

# 繪製散點圖
plt.scatter(df_combined['buy_ratio'], df_combined['price_change_day_1'], color='blue', label='Next Day')
plt.scatter(df_combined['buy_ratio'], df_combined['price_change_day_2'], color='green', label='Day 2')
plt.scatter(df_combined['buy_ratio'], df_combined['price_change_day_3'], color='red', label='Day 3')
plt.scatter(df_combined['buy_ratio'], df_combined['price_change_day_4'], color='cyan', label='Day 4')
plt.scatter(df_combined['buy_ratio'], df_combined['price_change_day_5'], color='magenta', label='Day 5')

# 添加標籤和標題
plt.xlabel('Buy Ratio')
plt.ylabel('Price Change Percentage (%)')
plt.title('Buy Ratio vs Price Change for Different Days')
plt.legend()

# 顯示圖形
plt.show()

# 計算回歸線參數並繪製散點圖及回歸線的函數
def plot_with_regression(x, y, title, color):
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, color=color)

    # 計算回歸線參數
    slope, intercept = np.polyfit(x, y, 1)
    plt.plot(x, slope * x + intercept, color='black', label='Regression Line')

    plt.xlabel('Buy Ratio')
    plt.ylabel('Price Change Percentage (%)')
    plt.title(title)
    plt.legend()
    plt.show()

# 去除含有NaN值的行
df_combined.dropna(subset=['price_change_day_1', 'price_change_day_2', 'price_change_day_3', 'price_change_day_4', 'price_change_day_5'], inplace=True)

# 繪製每一天的散點圖和回歸線
plot_with_regression(df_combined['buy_ratio'], df_combined['price_change_day_1'], 'Buy Ratio vs Next Day Price Change Percentage', 'blue')
plot_with_regression(df_combined['buy_ratio'], df_combined['price_change_day_2'], 'Buy Ratio vs Day 2 Price Change Percentage', 'green')
plot_with_regression(df_combined['buy_ratio'], df_combined['price_change_day_3'], 'Buy Ratio vs Day 3 Price Change Percentage', 'red')
plot_with_regression(df_combined['buy_ratio'], df_combined['price_change_day_4'], 'Buy Ratio vs Day 4 Price Change Percentage', 'cyan')
plot_with_regression(df_combined['buy_ratio'], df_combined['price_change_day_5'], 'Buy Ratio vs Day 5 Price Change Percentage', 'magenta')

"""零假設（H0）是：當凱基松山這間券商買進量佔當天總成交量的2%以上時，對該股票接下來五天的平均股價沒有顯著影響"""

df_combined['avg_price_change_5d'] = df_combined[['price_change_day_1','price_change_day_2', 'price_change_day_3', 'price_change_day_4', 'price_change_day_5']].mean(axis=1)


# 使用.loc[]來避免SettingWithCopyWarning
df_high_buy = df_combined[df_combined['buy_ratio'] >= 0.02].copy()
df_high_buy.loc[:, 'avg_price_change_5d'] = (df_high_buy[['price_change_day_1','price_change_day_2', 'price_change_day_3', 'price_change_day_4', 'price_change_day_5']].sum(axis=1)) / 5

# 繪製buy_ratio大於2%的scatter plot
plot_with_regression(df_high_buy['buy_ratio'], df_high_buy['price_change_day_1'], 'Buy Ratio >= 2% vs Next Day Price Change Percentage', 'blue')
plot_with_regression(df_high_buy['buy_ratio'], df_high_buy['price_change_day_2'], 'Buy Ratio >= 2% vs Day 2 Price Change Percentage', 'green')
plot_with_regression(df_high_buy['buy_ratio'], df_high_buy['price_change_day_3'], 'Buy Ratio >= 2% vs Day 3 Price Change Percentage', 'red')
plot_with_regression(df_high_buy['buy_ratio'], df_high_buy['price_change_day_4'], 'Buy Ratio >= 2% vs Day 4 Price Change Percentage', 'cyan')
plot_with_regression(df_high_buy['buy_ratio'], df_high_buy['price_change_day_5'], 'Buy Ratio >= 2% vs Day 5 Price Change Percentage', 'magenta')

df_combined

# 提取兩組數據：買進比例大於等於２% 的樣本和所有樣本
group1 = df_high_buy['avg_price_change_5d']
group2 = df_combined['avg_price_change_5d']

# 列出樣本數
group1_count = len(group1)
group2_count = len(group2)
print("買進比例大於等於 2% 的樣本數:", group1_count)
print("所有樣本數:", group2_count)

# 進行t檢定
t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=False)
print("虛無假設（H0）：當凱基松山這間券商買進量佔當天總成交量的 2% 以上時，對該股票 T0 到 T+1/T+2/T+3/T+4/T+5 的平均股價漲幅(%) 沒有顯著影響 (Beta = 0)")
print("t統計量:", t_stat)
print("p值:", p_value)

"""解讀結果
樣本數：
買進比例大於等於2%的樣本數為1719。
所有樣本的總數為72813。
t統計量：3.183073655332127

p值：0.0014817760048993428

結論
t統計量：這個值顯示兩組數據均值之間存在著一定的差異。在這種情況下，t統計量的值3.18表示有一定程度的差異。

p值：p值是觀察到的數據（或更極端情況）在零假設為真時發生的概率。這裡的p值為0.001481，這意味著如果零假設為真（即凱基松山買進量佔當天總成交量的2%以上時，對股票接下來五天的平均股價沒有顯著影響），則有0.14%的概率觀察到您的數據或更極端的結果。

由於p值（0.001481）小於一般的顯著性水平α = 0.05，拒絕H0零假設。這意味著有足夠的證據表明，當凱基松山的買進量佔當天總成交量的2%以上時，對股票接下來五天的平均股價有顯著影響

下面是根據12/27老師建議調整的
# New Approach
1. Define logBuyRatio = log(Buy Ratio) as the new explanatory variable
2. Show the scatter plot of the whole data
3. Do hypothesis of H_0: beta=0 vs H_1: beta\neq 0.
4. Try https://colab.research.google.com/drive/1HrDv6LrhkUxkAh1rVzD2n4xLaD_FcEvC?usp=sharing
"""

# 移除 Buy Ratio 為 0 的樣本
df_combined = df_combined[df_combined['buy_ratio'] > 0].copy()
# 計算 log(Buy Ratio)
df_combined['log_buy_ratio'] = np.log(df_combined['buy_ratio']+0.000000001)
# 去除含有NaN值的行
df_combined.dropna(subset=['price_change_day_1', 'price_change_day_2', 'price_change_day_3', 'price_change_day_4', 'price_change_day_5'], inplace=True)
# 繪製每一天的散點圖和回歸線
plot_with_regression(df_combined['log_buy_ratio'], df_combined['price_change_day_1'], 'Log Buy Ratio vs Next Day Price Change Percentage', 'blue')
plot_with_regression(df_combined['log_buy_ratio'], df_combined['price_change_day_2'], 'Log Buy Ratio vs Day 2 Price Change Percentage', 'green')
plot_with_regression(df_combined['log_buy_ratio'], df_combined['price_change_day_3'], 'Log Buy Ratio vs Day 3 Price Change Percentage', 'red')
plot_with_regression(df_combined['log_buy_ratio'], df_combined['price_change_day_4'], 'Log Buy Ratio vs Day 4 Price Change Percentage', 'cyan')
plot_with_regression(df_combined['log_buy_ratio'], df_combined['price_change_day_5'], 'Log Buy Ratio vs Day 5 Price Change Percentage', 'magenta')

#do hypothesis testing
from scipy import stats
import statsmodels.api as sm

# H0：log_buy_ratio 的回歸系數等於0，意味著 log_buy_ratio 對股價變動沒有影響。
# H1：log_buy_ratio 的回歸系數不等於0，意味著 log_buy_ratio 對股價變動有影響。

# Prepare x a and y for regression analysis
X = df_combined['log_buy_ratio']
Y = df_combined['avg_price_change_5d']

# Add constant to predictor variable
X = sm.add_constant(X)

# Fit linear regression model
model = sm.OLS(Y, X)
results = model.fit()

# Print regression parameters
print(results.summary())

"""檢視結果

回歸結果解讀
R-squared (R²)：0.000。這表明模型解釋的變異量非常小，log_buy_ratio 對 avg_price_change_5d 的解釋能力有限。

系數 (coef) for log_buy_ratio：0.0241。這意味著 log_buy_ratio 每增加一個單位，avg_price_change_5d 平均增加 0.0241 個百分點。

p 值 for log_buy_ratio：0.001。這個 p 值遠小於通常的顯著性水平（例如 0.05 或 0.01），這意味著我們可以拒絕零假設，認為 log_buy_ratio 對股價變動有顯著影響。

結論
線性回歸結果，有足夠的證據表明 log_buy_ratio 對股票接下來五天的平均股價變動有顯著影響。盡管影響的大小（系數）不大，但統計上是顯著的。

注意事項
模型解釋能力：雖然模型統計上顯著，但 R² 值非常低，說明 log_buy_ratio 變量對股價變動的解釋能力有限。可能還有其他未考慮的因素影響股價變動。

[github link](https://github.com/tw-lws/StockBrokerPriceCorrelation)

Restriction :
10 mins presentation
10 slides

1. Motivation

2. Data Visualization
3. 模型寫出來 (Model, H0) Formulation
4. 假設檢定六步驟
5. 結論

----
"""