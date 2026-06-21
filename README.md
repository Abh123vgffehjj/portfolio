# 🕷️ Abhijeet V S — Spider-Verse Portfolio

A **production-ready personal portfolio** for Abhijeet V S, built with a **Miles Morales Spider-Man** visual theme.  
It automatically updates itself when you upload your resume PDF, and has a full admin dashboard.

**Tech Stack:** Python Flask · MySQL · Vanilla JS · Bootstrap 5 · HTML5 · CSS3

**Live Site:** https://portfolio-art-connect.vercel.app  
**Admin Panel:** https://portfolio-art-connect.vercel.app/admin  
**GitHub:** https://github.com/Abh123vgffehjj/portfolio

---

## 🌟 Features

- ⚡ Spider-Verse animated particle web background
- 🎨 Matte black + Spider-Red glassmorphism design
- 🤖 Upload your PDF resume → database updates automatically
- 🔐 Secure admin dashboard at `/admin`
- 📊 Visitor analytics built in
- 📱 Fully responsive, mobile-first layout
- 🌙 Dark / Light theme toggle
- 📨 Contact form with validation and spam protection
- 🔍 Project search and category filter

---

## 📁 What Each File Does

```
portfolio/
│
├── app.py                ← The main Flask app. Run this to start the server.
├── config.py             ← Reads your .env settings (database, secret keys, etc.)
├── wsgi.py               ← Used by Railway/Gunicorn in production
├── requirements.txt      ← List of Python packages this project needs
├── Procfile              ← Tells Railway how to start the app
├── runtime.txt           ← Tells Railway which Python version to use
├── vercel.json           ← Config for Vercel deployment
├── .gitignore            ← Tells Git which files to ignore (like .env passwords)
├── .env.example          ← Template showing what your .env file should look like
│
├── database/
│   ├── schema.sql        ← Creates all the database tables (run this first)
│   └── sample_data.sql   ← Fills tables with Abhijeet's real data (run this second)
│
├── resume_parser/
│   └── parser.py         ← Reads your PDF resume and pulls out skills, projects, etc.
│
├── routes/
│   ├── api.py            ← All the public API endpoints (/api/projects, /api/skills, etc.)
│   └── admin.py          ← Admin dashboard pages and CRUD actions
│
├── models/
│   └── database.py       ← Handles connecting to MySQL and running queries
│
├── templates/
│   ├── index.html        ← The main portfolio page visitors see
│   ├── 404.html          ← Page not found error page
│   ├── 500.html          ← Server error page
│   └── admin/            ← All the admin dashboard HTML pages
│
└── static/
    ├── css/
    │   ├── style.css     ← All the Spider-Verse styling, animations, colors
    │   └── admin.css     ← Admin dashboard styling
    ├── js/
    │   ├── main.js       ← All JavaScript: animations, API calls, typing effect
    │   └── admin.js      ← Admin dashboard JavaScript
    └── resume/
        └── resume.pdf    ← Your resume PDF (place it here for the download button)
```

---

## 🏗️ Architecture

```
Browser → Vercel (Flask App) → Aiven MySQL Database
```

- **Vercel** hosts the Flask app — free forever
- **Aiven** hosts the MySQL database — free forever
- **GitHub** stores your code — free forever

---

## 🗺️ Complete Setup Guide

Do every step in order. Do not skip any step.

---

## STEP 1 — Install Python

Python is the programming language this project uses. You need version 3.10 or newer.

**Windows:**
1. Go to https://python.org/downloads
2. Click the yellow **Download Python 3.x.x** button
3. Run the installer
4. ⚠️ Check the box **"Add Python to PATH"** before clicking Install Now
5. Click **Install Now**

**Mac:**
```bash
brew install python3
```

**Linux:**
```bash
sudo apt update && sudo apt install python3 python3-pip git -y
```

**Check it worked:**
```bash
python --version
```
You should see: `Python 3.x.x`

---

