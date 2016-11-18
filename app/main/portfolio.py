class Portfolio(object):

    """Managing portfolio data"""

    def __init__(self, data=None):
        self.data = data

    def get_page_content(self, portfolio_item, page):
        return self.data[int(portfolio_item)-1][int(page)-1]

    def is_last_page(self, portfolio_item, page):
        if self.data is None:
            return True
        return int(page) >= len(self.data[int(portfolio_item)-1])

    def is_first_page(self, portfolio_item, page):
        if self.data is None:
            return True
        return int(page) == 1
