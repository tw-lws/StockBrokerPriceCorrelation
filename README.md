# StockBrokerPriceCorrelation

本儲存庫（Repository）專注於從網路上收集和分析券商分點的進出資訊以及股價資料。本專案的目的在於探究券商交易行為與股價波動之間的相關性。透過自動化腳本抓取最新的市場數據，並運用統計學方法來分析數據，旨在為投資者和市場分析師提供更深入的市場洞察。本項目包含數據收集、預處理、統計分析以及視覺化展示等多個模塊，適合對股市數據分析有興趣的開發者和分析師使用和貢獻。

## 特點

- **數據收集**：自動化從 FinMind API 抓取最新的券商分點交易和股價資料。
- **資料處理**：對收集到的原始數據進行清洗和預處理，以便於分析。
- **統計分析**：應用統計方法來分析券商行為與股價之間的關聯。
- **視覺化**：生成圖表和報告，以視覺化方式呈現分析結果。

## 專案結構

- `data_fetching`：包含數據抓取相關的腳本。
- `data_storage`：負責數據存儲和檔案管理。
- `data_analysis`：進行數據分析和處理的模塊。
- `visualization`：用於數據視覺化的腳本。
- `config`：存儲配置檔案，如 API 金鑰。
- `main.py`：專案的主要執行檔案。

## 安裝與使用

### 安裝

1. 安裝 Python 和虛擬環境：
   ```bash
   pyenv install 3.10.13
   python -m venv venv
   ```

2. 啟動虛擬環境並安裝依賴：
   ```bash
   source venv/bin/activate  # 在 Unix 或 MacOS 上
   venv\\Scripts\\activate     # 在 Windows 上
   pip install -r requirements.txt
   ```

3. 設定環境變量：
   在 `config` 資料夾中新增 `.env` 檔案，並添加您的 FinMind API 金鑰：
   ```
   FINMIND_API_KEY=xxxxxxx
   ```

### 使用

執行 `main.py` 來開始收集和分析數據：
```bash
python main.py
```