class standup_load_edit_form(NebriOS):
    listens_to = ['standup_project_name_lookup']

    def check(self):
        return True

    def action(self):
        if shared.standup_roster:
            for standup in shared.standup_roster:
                if standup["project_name"] == self.standup_project_name_lookup:

                    self.standup_project_name_edit = standup["project_name"]
                    self.standup_time_edit = standup["standup_time"]
                    self.standup_project_manager_edit = standup["project_manager"]
                    self.standup_project_manager_email_edit = standup["project_manager_email"]

                # This mess is because Forms don't handle Dictionaries :/

                    self.standup_dev_1_name_edit = standup["developers"][0]["dev_name"]
                    self.standup_dev_1_email_edit = standup["developers"][0]["dev_email"]
                    
                    try:
                        self.standup_dev_2_name_edit = standup["developers"][1]["dev_name"]
                        self.standup_dev_2_email_edit = standup["developers"][1]["dev_email"]
                    except IndexError:
                        pass
                    
                    try:
                        self.standup_dev_3_name_edit = standup["developers"][2]["dev_name"]
                        self.standup_dev_3_email_edit = standup["developers"][2]["dev_email"]
                    except IndexError:
                        pass
                    
                    try:
                        self.standup_dev_4_name_edit = standup["developers"][3]["dev_name"]
                        self.standup_dev_4_email_edit = standup["developers"][3]["dev_email"]
                    except IndexError:
                        pass
                    
                    
                    send_email(self.last_actor,
                                """An existing Standup has been found. Please edit here:
                                {{forms.standup_schedule_edit}}
                                """, subject="Edit Existing Standup")