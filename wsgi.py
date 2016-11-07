from flask import Flask

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from app.api import bp

app = Flask('app')
app.register_blueprint(bp)
application = DispatcherMiddleware(app)

if __name__ == "__main__":

    run_simple('localhost', 5000, application, use_reloader=True, use_debugger=True)
