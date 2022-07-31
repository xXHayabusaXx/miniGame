from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=40)])
    #remember_me = BooleanField('Remember Me')
    submit = SubmitField('Valider')
    
    
class IndexForm(FlaskForm):
    user_input = StringField('user_input', validators=[DataRequired()])
    submit = SubmitField('Valider')



class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password1 = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=40)])
    password2 = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=40)])
    submit = SubmitField('Valider')


class WithFriends(FlaskForm):
    submit = SubmitField('Valider')


class JoinWithFriends(FlaskForm):
    gameid = StringField('gameid', validators=[DataRequired(), Length(min=4, max=20)])
    submit = SubmitField('Valider')

