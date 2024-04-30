from trfocd import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
# SQLAlchemy used to create database tables using pythonic language (https://docs.sqlalchemy.org/en/14/core/metadata.html).
# SQLAlchemy used to set relationships between databases (https://docs.sqlalchemy.org/en/14/orm/relationship_api.html#sqlalchemy.orm)
# Werkzeug.security "generate_password_hash" and "check_password_hash" used to secure passwords (https://werkzeug.palletsprojects.com/en/2.3.x/utils/).
# Flask_login "UserMixin" and "login_manager" used to manage users (https://flask-login.readthedocs.io/en/latest/)


# Create the user table on the database with the following columns.
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(30), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    passwordHash = db.Column(db.String(128), unique=False, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    disclaimer = db.Column(db.Boolean, nullable=False, default=False)
    # Set up relationship between User table and ThoughtRecord and SafetyBehaviour tables.
    thoughtRecord=db.relationship("ThoughtRecord",backref="user",lazy=True)
    safetyBehaviour=db.relationship("SafetyBehaviour",backref="user",lazy=True)
#end of referenced code

    # Return user infromation to be accessed later
    def __repr__(self):
        return f"User('{self.username}', '{self.name}', '{self.email}', '{self.disclaimer}')"

    # Prevent password from being read.
    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    # Generate the password hash.
    @password.setter
    def password(self, password):
       self.passwordHash = generate_password_hash(password, method="pbkdf2:sha256:600000", salt_length=16)

    # Check password is correct.
    def verify_password(self, password):
       return check_password_hash(self.passwordHash, password)

    # Allow for sign-ins to take place
    @login_manager.user_loader
    def load_user(userId):
        return User.query.get(int(userId))


@login_manager.user_loader
def load_user(userId):
    return User.query.get(int(userId))

# Create the thought record table on the database with the following columns.
class ThoughtRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Take the primary key from "User" as a foreign key to link the thoughts to users.
    userIdforTR = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    dateTR = db.Column(db.Date, nullable=False)
    timeTR = db.Column(db.Time, nullable=False)
    situation = db.Column(db.Text, nullable=False)
    thought = db.Column(db.Text, nullable=False)
    feelings = db.Column(db.Text, nullable=False)
    feelingsStrength = db.Column(db.Integer, nullable=False)
    forEvidence = db.Column(db.Text, nullable=True)
    forEvidenceStrength = db.Column(db.Integer, nullable=True)
    againstEvidence = db.Column(db.Text, nullable=True)
    againstEvidenceStrength = db.Column(db.Integer, nullable=True)
    altThought = db.Column(db.Text, nullable=True)
    altFeelings = db.Column(db.Text, nullable=True)
    altFeelingsStrength = db.Column(db.Integer, nullable=True)
    # Set up relationship between ThoughtRecord table and SafetyBehaviour table.
    safetyBehaviour=db.relationship("SafetyBehaviour",backref="thought_record",lazy=True)

    def __repr__(self):
        return f"ThoughtRecord('{self.dateTR}', {self.timeTR}, '{self.situation}', '{self.thought}', \
            '{self.feelings}', '{self.feelingsStrength}', '{self.forEvidence}', '{self.forEvidenceStrength}', \
            '{self.againstEvidence}', '{self.againstEvidenceStrength}', '{self.altThought}', '{self.altFeelings}', '{self.altFeelingsStrength}')"

# Create the safety behaviour table on the database with the following columns.
class SafetyBehaviour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Take the primary key from "User" and "ThoughtRecord" as a foreign key to link the thoughts to users.
    userIdforSB = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    thoughtId = db.Column(db.Integer, db.ForeignKey("thought_record.id"), nullable=False)
    dateSB = db.Column(db.Date, nullable=False)
    timeSB = db.Column(db.Time, nullable=False)
    safetyBehaviour = db.Column(db.Text, nullable=False)
    durationSafetyBhr = db.Column(db.Integer, nullable=False)
    durationSafetyBmin = db.Column(db.Integer, nullable=False)
    durationSafetyBOPhr = db.Column(db.Integer, nullable=False)
    durationSafetyBOPmin = db.Column(db.Integer, nullable=False)
    thoughtAfterSB = db.Column(db.Text, nullable=True)
    feelingsAfterSB = db.Column(db.Text, nullable=True)
    feelingsAfterSBStrength = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"SafetyBehaviour('{self.dateSB}', {self.timeSB}, {self.safetyBehaviour}', '{self.durationSafetyBhr}, '{self.durationSafetyBmin}, \
            '{self.durationSafetyBOPhr}', '{self.durationSafetyBOPmin}, '{self.thoughtAfterSB}','{self.feelingsAfterSB}','{self.feelingsAfterSBStrength}')"