from flask import make_response, send_from_directory
from main import app
from func import limiter, log_route_info, check_session_id


@app.route('/favicon.ico')
@limiter.limit("50/minute")
@log_route_info
def favicon_ico():
    return make_response(send_from_directory(app.static_folder, 'icons/favicon.ico'))


@app.route('/favicon.svg')
@limiter.limit("50/minute")
@log_route_info
def favicon_svg():
    return make_response(send_from_directory(app.static_folder, 'icons/favicon.svg'))


@app.route('/favicon-16x16.png')
@limiter.limit("50/minute")
@log_route_info
def favicon_16():
    return make_response(send_from_directory(app.static_folder, 'icons/favicon-16x16.png'))


@app.route('/favicon-32x32.png')
@limiter.limit("50/minute")
@log_route_info
def favicon_32():
    return make_response(send_from_directory(app.static_folder, 'icons/favicon-32x32.png'))


@app.route('/apple-touch-icon.png')
@limiter.limit("50/minute")
@log_route_info
def apple_touch_icon():
    return make_response(send_from_directory(app.static_folder, 'icons/apple-touch-icon.png'))


@app.route('/apple-touch-icon-120x120.png')
@limiter.limit("50/minute")
@log_route_info
def apple_touch_icon_120():
    return make_response(send_from_directory(app.static_folder, 'icons/apple-touch-icon-120x120.png'))


@app.route('/apple-touch-icon-180x180.png')
@limiter.limit("50/minute")
@log_route_info
def apple_touch_icon_180():
    return make_response(send_from_directory(app.static_folder, 'icons/apple-touch-icon-180x180.png'))


@app.route('/apple-touch-icon-precomposed.png')
@limiter.limit("50/minute")
@log_route_info
def apple_touch_icon_precomposed():
    return make_response(send_from_directory(app.static_folder, 'icons/apple-touch-icon-120x120.png'))


@app.route('/android-chrome-192x192.png')
@limiter.limit("50/minute")
@log_route_info
def android_chrome_192():
    return make_response(send_from_directory(app.static_folder, 'icons//android-chrome-192x192.png'))


@app.route('/android-chrome-512x512.png')
@limiter.limit("50/minute")
@log_route_info
def android_chrome_512():
    return make_response(send_from_directory(app.static_folder, 'icons//android-chrome-512x512.png'))


@app.route('/site.webmanifest')
@limiter.limit("50/minute")
@log_route_info
def site_webmanifest():
    return make_response(send_from_directory(app.static_folder, 'site.webmanifest'))


@app.route('/index.js')
@limiter.limit("50/minute")
@log_route_info
@check_session_id
def index_js():
    return make_response(send_from_directory(app.static_folder, 'js/index.js'))


@app.route('/index.css')
@limiter.limit("50/minute")
@log_route_info
@check_session_id
def index_css():
    return make_response(send_from_directory(app.static_folder, 'css/index.css'))
