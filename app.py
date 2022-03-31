from flask import Flask, render_template, request
import json
import os
import requests

app = Flask(__name__)

URL = "http://0.0.0.0:8080"

@app.route("/")
def home():
    resp = requests.get(URL + "/api/image/")
    print(resp.json())
    if resp.status_code == 200:
        return render_template("home.html", resp=resp.json())
    else:
        return render_template("home.html")


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "GET":
        return render_template("add_image.html")
    else:
        file = []
        images = request.files.to_dict(flat=False)
        for image in images["files"]:
            # print(image)
            image.seek(0)
            file.append(("files", (image.filename, image.read(), image.content_type)))

        data = {
            "message": request.form.get("message"),
            # "tags": request.form.get("tags"),
            "tag": request.form.get("tags"),
        }
        resp = requests.post(
            URL + "/api/image/",
            data=data,
            files=file,
        )

        print(json.dumps(resp.json(), indent=4, sort_keys=True))

        return render_template("add_image.html")


if __name__ == "__main__":
    server_port = os.environ.get("PORT", "8000")
    app.run(debug=False, port=server_port, host="0.0.0.0")
