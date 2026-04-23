from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.record import RecordModel
from app.models.category import CategoryModel
from app.models.budget import BudgetModel
from datetime import datetime

record_bp = Blueprint('record', __name__, url_prefix='/records')

@record_bp.route('/')
def index():
    """
    顯示所有歷史收支紀錄列表，並支援日期區間、分類篩選。
    """
    records = RecordModel.get_all()
    categories = CategoryModel.get_all()
    
    month_filter = request.args.get('month')
    category_filter = request.args.get('category_id')
    
    if month_filter:
        records = [r for r in records if r['date'].startswith(month_filter)]
    if category_filter and category_filter.isdigit():
        records = [r for r in records if r['category_id'] == int(category_filter)]
        
    return render_template('records/index.html', records=records, categories=categories)

@record_bp.route('/new', methods=['GET'])
def new():
    """
    顯示新增收支紀錄的表單頁面。
    """
    categories = CategoryModel.get_all()
    return render_template('records/form.html', record=None, categories=categories)

@record_bp.route('/', methods=['POST'])
def create():
    """
    接收新增表單資料，驗證後寫入資料庫，並檢查是否超出預算，然後重導向至首頁。
    """
    amount_str = request.form.get('amount')
    type = request.form.get('type')
    date = request.form.get('date')
    category_id_str = request.form.get('category_id')
    note = request.form.get('note', '')
    
    if not amount_str or not type or not date or not category_id_str:
        flash('請填寫所有必填欄位', 'error')
        return redirect(url_for('record.new'))
        
    try:
        amount = float(amount_str)
        category_id = int(category_id_str)
    except ValueError:
        flash('金額或分類格式錯誤', 'error')
        return redirect(url_for('record.new'))
        
    result = RecordModel.create(amount, type, date, note, category_id)
    
    if result:
        flash('紀錄新增成功', 'success')
        
        # 檢查預算是否超支 (如果這是一筆支出)
        if type == 'expense':
            month = date[:7] # YYYY-MM
            budgets = BudgetModel.get_by_month(month)
            if budgets:
                budget_amount = budgets[0]['amount']
                # 計算當月總支出
                all_records = RecordModel.get_all()
                monthly_expenses = sum(r['amount'] for r in all_records if r['type'] == 'expense' and r['date'].startswith(month))
                
                if monthly_expenses > budget_amount:
                    flash(f'注意：本月總支出 ({monthly_expenses}) 已超過預算 ({budget_amount})！', 'warning')
                    
    else:
        flash('紀錄新增失敗', 'error')
        
    return redirect(url_for('main.index'))

@record_bp.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    """
    顯示編輯收支紀錄的表單頁面，帶入現有紀錄資料。
    """
    record = RecordModel.get_by_id(id)
    if not record:
        flash('找不到該紀錄', 'error')
        return redirect(url_for('record.index'))
        
    categories = CategoryModel.get_all()
    return render_template('records/form.html', record=record, categories=categories)

@record_bp.route('/<int:id>/update', methods=['POST'])
def update(id):
    """
    接收更新表單資料，更新資料庫後重導向至紀錄列表。
    """
    amount_str = request.form.get('amount')
    type = request.form.get('type')
    date = request.form.get('date')
    category_id_str = request.form.get('category_id')
    note = request.form.get('note', '')
    
    if not amount_str or not type or not date or not category_id_str:
        flash('請填寫所有必填欄位', 'error')
        return redirect(url_for('record.edit', id=id))
        
    try:
        amount = float(amount_str)
        category_id = int(category_id_str)
    except ValueError:
        flash('金額或分類格式錯誤', 'error')
        return redirect(url_for('record.edit', id=id))
        
    success = RecordModel.update(id, amount, type, date, note, category_id)
    if success:
        flash('紀錄更新成功', 'success')
    else:
        flash('紀錄更新失敗', 'error')
        
    return redirect(url_for('record.index'))

@record_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    從資料庫刪除指定紀錄，然後重導向至紀錄列表。
    """
    success = RecordModel.delete(id)
    if success:
        flash('紀錄刪除成功', 'success')
    else:
        flash('紀錄刪除失敗', 'error')
        
    return redirect(url_for('record.index'))
