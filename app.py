import os

import bottle
from beaker.middleware import SessionMiddleware

from auth import authorize, aaa
from regex import run_re, check_re, clean_data
from db import User, Entry, session as orm_session

app = bottle.app()
session_opts = {
    'session.cookie_expires': True,
    'session.encrypt_key': ("Those who dare to fail miserably can achieve "
                            "greatly."),
    'session.httponly': True,
    'session.timeout': 3600 * 24,  # 1 day
    'session.type': 'cookie',
    'session.validate_key': True,
}
app = SessionMiddleware(app, session_opts)

def get_flags():

    flags = ''
    if bottle.request.forms.get('icase'):
        flags += 'i'
    else:
        flags += '-'
    if bottle.request.forms.get('dall'):
        flags += 's'
    else:
        flags += '-'
    if bottle.request.forms.get('vbose'):
        flags += 'x'
    else:
        flags += '-'
    if bottle.request.forms.get('ascii'):
        flags += 'a'
    else:
        flags += '-'
    if bottle.request.forms.get('mline'):
        flags += 'm'
    else:
        flags += '-'

    return flags

def get_session_data():

    session = bottle.request.environ.get('beaker.session')

    pattern = session.get('pattern', '')
    if pattern:
        del session['pattern']
    testdata = session.get('testdata', '')
    if testdata:
        del session['testdata']
    flags = session.get('flags', '')
    if flags:
        del session['flags']
    else:
        flags = '-----'

    session.save()

    return pattern, testdata, flags

def prepare_data(pattern):

    pattern = pattern.replace('\\', '\\\\')
    pattern = pattern.replace('\r\n', '\\r\\n')
    pattern = pattern.replace('"', '\\"')
    pattern = pattern.replace('\'', '\\\'')

    return pattern

@bottle.route('/')
def index_get():

    if bottle.request.headers.get('X-Forwarded-Proto') == 'http':
        print('INSIDE IF')
        newurl = 'https:' + bottle.request.url.split(':', 1)[1]
        return bottle.redirect(newurl)

    if not aaa.user_is_anonymous:
        return bottle.redirect('/home')

    _ = get_session_data()  # delete saved session data, if any

    return bottle.template('index',
                           result=None,
                           testdata='',
                           pattern='',
                           flags='-----')

@bottle.post('/')
def index_post():

    pattern = bottle.request.forms.getunicode('pattern')
    testdata = bottle.request.forms.getunicode('testdata')
    flags = get_flags()

    result, modified_data = run_re(pattern, flags, testdata)

    pattern = prepare_data(pattern)

    session = bottle.request.environ.get('beaker.session')
    session['pattern'] = pattern
    if len(testdata) > 500:
        session['testdata'] = ''
    else:
        session['testdata'] = clean_data(testdata)
    session['flags'] = flags
    session.save()

    return bottle.template('index', result=result, testdata=modified_data,
                           pattern=pattern, flags=flags)


@bottle.route('/static/<filename>')
def server_static(filename):
    return bottle.static_file(filename, root='static')

@bottle.route('/home')
@authorize()
def home():

    username = aaa.current_user.username

    return bottle.template('home', username=username)

@bottle.route('/insert')
@authorize()
def insert_get():

    pattern, testdata, flags = get_session_data()

    return bottle.template('insert',
                           pattern=pattern,
                           testdata=testdata,
                           flags=flags,
                           description='',
                           errormsg=False,
                           successmsg=False)

@bottle.post('/insert')
@authorize()
def insert_post():

    pattern = bottle.request.forms.get('pattern')
    testdata = bottle.request.forms.get('testdata')
    description = bottle.request.forms.get('desc')
    flags = get_flags()

    if not check_re(pattern, flags):
        pattern = prepare_data(pattern)
        return bottle.template('insert',
                               pattern=pattern,
                               testdata=testdata,
                               description=description,
                               flags=flags,
                               errormsg=True,
                               successmsg=False)

    testdata = clean_data(testdata)

    entry = Entry(user=aaa.current_user.username,
                  pattern=pattern,
                  testdata=testdata,
                  description=description,
                  flags=flags)

    orm_session.add(entry)
    orm_session.commit()

    return bottle.template('insert',
                           pattern='',
                           testdata='',
                           description='',
                           flags='-----',
                           errormsg=False,
                           successmsg=True)

@bottle.route('/entries/u')
@bottle.route('/entries')
@authorize()
def entries():

    if bottle.request.url.rsplit('/', 1)[1] == 'u':
        msg = 'Entry updated.'
    else:
        msg = ''

    current_user = orm_session.query(User).get(aaa.current_user.username)
    ent = current_user.entries.order_by(Entry.date_added.desc()).all()
    matches = []
    for entry in ent:
        matches.append(
            run_re(entry.pattern, entry.flags, entry.testdata, 'N')[0]
        )

    return bottle.template('entries',
                           entries=ent,
                           matches=matches,
                           total=len(ent),
                           msg=msg)

@bottle.route('/edit/<id>')
@authorize()
def edit_get(id):

    entry = orm_session.query(Entry).get(id)

    if entry is None:
        bottle.abort(404)
    elif entry.user != aaa.current_user.username:
        bottle.abort(401)

    return bottle.template('edit',
                           eid=id,
                           pattern=prepare_data(entry.pattern),
                           flags=entry.flags,
                           testdata=entry.testdata,
                           description=entry.description,
                           errormsg=False,
                           result='')

@bottle.post('/edit/<id>')
@authorize()
def edit_post(id):

    pattern = bottle.request.forms.get('pattern')
    testdata = bottle.request.forms.get('testdata')
    description = bottle.request.forms.get('desc')
    save = bottle.request.forms.get('save')
    flags = get_flags()

    if save:
        if not check_re(pattern, flags):
            return bottle.template('edit',
                                   eid=id,
                                   pattern=prepare_data(pattern),
                                   flags=flags,
                                   testdata=clean_data(testdata),
                                   description=description,
                                   errormsg=True,
                                   result='')

        e = orm_session.query(Entry).get(id)
        e.pattern = pattern
        e.flags = flags
        e.testdata = clean_data(testdata)
        e.description = description

        orm_session.commit()

        return bottle.redirect('/entries/u')
    else:
        result, modified_data = run_re(pattern, flags, testdata)

        return bottle.template('edit',
                               eid=id,
                               pattern=prepare_data(pattern),
                               flags=flags,
                               testdata=modified_data,
                               description=description,
                               errormsg=False,
                               result=result)

@bottle.route('/delete/<id>')
@authorize()
def delete(id):

    entry = orm_session.query(Entry).get(id)

    if entry is None:
        bottle.abort(404)
    elif entry.user != aaa.current_user.username:
        bottle.abort(401)

    orm_session.delete(entry)
    orm_session.commit()

    return bottle.redirect('/entries')

if __name__ == '__main__':
    bottle.run(server='paste',
               app=app,
               host="0.0.0.0",
               port=int(os.environ.get("PORT", 5000)))
