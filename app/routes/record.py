from flask import Blueprint, render_template, request, redirect, url_for, flash

record_bp = Blueprint('record', __name__, url_prefix='/records')

@record_bp.route('/')
def index():
    """
    顯示所有歷史收支紀錄列表，並支援日期區間、分類篩選。
    """
    pass

@record_bp.route('/new', methods=['GET'])
def new():
    """
    顯示新增收支紀錄的表單頁面。
    """
    pass

@record_bp.route('/', methods=['POST'])
def create():
    """
    接收新增表單資料，驗證後寫入資料庫，並檢查是否超出預算，然後重導向至首頁或列表頁。
    """
    pass

@record_bp.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    """
    顯示編輯收支紀錄的表單頁面，帶入現有紀錄資料。
    """
    pass

@record_bp.route('/<int:id>/update', methods=['POST'])
def update(id):
    """
    接收更新表單資料，更新資料庫後重導向至紀錄列表。
    """
    pass

@record_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    從資料庫刪除指定紀錄，然後重導向至紀錄列表。
    """
    pass
