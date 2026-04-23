from flask import Blueprint, render_template, request
from app.models.record import RecordModel
from app.models.category import CategoryModel
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    儀表板/首頁。
    取得當月總收入、支出、結餘，分類統計圖表資料，以及近期的收支紀錄。
    """
    records = RecordModel.get_all()
    
    # 取得當前月份字串 YYYY-MM
    current_month = datetime.now().strftime('%Y-%m')
    
    # 過濾當月紀錄
    monthly_records = [r for r in records if r['date'].startswith(current_month)]
    
    total_income = sum(r['amount'] for r in monthly_records if r['type'] == 'income')
    total_expense = sum(r['amount'] for r in monthly_records if r['type'] == 'expense')
    balance = total_income - total_expense
    
    # 計算各分類支出，供圖表使用
    category_expenses = {}
    for r in monthly_records:
        if r['type'] == 'expense':
            cat = r['category_name'] or '未分類'
            category_expenses[cat] = category_expenses.get(cat, 0) + r['amount']
            
    # 近期 5 筆紀錄
    recent_records = records[:5]
    
    return render_template('index.html', 
                           total_income=total_income,
                           total_expense=total_expense,
                           balance=balance,
                           category_expenses=category_expenses,
                           recent_records=recent_records,
                           current_month=current_month)
