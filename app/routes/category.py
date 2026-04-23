from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.category import CategoryModel

category_bp = Blueprint('category', __name__, url_prefix='/categories')

@category_bp.route('/')
def index():
    """
    顯示所有分類列表 (包含內建與自訂分類)。
    """
    categories = CategoryModel.get_all()
    return render_template('categories/index.html', categories=categories)

@category_bp.route('/new', methods=['GET'])
def new():
    """
    顯示新增自訂分類的表單頁面。
    """
    return render_template('categories/form.html', category=None)

@category_bp.route('/', methods=['POST'])
def create():
    """
    接收新增分類表單資料，寫入資料庫後重導向至分類列表。
    """
    name = request.form.get('name')
    type = request.form.get('type')
    
    if not name or not type:
        flash('分類名稱與屬性為必填欄位', 'error')
        return redirect(url_for('category.new'))
        
    result = CategoryModel.create(name, type, is_default=False)
    if result:
        flash('分類新增成功', 'success')
    else:
        flash('分類新增失敗', 'error')
        
    return redirect(url_for('category.index'))

@category_bp.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    """
    顯示編輯自訂分類的表單頁面。
    """
    category = CategoryModel.get_by_id(id)
    if not category:
        flash('找不到該分類', 'error')
        return redirect(url_for('category.index'))
    if category['is_default']:
        flash('內建分類不可編輯', 'error')
        return redirect(url_for('category.index'))
        
    return render_template('categories/form.html', category=category)

@category_bp.route('/<int:id>/update', methods=['POST'])
def update(id):
    """
    接收更新分類表單資料，更新資料庫後重導向至分類列表。
    """
    name = request.form.get('name')
    type = request.form.get('type')
    
    if not name or not type:
        flash('分類名稱與屬性為必填欄位', 'error')
        return redirect(url_for('category.edit', id=id))
        
    success = CategoryModel.update(id, name, type)
    if success:
        flash('分類更新成功', 'success')
    else:
        flash('分類更新失敗 (可能為內建分類)', 'error')
        
    return redirect(url_for('category.index'))

@category_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除指定的自訂分類，然後重導向至分類列表。
    """
    success = CategoryModel.delete(id)
    if success:
        flash('分類刪除成功', 'success')
    else:
        flash('分類刪除失敗 (可能為內建分類或已被使用)', 'error')
        
    return redirect(url_for('category.index'))
