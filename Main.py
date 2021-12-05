from Global import API, app # app is required for Gunicorn.

import views.Planner
import views.Dev

# Check out views.* for more.

if __name__ == "__main__":
    app.run(port=8080, debug=True)
