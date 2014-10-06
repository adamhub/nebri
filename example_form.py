class hello_form(Form):

    def validate_bool_test_one(form, field, value):
        if value == False:
            raise ValidationError('Bool test one cannot be False!')

    def validate_age(form, field, age):
        if age < 18:
            field.value = 10
            raise ValidationError('You must be older than 18 to submit this form!')
        elif age > 99:
            raise ValidationError('Who are you? Superhuman?!')

    def validate_requested_on(form, field, value):
        field.value = datetime.now()

    def validate_requested_date(form, field, value):
        if not value > date.today():
            raise ValidationError('Date must be in the future!')

    form_title = 'Hello World!'
    form_instructions = 'Click on fields and try to fill them out!'

    name = String(label="Provide your name", message='Test message')
    age = Number(label="Provide your age", message='Test', required=True, validation=validate_age)
    other_number = Number(initial=2)
    bool_test_one = Boolean(required=True, initial=False, validation=validate_bool_test_one)
    bool_test_two = Boolean(required=True, initial=False, radio=True)
    bool_test_three = Boolean(required=True, initial=False, dropdown=True)
    combo_box_one = String(choices=[('AK', 'Arkansas',),('CA', 'California',)])
    combo_box_two = Number(choices=[(1, 'One',),(2, 'Two',)])
    multi_box_one = String(choices=[(1, 'One',),(2, 'Two',)], multiselect=True)
    when = DateTime(initial=datetime.now())
    requested_on = DateTime(initial=datetime.now(), validation=validate_requested_on)
    requested_date = Date(initial=date.today(), validation=validate_requested_date)
    requested_time = Time(initial=datetime.now())
