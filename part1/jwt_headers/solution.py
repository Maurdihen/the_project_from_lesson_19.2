# Напишите декоратор "auth_required" который проверяет 
# наличие в запросе наличие заголовка 
# Authorization (содержание может быть любым)
from flask import Flask
from flask import request, abort

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.url_map.strict_slashes = False


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        return func(*args, **kwargs)
    return wrapper

                  
@app.route("/")            
@auth_required             
def get_page():
   return {}

# Для самопроверки попробуйте запустить приложение и 
# отправить GET-запросы с заголовком Authorization и без

if __name__=="__main__":
    app.run()
