from flask import Flask, request, render_template, session
from flask_session import Session
from SPARQL_queries import create_df_level1, create_map_level1
from SPARQL_queries import create_df_level2_label, create_map_level2_label, create_abstract_level2_label
from SPARQL_queries import create_df_level2_name, create_map_level2_name, create_abstract_level2_name

# activate virtual env: venv\Scripts\activate.bat

# set variables in terminal:
# set FLASK_APP=app.py
# set FLASK_ENV=development

# to start the app, run "python app.py" or "flask run" in your terminal


app = Flask(__name__, template_folder="./Templates")
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)


@app.route("/")
def level1():
    return render_template('level1.html')


@app.route("/", methods=['POST'])
def level1_post():
    if "somebodys_label" in request.form:
        if "latitude" in request.form and request.form['latitude'] != "":
            session['latitude'] = request.form['latitude']
        if "longitude" in request.form and request.form['longitude'] != "":
            session['longitude'] = request.form['longitude']
        if request.form['somebodys_label'] != "":
            session['somebodys_label'] = request.form['somebodys_label']
            somebodys_label = session['somebodys_label']
            latitude = session['latitude']
            longitude = session['longitude']
            df = create_df_level2_label(somebodys_label, current_latitude=latitude, current_longitude=longitude)
            somebodys_name = df.loc[0, 'Person']
            df.drop(['x', 'Person'], axis=1, inplace=True)
            abstract = create_abstract_level2_label(somebodys_label, somebodys_name)
            _map = create_map_level2_label(somebodys_label)
        else:
            session['somebodys_name'] = request.form['somebodys_name']
            somebodys_name = session['somebodys_name']
            somebodys_label = ""
            latitude = session['latitude']
            longitude = session['longitude']
            df = create_df_level2_name(somebodys_name, current_latitude=latitude, current_longitude=longitude)
            df.drop(['x'], axis=1, inplace=True)
            abstract = create_abstract_level2_name(somebodys_name)
            _map = create_map_level2_name(somebodys_name)
        return render_template('level2.html',
                               latitude=latitude,
                               longitude=longitude,
                               somebody=somebodys_label,
                               somebodys_name=somebodys_name,
                               abstract=abstract,
                               column_names=df.columns.values,
                               row_data=list(df.values.tolist()),
                               zip=zip,
                               _map=_map)
    else:
        session['latitude'] = request.form['latitude']
        session['longitude'] = request.form['longitude']
        session['radius'] = request.form['radius']
        if session['radius'] == "":
            session['radius'] = '10'
        latitude = session['latitude']
        longitude = session['longitude']
        radius = session['radius']
        df = create_df_level1(latitude=latitude, longitude=longitude, radius=radius, limit='2000')
        df.drop(['x'], axis=1, inplace=True)
        _map = create_map_level1(latitude=latitude, longitude=longitude, radius=radius, limit='2000')
        return render_template('level1.html',
                               latitude=latitude,
                               longitude=longitude,
                               radius=radius,
                               string="You have entered the coordinates (" + latitude + ", " + longitude
                                      + ") and the radius " + radius + " km.",
                               column_names=df.columns.values,
                               row_data=list(df.values.tolist()),
                               link_column="Further Results",
                               zip=zip,
                               _map=_map)


@app.route("/level2")
def level2():
    try:
        latitude = session['latitude']
        longitude = session['longitude']
    except:
        latitude = ""
        longitude = ""
    somebodys_name = "somebody"
    return render_template('level2.html',
                           latitude=latitude,
                           longitude=longitude,
                           somebodys_name=somebodys_name)


@app.route("/level2", methods=['POST'])
def level2_post():
    if "latitude" in request.form and request.form['latitude'] != "":
        session['latitude'] = request.form['latitude']
    if "longitude" in request.form and request.form['longitude'] != "":
        session['longitude'] = request.form['longitude']
    if request.form['somebodys_label'] != "":
        session['somebodys_label'] = request.form['somebodys_label']
        somebodys_label = session['somebodys_label']
        latitude = session['latitude']
        longitude = session['longitude']
        df = create_df_level2_label(somebodys_label, current_latitude=latitude, current_longitude=longitude)
        somebodys_name = df.loc[0, 'Person']
        df.drop(['x', 'Person'], axis=1, inplace=True)
        abstract = create_abstract_level2_label(somebodys_label, somebodys_name)
        _map = create_map_level2_label(somebodys_label)
    else:
        session['somebodys_name'] = request.form['somebodys_name']
        somebodys_name = session['somebodys_name']
        somebodys_label = ""
        latitude = session['latitude']
        longitude = session['longitude']
        df = create_df_level2_name(somebodys_name, current_latitude=latitude, current_longitude=longitude)
        df.drop(['x'], axis=1, inplace=True)
        abstract = create_abstract_level2_name(somebodys_name)
        _map = create_map_level2_name(somebodys_name)
    return render_template('level2.html',
                           latitude=latitude,
                           longitude=longitude,
                           somebody=somebodys_label,
                           somebodys_name=somebodys_name,
                           abstract=abstract,
                           column_names=df.columns.values,
                           row_data=list(df.values.tolist()),
                           zip=zip,
                           _map=_map)


if __name__ == "__main__":
    app.run(debug=True)
