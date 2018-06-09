from flask_wtf import Form
from wtforms import TextField, SubmitField

class SearchForm(Form):
    keyword = TextField("Input keyword")
    submit = SubmitField("Search")

