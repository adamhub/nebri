import re

class standup_schedule_edit(Form):
    form_title = "Edit Standup Schedule"
    form_instructions = "Enter information regarding the Standup to Edit."

    def validate_email(form, field, email_address):
        if re.match(r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"'r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', email_address, re.IGNORECASE):
            return True
        raise ValidationError('Please provide a valid email address (Example = user@test.com)')


    standup_project_name_edit = String(label="Project Name", required=True)
    standup_time_edit = Time(required=True)
    standup_project_manager_edit = String(label="Project Manager", required=True)
    standup_project_manager_email_edit = String(label="Project Manager Email", required=True)

    standup_dev_1_name_edit = String(label="Developer Name #1", required=True)
    standup_dev_1_email_edit = String(label="Developer Email #1", message="Use additional developer fields as necessary", required=True)
    standup_dev_2_name_edit = String(label="Developer Name #2")
    standup_dev_2_email_edit = String(label="Developer Email #2")
    standup_dev_3_name_edit = String(label="Developer Name #3")
    standup_dev_3_email_edit = String(label="Developer Email #3")
    standup_dev_4_name_edit = String(label="Developer Name #4")
    standup_dev_4_email_edit = String(label="Developer Email #4")

    standup_schedule_edit = Boolean(initial=True, hidden=True)