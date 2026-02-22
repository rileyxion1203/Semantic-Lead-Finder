"""
app.py — Semantic Lead Finder (powered by Exa API)
Run: python3 app.py
Open: http://localhost:5001
"""

import os
import csv
import io
from flask import Flask, request, jsonify, send_file, render_template_string
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

with open(os.path.join(os.path.dirname(__file__), "index.html")) as f:
    HTML = f.read()


@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/api/status")
def status():
    key = os.getenv("EXA_API_KEY", "")
    return jsonify({"ready": bool(key), "mode": "exa_api"})


@app.route("/api/search")
def search():
    query = request.args.get("q", "").strip()
    num = int(request.args.get("top", 10))
    if not query:
        return jsonify({"error": "No query provided"}), 400
    try:
        from exa_search import search_companies
        results = search_companies(query, num_results=num)
        return jsonify({"results": results, "query": query})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/export")
def export():
    query = request.args.get("q", "").strip()
    num = int(request.args.get("top", 50))
    if not query:
        return jsonify({"error": "No query"}), 400
    from exa_search import search_companies
    results = search_companies(query, num_results=num)
    buf = io.StringIO()
    fields = ["rank", "title", "url", "highlight", "published_date"]
    writer = csv.DictWriter(buf, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(results)
    buf.seek(0)
    return send_file(
        io.BytesIO(buf.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name=f"leads_{query[:30].replace(' ','_')}.csv"
    )


if __name__ == "__main__":
    print("\n🔍 Semantic Lead Finder — powered by Exa API")
    print("   Open: http://localhost:5001\n")
    app.run(debug=False, port=5001)
