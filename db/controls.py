import hashlib
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from .model import User,ProjectName,engine

def make_passwd(passwd):
    return hashlib.sha224(passwd.encode('utf-8')).hexdigest()

def get_session():
    Session = sessionmaker(bind=engine)
    return Session()

def add_user(name,passwd):
    if name and passwd:
        sess = get_session()
        passwd = make_passwd(passwd)
        u = User(name=name,passwd=passwd)
        sess.add(u)
        sess.commit()
        return u

def get_user(name,passwd):
    if name and passwd:
        passwd = make_passwd(passwd)
        sess = get_session()
        q = sess.query(User).filter_by(name=name)
        res = q.filter_by(passwd=passwd).first()
        return res

def del_user(name):
    if name:
        sess = get_session()
        sess.query(User).filter_by(name=name).delete()

def add_proname(name,url,introduce):
    if name and url:
        p = ProjectName(name=name,url=url)
        if introduce:
            p.introduce = introduce
        sess = get_session()
        sess.add(p)
        sess.commit()

def chn_status(name):
    if name:
        sess = get_session()
        p = sess.query(ProjectName).filter_by(name=name).first()
        if p:
            p.status = not p.status
            sess.commit()

def get_pro(name):
    if name:
        sess = get_session()
        return sess.query(ProjectName).filter_by(name=name).first()

def get_all_user():
    sess = get_session()
    return sess.query(User).all()

def get_all_proj():
    sess = get_session()
    return sess.query(ProjectName).all()
