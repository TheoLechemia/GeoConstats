from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, DateField, SubmitField
from app.models import Constats
from .env import DB
from wtforms.validators import DataRequired
from shapely.geometry import point,polygon,linestring,asShape
from geoalchemy2.shape import from_shape

class LoginForm(FlaskForm):
    date = DateField('date')
    nbVictimes = IntegerField('nbVictimes')
    moment = StringField('moment')
    chien = BooleanField('chien')
    berger = BooleanField('berger')
    valide = StringField('valide')
    submit = SubmitField('Add to database')

    def validate_valide(self, valide):
        constats = Constats.query.filter_by(valide=valide.data).first()
        if constat is not None:
            raise ValidationError('Please use a different surname.')
    
    def validate_nbVictimes(self, nbVictimes):
        constats = Constats.query.filter_by(nbVictimes=nbVictimes.data).first()
        if constats is not None:
            raise ValidationError('Please use a different email address.')
                
    def validate_date(self, moment):
        constats = Constats.query.filter_by(moment=moment.data).first()
        if constats is not None:
            raise ValidationError('Please use a different name address.')
    def validate_date(self, date):
        constats = Constats.query.filter_by(date=date.data).first()
        if constats is not None:
            raise ValidationError('Please use a different name address.')    
