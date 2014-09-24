import re

class standup_schedule_new(Form):
    form_title = "New Standup Schedule"
    form_instructions = "Enter information regarding new Standup to schedule."


    def validate_email(form, field, email_address):
        if re.match(r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"'r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', email_address, re.IGNORECASE):
            return True
        raise ValidationError('Please provide a valid email address (Example = user@test.com)')


    standup_project_name = String(label="Project Name", message="To edit existing Project, use Edit Standup Schedule form", required=True)
    standup_time = Time(required=True)
    standup_project_manager = String(label="Project Manager", required=True)
    standup_project_manager_email = String(label="Project Manager Email", required=True)

    standup_dev_1_name = String(label="Developer Name #1", required=True)
    standup_dev_1_email = String(label="Developer Email #1", message="Use additional developer fields as necessary", required=True)
    standup_dev_2_name = String(label="Developer Name #2")
    standup_dev_2_email = String(label="Developer Email #2")
    standup_dev_3_name = String(label="Developer Name #3")
    standup_dev_3_email = String(label="Developer Email #3")
    standup_dev_4_name = String(label="Developer Name #4")
    standup_dev_4_email = String(label="Developer Email #4")

    standup_schedule_new = Boolean(initial=True, hidden=True)