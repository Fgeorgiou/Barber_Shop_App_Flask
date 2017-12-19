from flask import Blueprint

reg_user = Blueprint('reg_user', __name__)

from . import views