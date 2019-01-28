import os
import logging

import bottle
from cork import Cork
from bottle_flash2 import FlashPlugin
# import requests

DATABASE_URL = os.environ['DATABASE_URL']
DBNAME = DATABASE_URL.rsplit('/', 1)[1]

MAILID = os.environ['MAILID']
PASSWORD = os.environ['PASSWORD']

COOKIE_SECRET = os.environ['COOKIE_SECRET']

# SITE_VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'
# RECAPTCHA_SECRET = '6LfeHx4UAAAAAFWXGh_xcL0B8vVcXnhn9q_SnQ1b'

logging.basicConfig(format='heroku - - [%(asctime)s] %(message)s',
                    level=logging.DEBUG)

from cork.backends import SqlAlchemyBackend

if not DATABASE_URL.startswith('postgresql'):
    DATABASE_URL = 'postgresql:' + DATABASE_URL.split(':', 1)[1]

sa = SqlAlchemyBackend(DATABASE_URL,
                       initialize=True,
                       connect_args={'dbname': DBNAME})

SMTP_URL = ('starttls://' + MAILID + ':' + PASSWORD
            + '@smtp-mail.outlook.com:587')
aaa = Cork(smtp_url=SMTP_URL,
           email_sender=MAILID,
           backend=sa)

authorize = aaa.make_auth_decorator(fail_redirect="/login", role="user")

app = bottle.Bottle()
app.install(FlashPlugin(secret=COOKIE_SECRET))

def postd():
    return bottle.request.forms

def post_get(name, default=''):
    return bottle.request.POST.get(name, default).strip()

@bottle.route('/sorry_page')
def sorry_page():
    """Serve sorry page"""
    return '<p>Sorry, you are not authorized to perform this action</p>'

@bottle.route('/login')
@bottle.view('login_form')
def login_form():
    """Serve login form"""

    if bottle.request.headers.get('X-Forwarded-Proto') == 'http':
        newurl = 'https:' + bottle.request.url.split(':', 1)[1]
        return bottle.redirect(newurl)

    if not aaa.user_is_anonymous:
        return bottle.redirect('/home')

    session = bottle.request.environ.get('beaker.session')
    form = session.get('form', '')
    uname = session.get('uname', '')
    email = session.get('email', '')

    if form:
        del session['form']
    if uname:
        del session['uname']
    if email:
        del session['email']

    session.save()

    return {'app': app, 'form': form, 'uname': uname, 'email': email}

@bottle.post('/login')
def login():
    """Authenticate users"""
    username = post_get('username')
    password = post_get('password')

    session = bottle.request.environ.get('beaker.session')
    if session.get('pattern'):
        url = '/insert'
    else:
        url = '/home'

    session['form'] = 'form1'
    session['uname'] = username
    session.save()

    aaa.login(username, password,
              success_redirect=url,
              fail_redirect='/temp')

@bottle.route('/temp')
def pass_msg():

    app.flash('Invalid username/password.')
    return bottle.redirect('/login')

@bottle.route('/user_is_anonymous')
def user_is_anonymous():
    if aaa.user_is_anonymous:
        return 'True'

    return 'False'

@bottle.route('/logout')
def logout():
    aaa.logout(success_redirect='/')

def save_form_fields(form, username, email):

    session = bottle.request.environ.get('beaker.session')
    session['form'] = form
    session['uname'] = username
    session['email'] = email
    session.save()

@bottle.post('/register')
def register():
    """Send out registration email"""
    username = post_get('username')
    pass1 = post_get('password1')
    pass2 = post_get('password2')
    email = post_get('email_address')
    # token = post_get('g-recaptcha-response')

    error = False
    if len(username) < 3:
        app.flash('Username must have at least 3 characters.')
        error = True
    if len(pass1) < 8:
        app.flash('Password must have at least 8 characters.')
        error = True
    if pass1 != pass2:
        app.flash("Passwords don't match.")
        error = True

    # token could be blank if there is a delay between checking
    # the recaptcha box and clicking submit.
    # if not token:
    #     app.flash('Recaptcha required. Please try again.')
    #     error = True
    # else:
        # resp = requests.post(SITE_VERIFY_URL,
        #                      data={'secret': RECAPTCHA_SECRET,
        #                            'response': token})

        # if not resp.json().get('success'):
        #     app.flash('There was a recaptcha error.')
        #     error = True

    if error:
        save_form_fields('form2', username, email)
        return bottle.redirect('/login')

    try:
        aaa.register(username, pass1, email)
    except Exception as e:
        app.flash(str(e))
        save_form_fields('form2', username, email)
        return bottle.redirect('/login')
    else:
        return 'Please check your mailbox.'

@bottle.route('/validate_registration/<registration_code>')
def validate_registration(registration_code):
    """Validate registration, create user account"""
    try:
        aaa.validate_registration(registration_code)
    except Exception as e:
        logging.warning(str(e))
        return ('<head><title>Register</title></head>'
                '<p>This link is invalid.</p>')
    else:
        return 'Thanks. <a href="/login">Go to login</a>'


@bottle.post('/reset_password')
def send_password_reset_email():
    """Send out password reset email"""

    username = post_get('username')
    email = post_get('email_address')
    try:
        aaa.send_password_reset_email(
            username=username,
            email_addr=email
        )
    except Exception as e:
        app.flash(str(e))
        save_form_fields('form3', username, email)
        return bottle.redirect('/login')
    else:
        return 'Please check your mailbox.'


@bottle.route('/change_password/<reset_code>')
@bottle.view('password_change_form')
def change_password(reset_code):
    """Show password change form"""
    return dict(reset_code=reset_code, app=app)


@bottle.post('/change_password')
def change_password():
    """Change password"""
    password = post_get('password')
    reset_code = post_get('reset_code')

    if len(password) < 8:
        app.flash('Password must have at least 8 characters.')
        return bottle.redirect('/change_password/' + reset_code)

    aaa.reset_password(reset_code, password)
    return ('<head><title>Change password</title></head>'
            'Thanks. <a href="/login">Go to login</a>')


# admin views follow

@bottle.route('/admin')
@authorize(role="admin", fail_redirect='/sorry_page')
@bottle.view('admin_page')
def admin():
    """Only admin users can see this"""
    #aaa.require(role='admin', fail_redirect='/sorry_page')
    return dict(
        current_user = aaa.current_user,
        users = aaa.list_users(),
        roles = aaa.list_roles()
    )


@bottle.post('/create_user')
def create_user():
    try:
        aaa.create_user(postd().username, postd().role, postd().password)
        return dict(ok=True, msg='')
    except Exception as e:
        return dict(ok=False, msg=str(e))


@bottle.post('/delete_user')
def delete_user():
    try:
        aaa.delete_user(post_get('username'))
        return dict(ok=True, msg='')
    except Exception as e:
        print(e)
        return dict(ok=False, msg=str(e))


@bottle.post('/create_role')
def create_role():
    try:
        aaa.create_role(post_get('role'), post_get('level'))
        return dict(ok=True, msg='')
    except Exception as e:
        return dict(ok=False, msg=str(e))


@bottle.post('/delete_role')
def delete_role():
    try:
        aaa.delete_role(post_get('role'))
        return dict(ok=True, msg='')
    except Exception as e:
        return dict(ok=False, msg=str(e))
