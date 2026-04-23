from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.budget import BudgetModel
from datetime import datetime

budget_bp = Blueprint('budget', __name__, url_prefix='/budgets')

@budget_bp.route('/')
def index():
    """
    顯示每月預算清單與設定預算的表單。
    """
    budgets = BudgetModel.get_all()
    current_month = datetime.now().strftime('%Y-%m')
    current_budgets = BudgetModel.get_by_month(current_month)
    return render_template('budgets/index.html', budgets=budgets, current_budgets=current_budgets)

@budget_bp.route('/', methods=['POST'])
def save():
    """
    接收預算設定表單，儲存至資料庫後重導向至預算列表。
    支援新增或更新當月預算。
    """
    month = request.form.get('month')
    amount_str = request.form.get('amount')
    
    if not month or not amount_str:
        flash('月份與預算金額為必填欄位', 'error')
        return redirect(url_for('budget.index'))
        
    try:
        amount = float(amount_str)
    except ValueError:
        flash('預算金額格式錯誤', 'error')
        return redirect(url_for('budget.index'))
        
    existing_budgets = BudgetModel.get_by_month(month)
    if existing_budgets:
        # 如果該月總預算已存在，則更新第一筆
        success = BudgetModel.update(existing_budgets[0]['id'], amount)
        if success:
            flash('預算更新成功', 'success')
        else:
            flash('預算更新失敗', 'error')
    else:
        result = BudgetModel.create(month, amount)
        if result:
            flash('預算設定成功', 'success')
        else:
            flash('預算設定失敗', 'error')
            
    return redirect(url_for('budget.index'))
