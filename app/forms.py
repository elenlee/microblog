from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms import TextAreaField, SubmitField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length
from app.models import User
from flask_wtf.file import FileField, FileAllowed, FileRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[
        DataRequired(), Length(min=1, max=300)])
    submit = SubmitField('Submit')            

class UploadAvatarForm(FlaskForm):
    image = FileField('Choose new avatar', validators=[FileRequired(),
                      FileAllowed(['jpg', 'png'],
                      'The file format should be .jpg or .png.')])
    submit = SubmitField('Apply')