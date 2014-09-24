class standup_dev_forms_late(NebriOS):
    #listens_to = ['standup_dev_forms_late_manual']

    schedule = "*/5 * * * *"

    def check(self):
        if self.active_standup_instance_status == "pending" and datetime.now() >= self.active_standup_time:  # - timedelta(days=1):
            return True
        else:
            return False

    def action(self):

        self.active_standup_instance_status = "late"

        if shared.late_standups is None:
            shared.late_standups = []

        late_standup = {'standup_project_name': self.active_standup_project_name,
                        'standup_datetime': self.active_standup_time,
                        'standup_pid': self.PROCESS_ID, 'late_devs': []}

        for kid in children:
            if kid.standup_dev_form_status != "submitted":

                late_standup["late_devs"].append({'dev_name': kid.standup_dev_form_name,
                                                  'dev_email': kid.standup_dev_form_email,
                                                  'dev_form_pid': kid.PROCESS_ID})

                send_email(self.active_standup_project_manager_email,
                           """Hello %(active_standup_project_manager)s,

                           %(kid_standup_dev_form_name)s is late submitting their Standup for %(kid_active_standup_project_name)s.

                           Please handle this.


                           Regards,

                           -Nebri""" % {'active_standup_project_manager': self.active_standup_project_manager,
                                        'kid_standup_dev_form_name': kid.standup_dev_form_name,
                                        'kid_active_standup_project_name': kid.active_standup_project_name},

                           subject="Late Standup: %(dev_name)s - %(project_name)s" % {'dev_name': kid.standup_dev_form_name,
                                                                                      'project_name': kid.active_standup_project_name},
                           attach_variables=False)


                send_email(kid.standup_dev_form_email,
                           """Hello %(kid_standup_dev_form_name)s,

                           Your standup submission for %(kid_active_standup_project_name)s is late.

                           Please submit your standup information as soon as possible.


                           Thank you,

                           -Nebri""" % {'kid_standup_dev_form_name': kid.standup_dev_form_name,
                                        'kid_active_standup_project_name': kid.active_standup_project_name},

                           subject="Late Standup: %(project_name)s" % {'project_name': kid.active_standup_project_name},
                           attach_variables=False)


        shared.late_standups.append(late_standup)