#!env python
import os
venv = os.getenv("PYTHON_VIRTUALENV", "venv") + "/bin/activate_this.py"
execfile(venv, dict(__file__=venv))

import argparse
from werkzeug.contrib.profiler import ProfilerMiddleware
from api import app

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ok")
    parser.add_argument(
        "-d", "--debug", action="store_true", help="start in debug mode",
        default=False
        )
    parser.add_argument(
        '-p', '--port', action='store', type=int, help='port number',
        default=8080
        )
    parser.add_argument(
        '-o', '--profile', action='store_true', help='do profiling',
        default=False
        )
    args = parser.parse_args()
    if args.profile:
        app.config['PROFILE'] = True
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])

    app.run(debug=args.debug, host="127.0.0.1", port=args.port)
