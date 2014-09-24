class standup_lookup_existing_for_editing(Form):
    form_title = "Lookup Existing Standup"
    form_instructions = "Enter the Project Name of the Standup you would like to Edit"

    def get_project_names():
        projects = []
        for standup in shared.standup_roster:
            projects.append((standup["project_name"], standup["project_name"]))
        return projects

    standup_project_name_lookup = String(label="Project Name", choices=get_project_names(), required=True)
