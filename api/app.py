from flask import Flask, Response, request
from PIL import Image
from io import BytesIO

app = Flask(__name__)


def hex_2_rgb(h):
    if len(h) == 3:
        h = h + h
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def generate(width, height, color):
    if width>5000 or height>5000:
        raise Exception("No")
    try:
        c = hex_2_rgb(color)
    except:
        c = color
    im = Image.new("RGB", (width, height), c)
    fobj = BytesIO()
    im.save(fobj, "JPEG")
    return fobj


def image_response(width, height, color):
    try:
        b: BytesIO = generate(width, height, color)
    except:
        return "An error occured"
    return Response(
        b.getvalue(),
        headers={
            "content-type": "image/jpg",
            "content-disposition": 'inline; filename="filename.jpg"',
            "Cache-Control": "s-maxage=31536000, max-age=31536000, immutable",
        },
    )


@app.route("/<color>/<int:width>/<int:height>/", strict_slashes=False)
def all_params(color, width, height):
    return image_response(width, height, color)


@app.route("/<int:width>/<int:height>/", strict_slashes=False)
def dimensions(width, height):
    color = "black"
    return image_response(width, height, color)


@app.route("/")
@app.route("/<color>/", strict_slashes=False)
def color_only(color="black"):
    width = 150
    height = 150
    return image_response(width, height, color)


@app.route("/favicon.ico")
def no():
    return ""


@app.errorhandler(500)
def error_handler(e):
    return {"error": "An unknown error occured", "tb": f"{e}"}


@app.after_request
def cors(resp):
    resp.headers["access-control-allow-origin"] = request.headers.get("origin", "*")
    resp.headers["access-control-max-age"] = "86400"

    return resp


if __name__ == "__main__":
    app.run(debug=True)
