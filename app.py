import json
import os
import sqlite3

from flask import Flask, render_template

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.template_folder = 'templates'  # This assumes your templates are stored in a 'templates' folder in your project directory

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/authors")
def authors():
    # sample doc:
    cursor.execute("SELECT * FROM authors ORDER BY RANDOM() LIMIT 5")
    objects = cursor.fetchall()
    authors = [{ "name": obj[1].strip("_").replace("__", ", "), "titles": obj[2]} for obj in objects]
    print(authors)
    return render_template('authors.html', authors=authors)

@app.route("/papers")
def papers():
    # sample doc:
    # (68748, '2019-12-03', '{"id": "1912.00466", "submitter": "Nupur Kumari", "authors": "Tejus Gupta, Abhishek Sinha, Nupur Kumari, Mayank Singh, Balaji\\n  Krishnamurthy", "title": "A Method for Computing Class-wise Universal Adversarial Perturbations", "comments": null, "journal-ref": null, "doi": null, "report-no": null, "categories": "cs.LG cs.CR cs.CV stat.ML", "license": "http://arxiv.org/licenses/nonexclusive-distrib/1.0/", "abstract": "  We present an algorithm for computing class-specific universal adversarial\\nperturbations for deep neural networks. Such perturbations can induce\\nmisclassification in a large fraction of images of a specific class. Unlike\\nprevious methods that use iterative optimization for computing a universal\\nperturbation, the proposed method employs a perturbation that is a linear\\nfunction of weights of the neural network and hence can be computed much\\nfaster. The method does not require any training data and has no\\nhyper-parameters. The attack obtains 34% to 51% fooling rate on\\nstate-of-the-art deep neural networks on ImageNet and transfers across models.\\nWe also study the characteristics of the decision boundaries learned by\\nstandard and adversarially trained models to understand the universal\\nadversarial perturbations.\\n", "versions": [{"version": "v1", "created": "Sun, 1 Dec 2019 18:22:14 GMT"}], "update_date": "2019-12-03", "authors_parsed": [["Gupta", "Tejus", ""], ["Sinha", "Abhishek", ""], ["Kumari", "Nupur", ""], ["Singh", "Mayank", ""], ["Krishnamurthy", "Balaji", ""]]}')
    cursor.execute("SELECT * FROM documents ORDER BY RANDOM() LIMIT 5")
    objects = cursor.fetchall()
    papers = [json.loads(obj[2]) for obj in objects]
    return render_template('papers.html', papers=papers)

if __name__ == '__main__':
    data_folder = '/Users/johnmorris/arxiv-gpt/data/'
    conn = sqlite3.connect(
        os.path.join(data_folder, 'database.db'), check_same_thread=False
    )
    cursor = conn.cursor()
    app.run(debug=True)
    conn.close()