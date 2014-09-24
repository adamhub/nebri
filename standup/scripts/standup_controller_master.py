class standup_controller_master(NebriOS):
    listens_to = ['standup_controller_go', 'standup_controller_loop_hack']
    ## Dripped every 5 minutes

    def check(self):
        #return False  ## Use this to kill the loops

        return True

        ## Let's do all the logic in the Action


    def action(self):

        self.status = "RAN"

        for standup in shared.standup_roster:

            if (standup["status"] != "active"
              and parse_datetime(standup["standup_time"]) - datetime.now() <= timedelta(minutes=30)
              and (not "last_run" in standup or parse_datetime(standup["last_run"]).date() != datetime.now().date())):

                ## This must be date-agnostic.  It must only care about the time.

                standup["status"] = "active"
                standup["last_run"] = datetime.now()

                new_child.active_standup_instance_status = "pending"
                new_child.active_standup_project_name = standup["project_name"]
                new_child.active_standup_time = standup["standup_time"]
                new_child.active_standup_project_manager = standup["project_manager"]
                new_child.active_standup_project_manager_email = standup["project_manager_email"]
                new_child.active_standup_developers = standup["developers"]
                new_child.active_standup_dev_loop_hack = len(standup["developers"])
                new_child.active_standup_dev_loop_hack_initial = len(standup["developers"])

                if not self.projects_activated:
                    self.projects_activated = []

                self.projects_activated.append({"project_name":standup["project_name"], "pid":"Unknown"})


                if self.standup_controller_loop_hack:
                    self.standup_controller_loop_hack += 1
                else:
                    self.standup_controller_loop_hack = 1

                break
                ## This break stops the script after the first match in the loop,
                ## and basically allows the script to restart the for loop within a new 'instance',
                ## so that the new_child functions work