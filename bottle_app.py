from bottle import route,run,error,static_file,request,default_app
from bottle import mako_template as template
from mylib.captcha import utils
import settings
import random
from db import controls

def gen_verify_text():
    verifytext = utils.getstr(
        random.choice(settings.CPTCH_STR['cpth_len']),
        random.choice(settings.CPTCH_STR['cpth_type']),
        settings.CPTCH_STR['filte_char'])
    # v_key = tools.make_verifytext_key(verifytext)
    # return verifytext,v_key
    return verifytext


@error(404)
def error404(error):
    return 'Url not Found!'

@route('/static/<filename>')
def serv_static(filename):
    root = './views/js'
    if filename.endswith('js'):
        root = './views/js/js'
    elif filename.endswith('css'):
        root = './views/js/css'
    return static_file(filename,root=root)

@route('/captcha')
def gen_captcha():
    verifytext = gen_verify_text()
    print(verifytext)
    kwargs = {}
    kwargs.update(settings.CPTCH)
    kwargs.update({"text":verifytext,'font_color': random.choice(settings.INK),})
    period = random.uniform(0.11, 0.15)
    amplitude = random.uniform(3.0, 6.5)
    kwargs['distortion'] = [period, amplitude, (2.0, 0.2)]
    image = utils.gen_captcha(**kwargs)
    print(',,,,,,,,,,,,,,', image['text'])
    self.write(image['src'])

@route('/')
def index():
    current_user = ''
    if 'uname' in request.cookies:
        current_user = request.cookies.uname
    urls = controls.get_all_proj()
    return template('index',current_user=current_user,urls=urls)

@route('/login')
def login():
    hint_info = 'abc'
    return template('login',hint_info=hint_info)

@route('/login',method='POST')
def login_pst():
    pass

application = default_app()
# run(debug=True,reload=True)