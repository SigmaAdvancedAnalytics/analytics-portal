# Bokeh Flasker  
A tool for turning Bokeh figures into Flask apps simply and reliably.  
Currently creates a naive list of divs from the Bokeh graphs provided, but in future will integrate with interactive layout design tools.  

# Features  
[x] Creates and starts a Flask App on localhost:5000/  
[x] Accepts a list of Bokeh figures and generates the required Divs  
[ ] Compatibility with Bokeh server, callbacks and apps  
[ ] Compatibility with layout design tool (undecided, maybe Gridster or Razzle)  

# Setup
* Clone repository
* (From inside repository) run:   
	`docker build -t bokeh_flasker .`
* Run:  
 `docker run --rm -it -p 5000:5000 -v ${PWD}:/home bokeh_flasker /bin/bash -c "python /home/main.py"`  
* Check localhost:5000




