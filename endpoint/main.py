from endpoint import create_app, start_app

#create the flask app
app = create_app()

#Run the app
start_app(app,debug=True)