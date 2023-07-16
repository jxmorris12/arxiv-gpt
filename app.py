import json
import os
import random
import requests
import sqlite3

from flask import Flask, render_template
from topics import TOPICS

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.template_folder = 'templates'  # This assumes your templates are stored in a 'templates' folder in your project directory

@app.route("/")
def home():
    paper_ids = user_cursor.execute("SELECT * FROM saved_papers").fetchall()
    paper_ids = [paper_id for id, paper_id in paper_ids]
    print(paper_ids)
    return render_template('home.html', paper_ids=paper_ids)

@app.route("/authors")
def authors():
    # sample doc:
    cursor.execute("SELECT * FROM authors ORDER BY RANDOM() LIMIT 50")
    objects = cursor.fetchall()
    authors = [{ "name": obj[1].strip("_").replace("__", ", "), "titles": obj[2]} for obj in objects]
    print(authors)
    return render_template('authors.html', authors=authors)

@app.route("/topics")
def topics():
    # sample doc:
    base_colors = ["slate",  "red", "orange", "amber", "lime", "teal", "sky", "indigo", "violet", "purple", "fuchsia", "pink", "rose"]
    colors = base_colors
    while len(colors) < len(TOPICS):
        colors += base_colors
    colors = random.sample(colors, k=len(TOPICS))
    return render_template('topics.html', topics=zip(colors, TOPICS))

@app.route("/papers")
def papers():
    # sample doc:
    # (68748, '2019-12-03', '{"id": "1912.00466", "submitter": "Nupur Kumari", "authors": "Tejus Gupta, Abhishek Sinha, Nupur Kumari, Mayank Singh, Balaji\\n  Krishnamurthy", "title": "A Method for Computing Class-wise Universal Adversarial Perturbations", "comments": null, "journal-ref": null, "doi": null, "report-no": null, "categories": "cs.LG cs.CR cs.CV stat.ML", "license": "http://arxiv.org/licenses/nonexclusive-distrib/1.0/", "abstract": "  We present an algorithm for computing class-specific universal adversarial\\nperturbations for deep neural networks. Such perturbations can induce\\nmisclassification in a large fraction of images of a specific class. Unlike\\nprevious methods that use iterative optimization for computing a universal\\nperturbation, the proposed method employs a perturbation that is a linear\\nfunction of weights of the neural network and hence can be computed much\\nfaster. The method does not require any training data and has no\\nhyper-parameters. The attack obtains 34% to 51% fooling rate on\\nstate-of-the-art deep neural networks on ImageNet and transfers across models.\\nWe also study the characteristics of the decision boundaries learned by\\nstandard and adversarially trained models to understand the universal\\nadversarial perturbations.\\n", "versions": [{"version": "v1", "created": "Sun, 1 Dec 2019 18:22:14 GMT"}], "update_date": "2019-12-03", "authors_parsed": [["Gupta", "Tejus", ""], ["Sinha", "Abhishek", ""], ["Kumari", "Nupur", ""], ["Singh", "Mayank", ""], ["Krishnamurthy", "Balaji", ""]]}')
    cursor.execute("SELECT * FROM documents ORDER BY RANDOM() LIMIT 50")
    objects = cursor.fetchall()
    papers = [json.loads(obj[2]) for obj in objects]
    return render_template('papers.html', papers=papers)

@app.route('/save/paper/<string:paper_id>', methods=['POST'])
def save_paper(paper_id: str):
    # Perform the POST request
    response = requests.post('http://example.com/your-post-endpoint', data={'id': paper_id})

    user_cursor.execute("INSERT OR IGNORE INTO saved_papers (paper_id) VALUES (?)", (paper_id,))
    user_conn.commit()

    print("saved paper", paper_id)

    # Check the response and return a result
    if response.status_code == 200:
        return 'POST request successful'
    else:
        return 'POST request failed'

if __name__ == '__main__':
    data_folder = '/Users/johnmorris/arxiv-gpt/data/'

    # data database
    conn = sqlite3.connect(
        os.path.join(data_folder, 'database.db'), check_same_thread=False
    )
    cursor = conn.cursor()

    # user database
    user_conn = sqlite3.connect(
        os.path.join(data_folder, 'user.db'), check_same_thread=False
    )
    user_cursor = conn.cursor()
    user_cursor.execute('''CREATE TABLE IF NOT EXISTS saved_papers
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    paper_id TEXT)''')


    app.run(debug=True, port=8001)
    conn.close()