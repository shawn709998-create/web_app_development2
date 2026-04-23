from flask import Blueprint, render_template, request, redirect, url_for, flash

category_bp = Blueprint('category', __name__, url_prefix='/categories')

@category_bp.route('/')
def index():
    """
    顯示所有分類列表 (包含內建與自訂分類)。
    """
    pass

@category_bp.route('/new', methods=['GET'])
def new():
    """
    顯示新增自訂分類的表單頁面。
    """
    pass

@category_bp.route('/', methods=['POST'])
def create():
    """
    接收新增分類表單資料，寫入資料庫後重導向至分類列表。
    """
    pass

@category_bp.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    """
    顯示編輯自訂分類的表單頁面。
    """
    pass

@category_bp.route('/<int:id>/update', methods=['POST'])
def update(id):
    """
    接收更新分類表單資料，更新資料庫後重導向至分類列表。
    """
    pass

@category_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除指定的自訂分類，然後重導向至分類列表。
    """
    pass
