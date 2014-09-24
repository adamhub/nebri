class standup_controller_per_instance(NebriOS):
    listens_to = ['active_standup_project_name', 'active_standup_dev_loop_hack']

    def check(self):
        #return False ## Use this to kill the loops

        if self.active_standup_dev_loop_hack > 0:
            return True

    def action(self):

        if self.active_standup_dev_loop_hack == self.active_standup_dev_loop_hack_initial:
            for project in parent.projects_activated:
                if project["project_name"] == self.active_standup_project_name:
                    project["pid"] = self.PROCESS_ID

        if not self.dev_forms_activated:
            self.dev_forms_activated = []

        for dev in self.active_standup_developers:
            if "form_status" not in dev:

                dev["form_status"] = "active"

                new_child.standup_dev_form_name = dev["dev_name"]
                new_child.standup_dev_form_email = dev["dev_email"]
                new_child.standup_dev_form_status = "pending"
                new_child.active_standup_project_name = self.active_standup_project_name
                new_child.active_standup_time = self.active_standup_time
                new_child.active_standup_project_manager = self.active_standup_project_manager
                new_child.active_standup_project_manager_email = self.active_standup_project_manager_email


                self.dev_forms_activated.append(dev)

                self.active_standup_dev_loop_hack -= 1

                break