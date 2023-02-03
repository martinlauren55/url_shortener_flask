import pathlib
from flask import Flask, render_template, url_for, request, redirect

from lib.libs import Config, CheckUrl
from lib.yaml_lib import YamlManager
from lib.db_manager import DB_Manager
from lib import export_data_yml_to_redis as exp_data


current_dir = pathlib.Path.cwd()

conf = Config(pathlib.Path(current_dir, "pref.json"))
yaml_manager = YamlManager(path=pathlib.Path("data", conf.name_yaml_bd))

if conf.storage == 'redis':
    exp_data.export_data(yaml_manager, conf)


db = DB_Manager(config_class=conf, yaml_manager_class=yaml_manager)

app = Flask(__name__)


def add_link(value, method):
    key = db.unique_link(generate_method=method)
    db.save(key=key, value=value)
    return {'key': key, 'value': value}


# Home
@app.route('/', methods=['POST', 'GET'])
def index():
    all_links = {}
    if db.get_keys():
        for key in db.get_keys():
            all_links.update({key: db.get_by_key(key)})

    if request.method == "POST":
        value = request.form['full_link']

        if db.value_exists(value):
            key = db.value_exists(value)
            primary_div = True
            return render_template("index.html",
                                   all_links=all_links,
                                   primary_div=primary_div,
                                   key=key,
                                   domen_name=conf.domen_name)
        else:
            check = CheckUrl(value)
            if check.is_link:
                primary_div = True
                new_link = add_link(value=request.form['full_link'], method=request.form['generate_method'])
                return render_template("index.html",
                                       all_links=all_links,
                                       primary_div=primary_div,
                                       key=new_link['key'],
                                       domen_name=conf.domen_name)
            else:
                danger_div = True
                return render_template("index.html",
                                       value=value,
                                       all_links=all_links,
                                       danger_div=danger_div)

    else:
        short_link_div = False
        return render_template("index.html",
                               all_links=all_links,
                               short_link_div=short_link_div)


# Redirect by short link
@app.route('/<string:key>')
def redirecting(key):
    if db.key_exist(key):
        value = db.get_by_key(key)
        return render_template("redirect.html", value=value)
    else:
        return render_template('404.html')


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')
