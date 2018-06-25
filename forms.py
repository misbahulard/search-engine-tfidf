from flask_wtf import Form
from wtforms import TextField, SubmitField

class SearchForm(Form):
    """Search Form for searching purpose"""
    
    keyword = TextField("Input keyword")
    submit = SubmitField("Search")
