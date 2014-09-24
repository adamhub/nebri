class standup_new_standup_schedule(NebriOS):
    listens_to = ['standup_schedule_new']

    def check(self):
        if shared.standup_roster:
            for standup in shared.standup_roster:
                if standup["project_name"] == self.standup_project_name:
                    new_child.standup_project_name_lookup = self.standup_project_name
                    new_child.standup_creation_attempted = True
                    return False
            return True
        else:
            shared.standup_roster = []
            return True


    def action(self):

        ## Forms should be able to handle Dictionaries as input
        dev_list = []
        if self.standup_dev_1_name and self.standup_dev_1_email:
            dev_list.append({"dev_name":self.standup_dev_1_name, "dev_email":self.standup_dev_1_email})
        if self.standup_dev_2_name and self.standup_dev_2_email:
            dev_list.append({"dev_name":self.standup_dev_2_name, "dev_email":self.standup_dev_2_email})
        if self.standup_dev_3_name and self.standup_dev_3_email:
            dev_list.append({"dev_name":self.standup_dev_3_name, "dev_email":self.standup_dev_3_email})
        if self.standup_dev_4_name and self.standup_dev_4_email:
            dev_list.append({"dev_name":self.standup_dev_4_name, "dev_email":self.standup_dev_4_email})

        ## Convert DateTime value from Form to simply Time?   Date is irrelevant here.

        shared.standup_roster.append({"project_name":self.standup_project_name, "standup_time":self.standup_time, "project_manager":self.standup_project_manager, "project_manager_email":self.standup_project_manager_email, "status":"idle", "developers":dev_list})

        self.status = "Standup Successfully Scheduled"