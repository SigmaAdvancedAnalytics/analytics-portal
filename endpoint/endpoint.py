from bokeh.embed import components
from flask import Flask, render_template, request
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

import json
import urllib
import pickle
import hashlib
import hmac
import time


# CONIFG
TOKEN_LIFETIME = 20 # in seconds



def sign(msg):
    secret = b"A9yMkZuMlvasdsdfdgkjasdblj"
    hash_gen = hmac.new(secret, msg.encode('utf-8'), hashlib.sha256)
    signature = hash_gen.hexdigest()

    return signature

# initialise app
def create_app():
    app = Flask(__name__)

    # add '/' app route
    @app.route('/get_report_url', methods=['POST'])
    def get_report_url():
        def get_ticket_id():
            # TODO(mkeyhani): get trusted ticket
            return "1"

        # CONFIG
        #----------------------------------------------------
        TABLEAU_URL = "https://reports.org"

        # Base URLs for different results generators
        BASE_URLS = {
            'tableau' : "https://reports2.org",
            'bokeh' : "http://gitlab.services"
        }

        # Used for building the report subtitle
        DISCLAIMER = ""
        OLD_ALIGNMENT_MESSAGE = ""


        # Post request parameters
        for_ipad = request.values.get('for_ipad')
        report_doc_code = request.values.get('report_doc_code')
        username = request.values.get('username')
        user_role = '' # TODO(mkeyhani): grab this

        report_name = request.values.get('report_name')
        report_height = request.values.get('report_height')
        report_width = request.values.get('report_width')
        report_generator = request.values.get('report_generator')
        workbook = request.values.get('workbook')
        sheet = request.values.get('sheet')
        season = int(request.values.get('season'))


        print(report_generator)
         # Build the report URL
        if report_generator == 'tableau':
            url_params = {
                'tableau_base_url': TABLEAU_URL,
                'username': username,
                'workbook': workbook,
                'sheet': sheet,
                'ticket_id': get_ticket_id()
            }

            report_url_tmp = "{tableau_base_url}/views/{workbook}/{sheet}?&:embed=yes&:toolbar=top"
        
            if (season >=2018):
                subtitle = DISCLAIMER
            else:
                subtitle = DISCLAIMER + ' ' + OLD_ALIGNMENT_MESSAGE

        elif report_generator == 'bokeh':
            url_params = {.kenna.local
                'base_url': 'http://reports.services',
                #'base_url': 'http://gitlab.services', 
                'report_name': report_name,
                'expiry': int(time.time()) + TOKEN_LIFETIME
            }
            report_url_tmp = "{base_url}/{report_name}?Expiry={expiry}"
            subtitle = "something"

        report_url = report_url_tmp.format(**url_params)
        # Add Signature
        report_url += '&Signature=%s' % sign(report_url)
        
       #url_tmp = "{tableau_url}/trusted/{ticket_id}/views/{workbook}/{sheet}?&:embed=yes&:toolbar=top"
        # report_html = urllib.request.urlopen(url).read()
        
        # TODO(mkeyhani): this may be better done in the template
        # Build the subtitle 

        html = render_template('report.html',
            report_name=report_name,
            subtitle=subtitle,
            report_url=report_url,
            report_width=report_width,
            report_height=report_height
        ) 

        headers = {
            'Cache-Control': 'NoCache',
            'Content-Type': 'Text/Plain; charset=utf-8'
        }

        return encode_utf8(html), 200, headers
    return app


# start the app
def start_app(app,debug):
    #0.0.0.0 is required due to how binding container ports to the host works
    app.run(debug=debug,host='0.0.0.0')