## STEP 2 — Install Git

**Windows:** Download from https://git-scm.com/download/win and install.

**Mac:**
```bash
brew install git
```

**Linux:**
```bash
sudo apt install git -y
```

**Configure Git (do this once):**
```bash
git config --global user.name "Abhijeet V S"
git config --global user.email "youremail@gmail.com"
```

**Check it worked:**
```bash
git --version
```

---

## STEP 3 — Download This Project

```bash
git clone https://github.com/Abh123vgffehjj/portfolio.git
cd portfolio
```

All commands from now on must be run from inside the `portfolio` folder.

---

## STEP 4 — Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

Your terminal prompt will now show `(venv)` at the start. Every time you reopen your terminal, run the activate command again before doing anything.

---

## STEP 5 — Install Python Packages

```bash
pip install -r requirements.txt
```

Wait for it to finish (1-2 minutes). You should see `Successfully installed` at the end.

---

## STEP 6 — Create Your `.env` File

```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

Leave this file for now. You will fill in the database values after setting up Aiven in Step 8.

---

## STEP 7 — Create GitHub Account and Repository

### 7a. Create GitHub Account
1. Go to https://github.com
2. Click **Sign up**
3. Enter email, password, username
4. Verify your email

### 7b. Create Repository
1. Click **+** icon (top right) → **New repository**
2. Name: `portfolio`
3. Visibility: **Public**
4. ⚠️ Do NOT check any of the initialize options
5. Click **Create repository**

### 7c. Push Your Code to GitHub
```bash
git init
git add .
git commit -m "Initial commit: Spider-Verse Portfolio"
git branch -M main
git remote add origin https://github.com/Abh123vgffehjj/portfolio.git
git push -u origin main
```

When asked for password — use a **Personal Access Token** (not your GitHub password):
1. GitHub → your profile picture → **Settings**
2. Scroll down → **Developer settings**
3. **Personal access tokens** → **Tokens (classic)**
4. **Generate new token (classic)**
5. Name: `portfolio`
6. Expiration: **No expiration**
7. Check **repo** scope
8. Click **Generate token**
9. Copy the token and paste it as your password

---

## STEP 8 — Set Up Aiven Free MySQL Database

Aiven gives you a **free MySQL database forever** — no credit card needed.

### 8a. Create Aiven Account
1. Go to https://aiven.io
2. Click **Sign up**
3. Sign up with Google (easiest)

### 8b. Create Free MySQL Service
1. Click **Create service**
2. Select **MySQL**
3. Select **Free plan**
4. Choose region: **Google Cloud → Iowa** (or closest to you)
5. Service name: `portfolio-mysql`
6. Click **Create free service**
7. Wait 2 minutes until it shows **Running** (green dot)

### 8c. Get Connection Details
1. Click on your MySQL service
2. Click **Overview** tab
3. Find **Connection information** section
4. Note down:
   - **Host**
   - **Port**
   - **User** (usually `avnadmin`)
   - **Password** (click eye icon to reveal)
   - **Database** = `defaultdb`

### 8d. Update Your `.env` File

Open the `.env` file and fill in your Aiven values:

```
MYSQL_HOST=your-aiven-host-here
MYSQL_PORT=your-aiven-port-here
MYSQL_USER=avnadmin
MYSQL_PASSWORD=your-aiven-password-here
MYSQL_DATABASE=defaultdb
SECRET_KEY=spiderverse-abhijeet-secret-key-2025-xYz
ADMIN_USERNAME=admin
ADMIN_PASSWORD=Admin@123
FLASK_ENV=development
```

Rules:
- No quotes around values
- No spaces around the = sign
- Save the file

---

## STEP 9 — Connect Aiven in MySQL Workbench

Download MySQL Workbench from https://dev.mysql.com/downloads/workbench/ if you don't have it.

1. Open MySQL Workbench
2. Click **+** to add new connection
3. Fill in:
   - **Connection Name:** `Aiven Portfolio`
   - **Hostname:** your Aiven host
   - **Port:** your Aiven port
   - **Username:** `avnadmin`
4. Click **Store in Vault** → enter your Aiven password
5. Click **Advanced** tab → find SSL section → set **Use SSL** to `Require`
6. Click **OK**
7. Double click the connection — it should connect ✅

---

## STEP 10 — Import Database Schema and Data

### 10a. Run schema.sql (creates tables)

In MySQL Workbench:
1. Click **File** → **Open SQL Script**
2. Open `portfolio/database/schema.sql`
3. Click the **lightning bolt ⚡** button
4. Wait for green checkmarks

Or in terminal:
```bash
mysql -h YOUR_AIVEN_HOST -P YOUR_AIVEN_PORT -u avnadmin -p --ssl-mode=REQUIRED defaultdb < database/schema.sql
```

### 10b. Run sample_data.sql (fills data)

In MySQL Workbench:
1. Click **File** → **Open SQL Script**
2. Open `portfolio/database/sample_data.sql`
3. Click the **lightning bolt ⚡** button

Or in terminal:
```bash
mysql -h YOUR_AIVEN_HOST -P YOUR_AIVEN_PORT -u avnadmin -p --ssl-mode=REQUIRED defaultdb < database/sample_data.sql
```

### 10c. Verify Data

```bash
mysql -h YOUR_AIVEN_HOST -P YOUR_AIVEN_PORT -u avnadmin -p --ssl-mode=REQUIRED defaultdb -e "SELECT COUNT(*) as projects FROM projects; SELECT COUNT(*) as skills FROM skills; SELECT COUNT(*) as certifications FROM certifications; SELECT COUNT(*) as achievements FROM achievements;"
```

You should see **3, 21, 3, 4** ✅

---

## STEP 11 — Add SSL Support in Code

Open `models/database.py` and replace the `get_db_config` function with:

```python
def get_db_config():
    return {
        'host': os.environ.get('MYSQL_HOST', 'localhost').strip(),
        'port': int(os.environ.get('MYSQL_PORT', '3306').strip()),
        'user': os.environ.get('MYSQL_USER', 'root').strip(),
        'password': os.environ.get('MYSQL_PASSWORD', '').strip(),
        'database': os.environ.get('MYSQL_DATABASE', 'defaultdb').strip(),
        'charset': 'utf8mb4',
        'use_unicode': True,
        'autocommit': False,
        'connection_timeout': 10,
        'ssl_disabled': False,
    }
