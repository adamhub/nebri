from yahoo_finance import Share


class yahoo_finance_connector(NebriOS):
    listens_to = ['yahoo_finance_connect']
        # set a drip at the frequency you like

    def check(self):
        return self.yahoo_finance_connect == True

    def action(self):
        self.yahoo_finance_connect = "RAN"
        code = 'GOOG' # stock symbol here
        
        s = Share(code)
        price = s.get_price()
        
        self.price = price
