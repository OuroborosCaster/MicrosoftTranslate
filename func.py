from datetime import datetime
from bson.objectid import ObjectId
import functools, uuid, requests
from flask import request, session, make_response
from flask_limiter import Limiter
from flask_pymongo import PyMongo
from main import app

# redis数据库配置
redis_password = app.config['REDIS_PASSWORD']
redis_host = app.config['REDIS_HOST']
redis_port = app.config['REDIS_PORT']
redis_db = app.config['REDIS_DB']


def get_real_ip():
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        # 如果 X-Forwarded-For 存在，取其值
        ip = x_forwarded_for.split(",")[-1].strip()
    else:
        # 否则，取 remote_address
        ip = request.remote_addr
    return ip


limiter = Limiter(
    app=app,
    storage_uri=f'redis://:{redis_password}@{redis_host}:{redis_port}/{redis_db}',
    key_func=get_real_ip  # 使用访问者的 IP 地址作为标识
)


def translate_api(source, target, text):
    api_key = app.config['API_KEY']
    print(api_key, type(api_key))
    endpoint = "https://api.cognitive.microsofttranslator.com"
    location = "global"
    path = '/translate'
    constructed_url = endpoint + path
    params = {
        'api-version': '3.0',
        'from': source,
        'to': target
    }
    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': text
    }]

    translate_request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = translate_request.json()

    return response


snow_flake_api = app.config['SNOWFLAKE_API']


def get_id():
    response = requests.get(snow_flake_api).json()
    return response['id']


def get_key():
    PreObjectId = oct(get_id())[2:]
    if len(PreObjectId) == 20:
        key = ObjectId("7777" + PreObjectId)
    elif len(PreObjectId) == 21:
        key = ObjectId("888" + PreObjectId)
    else:
        key = ObjectId("99" + PreObjectId)
    return key


mongo = PyMongo(app)


def log_route_info(route_func):
    @functools.wraps(route_func)
    def wrapper(*args, **kwargs):
        # 获取请求接收的时间
        request_received_at = datetime.now()
        # 插入数据库后的主键
        record_id = get_key()

        # 如果请求的路径是 "/"，则生成一个新的会话 ID
        if request.path == "/":
            session['id'] = get_id()

        # 获取会话 ID，如果会话中没有 ID，则生成一个新的
        session_id = get_id() if 'id' not in session else session['id']

        # 获取请求的来源 IP
        ip = get_real_ip()

        # 获取请求的类型（GET、POST 等）
        request_type = request.method

        # 获取请求的路径
        request_path = request.path

        # 获取请求的头部信息
        request_headers = request.headers

        # 从请求头中获取 Referer 字段
        referer = request_headers.get('Referer')

        # 从请求头中获取 User-Agent 字段
        User_Agent = request_headers.get('User-Agent')

        # 调用原路由函数并获取响应
        response = route_func(*args, **kwargs)

        # 获取响应生成的时间
        response_generated_at = datetime.now()

        # 计算处理请求并生成响应所花费的时间
        processing_time = response_generated_at - request_received_at

        # 获取响应的状态码
        response_code = response.status_code

        # 获取响应的头部信息
        response_headers = response.headers

        # 访问记录
        record = {
            '_id': record_id,
            'request_received_at': str(request_received_at),
            'session_id': session_id,
            'ip': ip,
            'request_type': request_type,
            'request_path': request_path,
            'request_headers': str(request_headers),
            'referer': referer,
            'User_Agent': User_Agent,
            'response_generated_at': str(response_generated_at),
            'processing_time': "{:.3f} ms".format(processing_time.total_seconds() * 1000),
            'response_code': response_code,
            'response_headers': str(response_headers),
        }
        mongo.db[app.config["MONGO_COLLECTION"]].insert_one(record)
        return response

    return wrapper


def check_session_id(route_func):
    @functools.wraps(route_func)
    def wrapper(*args, **kwargs):
        if 'id' not in session:
            return make_response('', 403)
        return route_func(*args, **kwargs)

    return wrapper


@app.errorhandler(429)
@log_route_info
def ratelimit_handler(e):
    return make_response(e, 429)
