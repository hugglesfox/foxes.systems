from flask_frozen import Freezer
from blog import app

app.config['FREEZER_DESTINATION'] = '../docs'
app.config['FREEZER_RELATIVE_URLS'] = False
app.config['FREEZER_REMOVE_EXTRA_FILES'] = False

freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()
