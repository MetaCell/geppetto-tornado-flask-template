from flask import Blueprint
from flask import Flask, send_from_directory, jsonify, render_template

pygeppetto_core = Blueprint('pygeppetto_core', __name__, template_folder='org.geppetto.frontend/src/main/webapp/build')
pygeppetto_core.debug = True
# pygeppetto_core.config['ERROR_404_HELP'] = False


# @pygeppetto_core.errorhandler(404)
# def page_not_found(e):
#     return jsonify(error=404, text="The requested URL was not found on the server"), 404


@pygeppetto_core.route('/')
def geppetto(name=None):
    print("Serving Geppetto Page")
    return render_template('geppetto.vm')