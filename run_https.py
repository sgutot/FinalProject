# run_https.py

import subprocess
import os
import sys

def run_django_https():
    manage_py = os.path.join(os.path.dirname(__file__), 'manage.py')

    cert_path = "C:/mkcert/localhost.pem"
    key_path = "C:/mkcert/localhost-key.pem"

    command = [
        sys.executable,
        manage_py,
        'runserver_plus',
        '--cert', cert_path,
        '--key', key_path,
        '0.0.0.0:8000',
    ]

    subprocess.run(command)

if __name__ == '__main__':
    run_django_https()
