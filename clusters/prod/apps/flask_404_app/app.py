from flask import Flask, render_template, make_response

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    response = make_response(render_template("404.html"), 404)
    
    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Content-Security-Policy"] = "default-src 'self'; style-src 'self';"
    
    return response

if __name__ == "__main__":
    # Debug disabled for production
    app.run(host="0.0.0.0", port=5000)
