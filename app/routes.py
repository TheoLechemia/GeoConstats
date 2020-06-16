from flask import Flask, render_template, flash, redirect, url_for, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from .env import DB
from app.models import Constats
from app.forms import LoginForm
from sqlalchemy import func
import json
from shapely.geometry import Point, shape
from shapely import wkb
from shapely.ops import transform
from geoalchemy2.shape import to_shape, from_shape

app = Flask(__name__)

app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://raph:Raphael18@localhost:5432/geoConstat"

with app.app_context():
    from .models import Constats
    from app.forms import LoginForm
    from .env import DB
    DB.init_app(app)
    Constats.query.all()


@app.route("/")
@app.route("/map")
def map():
    dataGeom = DB.session.query(Constats,func.ST_AsGeoJson(func.ST_Transform(Constats.the_geom_point,4326))).all()
    cnsts=[]
    for d in dataGeom:
        geojson=json.loads(d[1])
        dico={}
        dico['geometry']=geojson
        dico['properties']={}
        dico['properties']['id_constat']=d[0].id_constat
        dico['properties']['date_attaque']=d[0].date_attaque
        dico['properties']['date_constat']=d[0].date_constat
        dico['properties']['nom_agent1']=d[0].nom_agent1
        dico['properties']['nom_agent2']=d[0].nom_agent2
        dico['properties']['proprietaire']=d[0].proprietaire
        dico['properties']['type_animaux']=d[0].type_animaux
        dico['properties']['nb_victimes_mort']=d[0].nb_victimes_mort
        dico['properties']['nb_victimes_blesse']=d[0].nb_victimes_blesse
        dico['properties']['statut']=d[0].statut
        cnsts.append(dico)        
    return render_template('map.html', title='Map', Constats=cnsts)

@app.route('/form',methods=['GET', 'POST'])
def form():
    form = LoginForm()
    return render_template('add.html', title="Add_to_database", form=form )

@app.route('/add', methods=['GET', 'POST'])
def add():
    data=request.json
    p2154=DB.session.query(func.ST_AsGeoJson(func.ST_Transform(func.ST_SetSRID(func.ST_Point(data['geom']['lng'],data['geom']['lat']),4326),2154)))
    json2154=json.loads(p2154[0][0])
    constats = Constats(
        date_attaque=data['date_attaque'],
        date_constat=data['date_constat'],
        nom_agent1=data['nom_agent1'],
        nom_agent2=data['nom_agent2'],
        proprietaire=data['proprietaire'],
        type_animaux=data['type_animaux'],
        nb_victimes_mort=data['nb_victimes_mort'],
        nb_victimes_blesse=data['nb_victimes_blesse'],
        statut=data['statut'],
        the_geom_point=from_shape(Point(json2154['coordinates'][0],json2154['coordinates'][1]),srid=2154)
    )    
    DB.session.add(constats)
    DB.session.commit()
    return redirect(url_for('map'))

@app.route('/update/<idc>', methods=['GET', 'POST'])
def update(idc):
    dataGeom = DB.session.query(Constats,func.ST_AsGeoJson(func.ST_Transform(Constats.the_geom_point,4326))).filter(Constats.id_constat==idc).all()
    geojson=json.loads(dataGeom[0][1])
    dico={}
    dico['geometry']=geojson
    dico['properties']={}
    dico['properties']['id_constat']=dataGeom[0][0].id_constat
    dico['properties']['date_attaque']=dataGeom[0][0].date_attaque
    dico['properties']['date_constat']=dataGeom[0][0].date_constat
    dico['properties']['nom_agent1']=dataGeom[0][0].nom_agent1
    dico['properties']['nom_agent2']=dataGeom[0][0].nom_agent2
    dico['properties']['proprietaire']=dataGeom[0][0].proprietaire
    dico['properties']['type_animaux']=dataGeom[0][0].type_animaux
    dico['properties']['nb_victimes_mort']=dataGeom[0][0].nb_victimes_mort
    dico['properties']['nb_victimes_blesse']=dataGeom[0][0].nb_victimes_blesse
    dico['properties']['statut']=dataGeom[0][0].statut
    form = LoginForm()
    return render_template('update.html', title='Map',form=form,Constats=dico)

@app.route('/updateDB',methods=['GET', 'POST'])
def updateDB():
    data=request.json
    p2154=DB.session.query(func.ST_AsGeoJson(func.ST_Transform(func.ST_SetSRID(func.ST_Point(data['geom']['lng'],data['geom']['lat']),4326),2154)))
    json2154=json.loads(p2154[0][0])    
    #Remplacer add par update. Passer l'id_constat dans le python pour trouver la ligne à update
    cst=DB.session.query(Constats).filter(Constats.id_constat==data['id_constat']).one()
    print(cst)
    cst.date_attaque=data['date_attaque']
    cst.date_constat=data['date_constat']
    cst.nom_agent1=data['nom_agent1']
    cst.nom_agent2=data['nom_agent2']
    cst.proprietaire=data['proprietaire']
    cst.type_animaux=data['type_animaux']
    cst.nb_victimes_mort=data['nb_victimes_mort']
    cst.nb_victimes_blesse=data['nb_victimes_blesse']
    cst.statut=data['statut']
    cst.the_geom_point=from_shape(Point(json2154['coordinates'][0],json2154['coordinates'][1]),srid=2154)
    DB.session.commit()       
    return redirect(url_for('map'))
    
