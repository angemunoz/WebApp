from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField, DateField, RadioField, TimeField
from wtforms.validators import email_validator, DataRequired, Length, Email, EqualTo, ValidationError, Regexp, InputRequired, Optional
from trfocd.models import User, ThoughtRecord, SafetyBehaviour
from wtforms.widgets import TextArea, Select, CheckboxInput, ListWidget, TimeInput, DateInput
from datetime import date, datetime
# wtforms fields from (https://wtforms.readthedocs.io/en/2.3.x/fields/)
# flask_wtf from (https://flask-wtf.readthedocs.io/en/0.15.x/form/)
# wtforms validators from (https://wtforms.readthedocs.io/en/2.3.x/validators/)
# wtforms widgets from (https://wtforms.readthedocs.io/en/2.3.x/widgets/)


# Create form for signing up. 
class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=25)])
    name = StringField ('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    # Regexp is a regular expression that searches the string for matches. If not matches found it fails.
    # ^ start 
    # () group
    # ?=.* at least one
    # [A-Z] capital letter present on the string
    # [a-z] lowercase letter present on the string
    # [0-9] number present on the string
    # {9,50} a minimum of 9 characters, maximum of 50
    password = PasswordField('Password (Must contain at least one number, uppercase and lowercase letter)', validators=[DataRequired(), Regexp("^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{9,50}$", message="Password must include at least an UPPERCASE character, a lowercase character and a number")])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    disclaimer = BooleanField("Please read the following statement and click the box to agree", widget=CheckboxInput())
    submit = SubmitField('Sign Up')

    # Validation of username
    def validate_username(self, username):
        username = User.query.filter_by(username=username.data).first()
        if username is not None:
            raise ValidationError(message="Username already exist. Please choose a different one.")

    # Validation of email
    def validate_email(self,email):
        userEmail = User.query.filter_by(email=email.data).first()
        if userEmail is not None:
            raise ValidationError(message="Email address is already associated with an account, please log in.")
        
    # Validation of disclaimer
    def validate_disclaimer(self,disclaimer):
        userDisclaimer = disclaimer=disclaimer.data
        if userDisclaimer is False:
            raise ValidationError(message="You must agree with the statement to sign up.")


# Create form for logging in
class SignInForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Signin")


# Create form for registering thought records
class ThoughtRecordForm(FlaskForm):
    # Instantiate a list that holds 0-10 to facilitate repeptition of radioFields.
    listInt = list(range(11))
    dateTR = DateField("Date", validators=[InputRequired()], widget = DateInput(), default=date.today())
    timeTR = TimeField("Time", validators=[InputRequired()], widget = TimeInput(), default=datetime.now().time())
    situation = StringField("Situation",validators=[InputRequired()], widget=TextArea())
    thought = StringField("Intrusive thought",validators=[InputRequired()], widget=TextArea())
    feelings = StringField("Feelings",validators=[InputRequired()], widget=TextArea())
    feelingsStrength = RadioField("Strenght of feelings", choices=listInt, coerce=int, widget=ListWidget(), validators=[InputRequired()])
    forEvidence = StringField("Evidence for the thought (optional)", widget=TextArea())
    forEvidenceStrength = RadioField("Strenght of belief in evidence for the thought (optional)", choices=listInt, coerce=int, widget=ListWidget(), validators=[Optional()])
    againstEvidence = StringField("Evidence against the thought (optional)", widget=TextArea())
    againstEvidenceStrength = RadioField("Strenght of belief in evidence against the thought (optional)", choices=listInt, coerce=int, widget=ListWidget(), validators=[Optional()])
    altThought = StringField("Alternative thought (optional)", widget=TextArea())
    altFeelings = StringField("Alternative feelings (optional)", widget=TextArea())
    altFeelingsStrength = RadioField("Strenght of alternative feelings (optional)", choices=listInt, coerce=int, widget=ListWidget(), validators=[Optional()])
    submit = SubmitField('Submit Thought Record')

    # Code to validate date is not in the future. 
    def validate_dateTR(self, dateTR):
        if dateTR.data > date.today():
            raise ValidationError("Date cannot be in the future")
        
    #Code to validate the time is not on the future
    def validate_timeTR(self, timeTR):
        if timeTR.data > datetime.now().time() and self.dateTR.data == date.today():
            raise ValidationError("Time cannot be in the future")


# Create form for registering safety behvaiours
class SafetyBehaviourForm(FlaskForm):
    # Instantiate lists to simplify repeated numeric options.
    minList = list(range(60))
    hrList = list(range(24))
    listInt = list(range(11))
    dateSB = DateField("Date", validators=[InputRequired()], widget = DateInput(), default=date.today())
    timeSB = TimeField("Time", validators=[InputRequired()], widget = TimeInput(), default=datetime.now().time())
    safetyBehaviour = StringField("Safety Behaviour",validators=[InputRequired()], widget=TextArea())
    durationSafetyBhr = SelectField("Hours", validators=[InputRequired()], choices=hrList, widget = Select(), coerce = int, default = 0)
    durationSafetyBmin = SelectField("Minutes", validators=[InputRequired()], choices=minList, widget = Select(), coerce = int)
    durationSafetyBOPhr = SelectField("Hours", validators=[InputRequired()], choices=hrList, widget = Select(), coerce = int, default = 0)
    durationSafetyBOPmin = SelectField("Minutes", validators=[InputRequired()], choices=minList, widget = Select(), coerce = int)
    thoughtAfterSB = StringField("Thoughts after completing Safety Behaviour (optional)", widget=TextArea())
    feelingsAfterSB = StringField("Feelings after completing Safety Behaviour (optional)", widget=TextArea())
    feelingsAfterSBStrength = RadioField("Strenght of alternative feelings (optional)", choices=listInt, coerce=int, widget=ListWidget(), validators=[Optional()])
    submit = SubmitField('Submit Safety Behaviour') 


    # Code to validate date is not in the future
    def validate_dateSB(self, dateSB):
        if dateSB.data > date.today():
            raise ValidationError("Date cannot be in the future")

    def validate_timeSB(self, timeSB):
        if timeSB.data > datetime.now().time() and self.dateSB.data == date.today():
            raise ValidationError("Time cannot be in the future")


#
class SelectDateForm(FlaskForm):
    selectDate = DateField("Select the date you want to see.", validators=[InputRequired()], widget = DateInput(), default=date.today())