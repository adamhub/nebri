class standup_dev_form(Form):
    form_title = "Standup Form"
    form_instructions = "Submit your 3 Standup Questions for the standup today."

    question_1 = String(label="What did you work on last?", required=True)
    question_2 = String(label="What will you work on next?", required=True)
    question_3 = String(label="Is there anything blocking you from being productive?", required=True)

    standup_dev_form_submission_time = DateTime(initial=datetime.now(), hidden=True)