```

Save the file.

---

## STEP 12 — Add Your Resume PDF

Place your resume PDF in the `static/resume/` folder and rename it to `resume.pdf`:

```
portfolio/static/resume/resume.pdf
```

The Download Resume button will now serve this file.

---

## STEP 13 — Test Locally

Make sure virtual environment is activated (you see `(venv)` in terminal), then:

```bash
python app.py
```

Open **http://localhost:5000** — you should see the full Spider-Verse portfolio with all your data. ✅

Test admin at **http://localhost:5000/admin**
- Username: `admin`
- Password: `Admin@123`

Stop the server with `Ctrl+C` when done.

---

## STEP 14 — Push All Changes to GitHub

```bash
git add .
git commit -m "Add Aiven SSL support and resume PDF"
git push
```

---

## STEP 15 — Deploy to Vercel

### 15a. Create Vercel Account
1. Go to https://vercel.com
2. Click **Sign Up** → **Continue with GitHub**
3. Authorize Vercel

### 15b. Import Project
1. Click **Add New Project**
2. Find your `portfolio` repository → click **Import**
3. Click **Deploy** (it will fail first time — that is okay)

### 15c. Add Environment Variables
1. Go to your project → **Settings** → **Environment Variables**
2. Add all 9 variables:

| Name | Value |
|------|-------|
| `MYSQL_HOST` | Your Aiven host |
| `MYSQL_PORT` | Your Aiven port |
| `MYSQL_USER` | `avnadmin` |
| `MYSQL_PASSWORD` | Your Aiven password |
| `MYSQL_DATABASE` | `defaultdb` |
| `SECRET_KEY` | Any long random string |
| `ADMIN_USERNAME` | `admin` |
| `ADMIN_PASSWORD` | `Admin@123` |
| `FLASK_ENV` | `production` |

### 15d. Disable Vercel Authentication
1. **Settings** → **Deployment Protection**
2. Turn **Vercel Authentication** → **OFF**
3. Click **Save**

### 15e. Redeploy
1. Click **Deployments** tab
2. Click `...` next to latest deployment
3. Click **Redeploy**
4. Wait 1 minute

### 15f. Get Your Live URL
Your portfolio is now live at the URL Vercel gives you! 🎉

---

## STEP 16 — Update Your Portfolio

### Method A — Admin Dashboard (No coding)
Go to `/admin` and use the sidebar to:
- Add/edit/delete projects
- Add/delete skills
- Add/delete certifications
- Add/delete achievements
- View contact messages
- View visitor analytics
- Upload resume PDF to auto-update

### Method B — Push code changes
```bash
git add .
git commit -m "Your change description"
git push
```
Vercel auto-redeploys in 1 minute.

### Method C — Update database directly
```bash
# Update email
mysql -h YOUR_AIVEN_HOST -P YOUR_AIVEN_PORT -u avnadmin -p --ssl-mode=REQUIRED defaultdb -e "UPDATE profile SET email='youremail@gmail.com' WHERE id=1;"

