from Main import generate_sentences, construct_weighted_graph, read_and_parse
from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
graph = {}

with open("book-titles.txt", "r") as file:
    text_from_file = file.read().splitlines()
preprocessed_data = read_and_parse(text_from_file)
graph = construct_weighted_graph(preprocessed_data)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"txt"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=["POST"])
def upload_files():
    combined_text = []
    if "files[]" not in request.files:
        return redirect(request.url)
    files = request.files.getlist("files[]")
    for file in files:
        if file.filename == "":
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)
            with open(file_path, "r") as file:
                text_from_file = file.read().splitlines()
                combined_text.extend(text_from_file)
    preprocessed_data = read_and_parse(combined_text)
    global graph
    graph = construct_weighted_graph(preprocessed_data)

    return redirect(url_for("index"))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    num_sentences = int(request.form["num_sentences"])
    sentences = generate_sentences(graph, num_sentences)
    return render_template("index.html", sentences=sentences)


@app.route("/save", methods=["POST"])
def save():
    sentences = request.form["sentences"]
    with open("generated_text.txt", "w") as f:
        f.write(sentences)
    return "Text saved successfully in 'generated_text.txt'!"


if __name__ == "__main__":
    app.run(debug=True)
