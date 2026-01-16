import secrets
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, TextAreaField
from wtforms.validators import DataRequired, ValidationError

from config import Config

# For delete_entry route (for CSRF validation)
class EmptyForm(FlaskForm):
    pass 

class EntryForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    body = TextAreaField("Content", validators=[DataRequired()])
    is_published = BooleanField("Is Published?")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    def validate_username(self, field):
        if field.data != Config.ADMIN_USERNAME:
            raise ValidationError("Invalid username")
        return field.data

    def validate_password(self, field):
        # Prevent timing attacks by NOT USING != operator.
        # Still less secure than hashing.
        if not secrets.compare_digest(field.data, Config.ADMIN_PASSWORD):
            raise ValidationError("Invalid password")
        return field.data
