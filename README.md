LocalGigs

LocalGigs is a mini catalog of local music concerts and live performances.
The project was created as a one-week pilot task with a public catalog, concert details page, admin panel, PostgreSQL database and Docker setup.

Business idea

LocalGigs helps users discover local concerts, live performances and music events by city and genre.

The business model is based on free basic listings + paid Featured placement.

Basic listings are free, so local musicians and organizers can easily publish events and grow the catalog. Event organizers can pay for Featured placement. Featured concerts are shown first on the homepage and visually highlighted with a badge and special design.

This works because local artists need visibility, while users want to quickly find interesting live events nearby.

Features
Public part
homepage with concert cards;
concert details page;
filters by city;
Featured concerts shown first;
custom 404 page;
responsive layout;
additional concert information:
organizer;
start time;
duration;
age limit;
atmosphere/mood.
Admin part
simple password-protected admin login;
admin dashboard with all concerts;
create concert;
edit concert;
soft delete concert;
restore deleted concert;
delete confirmation page;
toggle Featured status;
audit log with admin actions;
form validation.
Infrastructure
Docker Compose setup;
PostgreSQL database in Docker;
seed script with 10 realistic concerts;
environment variables via .env;
.env.example included.
Tech stack
Python
Flask
PostgreSQL
Jinja Templates
HTML/CSS
Docker Compose


Project structure
localgigs/
├── static/
│   └── style.css
├── templates/
│   ├── index.html
│   ├── details.html
│   ├── 404.html
│   ├── admin.html
│   ├── create.html
│   ├── edit.html
│   ├── delete_confirm.html
│   ├── audit_log.html
│   └── login.html
├── app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore


Screenshots
Homepage
(фото)
Concert details
(фото)
Admin dashboard
(фото)
Create concert form
(фото)
Edit concert form
(фото)
Audit log
(фото)
Mobile version
(фото)

How to run

Clone the repository:

git clone https://github.com/YOUR_USERNAME/localgigs.git
cd localgigs

Create .env from .env.example:

cp .env.example .env

On Windows PowerShell:

Copy-Item .env.example .env

Start the project:

docker compose up --build

Open the website:
http://localhost:5000

