import json
from constants import *
from flask import jsonify, request, render_template, make_response, redirect
from main import app
from func import limiter, translate_api, log_route_info, check_session_id


@app.route('/')
@limiter.limit("50/minute")
@log_route_info
def home():
    return make_response(render_template('index.html'))


@app.route('/api/languages')
@limiter.limit("4000/day;1000/hour")
@log_route_info
@check_session_id
def languages():
    return make_response(json.dumps(get_languages()))


@app.route('/api/translate', methods=['POST'])
@limiter.limit("2000/day;500/hour")
@log_route_info
@check_session_id
def translate():
    data = request.get_json()  # 获取 JSON 数据
    text = translate_api(data['source'], data['target'], data['text'])[0]['translations'][0]['text']
    result = {'result': text}
    return make_response(jsonify(result))


@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH', 'CONNECT', 'TRACE'])
@log_route_info
def catch_all(path):
    return make_response(redirect('https://www.usa.gov/' + path))
