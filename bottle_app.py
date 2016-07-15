from bottle import route,run,error,static_file,request,default_app,response,redirect
from bottle import mako_template as template
from mylib.captcha import utils
import settings
import random
import datetime
import os
from db import controls

def gen_verify_text():
    verifytext = utils.getstr(
        random.choice(settings.CPTCH_STR['cpth_len']),
        random.choice(settings.CPTCH_STR['cpth_type']),
        settings.CPTCH_STR['filte_char'])
    # v_key = tools.make_verifytext_key(verifytext)
    # return verifytext,v_key
    return verifytext

def set_hint_info(info):
    response.set_cookie('uname',
                info.encode().decode('ISO-8859-1'),httponly='on')

def get_hint_info():
    info = request.cookies.hint_info
    request.cookies.hint_info = ''
    return info

@error(404)
def error404(error):
    return 'Url not Found!'

@route('/static/<filename>')
def serv_static(filename):
    root = '/home/cloveses/mysite/views/js'
    if filename.endswith('js'):
        root = '/home/cloveses/mysite/views/js/js'
    elif filename.endswith('css'):
        root = '/home/cloveses/mysite/views/js/css'
    return static_file(filename,root=root)

@route('/captcha')
def gen_captcha():
    response.content_type = "image/jpeg"
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
    return image['src']

@route('/')
def index():
    current_user = ''
    if 'uname' in request.cookies:
        current_user = request.cookies.uname
    urls = controls.get_all_proj()
    hint_info = get_hint_info()
    return template('index',current_user=current_user,urls=urls,hint_info='abc')

@route('/login')
def login():
    hint_info = get_hint_info()
    return template('login',hint_info=hint_info)

def signact(name,passwd):
    u = controls.add_user(name,passwd)
    return u


def loginact(name,passwd):
    u = controls.get_user(name,passwd)
    return u

def adm_login(name,passwd):
    td = datetime.date.today()
    td = td.isoformat()
    td = td.split('-')[1:]
    tdv = passwd[-4:]
    if tdv[:2] == td[0] and tdv[2:] == td[1]:
        passwd = passwd[:-4]
        passwd = controls.make_passwd(passwd)
        if passwd == settings.mgrinfo['passwd']:
            response.set_cookie('uname',
                name.encode().decode('ISO-8859-1'),httponly='on')
            return True

@route('/login',method='POST')
def login_pst():
    name = request.forms.name
    passwd =request.forms.passwd
    action = request.forms.action
    vf_txt = request.forms.vf_txt
    if vf_txt:
        set_hint_info('验证码错误！')
        redirect('/login')
    if name and passwd and action:
        if name == settings.mgrinfo['name']:
            if adm_login(name,passwd):
                redirect('/')
        else:
            u = None
            if action == 'login':
                u = loginact(name,passwd)
            elif action == 'sign':
                if controls.user_exist(name):
                    set_hint_info('用户名已存在！')
                    redirect('/login')
                u = signact(name,passwd)
            if u:
                response.set_cookie('uname',u.name.encode().decode('ISO-8859-1'),httponly='on')
                redirect('/')
                # return u.name
            else:
                redirect('/login')
    else:
        set_hint_info('姓名或密码不能为空！')
        redirect('/login')

@route('/logout')
def logout():
    response.set_cookie('uname','')
    redirect('/')

@route('/admin')
def admin_get():
    if request.cookies.uname != settings.mgrinfo['name']:
        redirect('/')
    name = request.query.name if 'name' in request.query else ''
    if name:
        controls.del_user(name)
    pname = request.query.pname if 'pname' in request.query else ''
    if pname:
        controls.chn_status(pname)
    all_user = controls.get_all_user()
    all_proj = controls.get_all_proj()
    hint_info = get_hint_info()
    paras = {"hint_info":hint_info,
    'all_user':all_user if all_user else [],
    'all_proj':all_proj if all_proj else [],
    'current_user':settings.mgrinfo['name'],}
    return template('admin',**paras)

@route('/admin',method="POST")
def admin_pst():
    if request.cookies.uname != settings.mgrinfo['name']:
        redirect('/')
    name = request.forms.name if 'name' in request.forms else ''
    url = request.forms.url if 'url' in request.forms else ''
    introduce = request.forms.introduce if 'introduce' in request.forms else ''
    if name and url:
        if controls.proj_exist(name,url):
            set_hint_info('项目名或URL地址重复！')
            redirect('/admin')
        controls.add_proname(name,url,introduce)
    else:
        set_hint_info('add projectname failure!')
    redirect('/admin')

@route('/upload/<url>')
def upload(url=''):
    if not request.cookies.uname:
        redirect('/')
    uname = request.cookies.uname
    urls = controls.get_all_proj()
    name,introduce = controls.get_info_url(url)
    hint_info = get_hint_info()
    paras = {
        'hint_info':hint_info,
        "upload_max_size":settings.UPLOAD_MAX_SIZE ,
        'urls':urls,
        'introduce':introduce,
        'name':name,
        'curl':url,
        'current_user':uname,
    }
    return template('upload',**paras)

@route('/upload/<url>',method='POST')
def upload_pst(url=''):
    if not request.cookies.uname and url:
        redirect('/')
    uname = request.cookies.uname
    upfile = request.files.get('myfile')
    name,ext = os.path.split(upfile.filename)
    mypath = settings.UPLOAD_DIR
    if not os.path.exists(mypath):
        os.makedirs(mypath)
    upfile.filename = '.'.join((uname,ext))
    if os.path.exists(os.path.join(mypath,upfile.filename)):
        os.remove(os.path.join(mypath,upfile.filename))
    upfile.save(mypath)
    uploadfile = os.path.join(mypath,upfile.filename)
    from mylib.myxltools import verify
    mset = __import__('_'.join((url,'set')))
    info = verify.verify_file(uploadfile,mset.filters,mset.limits,mset.ncols)
    if info:
        os.remove(uploadfile)
        info = '数据有误，请重新上传！\n' + info
        return info
    else:
        return '上传成功！'



application = default_app()
# run(debug=True,reload=True)