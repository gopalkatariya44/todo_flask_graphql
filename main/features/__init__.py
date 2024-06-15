from .todos import todo_controller
from .auth import auth_controller
from .payment import payment_controller
from .. import app

app.register_blueprint(auth_controller.router)
app.register_blueprint(todo_controller.router)
app.register_blueprint(payment_controller.router)
