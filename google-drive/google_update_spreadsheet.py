import gspread
from oauth2client.client import OAuth2Credentials


class google_update_spreadsheet(NebriOS):
    listens_to = ['shared.update_gsheet']

    def check(self):
        #if shared.client_credentials and \
        #   shared.update_gsheet['filename'] and \
        #   shared.update_gsheet['data']:
        #    return True
        return True

    def action(self):
        credentials = OAuth2Credentials.from_json(shared.client_credentials)
        gc = gspread.authorize(credentials)
        
        # get worksheet
        sh = gc.open(shared.update_gsheet['filename'])
        worksheet = sh.get_worksheet(0)

        # data
        datalist = shared.update_gsheet['data']

        # loop through each data for row
        row = 1
        for k in range(0, len(datalist)):
            col_num = len(datalist[k])
            col_letter = chr(ord('A') + col_num - 1)

            row_range = 'A{row}:{col}{row}'.format(row=row, col=col_letter)
            cell_list = worksheet.range(row_range)

            # loop through data and write in cell
            for i in range(0, len(cell_list)):
                cell_list[i].value = datalist[k][i]
            worksheet.update_cells(cell_list)
            row += 1
