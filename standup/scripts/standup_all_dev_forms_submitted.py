class standup_all_dev_forms_submitted(NebriOS):
    listens_to = ['child.standup_dev_form_submission_time']

    def check(self):
        for kid in children:
            if kid.standup_dev_form_submission_time is None:
                return False

        #return False  ## Use this to kill the loops

        return True

    def action(self):
        self.active_standup_instance_status = "complete"

        for standup in shared.standup_roster:
            if standup["project_name"] == self.active_standup_project_name:
                standup["status"] = "idle"

        for late_standup in shared.late_standups[:]:
            if late_standup["standup_pid"] == self.PROCESS_ID:
                shared.late_standups.remove(late_standup)

        recipients = self.active_standup_project_manager_email
        for dev in self.active_standup_developers:
            recipients += ", %s" % dev["dev_email"]

        body = """Hello %(project_name)s team,

                Here are the submitted standup answers for today:

                """ % {'project_name': self.active_standup_project_name}

        for form in children:
            body += """%(dev_name)s:

                    1) %(question_1)s
                    2) %(question_2)s
                    3) %(question_3)s

                    """ % {'dev_name': form.standup_dev_form_name, 'question_1': form.question_1, 'question_2': form.question_2, 'question_3': form.question_3}

        body += """Thank you for all submitting your standup forms on time!

                Our standup is scheduled to begin at %(standup_time)s.


                Thanks,

                -%(project_manager)s
                """ % {'standup_time': self.active_standup_time, 'project_manager': self.active_standup_project_manager}

        send_email(recipients, body, subject="Standup Answers - %s" % self.active_standup_project_name, attach_variables=False)