from flask import Flask, render_template, request
import pandas as pd
from faker import Faker
import os
import sys

# 导入自定义包
sys.path.append('/home/ubuntu/PycharmProjects/Chat-Analysis/ScrapySpider/playwright_spider')
from config import sqlalchemy_uri  # noqa


app = Flask(__name__)


# 将数据导入和处理封装成一个函数
def load_and_process_data(search_query=None):
    # 获取当前文件所在的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data', 'user_clean.csv')
    df = pd.read_csv(file_path)

    # 指定需要查找的列
    columns_to_search = ['name', 'Profile', 'tag']
    target_string = '萝'

    # 使用 apply 和 str.contains 来对指定列进行查找
    df = df[df[columns_to_search].apply(lambda col: col.astype(str).str.contains(target_string, na=False)).any(axis=1)].sort_values(by='rank', ascending=False)

    # 搜索框
    if search_query:
        # 寻找df列user_name,user_service,user_position,user_tag,user_profile列中包含搜索框内容的行
        df = df[df.apply(lambda x: x.str.contains(search_query, case=False).any(), axis=1)]

    # 转为字典
    users = df.to_dict('records')
    return users


# 创建一个分页功能的函数
def paginate(data, page, per_page=30, page_display=15):
    start = (page - 1) * per_page
    end = start + per_page

    data_to_display = data[start:end]

    total_pages = len(data) // per_page
    if len(data) % per_page != 0:
        total_pages += 1

    half_display = page_display // 2
    if page - half_display <= 0:
        page_range = list(range(1, min(page_display + 1, total_pages + 1)))
    elif page + half_display > total_pages:
        page_range = list(range(max(1, total_pages - page_display + 1), total_pages + 1))
    else:
        page_range = list(range(page - half_display, page + half_display + 1))

    return {'items': data_to_display, 'total_pages': total_pages, 'page': page, 'page_range': page_range}


@app.route('/old', methods=['GET', 'POST'])
def index_old():
    # Get the search query from the form
    search_query = request.form.get('search_query')

    # 导入数据
    users = load_and_process_data(search_query)

    # 分页
    # Get the page number from the URL parameters (default to 1 if not present)
    page = request.args.get('page', 1, type=int)

    # Use paginate function to get the users to display and total pages
    pagination_info = paginate(users, page, 30, 10)
    return render_template('index.html', users=pagination_info['items'], **pagination_info)


def create_fake():
    fake = Faker('zh_CN')
    # 随机创建100个员工列表
    users = [{'img': fake.image_url(), 'name': fake.name(), 'position': fake.city(), 'tag': fake.job(), 'profile': fake.address(),
              'service': fake.company()} for _ in range(10)]
    return users


@app.route('/', methods=['GET', 'POST'])
def index():
    # Get the search query from the form
    search_query = request.form.get('search_query')

    # 导入数据
    users = load_and_process_data(search_query)

    # 分页
    # Get the page number from the URL parameters (default to 1 if not present)
    page = request.args.get('page', 1, type=int)

    # Use paginate function to get the users to display and total pages
    pagination_info = paginate(users, page, 30, 10)

    return render_template('index.html', users=pagination_info['items'], **pagination_info)


if __name__ == '__main__':
    app.run()
