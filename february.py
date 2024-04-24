import logging
import requests
from flask import Flask, Response, request
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/image-proxy')
def image_proxy():
    url = request.args.get('url')

    if not url:
        return Response("Missing 'url' parameter", status=400)

    # Fetch the image from the URL
    try:
        logger.info(f"Fetching image from URL: {url}")
        response = requests.get(url)

        # Check if the response is successful and contains an image
        if response.status_code == 200 and response.headers.get('Content-Type', '').startswith('image'):
            return Response(response.content, mimetype=response.headers['Content-Type'])
        else:
            logger.error(f"Failed to fetch image from URL: {url}, status code: {response.status_code}, Content-Type: {response.headers.get('Content-Type')}")
            return Response("Failed to fetch image from URL", status=response.status_code)

    except Exception as e:
        logger.exception(f"Error fetching image from URL: {url}, error: {e}")
        return Response("Error fetching image", status=500)


if __name__ == '__main__':
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # Run the app using gunicorn server
    logger.info("Starting image proxy server...")
    app.run(host='0.0.0.0', port=7507)
