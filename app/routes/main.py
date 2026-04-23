from flask import Blueprint, render_template, request

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    儀表板/首頁。
    取得當月總收入、支出、結餘，分類統計圖表資料，以及近期的收支紀錄。
    """
    pass