# Update LinkedIn
mysql -h YOUR_AIVEN_HOST -P YOUR_AIVEN_PORT -u avnadmin -p --ssl-mode=REQUIRED defaultdb -e "UPDATE profile SET linkedin='https://linkedin.com/in/abhijeetvs2308' WHERE id=1;"

# Update GitHub
mysql -h YOUR_AIVEN_HOST -P YOUR_AIVEN_PORT -u avnadmin -p --ssl-mode=REQUIRED defaultdb -e "UPDATE profile SET github='https://github.com/Abh123vgffehjj' WHERE id=1;"

# Update bio
mysql -h YOUR_AIVEN_HOST -P YOUR_AIVEN_PORT -u avnadmin -p --ssl-mode=REQUIRED defaultdb -e "UPDATE profile SET summary='Your new bio text here' WHERE id=1;"
```

---

## 🔧 Troubleshooting

### "No module named flask"
Virtual environment not activated. Run:
```bash
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### "Can't connect to MySQL"
1. Check your `.env` file has correct Aiven credentials
2. Make sure you are connected to internet
3. Aiven requires SSL — make sure `ssl_disabled: False` is in `database.py`

### "Table doesn't exist"
You forgot to run `schema.sql`. Go back to Step 10a.

### Portfolio shows "Loading..." forever
1. Open browser → press F12 → Console tab
2. Look for red errors
3. Usually means environment variables wrong on Vercel
4. Check all 9 variables in Vercel Settings → Environment Variables

### Admin login fails
Check `ADMIN_USERNAME` and `ADMIN_PASSWORD` match exactly in Vercel environment variables.

### Git push asks for password
Use your Personal Access Token (not GitHub password). See Step 7c.

### Vercel shows 401 error
Go to Vercel → Settings → Deployment Protection → turn OFF Vercel Authentication.

### Resume upload shows 500 error
This is fixed in the latest code. Make sure you have pushed the latest `routes/admin.py` to GitHub.

### CSS not loading on Vercel (site looks unstyled)
Make sure your `vercel.json` includes the static files build:
```json
{
  "version": 2,
  "builds": [
    { "src": "app.py", "use": "@vercel/python" },
    { "src": "static/**", "use": "@vercel/static" }
  ],
  "routes": [
    { "src": "/static/(.*)", "dest": "/static/$1" },
    { "src": "/(.*)", "dest": "app.py" }
  ]
}
```

