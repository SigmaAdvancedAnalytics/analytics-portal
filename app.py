from bokeh.embed import components
from flask import Flask, render_template
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

# initialise app
def create_app(figures):
	app = Flask(__name__)

	# add '/' app route
	@app.route('/')
	def index():

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
	    return encode_utf8(html)
	return app

# start the app
def start_app(app,debug):
	#0.0.0.0 is required due to how binding container ports to the host works
	app.run(debug=debug,host='0.0.0.0')
