from bokeh.embed import components
from flask import Flask, render_template, request
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from bokeh.plotting import figure
import hmac
import hashlib
import time


# CONFIG
#--------------------
ERROR_MSG = {
    'invalid_signature': 'Token signature is not valid.',
    'token_expired': 'Access token has expired.'
}

def sign(msg):
    secret = b"A9yMkZuMlvasdsdfdgkjasdblj"
    hash_gen = hmac.new(secret, msg.encode('utf-8'), hashlib.sha256)
    signature = hash_gen.hexdigest()

    return signature

def check_signature(msg, signature):
    return sign(msg) == signature  # TODO(mkeyhani): use digest_comparsion to pevent timing attacks

# initialise app
def create_app():
    app = Flask(__name__)

    # add '/' app route
    @app.route('/Test navy bokeh')
    def index():
        fig = figure(plot_width=600, plot_height=600)
        fig.vbar(
            x=[1, 2, 3, 4],
            width=0.5,
            bottom=0,
            top=[1.7, 2.2, 4.6, 3.9],
            color='navy'
        )
        #store required figures as a list
        figures = [fig,fig,fig]


        # grab the static resources
        js_resources = INLINE.render_js()
        css_resources = INLINE.render_css()


        # assign the dynamic resources
        jquery_draggable = "<script type='text/javascript'>$( function() {$('#fig{~}').resizable({grid:[10,10]}).draggable({containment:\"#dashboard\"});});</script>"
        plot_scripts = '' 
        plot_divs = ''
        for idx,fig in enumerate(figures):
            script,div = components(fig)
            plot_scripts = plot_scripts + jquery_draggable.replace('{~}',str(idx))
            plot_scripts = plot_scripts + script + '\n'
            div = div.replace('\"bk-root\"','\"bk-root\" id=\"fig{}\" style=\"width: 500px; height:500px; padding: 10px;\"').format(idx)
            plot_divs = plot_divs + div + '\n'
       
        # render template
        html = render_template(
            'index.html',
            js_resources=js_resources,
            plot_scripts=plot_scripts,
            css_resources=css_resources,
            plot_divs=plot_divs
        )

        signature = request.args.get('Signature')
        if not signature:
            return 'URL is not singend.'

        expiry = request.args.get('Expiry')
        if not expiry:
            return 'Expiry time not found.'
        if int(time.time()) > int(expiry):
            return ERROR_MSG['token_expired']

        # remove the signature from url
        url_without_signature = request.url[:request.url.find('&Signature=')]

        if check_signature(url_without_signature, signature):
            return encode_utf8(html)
        else:
            return ERROR_MSG['invalid_signature']


    @app.route('/Test yellow bokeh')
    def index2():
        fig = figure(plot_width=600, plot_height=600)
        fig.vbar(
            x=[1, 2, 3, 4],
            width=0.5,
            bottom=0,
            top=[1.7, 2.2, 4.6, 3.9],
            color='yellow'
        )
        #store required figures as a list
        figures = [fig,fig,fig]


        # grab the static resources
        js_resources = INLINE.render_js()
        css_resources = INLINE.render_css()


        # assign the dynamic resources
        jquery_draggable = "<script type='text/javascript'>$( function() {$('#fig{~}').resizable({grid:[10,10]}).draggable({containment:\"#dashboard\"});});</script>"
        plot_scripts = '' 
        plot_divs = ''
        for idx,fig in enumerate(figures):
            script,div = components(fig)
            plot_scripts = plot_scripts + jquery_draggable.replace('{~}',str(idx))
            plot_scripts = plot_scripts + script + '\n'
            div = div.replace('\"bk-root\"','\"bk-root\" id=\"fig{}\" style=\"width: 500px; height:500px; padding: 10px;\"').format(idx)
            plot_divs = plot_divs + div + '\n'
       
        # render template
        html = render_template(
            'index.html',
            js_resources=js_resources,
            plot_scripts=plot_scripts,
            css_resources=css_resources,
            plot_divs=plot_divs
        )

        signature = request.args.get('Signature')
        if not signature:
            return 'URL is not singend.'

        expiry = request.args.get('Expiry')
        if not expiry:
            return 'Expiry time not found.'
        if int(time.time()) > int(expiry):
            return ERROR_MSG['token_expired']

        # remove the signature from url
        url_without_signature = request.url[:request.url.find('&Signature=')]

        if check_signature(url_without_signature, signature):
            return encode_utf8(html)
        else:
            return ERROR_MSG['invalid_signature']

    return app

# start the app
def start_app(app,debug):
    #0.0.0.0 is required due to how binding container ports to the host works
    app.run(debug=debug,host='0.0.0.0')