---

## ❓ Frequently Asked Questions

**Q: Is this free forever?**  
Yes. Vercel is free forever. Aiven free MySQL is free forever. GitHub is free. No credit card needed for any of them.

**Q: What happened to Railway?**  
Railway only gives $5 free credits which expire after 30 days. We switched to Aiven which is free forever.

**Q: How do I change my name or bio?**  
Use the admin dashboard OR run a MySQL UPDATE command (see Step 16 Method C).

**Q: How do I add a new project?**  
Go to `/admin` → **Projects** → **Add Project** → fill in the form → click **Create Project**.

**Q: How do I change my admin password?**  
Update `ADMIN_PASSWORD` in Vercel environment variables and redeploy.

**Q: How do I change the accent color from red to something else?**  
Open `static/css/style.css` → find `:root { }` at the top → change `--red: #E11D2E` to any color.

**Q: The resume parser didn't extract my data correctly.**  
PDF parsing depends on your PDF format. Manually update your data through the admin dashboard instead.

**Q: How do I see who contacted me?**  
Go to `/admin` → **Messages** in the sidebar.

**Q: How do I connect a custom domain?**  
Vercel → Settings → Domains → Add your domain → follow the DNS instructions.

**Q: Git push says authentication failed.**  
Use your Personal Access Token as password. See Step 7c for how to create one.

**Q: Vercel auto-redeploys when I push to GitHub?**  
Yes, automatically. Every `git push` triggers a new deployment in about 1 minute.

**Q: Can I upload my resume PDF through admin to update the portfolio?**  
Yes. Go to `/admin` → **Upload Resume** → drag and drop your PDF → click Upload. The system extracts skills, projects, certifications and achievements automatically. Check and fix anything it missed through the admin forms.

**Q: How do I view visitor analytics?**  
Go to `/admin` → **Analytics** in the sidebar.

**Q: Can I have GitHub and Live Demo links on my projects?**  
Yes. Go to `/admin` → **Projects** → **Edit** → fill in GitHub URL and/or Live URL fields. Leave them blank if you don't have links.

---

## 🏗️ How Everything Connects

```
┌─────────────────────────────────────────────────┐
│              VISITOR'S BROWSER                  │
│  Loads portfolio → JS fetches data from API     │
└──────────────────┬──────────────────────────────┘
                   │ HTTP
                   ▼
┌─────────────────────────────────────────────────┐
│         VERCEL — FLASK APP (Free Forever)       │
│                                                 │
│  GET  /              → portfolio page           │
│  GET  /api/projects  → JSON projects data       │
│  GET  /api/skills    → JSON skills data         │
│  POST /api/contact   → saves message to DB      │
│  GET  /admin/        → admin dashboard          │
└──────────────────┬──────────────────────────────┘
                   │ SQL
                   ▼
┌─────────────────────────────────────────────────┐
│         AIVEN — MYSQL DATABASE (Free Forever)   │
│                                                 │
│  profile        → name, bio, email, social      │
│  education      → degree, institution, CGPA     │
│  projects       → title, description, tech      │
│  skills         → name, category, proficiency   │
│  certifications → name, issuer, date            │
│  achievements   → title, description, date      │
│  contacts       → contact form messages         │
│  visitors       → analytics / page views        │
│  resume_uploads → uploaded PDF history          │
│  admin_users    → admin login credentials       │
└─────────────────────────────────────────────────┘
```

---

## 🔮 Future Improvements

- 📧 Email notifications for contact form (SendGrid)
- 📸 Project image upload from admin dashboard
- 📈 Charts in analytics page
- 🔗 GitHub API to auto-show repositories
- 🌍 Tamil language toggle
- 📱 Progressive Web App (PWA) support

---

## 📜 License

MIT License — free to use, modify, and share.

---

*Built with ❤️ and 🕷️ by Abhijeet V S — "Anyone Can Wear The Mask"*
