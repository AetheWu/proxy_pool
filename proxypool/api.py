"这是一个api模块，实现了一个轻量的基于flask的web框架，用来从数据库中获取可用proxy地址"

from flask import Flask,g

from proxypool.mongo_client import MongoClient

__all__ = ['app']

app = Flask(__name__)

def get_conn():
    if not hasattr(g, 'mongo'):
        g.mongo = MongoClient()
    return  g.mongo

@app.route('/')
def index():
    conn = get_conn()
    proxy =   conn.get_proxy()
    count = conn.count()

    return '''
    <h1>代理池</h1>
    <div>
    <li>代理地址：%s</li>
    <li>代理数量：%d</li>
    </div>
    <br>
    <a href="/">
    <button>刷新</button>
    </a>
    ''' %(proxy,count)

# @app.route('/random')
# def get_proxy():
#     conn = get_conn()
#     return conn.get_proxy()
#
# @app.route('/count')
# def get_counts():
#     conn = get_conn()
#     return '代理池可用代理地址数量：'+ str(conn.count())

if __name__ == '__main__':
    app.run()