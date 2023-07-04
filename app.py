from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/home')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/', methods=['GET', 'POST'])
def index():  # put application's code here
    # Get the search query from the form
    search_query = request.form.get('search_query')

    # Replace with your actual data
    import pandas as pd
    DS_PATH = '/Users/colin/Library/Mobile Documents/com~apple~CloudDocs/PycharmProjects/Chat-Analysis/DataSets/2023-Escort'
    df = pd.read_csv(f'{DS_PATH}/天空猫的树洞/user_info/user_card.csv')
    df = df.rename(
            columns={'info_0': 'user_grade', 'info_2': 'user_name', 'info_4': 'user_service', 'info_5': 'user_position',
                     'info_6': 'user_tag',
                     'info_7': 'user_profile', 'audio_url': 'user_audio_url'})
    df = df.filter(regex=r'^(?!gift_|info_)', axis=1)

    # 搜索框
    if search_query:
        # 寻找df列user_name,user_service,user_position,user_tag,user_profile列中包含搜索框内容的行
        df = df[df.apply(lambda x: x.str.contains(search_query, case=False).any(), axis=1)]

    users = df.to_dict('records')
    for user in users: user['user_image_paths'] = [user.pop(f'img_{i}') for i in range(5)]

    # 分页
    # Get the page number from the URL parameters (default to 1 if not present)
    page = request.args.get('page', 1, type=int)
    users_per_page = 20
    # Calculate the start and end indices for the slice of users to display
    start = (page - 1) * users_per_page
    end = start + users_per_page

    # Get the slice of users to display
    users_to_display = users[start:end]
    # Calculate the total number of pages
    total_pages = len(users) // users_per_page
    if len(users) % users_per_page != 0:
        total_pages += 1

    return render_template('index.html', users=users_to_display, page=page, users_per_page=users_per_page, total_pages=total_pages)


# http://192.168.3.29:5000
if __name__ == '__main__':
    app.run()
