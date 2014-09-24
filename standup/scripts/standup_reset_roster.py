class standup_reset_roster(NebriOS):
    listens_to = ['standup_reset_roster']

    def check(self):
        return True

    def action(self):

        for standup in shared.standup_roster:

            if "last_run" in standup:

               standup["last_run"] = parse_datetime(standup["last_run"]) - timedelta(days=1)
               standup["status"] = "idle"
               standup["standup_time"] = datetime.now() + timedelta(minutes=30)