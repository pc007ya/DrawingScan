# 📐 FAI 工程圖面自動化辨識系統 (完全開源版)

本項目基於 `PaddleOCR` 與 `Flask`，實現不依賴第三方付費 API 的本地化安全 FAI（首件檢查）圖面數據提取。

## 🚀 快速啟動本地 Web 端

1. **安裝系統環境依賴 (Poppler)**：
   - **Mac**: `brew install poppler`
   - **Linux**: `sudo apt-get install poppler-utils`
   - **Windows**: 下載 poppler 壓縮包並配置其 `bin` 目錄至環境變數。

2. **安裝 Python 依賴套件**：
   ```bash
   pip install -r requirements.txt