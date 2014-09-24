class standup_load_dev_form(NebriOS):
    listens_to = ['standup_dev_form_name']

    def check(self):
        return True

    def action(self):
        self.standup_dev_form_status = "sent"

        for dev_form in parent.dev_forms_activated:
            if dev_form["dev_name"] == self.standup_dev_form_name:
                dev_form["pid"] = self.PROCESS_ID

        send_email(self.standup_dev_form_email,
                    """Hello {{standup_dev_form_name}},

                    The {{active_standup_project_name}} standup meeting with {{active_standup_project_manager}} is schedule to start at {{active_standup_time}}.

                    Please submit your 3 Standup Questions to this form before the meeting begins.

                    {{forms.standup_dev_form}}

                    Thank you.
                    """,
                    subject="Standup Form: %s" % self.active_standup_project_name,
                    attach_variables=False)