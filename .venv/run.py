from app import create_app
import os
os.environ['FLASK_APP'] = 'run.py'
os.environ['FLASK_ENV'] = 'development'

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)