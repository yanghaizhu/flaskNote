from  flask import Flask, render_template, request, url_for, redirect,make_response,json, jsonify
from  wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo


# define form model class 
class todoForm(FlaskForm):
    user_name = StringField(label='title', validators=[DataRequired("can not no data")])
    submit = SubmitField(label='submit')
                            
