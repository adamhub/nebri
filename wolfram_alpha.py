""" Sends email alert when company revenue becomes large certain threshold.
    It uses Wolfram Alpha.
"""
import re
import requests

def get_company_revenue(company):
    """ Finds revenue of a company using Wolfram Alpha
        Returns revenue in billions of US dollars
    """
    resp = requests.get("http://www.wolframalpha.com/input/?i={}+revenue".format(company))
    reg_exp = re.compile(
    r"""/input/
    \?i=(\d+(\.\d+)?)
    \+billion
    \+US
    \+dollars
    \+per
    \+year""", re.VERBOSE)
    match = re.search(reg_exp, resp.text)
    if match:
        return float(match.group(1))
    else:
        raise ValueError("Can't extract revenue data")

class wolframQuery(NebriOS):
    schedule = "0 0 * * *" # daily
    #schedule = "* * * * *" # each minute
    my_email = "email@example.com"
    company_name = "google"
    threshold_revenue = 300 #in billions

    def check(self):
        return get_company_revenue(self.company_name) >= self.threshold_revenue

    def action(self):
        self.example = "Ran"
        send_email (self.my_email,
        """ Revenue of company {} is now {} billions of US dollars
        """.format(self.company_name, get_company_revenue(self.company_name))
        )
