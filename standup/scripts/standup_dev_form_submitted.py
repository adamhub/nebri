class standup_dev_form_submitted(NebriOS):
    listens_to = ['standup_dev_form_submission_time']

    def check(self):
        return True

    def action(self):
        self.standup_dev_form_status = "submitted"

        # Do something... send something to someone... not sure