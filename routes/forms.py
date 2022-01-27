from flask_wtf import FlaskForm
from wtforms.fields import PasswordField,StringField,SubmitField,SelectField, choices
from wtforms.fields.simple import EmailField
from models.model import Produtos,Seller
from wtforms_sqlalchemy.fields import QuerySelectField

class LoginForm(FlaskForm):
    usuario = StringField("Usuario")
    email = EmailField("email")
    senha = PasswordField("Senha")
    submit = SubmitField("Entrar")








   
 


       



