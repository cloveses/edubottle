import hashlib
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from .model import User,ProjectName,engine

def make_passwd(passwd):
    return hashlib.sha224(passwd.encode('utf-8')).hexdigest()

def get_session():
    Session = sessionmaker(bind=engine)
    return Session()

def user_exist(name):
    sess = get_session()
    q = sess.query(User).filter_by(name=name).first()
    sess.close()
    if q:
        return True

def add_user(name,passwd):
    if name and passwd:
        sess = get_session()
        passwd = make_passwd(passwd)
        u = User(name=name,passwd=passwd)
        sess.add(u)
        sess.commit()
        sess.close()
        return u

def get_user(name,passwd):
    if name and passwd:
        passwd = make_passwd(passwd)
        sess = get_session()
        q = sess.query(User).filter_by(name=name)
        res = q.filter_by(passwd=passwd).first()
        sess.close()
        return res

def del_user(name):
    if name:
        sess = get_session()
        sess.query(User).filter_by(name=name).delete()
        sess.commit()
        sess.close()

def proj_exist(name,url):
    sess = get_session()
    q = sess.query(ProjectName).filter_by(name=name).first()
    if q:
        sess.close()
        return True
    q = sess.query(ProjectName).filter_by(url=url).first()
    if q:
        sess.close()
        return True

def add_proname(name,url,introduce):
    if name and url:
        p = ProjectName(name=name,url=url)
        if introduce:
            p.introduce = introduce
        sess = get_session()
        sess.add(p)
        sess.commit()
        sess.close()

def chn_status(name):
    if name:
        sess = get_session()
        p = sess.query(ProjectName).filter_by(name=name).first()
        if p:
            p.status = not p.status
            sess.commit()
            sess.close()

def del_pro(name):
    if name:
        sess = get_session()
        sess.query(ProjectName).filter_by(name=name).delete()
        sess.commit()
        sess.close()

def get_pro(name):
    if name:
        sess = get_session()
        res = sess.query(ProjectName).filter_by(name=name).first()
        sess.close()
        return res

def get_all_user():
    sess = get_session()
    res = sess.query(User).all()
    sess.close()
    return res

def get_all_proj():
    sess = get_session()
    res = sess.query(ProjectName).all()
    sess.close()
    return res

def get_open_proj():
    sess = get_session()
    res = sess.query(ProjectName).filter_by(status=True).all()
    sess.close()
    return res

def get_info_url(url):
    if url:
        sess = get_session()
        proj = sess.query(ProjectName).filter_by(url=url).first()
        sess.close()
        if proj:
            return proj.name,proj.introduce
    return '',''
