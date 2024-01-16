# StockBrokerPriceCorrelation Repo介紹

本儲存庫（Repository）專注於從網路上收集和分析券商分點的進出資訊以及股價資料。本專案的目的在於探究券商交易行為與股價波動之間的相關性。透過自動化腳本抓取最新的市場數據，並運用統計學方法來分析數據，旨在為投資者和市場分析師提供更深入的市場洞察。本項目包含數據收集、預處理、統計分析等多個模塊，適合對股市數據分析有興趣的開發者和分析師使用和貢獻。

分析結果做為陽明交大112-1學期財金所碩士專班統計學期末專題報告使用

# 目錄 

- [StockBrokerPriceCorrelation Repo介紹](#stockbrokerpricecorrelation-repo介紹)
- [目錄](#目錄)
- [研究動機](#研究動機)
  - [簡報](#簡報)
  - [程式碼](#程式碼)
    - [資料清理以及統計分析請參考](#資料清理以及統計分析請參考)
    - [資料爬蟲程式](#資料爬蟲程式)
  - [此次研究所用的資料集](#此次研究所用的資料集)
  - [特點](#特點)
  - [專案結構](#專案結構)
  - [安裝與使用](#安裝與使用)
    - [雲端colab](#雲端colab)
    - [Local端安裝](#local端安裝)
    - [取得資料](#取得資料)
    - [直接從雲端硬碟下載現有資料並進行資料清理以及統計運算](#直接從雲端硬碟下載現有資料並進行資料清理以及統計運算)
  - [About Authors](#about-authors)



# 研究動機
常常會聽說台灣股市屬於淺碟型市場，胃納量不大，這導致中小型個股很容易受到特定大戶的行為而推動，若上述傳說為真，並且能找出大戶交易與個股股價的關係，或許就有機會設計成一套交易策略，讓我們可以跟著大戶的行為走，分一杯羹！
由於證交所有提供每日的各券商分點交易量，而坊間也流傳著許多股市大戶使用的分點，故我們可以由此來推測特定分點與個股走勢個關係，以此來驗證看看這些鄉野奇談是否屬實，或者能否捕捉到其他有趣的資訊。

## 簡報
[分析結果請參考此連結](https://docs.google.com/presentation/d/1xgA9WUcNeiToYA-dn7BfhoFJ0nH_cIyZJ6PIvseQizs/edit#slide=id.p)
或者點開Repo內的`統計簡報-Final Project_StockBrokerPriceCorrelation_劉緯軒_劉岳樺.pptx`檔案

## 程式碼
### 資料清理以及統計分析請參考

- `BrokerAndPriceCorrelation.py`: 進行數據整理以及統計分析之腳本，並產出結果(Python Script)
- `BrokerAndPriceCorrelation.ipynb`: 進行數據整理以及統計分析之腳本，並產出結果(Notebook)
兩個執行結果是一樣的，僅呈現方式不同

### 資料爬蟲程式
請參考[專案結構](#專案結構)

## 此次研究所用的資料集
因為此研究所使用的資料過大，github不讓上傳過大的檔案，故將資料的下載直接寫在BrokerAndPriceCorrelation內
***會直接從雲端硬碟下載需要的資料***，不需要手動下載

***若是不想另外從Finmind下載資料，可以使用我們上述分析時使用的資料，可安裝完需要的套件後直接執行`BrokerAndPriceCorrelation.ipynb`檔案***



## 特點

- **數據收集**：自動化從 FinMind API 抓取最新的券商分點交易和股價資料。
- **資料處理**：對收集到的原始數據進行清洗和預處理，以便於分析。
- **統計分析**：應用統計方法來分析券商行為與股價之間的關聯。
- **視覺化**：生成圖表和報告，以視覺化方式呈現分析結果。

## 專案結構

- `BrokerAndPriceCorrelation.py`: 進行數據整理以及統計分析之腳本，並產出結果(Python Script)
- `BrokerAndPriceCorrelation.ipynb`: 進行數據整理以及統計分析之腳本，並產出結果(Notebook)
- `data_fetching`：包含數據抓取相關的腳本。
- `data_storage`：負責數據存儲和檔案管理。 但是因為github不讓上傳這麼大的CSV故缺少部分資料，可使用BrokerAndPriceCorrelation.py檔案裡面的連結
- `data_analysis`：進行數據分析和處理的模塊。
- `visualization`：用於數據視覺化的腳本。
- `config`：存儲配置檔案，如 API 金鑰。
- `main.py`：從Finmind抓取資料時的主要執行檔案。

## 安裝與使用

### 雲端colab
請前往[Google Colab](https://colab.research.google.com/drive/1EXgX96hCyUnJPUcVNC5o-M2NoZ28ivBC#scrollTo=BkqEIJXjGD_i)

### Local端安裝

1. 安裝 Python 和虛擬環境：
   ```bash
   pyenv install 3.10.13
   python -m venv venv
   ```

2. 啟動虛擬環境並安裝依賴：
   ```bash
   source venv/bin/activate  # 在 Unix 或 MacOS 上 or
   . venv\\Scripts\\activate     # 在 Windows 上
   pip install -r requirements.txt
   ```

### 取得資料
***若要使用爬蟲幫忙抓取資料請進行步驟`3,4`否則可跳過此步驟直接去`5,6`可直接從雲端抓取準備好的資料集來做分析***

3. 設定環境變量：
   在 `config` 資料夾中新增 `.env` 檔案，並添加您的 FinMind API 金鑰：
   ```
   FINMIND_API_KEY=xxxxxxx
   ```

4. 使用爬蟲抓取資料


執行 `main.py` 來開始從Finmind下載數據，並將資料儲存在data內：
```bash
python main.py
```

### 直接從雲端硬碟下載現有資料並進行資料清理以及統計運算
***步驟5, 6擇一即可***

5. 執行 `BrokerAndPriceCorrelation.py` 來自動下載和分析數據並且產出結果：
```bash
python BrokerAndPriceCorrelation.py
```

6. 或者使用jupyter notebbok
執行 `BrokerAndPriceCorrelation.ipynb` 來下載跟分析數據，並且產出結果


## About Authors
[Steven Liu](https://github.com/tw-lws) and [Yuehua-Liu](https://github.com/Yuehua-Liu)

指導教授: [Huei-Wen Teng](https://hackmd.io/@hwteng/HyKOPoA6d)
