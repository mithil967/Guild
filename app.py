import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from bot_worker import bot

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-this-before-deploy")

def authorized():
    return bool(session.get("authorized"))

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    if request.method == "POST":
        password = request.form.get("password", "")
        expected = os.environ.get("ADMIN_PASSWORD", "")
        if not expected:
            error = "ADMIN_PASSWORD environment variable is not configured."
        elif password and password == expected:
            session["authorized"] = True
            return redirect(url_for("dashboard"))
        else:
            error = "Incorrect password."
    if authorized():
        return redirect(url_for("dashboard"))
    return render_template("login.html", error=error)

@app.route("/dashboard")
def dashboard():
    if not authorized():
        return redirect(url_for("index"))
    return render_template("dashboard.html")

@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.get("/api/status")
def status():
    if not authorized():
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(bot.status())

@app.post("/api/start")
def start_bot():
    if not authorized():
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json(silent=True) or {}
    label = str(data.get("label", "Demo run"))[:60]
    bot.start(label)
    return jsonify({"ok": True, "status": bot.status()})

@app.post("/api/stop")
def stop_bot():
    if not authorized():
        return jsonify({"error": "Unauthorized"}), 401
    bot.stop()
    return jsonify({"ok": True, "status": bot.status()})

@app.get("/health")
def health():
    return jsonify({"ok": True, "service": "Guild Bot Dashboard"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "10000")))
