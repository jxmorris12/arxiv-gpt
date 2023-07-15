from flask import Flask, render_template

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.template_folder = 'templates'  # This assumes your templates are stored in a 'templates' folder in your project directory

@app.route("/")
def hello_world():
    print("calling render template")
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)