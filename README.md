## Project Highlights

- Developed and implemented a relational database schema with SQLite to manage moviemedia, movies, platforms, genres, cast, creators, writers, and user interactions.
- Built a fully functional RESTful API system using Django Rest Framework (DRF) for media content operations.
- Enforced API security with token-based authentication, custom permissions, throttling, and pagination.
- Integrated dynamic filtering, searching, and ordering to enhance API usability.
- Integrated Cloudinary to decouple media file handling, enabling scalable delivery and reducing backend load.
- Used Django Debug Toolbar and Django Silk to detect and optimize slow or duplicate database queries.
- Implemented signals to automate creation of user profiles and dashboards on registration.
- Optimized performance through caching and minimized redundant database hits.
- Developed a recommendation system to suggest personalized movie content to users.
- Wrote extensive unit tests to simulate and validate core functionalities across apps.
- Documented all API endpoints using Swagger UI and Redoc for easy developer integration.
- Followed a CI/CD pipeline to deploy the backend on a cloud environment for production.


## Setup Command 
```
# Create virtual environment (using Python 3's built-in venv)
python3 -m venv .venv

# Activate virtual environment (Linux/macOS)
source .venv/bin/activate

# Activate virtual environment (Windows PowerShell)
# .venv\Scripts\Activate.ps1

# Install dependencies (assuming requirements.txt exists)
pip install -r requirements.txt

# python3 manage.py makemigrations
# python3 manage.py migrate

# Run Django development server
python manage.py runserver
```
