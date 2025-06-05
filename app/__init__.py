import os
from flask import Flask
from flask_hashing import Hashing


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads'

app.secret_key = 'e2e62cdb171271f0b12e5043f9f84208eba1f05c8658704e'
PASSWORD_SALT = '1234abcd'

hashing = Hashing(app)

 # ----Import all common routes 
# from app import home
# from app import database
from app import auth
from app import voting




if __name__ == '__main__':
    app.run(debug=True, port=5000)
 
   # If running on PythonAnywhere
# if os.environ.get('PYTHONANYWHERE_SITE'):
#     from werkzeug.middleware.proxy_fix import ProxyFix
#     app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1) 
'''
# If our app is running on PythonAnywhere, we're behind a proxy and Flask's
# request.remote_addr will always return the local loopback address: not the
# actual IP address of the client. To address this, we configure the app to
# expect a single proxy when running on PA.
#
# See https://flask.palletsprojects.com/en/2.3.x/deploying/proxy_fix/
#
if os.environ.get('PYTHONANYWHERE_SITE'):
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
'''
