from flask import Blueprint

main = Blueprint('main', __name__)

from .portfolio import Portfolio
portfolio_content = Portfolio()

from . import index, pr_data
