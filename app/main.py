from flask import Flask, request, jsonify, redirect
from app.storage import URLStore
from app.utils import generate_short_code, is_valid_url
from app.URLStore import URLStore 


app = Flask(__name__)
store = URLStore()

@app.route("/api/shorten", methods=["POST"])
def shorten():
    if not request.is_json:
        return jsonify({"error": "Expected JSON body"}), 400

    data = request.get_json()
    url = data.get("url", "").strip()

    if not url or not is_valid_url(url):
        return jsonify({"error": "Invalid URL"}), 400

    # Generate unique short code
    while True:
        code = generate_short_code()
        if not store.exists(code):
            break

    store.save(code, url)

    return jsonify({
        "short_code": code,
        "short_url": request.host_url + code
    }), 201

@app.route("/<short_code>", methods=["GET"])
def redirect_url(short_code):
    entry = store.get(short_code)
    if not entry:
        return jsonify({"error": "Short code not found"}), 404

    store.increment_clicks(short_code)
    return redirect(entry["url"])

@app.route("/api/stats/<short_code>", methods=["GET"])
def stats(short_code):
    entry = store.get(short_code)
    if not entry:
        return jsonify({"error": "Short code not found"}), 404

    return jsonify({
        "url": entry["url"],
        "clicks": entry["clicks"],
        "created_at": entry["created_at"].isoformat()
    })

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

# Return JSON for 404 and 500 errors instead of HTML
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500
@app.route("/", methods=["GET"])
def home():
    all_urls = []
    for code, data in store.get_all():
        all_urls.append({
            "short_code": code,
            "short_url": request.host_url + code,
            "long_url": data["url"],
            "clicks": data["clicks"],
            "created_at": data["created_at"].isoformat()
        })

    return jsonify(all_urls)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

