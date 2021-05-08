from flask import Flask, request, jsonify, redirect
import sys
import os
import pickle
import uuid
import codecs
from datetime import datetime, timedelta

from googleapiclient.errors import HttpError

from gs_sdk.gs_admin import GS_Admin
from gs_sdk.credentials_setup import Credentials_Setup

from db import GS_Config, Code

from config import CORS, \
    NO_BANNER, \
    USE_PYINSTALLER, \
    LOG_FILE

if NO_BANNER:
    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None

static_folder = 'static'
if USE_PYINSTALLER and \
        getattr(sys, 'frozen', False) and \
        hasattr(sys, '_MEIPASS'):
    static_folder = os.path.join(sys._MEIPASS, static_folder)
app = Flask(__name__, static_url_path='', static_folder=static_folder)

if CORS:
    from flask_cors import CORS

    CORS(app)

gs_config = GS_Config()
code = Code()


@app.route('/createUser', methods=['POST'])
def create_user():
    data = request.json

    try:
        if code.check(data['code']):
            gs = gs_config.get_gs(gs_id=data['institute'])

            for domain in gs['domains']:

                if domain['domain_display'] == data['email']['domain']:
                    primary_email = data['email']['username'] + '@' + domain['domain']

                    gs_admin = GS_Admin(
                        credentials=pickle.loads(
                            codecs.decode(gs['pickled'].encode(), 'base64')
                        )
                    )
                    account = gs_admin.create_user(
                        primary_email=primary_email,
                        given_name=data['email']['username'],
                        family_name=gs['name'],
                        org_unit_path=gs['org_unit_path']
                    )

                    do_log(
                        f"{(datetime.utcnow() + timedelta(hours=8)).strftime('%m/%d, %H:%M:%S')}: "
                        f"{data['code']} 激活了 {primary_email}"
                    )
                    code.delete(data['code'])

                    return jsonify({
                        'success': True,
                        'account': account
                    })

                else:
                    raise Exception('域名无效')

        else:
            raise Exception('激活码无效')

    except HttpError as e:
        if e.resp.status == 409:
            return jsonify({
                'success': False,
                'msg': '用户名已存在'
            })
        else:
            return jsonify({
                'success': False,
                'msg': f'{e}'
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'msg': f'{e}'
        })


@app.route('/getGSConfig', methods=['POST'])
def get_site_config():
    return jsonify(gs_config.get_gs_config())


@app.route('/', methods=['GET'])
def serve_html():
    return app.send_static_file('index.html')


@app.route('/static/js/<file>', methods=['GET'])
def serve_js(file):
    return app.send_static_file(f'static/js/{file}')


@app.route('/static/css/<file>', methods=['GET'])
def serve_css(file):
    return app.send_static_file(f'static/css/{file}')


@app.errorhandler(404)
def not_found(e):
    return redirect('/')


def do_log(line):
    open(LOG_FILE, 'a', encoding='utf-8').write(f'{line}\n')


def add_gs():
    email = input('\n请输入 GS 管理员账号邮箱: ').strip().lower()

    print(
        '\n1. 浏览器匿名模式打开网页 https://developers.google.com/admin-sdk/directory/v1/quickstart/python\n'
        '2. 登录你要添加的 GS 管理员账号\n'
        '3. 点击启用 Directory API 按钮，创建 Desktop 程序\n'
        '4. 把获得的 client_id 和 client_secret 复制粘贴到下方'
    )

    client_id = input('client_id: ').strip()
    client_secret = input('client_secret: ').strip()

    cs = Credentials_Setup()
    auth_url = cs.get_auth_url(
        client_id=client_id,
        client_secret=client_secret,
        scopes=['https://www.googleapis.com/auth/admin.directory.user']
    )

    print(
        f'\n5. 请在刚才的浏览器匿名模式中打开链接 {auth_url}\n'
        '6. 选择你的 GS 管理员账号并授权\n'
        '7. 将网页上显示的授权码粘贴在下方'
    )

    auth_code = input('授权码: ').strip()

    credentials = cs.get_credentials(auth_code=auth_code)

    pickled = codecs.encode(pickle.dumps(credentials), 'base64').decode()

    domains = []
    while True:
        domain = input('\n请输入此 GS 管理员域下你想用的域名 (不带 @，如 abc.edu): ').strip()
        domain_display = input('请输入你想在网页上显示的域名 (用来隐藏域名，如 *.edu): ').strip()

        domains.append({
            'domain': domain,
            'domain_display': domain_display,
        })

        if input('\n回车以继续添加域名，输入 n 将进入下一步: ') == 'n':
            break

    name = input('\n请输入你想在网页上显示的学校名称 (如 母鸡大学): ').strip()

    org_unit_path = input('\n请输入创建的 GS 子号的单位路径 (默认 /): ').strip()

    gs_config.add_gs({
        'email': email,
        'pickled': pickled,
        'domains': domains,
        'name': name,
        'org_unit_path': org_unit_path or '/',
        'id': str(uuid.uuid4()),
    })

    print('\nGS 添加成功')


def remove_gs():
    print()
    gs_all = gs_config.get_all()
    for (i, gs) in enumerate(gs_all):
        print(f'{i}. {gs["email"]}')

    index = int(input('请输入要移除的账号序号: '))
    gs_config.remove_gs(gs_all[index]['id'])
    print('账号移除成功')


def add_code():
    codes = code.add(amount=int(input('\n请输入生成激活码数量: ')))
    print('\n激活码生成完毕')
    for c in codes:
        print(c)


def show_code():
    codes = code.get_all()
    for c in codes:
        print(c)


def app_run():
    port = int(input('\n请输入程序运行端口 (默认 2333): ') or 2333)
    print('程序启动成功，请用 screen/nohup 后台运行并配合宝塔反代端口，Ctrl C 或关闭 SSH 将停止程序')
    app.run(
        host='0.0.0.0',
        port=port
    )


if __name__ == '__main__':
    print('''
    ========================
      GS 网页自助建号小助手
     github.com/zayabighead
    ========================

    1. 添加 GS 管理员账号
    2. 移除 GS 管理员账号
    
    3. 生成激活码
    4. 查看激活码
    
    5. 启动程序

    注: 添加管理员和生成激活码时请确保程序未运行，添加完后再启动程序
    ''')

    option = int(input('请选择操作: ').strip())

    if option == 1:
        add_gs()

    elif option == 2:
        remove_gs()

    elif option == 3:
        add_code()

    elif option == 4:
        show_code()

    elif option == 5:
        app_run()
