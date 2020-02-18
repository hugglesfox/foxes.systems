from flask_frozen import Freezer
from blog import app

app.config['FREEZER_DESTINATION'] = '../public'
app.config['FREEZER_RELATIVE_URLS'] = True
freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()
