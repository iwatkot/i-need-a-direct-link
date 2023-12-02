import os
from flask import (
    Flask,
    request,
    redirect,
    url_for,
    render_template,
    flash,
    send_from_directory,
)
from werkzeug.utils import secure_filename


import src.globals as g

logger = g.Logger(__name__)
app = Flask(__name__)
app.secret_key = g.FLASK_KEY


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    logger.info("Upload of file started...")
    if "file" not in request.files:
        flash("No file was uploaded.")
        logger.error("No file was uploaded.")
        return redirect(url_for("index"))
    file = request.files["file"]
    if file.filename == "":
        flash("No file was selected.")
        logger.error("No file was selected.")
        return redirect(url_for("index"))
    if file:
        logger.info("File was uploaded successfully.")
        filename = secure_filename(file.filename)
        filename_with_number = g.get_file_number() + "_" + filename
        file.save(os.path.join(g.UPLOADS_DIR, filename_with_number))
        if (
            os.path.getsize(os.path.join(g.UPLOADS_DIR, filename_with_number))
            > 50000000
        ):
            flash("File is larger than 50 MB.")
            logger.error("File is larger than 50 MB.")
            try:
                os.remove(os.path.join(g.UPLOADS_DIR, filename_with_number))
            except OSError:
                pass
            return redirect(url_for("index"))
        logger.info(f"File was saved successfully with name: {filename_with_number}")
        file_id = g.save_id(filename_with_number)
        return redirect(
            url_for("uploaded", filename=filename_with_number, file_id=file_id)
        )
    return render_template("index.html")


@app.route("/uploaded/<filename>/<file_id>", methods=["GET"])
def uploaded(filename: str, file_id: str):
    return render_template("uploaded.html", filename=filename, file_id=file_id)


@app.route("/delete", methods=["GET"])
def delete_page():
    return render_template("delete.html")


@app.route("/delete", methods=["POST"])
def delete():
    file_id = request.form.get("fileId")
    g.delete_id(file_id)
    flash("File was deleted.")
    return redirect(url_for("index"))


@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    return send_from_directory(g.UPLOADS_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(port=80, host="0.0.0.0")
