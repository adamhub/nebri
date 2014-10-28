class home_genie_motion_sensor(NebriOS):
    listens_to = ['hg_motion']

    def check(self):
        return True

    def action(self):
        self.ran = True
