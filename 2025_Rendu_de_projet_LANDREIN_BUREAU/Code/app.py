from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os
import subprocess
import traceback
import sys

app = Flask(__name__)
app.secret_key = "aorte_secret_key"

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'nii', 'nii.gz'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files or 'mode' not in request.form:
            flash("Fichier ou mode non spécifié.", "error")
            return redirect(request.url)

        file = request.files['file']
        mode = request.form['mode']

        if file.filename == '':
            flash("Nom de fichier vide.", "error")
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash("Format de fichier non supporté. Utilisez un .nii ou .nii.gz", "error")
            return redirect(request.url)

        filename = file.filename.replace(" ", "_")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(filepath)

        try:
            script = "reconstruction_avec_coupe.py" if mode == "avec" else "reconstruction_sans_coupe.py"
            python_exec = sys.executable or "python"
            result = subprocess.run([python_exec, script, filepath],
                                    capture_output=True, text=True, check=True)
            print("Sortie reconstruction :\n", result.stdout)
            flash("Modèle généré avec succès !", "success")
        except subprocess.CalledProcessError as e:
            flash(f"Erreur : {e}", "error")
            print(traceback.format_exc())

        return redirect(url_for('index'))
    return render_template('index2.html')

@app.route('/telecharger-stl')
def telecharger_stl():
    for name in ["aorte_poisson_lisse.stl", "aorte_poisson_coupe.stl"]:
        path = os.path.join("static", name)
        if os.path.exists(path):
            return send_file(path, as_attachment=True)
    flash("Aucun fichier STL généré pour le moment.", "error")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
