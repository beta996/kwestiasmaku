import os

from web_server import app

if __name__ == '__main__':


    app.run(port=int(os.getenv('PORT', 33507)))
