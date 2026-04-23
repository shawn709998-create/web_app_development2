# 流程圖文件：個人記帳簿系統

本文件根據 `docs/PRD.md` 與 `docs/ARCHITECTURE.md` 規劃了個人記帳簿系統的使用者操作路徑（User Flow）與系統資料流（Sequence Diagram）。

## 1. 使用者流程圖 (User Flow)

這張圖展示了使用者進入系統後，可以進行的各種操作路徑，涵蓋了主要功能如記帳、查看圖表、管理分類與預算。

```mermaid
flowchart LR
    Start([使用者開啟網頁]) --> Home[首頁 / 儀表板]
    
    Home --> Action{要執行什麼操作？}
    
    %% 記錄收入與支出
    Action -->|新增紀錄| AddRecord[點擊新增收支]
    AddRecord --> Form[填寫金額、日期、分類、備註]
    Form --> SubmitRecord[送出表單]
    SubmitRecord --> Home
    
    %% 顯示餘額與圖表分析
    Action -->|查看圖表| ViewChart[檢視當月收支比例與趨勢]
    ViewChart --> Home
    
    %% 查詢與篩選
    Action -->|查詢歷史紀錄| ViewHistory[進入紀錄列表頁]
    ViewHistory --> Filter[設定日期區間、分類或關鍵字]
    Filter --> FilteredList[顯示篩選後的紀錄列表]
    FilteredList --> EditDel{編輯或刪除？}
    EditDel -->|編輯| EditForm[修改紀錄內容]
    EditForm --> SubmitEdit[儲存修改]
    SubmitEdit --> FilteredList
    EditDel -->|刪除| DeleteConfirm[確認刪除]
    DeleteConfirm --> FilteredList
    FilteredList --> Home
    
    %% 分類管理
    Action -->|管理分類| ManageCategory[進入分類設定頁]
    ManageCategory --> AddCategory[新增自訂分類]
    ManageCategory --> EditCategory[編輯現有分類]
    ManageCategory --> DeleteCategory[刪除分類]
    AddCategory --> ManageCategory
    EditCategory --> ManageCategory
    DeleteCategory --> ManageCategory
    ManageCategory --> Home
    
    %% 預算設定
    Action -->|設定預算| ManageBudget[進入預算設定頁]
    ManageBudget --> SetBudget[設定每月總預算或分類預算]
    SetBudget --> ManageBudget
    ManageBudget --> Home
```

## 2. 系統序列圖 (Sequence Diagram)

這張圖描述了「使用者點擊新增一筆收支紀錄」到「資料成功存入資料庫」並返回頁面的完整流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (HTML/JS)
    participant Flask as Flask Route (Controller)
    participant Model as Database Model
    participant DB as SQLite

    User->>Browser: 填寫收支表單並點擊「儲存」
    Browser->>Flask: POST /record/add (傳遞表單資料)
    
    Note over Flask: 驗證資料 (如必填欄位、金額格式)
    
    alt 資料驗證失敗
        Flask-->>Browser: 回傳錯誤訊息與原表單
        Browser-->>User: 畫面顯示「請填寫正確資料」
    else 資料驗證成功
        Flask->>Model: 呼叫 Record.create(...)
        Model->>DB: 執行 SQL INSERT 語法
        DB-->>Model: 寫入成功
        Model-->>Flask: 回傳新建立的紀錄 ID
        
        Note over Flask: 檢查是否超支 (預算提醒)
        Flask->>Model: 查詢當月總支出與預算
        Model->>DB: SELECT 總支出, 預算
        DB-->>Model: 回傳金額
        Model-->>Flask: 回傳金額
        
        alt 目前支出 > 預算
            Flask->>Flask: 設定 Flash Message：「已超過本月預算！」
        end
        
        Flask-->>Browser: 重導向 (Redirect) 至首頁
        Browser->>Flask: GET /
        Flask->>Model: 取得首頁所需資料
        Model->>DB: SELECT...
        DB-->>Model: 回傳資料
        Model-->>Flask: 回傳資料
        Flask-->>Browser: 回傳渲染後的 HTML
        Browser-->>User: 顯示更新後的儀表板與餘額
    end
```

## 3. 功能清單對照表

以下為 PRD 中定義的主要功能，其預估對應的 URL 路徑與 HTTP 方法：

| 功能項目 | 頁面/操作說明 | HTTP 方法 | URL 路徑預估 |
| --- | --- | --- | --- |
| **首頁與餘額統計** | 顯示儀表板、總收支、剩餘金額 | GET | `/` |
| **圖表分析** | 顯示收支圓餅圖與折線圖 (可整合於首頁) | GET | `/` 或 `/dashboard` |
| **新增紀錄** | 顯示新增表單頁面 | GET | `/record/add` |
| **儲存新紀錄** | 處理表單送出並寫入資料庫 | POST | `/record/add` |
| **查詢與篩選紀錄** | 顯示歷史紀錄列表並支援條件篩選 | GET | `/records` |
| **編輯紀錄** | 顯示編輯表單頁面 | GET | `/record/edit/<id>` |
| **儲存編輯紀錄** | 處理修改內容並更新資料庫 | POST | `/record/edit/<id>` |
| **刪除紀錄** | 刪除特定一筆紀錄 | POST | `/record/delete/<id>` |
| **分類管理列表** | 顯示內建與自訂分類 | GET | `/categories` |
| **新增/編輯分類** | 處理新增或修改分類 | POST | `/category/save` |
| **預算設定** | 顯示與修改每月預算 | GET / POST | `/budget` |
