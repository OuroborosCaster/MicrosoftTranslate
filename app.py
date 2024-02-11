from flask import Flask,jsonify,request,render_template,redirect,send_from_directory
from flask_limiter import Limiter
import os, requests, uuid
app = Flask(__name__)

def limit_key_func():
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
    key_func=limit_key_func # 使用访问者的 IP 地址作为标识

)


@app.route('/')
def home():

    return render_template('translator.html')


@limiter.limit("4000/day;1000/hour")
@app.route('/api/languages')
def languages():
    languages = {'af': '南非荷兰语', 'sq': '阿尔巴尼亚语', 'am': '阿姆哈拉语', 'ar': '阿拉伯语', 'hy': '亚美尼亚语',
                 'as': '阿萨姆语', 'az': '阿塞拜疆语(拉丁语)', 'bn': '孟加拉语', 'ba': '巴什基尔语', 'eu': '巴斯克语',
                 'bho': '比哈尔语', 'brx': '博多语(印度阿萨姆邦)', 'bs': '波斯尼亚语(拉丁语系)', 'bg': '保加利亚语',
                 'yue': '粤语(繁体)', 'ca': '加泰罗尼亚语', 'lzh': '文言文', 'zh-Hans': '中文(简体)',
                 'zh-Hant': '中文(繁体)', 'sn': '绍纳语', 'hr': '克罗地亚语', 'cs': '捷克语', 'da': '丹麦语',
                 'prs': '达里语', 'dv': '马尔代夫语', 'doi': '多格拉语(印度)', 'nl': '荷兰语', 'en': '英语',
                 'et': '爱沙尼亚语', 'fo': '法罗语', 'fj': '斐济语', 'fil': '菲律宾语', 'fi': '芬兰语', 'fr': '法语',
                 'fr-ca': '法语(加拿大)', 'gl': '加利西亚语', 'ka': '格鲁吉亚语', 'de': '德语', 'el': '希腊语',
                 'gu': '古吉拉特语', 'ht': '海地克里奥尔语', 'ha': '豪撒语', 'he': '希伯来语', 'hi': '印地语',
                 'mww': '白苗语（拉丁语）', 'hu': '匈牙利语', 'is': '冰岛语', 'ig': '伊博语', 'id': '印度尼西亚语',
                 'ikt': '因纽纳敦语', 'iu': '因纽特语', 'iu-Latn': '因纽特语(拉丁语)', 'ga': '爱尔兰语',
                 'it': '意大利语', 'ja': '日语', 'kn': '卡纳达语', 'ks': '克什米尔语', 'kk': '哈萨克语', 'km': '高棉语',
                 'rw': '卢旺达语', 'tlh-Latn': '克林贡语', 'tlh-Piqd': '克林贡语(plqaD)', 'gom': '孔卡尼语',
                 'ko': '朝鲜语', 'ku': '库尔德语(中部)', 'kmr': '库尔德语(北部)', 'ky': '吉尔吉斯语(西里尔语)',
                 'lo': '老挝语', 'lv': '拉脱维亚语', 'lt': '立陶宛语', 'ln': '林加拉语', 'dsb': '下索布语',
                 'lug': '卢干达语', 'mk': '马其顿语', 'mai': '迈蒂利语', 'mg': '马达加斯加语', 'ms': '马来语(拉丁语系)',
                 'ml': '马拉雅拉姆语', 'mt': '马耳他语', 'mi': '毛利语', 'mr': '马拉地语',
                 'mn-Cyrl': '蒙古语(西里尔文)', 'mn-Mong': '蒙古语(传统)', 'my': '缅甸', 'ne': '尼泊尔语',
                 'nb': '挪威语', 'nya': '尼昂加语', 'or': '奥里亚语', 'ps': '普什图语', 'fa': '波斯语', 'pl': '波兰语',
                 'pt': '葡萄牙语（巴西）', 'pt-pt': '葡萄牙语(葡萄牙)', 'pa': '旁遮普语', 'otq': '克雷塔罗奥托米语',
                 'ro': '罗马尼亚语', 'run': '隆迪语', 'ru': '俄语', 'sm': '萨摩亚语(拉丁语)',
                 'sr-Cyrl': '塞尔维亚语（西里尔）', 'sr-Latn': '塞尔维亚语（拉丁）', 'st': '南索托语', 'nso': '北索托语',
                 'tn': '茨瓦纳语', 'sd': '信德语', 'si': '僧伽罗语', 'sk': '斯洛伐克语', 'sl': '斯洛文尼亚语',
                 'so': '索马里语（阿拉伯语）', 'es': '西班牙语', 'sw': '斯瓦希里语（拉丁语）', 'sv': '瑞典语',
                 'ty': '塔希提语', 'ta': '泰米尔语', 'tt': '鞑靼语（拉丁语）', 'te': '泰卢固语', 'th': '泰语',
                 'bo': '藏语', 'ti': '提格里尼亚语', 'to': '汤加语', 'tr': '土耳其语', 'tk': '土库曼语(拉丁语)',
                 'uk': '乌克兰语', 'hsb': '上索布语', 'ur': '乌尔都语', 'ug': '维吾尔语（阿拉伯语）',
                 'uz': '乌兹别克语(拉丁文)', 'vi': '越南语', 'cy': '威尔士语', 'xh': '班图语', 'yo': '约鲁巴语',
                 'yua': '尤卡坦玛雅语', 'zu': '祖鲁语'}

    return jsonify(languages)

@limiter.limit("2000/day;500/hour")
@app.route('/api/translate', methods=['POST'])
def translate():
    data = request.get_json()  # 获取 JSON 数据
    # print(data)
    text = translate_api(data['source'], data['target'],data['text'])[0]['translations'][0]['text']

    result={'result':text}
    return jsonify(result)

def translate_api(source,target,text):

    api_key=os.getenv('api_key')
    print(api_key,type(api_key))
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

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    return response

@app.route('/static/<path:filename>')
@limiter.limit("5/minute")  # 对该路由进行特定的限制：每分钟5次
def static_file(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH', 'CONNECT', 'TRACE'])
def catch_all(path):
    return redirect('https://www.usa.gov/'+path)

if __name__ == '__main__':
    app.run(threaded=True)
