import pandas as pd
import folium
from folium.plugins import MarkerCluster

import sqlite3

from flask import Flask, request, render_template, url_for 
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        conn = sqlite3.connect('restau.db')
        df = pd.read_csv('fooding.csv')
        df.to_sql('restau', conn, if_exists='replace', index=False)
        code_postal = request.form.get('code_postal')
        cuisine = request.form.get('cuisine').strip()
        prix = request.form.get('prix')
        print(cuisine, prix, code_postal)

        cur = conn.cursor()
        cur.execute("SELECT * FROM restau WHERE cp ='{}' and prix = '{}' and specialite1 = '{}' or specialite2 = '{}' or specialite3 = '{}'".format(code_postal, prix, cuisine,cuisine,cuisine))
        rows = cur.fetchall()
        print(rows)
        new_df = pd.DataFrame(rows, columns=['Nom','Type','CP', 'Adresse', 'Latitude', 'Longitude', 'Telephone','Prix', 'Specialite1', 'Specialite2', 'Specialite3'])

        rest_map = folium.Map(location=[48.8,2.35],zoom_start=10, tiles='OpenStreetMap')

        marker_cluster = folium.plugins.MarkerCluster().add_to(rest_map)

        for i in new_df.index:
            marker = folium.Marker(location=(round(new_df['Latitude'].loc[i],6),round(new_df['Longitude'].loc[i],6)), popup=(str(new_df['Nom'].loc[i]) +' ||| '+'Telephone'+str(new_df['Telephone'].loc[i],))).add_to(marker_cluster)

        rest_map.save('templates/new_carte.html')
        return render_template('new_carte.html')
    return render_template('home.html') 










