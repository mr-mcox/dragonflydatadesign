from flask import Blueprint

main = Blueprint('main', __name__)

portfolio_data = [
    [{'title': 'The Situation', 'picture': 'pr-1-spreadsheet.png',
      'copy': 'We learned from a regional data analyst that a challenge that coaches in his region faced was in sharing the long term development arc of teachers with other staff who supported them. Coaches had difficulty reconstructing what occurred weeks and months prior as their only analysis tools were spreadsheets that tabulated current results.'},
     {'title': 'The Next Page', 'picture': 'pr-2-exploration.png',
      'copy': 'To address this need, we applied lean design principles to pilot an interactive high level view on teacher data.'}]
]

from .portfolio import Portfolio
portfolio_content = Portfolio(data=portfolio_data)
# portfolio_content = Portfolio()

from . import index, pr_data
