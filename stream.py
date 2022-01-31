import io
import secrets
import pyautogui
from flask import Flask, Response, render_template_string, send_file, request, redirect, url_for, make_response

app = Flask(__name__)
tokens = []


@app.route("/")
def index():
    return render_template_string("""<html>
        <head>
            <title>Log in</title>
        </head>
        <style>
            body{
                display: flex;
                justify-content: center;
                align-items: center;
            }
            
            form {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }
            
            input {
                margin: 10px;
            }
        </style>
        <body>
            <form method="POST" action="{{ url_for("auth") }}">
              <label for="password">Password:</label>
              <input type="password" id="password" name="password">
              <input type="submit" value="Continue">
            </form>
        </body>
    </html>""")


@app.route("/auth", methods=["POST"])
def auth():
    password = request.form.get("password")
    if password and password == "1667":
        token = secrets.token_urlsafe(20)
        tokens.append(token)
        resp = make_response(redirect(url_for("main")))
        resp.set_cookie("token", token)
        return resp
    return redirect(url_for("index"))


@app.route("/stream")
def main():
    token = request.cookies.get("token")
    if token and token in tokens:
        return render_template_string("""<html>
        <head>
            <title>Stream</title>
            <meta name="viewport" content="user-scalable=no,initial-scale=1.0,maximum-scale=1.0" />
            <meta name="apple-mobile-web-app-capable" content="yes" />
            <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
            <meta name="apple-mobile-web-app-title" content="Stream">
            <link rel="apple-touch-icon" href="icon">
            <link rel="icon" href="icon">
        </head>

        <style>
            * {
                margin: 0;
            }

            img {
                width: 100%;
                max-height: 100%;
            }

            body {
                background-color: black
            }
        </style>

        <body>
            <img src="{{ url_for("stream") }}">
        </body>
    </html>""")
    else:
        return redirect(url_for("index"))


@app.route("/stream/live")
def stream():
    token = request.cookies.get("token")
    if token and token in tokens:
        return Response(image(), mimetype="multipart/x-mixed-replace; boundary=frame")
    else:
        return redirect(url_for("index"))


@app.route("/icon")
def icon():
    return send_file("icon.png")


def image():
    while True:
        buffer = io.BytesIO()
        pyautogui.screenshot().save(buffer, format="jpeg")
        yield b'--frame\r\nContent-type: image/jpeg\r\n\r\n' + buffer.getvalue() + b"\r\n"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
