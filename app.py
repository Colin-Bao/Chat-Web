from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)


# 将数据导入和处理封装成一个函数
def load_and_process_data(search_query=None):
    # 获取当前文件所在的目录
    # ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../"))
    # DS_PATH = f'{ROOT_PATH}/DataSets/2023-Escort'
    df = pd.read_csv(f'/home/ubuntu/PycharmProjects/Chat-Analysis/DataSets/2023-Escort/dbs/user_card_all.csv')

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
