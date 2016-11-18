class Portfolio(object):

    """Managing portfolio data"""

    def __init__(self, data=None):
        self.data = data

    def get_page_content(self, portfolio_item, page):
        return self.data[portfolio_item-1][page-1]

    def is_last_page(self, portfolio_item, page):
        return False
