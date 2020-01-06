from app import app

class Route():
    def __init__(self):

        if app.config['WEB_ENABLE']:
            from app.controllers.user import User
            User()
            from app.controllers.main import Main
            Main()
        else:
            from app.controllers.empty import Empty
            Empty()
            

        if app.config['API_ENABLE']:
            from app.apis.user import userapi
            app.register_blueprint(userapi, url_prefix='/api/v1/user')
