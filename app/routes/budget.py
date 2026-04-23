from flask import Blueprint, render_template, request, redirect, url_for, flash

budget_bp = Blueprint('budget', __name__, url_prefix='/budgets')

@budget_bp.route('/')
def index():
    """
    顯示每月預算清單與設定預算的表單。
    """
    pass

@budget_bp.route('/', methods=['POST'])
def save():
    """
    接收預算設定表單，儲存至資料庫後重導向至預算列表。
    支援新增或更新。
    """
    pass
