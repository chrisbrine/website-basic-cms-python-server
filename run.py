from dotenv import load_dotenv

load_dotenv()

from server import app
from server import db

if __name__ == '__main__':
  app.run(debug=True, port=8000)
