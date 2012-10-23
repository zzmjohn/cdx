from flask import (
    render_template, request, current_app,
    send_from_directory, make_response)
import flask
import os
import logging
import uuid
import urlparse

from cdx.app import app

import cdx.bbmodel as bbmodel
import cdx.wsmanager as wsmanager
import cdx.models.user as user
import cdx.models.docs as docs
import cdx.models.convenience as mconv
import cdx.controllers.maincontroller as maincontroller
from cdx.settings import ENV

#main pages

# @app.route('/cdx/')
# @app.route('/cdx/<path:unused>/')
# def index(*unused_all, **kwargs):
#     current_user = mconv.from_wakari(current_app, request)
#     if current_user is None:
#         #redirect to login, we don't have login page yet..
#         pass
#     return render_template('cdx.html', NODE_INSTALLED=False)

# @app.route('/cdx_help')
# @app.route('/cdx_help/<path:unused>/')
# def cdx_help(*unused_all, **kwargs):
#     current_user = mconv.from_wakari(current_app, request)
#     if current_user is None:
#         #redirect to login, we don't have login page yet..
#         pass
#     return render_template('cdx_help.html')

@app.route('/cdx/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/x-icon')

@app.route('/cdx/userinfo/')
def get_user():
    user = mconv.from_wakari(current_app, request)
    return current_app.ph.serialize_web(user.to_public_json())

if not ENV.DEBUG:
    print 'not ENV.DEBUG'
    FS_ROOT = "/user_home/"
else:
    print 'ENV DEBUG'
    FS_ROOT = "/tmp/"


def _write_plot_file(username, homedir, docid, apikey, url):
    fpath = os.path.join(homedir, 'scripts', 'wkplot.py')
    with open(fpath, 'w+') as f:
        f.write("from cdxlib import plot\n")
        clientcode = "p = plot.PlotClient('%s', '%s', '%s')\n"
        clientcode = clientcode % (docid, url, apikey)
        f.write(clientcode)
    if ENV.USE_CHMOD:
        os.system("sudo chown %s  %s " % (username, fpath))
                
def write_plot_file(docid, apikey, url):
    try:
        session = app.Session()
        authuser, wakuser = mconv.get_current_user(session, request)
        username = authuser.username
        homedir = os.path.join(FS_ROOT, username)
        _write_plot_file(username, homedir, docid, apikey, url)
    finally:
        session.close()
    
@app.route('/cdx/cdxinfo/<docid>')
def get_cdx_info(docid):
    doc = docs.Doc.load(app.model_redis, docid)
    user = mconv.from_wakari(current_app, request)
    if not ((user.username in doc.rw_users) or (user.username in doc.r_users)):
        return null
    plot_context_ref = doc.plot_context_ref
    all_models = current_app.collections.get_bulk(docid)
    all_models = [x.to_broadcast_json() for x in all_models]
    returnval = {'plot_context_ref' : plot_context_ref,
                 'docid' : docid,
                 'all_models' : all_models,
                 'apikey' : doc.apikey}
    returnval = current_app.ph.serialize_web(returnval)
    write_plot_file(docid, doc.apikey, "https://" + request.host)
    return returnval
