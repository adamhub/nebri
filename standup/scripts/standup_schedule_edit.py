class standup_schedule_edit(NebriOS):
    listens_to = ['standup_schedule_edit']

    def check(self):
        return True

    def action(self):
        if shared.standup_roster:
            for standup in shared.standup_roster:
                if standup["project_name"] == self.standup_project_name_lookup:
                    standup["project_name"] = self.standup_project_name_edit
                    standup["standup_time"] = self.standup_time_edit
                    standup["project_manager"] = self.standup_project_manager_edit
                    standup["project_manager_email"] = self.standup_project_manager_email_edit

                    del standup["developers"]

                # Again, this mess is because Forms don't handle Dictionaries

                    dev_list = []

                    dev_list.append({"dev_name":self.standup_dev_1_name_edit, "dev_email":self.standup_dev_1_email_edit})

                    if self.standup_dev_2_name_edit and self.standup_dev_2_email_edit:
                        dev_list.append({"dev_name":self.standup_dev_2_name_edit, "dev_email":self.standup_dev_2_email_edit})

                    if self.standup_dev_3_name_edit and self.standup_dev_3_email_edit:
                        dev_list.append({"dev_name":self.standup_dev_3_name_edit, "dev_email":self.standup_dev_3_email_edit})

                    if self.standup_dev_4_name_edit and self.standup_dev_4_email_edit:
                        dev_list.append({"dev_name":self.standup_dev_4_name_edit, "dev_email":self.standup_dev_4_email_edit})

                    standup["developers"] = dev_list

                    self.status = "Standup Successfully Edited"