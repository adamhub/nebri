from refreshbooks import api

class freshbooks_monitor(NebriOS):
    listens_to = ['check_freshbooks']

    def check(self):
        client = api.TokenClient('tomk.freshbooks.com', '69d163aace46d80aaaba0fe73b0d42b9', user_agent='Nebri/1.0')

        now = datetime.now()

        invoice_response = client.invoice.list()

        invoice_names = []

        for invoice in invoice_response.invoices.invoice:
            if (invoice.status != 'paid' and float(str(invoice.amount)) > 3000 and (now - datetime.strptime(invoice.date, '%Y-%m-%d %H:%M:%S')).days >= 21):
                invoice_names.append(invoice.invoice_id)

        if invoice_names:
            self.invoice_names = invoice_names
            return True

        return False

    def action(self):
        send_email('tomk@bixly.com', """
            Invoice(s) %s are over 3 weeks old and have not been paid.
            """ % (', '.join(self.invoice_names)))
        self.invoices = True
