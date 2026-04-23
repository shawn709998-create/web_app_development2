# 路由設計文件：個人記帳簿系統

本文件基於 PRD 與架構設計，規劃 Flask 應用程式的所有路由、對應的視圖函式與 Jinja2 模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| **儀表板/首頁** | GET | `/` | `index.html` | 顯示當月總收支、餘額統計、近期紀錄及收支圓餅圖 |
| **紀錄列表** | GET | `/records` | `records/index.html` | 顯示歷史收支紀錄列表，支援日期與分類篩選 |
| **新增紀錄頁面** | GET | `/records/new` | `records/form.html` | 顯示新增一筆收支紀錄的表單 |
| **建立紀錄** | POST | `/records` | — | 接收新增表單資料，寫入 DB，重導向至首頁或列表頁 |
| **編輯紀錄頁面** | GET | `/records/<id>/edit` | `records/form.html` | 顯示修改該筆紀錄的表單 (帶入現有資料) |
| **更新紀錄** | POST | `/records/<id>/update` | — | 接收更新表單資料，修改 DB，重導向至列表頁 |
| **刪除紀錄** | POST | `/records/<id>/delete` | — | 將特定紀錄從 DB 刪除，重導向至列表頁 |
| **分類列表** | GET | `/categories` | `categories/index.html` | 顯示系統內建與使用者自訂的收支分類 |
| **新增分類頁面** | GET | `/categories/new` | `categories/form.html` | 顯示新增自訂分類的表單 |
| **建立分類** | POST | `/categories` | — | 接收新增分類資料，寫入 DB，重導向至分類列表 |
| **編輯分類頁面** | GET | `/categories/<id>/edit` | `categories/form.html` | 顯示編輯自訂分類的表單 |
| **更新分類** | POST | `/categories/<id>/update` | — | 接收更新分類資料，修改 DB，重導向至分類列表 |
| **刪除分類** | POST | `/categories/<id>/delete` | — | 將自訂分類從 DB 刪除，重導向至分類列表 |
| **預算列表與設定** | GET | `/budgets` | `budgets/index.html` | 顯示每月預算清單與設定預算的表單 |
| **儲存預算** | POST | `/budgets` | — | 接收預算設定，寫入或更新 DB，重導向至預算列表 |

## 2. 每個路由的詳細說明

### 儀表板 (Blueprint: `main`)
- **GET `/`**
  - 輸入：無
  - 處理邏輯：計算當月總收入與支出、剩餘金額。取得圓餅圖所需的分類統計資料。取得最近的 5 筆紀錄。
  - 輸出：渲染 `index.html`
  - 錯誤處理：若資料庫連線失敗顯示 500 錯誤。

### 收支紀錄 (Blueprint: `record`)
- **GET `/records`**
  - 輸入：URL 參數 `month`, `category_id`, `keyword` (用於篩選)
  - 處理邏輯：根據參數呼叫 Model 取得篩選後的紀錄列表。
  - 輸出：渲染 `records/index.html`
- **GET `/records/new`**
  - 輸入：無
  - 處理邏輯：取得所有分類列表供下拉選單使用。
  - 輸出：渲染 `records/form.html`
- **POST `/records`**
  - 輸入：表單欄位 `amount`, `type`, `date`, `category_id`, `note`
  - 處理邏輯：驗證金額與必填欄位。呼叫 `RecordModel.create()`。檢查是否超支並設定 Flash 訊息。
  - 輸出：重導向至 `/`
  - 錯誤處理：資料驗證失敗則渲染 `records/form.html` 並顯示錯誤訊息。
- **POST `/records/<id>/delete`**
  - 輸入：URL 參數 `id`
  - 處理邏輯：呼叫 `RecordModel.delete(id)`
  - 輸出：重導向至 `/records`

### 分類管理 (Blueprint: `category`)
- **GET `/categories`**
  - 處理邏輯：取得所有內建與自訂分類。
  - 輸出：渲染 `categories/index.html`
- **POST `/categories`**
  - 輸入：表單欄位 `name`, `type`
  - 處理邏輯：呼叫 `CategoryModel.create()`。
  - 輸出：重導向至 `/categories`

### 預算設定 (Blueprint: `budget`)
- **GET `/budgets`**
  - 處理邏輯：取得歷史與當前月份預算設定。
  - 輸出：渲染 `budgets/index.html`
- **POST `/budgets`**
  - 輸入：表單欄位 `month`, `amount`, `category_id` (選填)
  - 處理邏輯：呼叫 `BudgetModel.create()` 或 `update()`。
  - 輸出：重導向至 `/budgets`

## 3. Jinja2 模板清單

所有模板皆預計位於 `app/templates/` 目錄下：

- `base.html`：**基礎版型**。包含共用字體、CSS 引入、頂部導覽列 (Navbar) 與 Flash 訊息顯示區塊。以下所有頁面皆繼承此模板 (`{% extends "base.html" %}`)。
- `index.html`：儀表板頁面。
- `records/index.html`：紀錄列表頁面。
- `records/form.html`：共用的新增/編輯紀錄表單。
- `categories/index.html`：分類列表頁面。
- `categories/form.html`：共用的新增/編輯分類表單。
- `budgets/index.html`：預算列表與設定頁面。

## 4. 路由骨架程式碼
已在 `app/routes/` 中建立各模組檔案，包含使用 Flask Blueprint 的骨架。
