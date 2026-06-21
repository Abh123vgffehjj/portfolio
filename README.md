# 🕷️ Abhijeet V S — Spider-Verse Portfolio

A **production-ready personal portfolio** for Abhijeet V S, built with a **Miles Morales Spider-Man** visual theme.  
It automatically updates itself when you upload your resume PDF, and has a full admin dashboard.

**Tech Stack:** Python Flask · MySQL · Vanilla JS · Bootstrap 5 · HTML5 · CSS3

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
├── vercel.json           ← Config if you ever deploy on Vercel instead
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
│   ├── 404.html          ← "Page not found" error page
│   ├── 500.html          ← "Server error" page
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

## 🗺️ Complete Setup Guide

This guide goes in order. **Do not skip steps.** Each step depends on the previous one.

---

## STEP 1 — Install Python

Python is the programming language this project uses. You need version 3.10 or newer.

**Windows:**
1. Go to https://python.org/downloads
2. Click the yellow **"Download Python 3.x.x"** button
3. Run the installer
4. ⚠️ **IMPORTANT:** At the bottom of the first installer screen, check the box that says **"Add Python to PATH"** before clicking Install Now
5. Click **Install Now**

**Mac:**
1. Open **Terminal** (press Cmd+Space, type Terminal, press Enter)
2. Type this and press Enter:
   ```
   brew install python3
   ```
   If you get "brew not found", first install Homebrew from https://brew.sh

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip git -y
```

**How to check Python installed correctly:**  
Open Terminal (or Command Prompt on Windows) and type:
```
python --version
```
You should see something like: `Python 3.11.5`  
If you see "command not found", try `python3 --version` instead.

---

## STEP 2 — Install Git

Git is a tool that tracks your code changes and lets you upload to GitHub.

**Windows:** Go to https://git-scm.com/download/win and download + run the installer. Click Next through all the options (defaults are fine).

**Mac:** Open Terminal and type:
```
brew install git
```

**Linux:**
```bash
sudo apt install git -y
```

**Check Git installed:**
```
git --version
```
You should see: `git version 2.x.x`

**Configure Git with your name and email** (do this once):
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

---

## STEP 3 — Download This Project

Open Terminal (or Git Bash on Windows) and run:

```bash
git clone https://github.com/YOUR-USERNAME/portfolio.git
```

Replace `YOUR-USERNAME` with your actual GitHub username.  

This creates a folder called `portfolio` on your computer.

Now enter that folder:
```bash
cd portfolio
```

From now on, **all commands must be run from inside this `portfolio` folder**.

---

## STEP 4 — Create a Python Virtual Environment

A virtual environment is a private, isolated space for this project's Python packages. Think of it as a separate toolbox just for this project, so it doesn't interfere with anything else on your computer.

```bash
# Windows (Command Prompt)
python -m venv venv

# Windows (PowerShell)
python -m venv venv

# Mac / Linux
python3 -m venv venv
```

Now **activate** it:

```bash
# Windows (Command Prompt)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Mac / Linux
source venv/bin/activate
```

**How to know it worked:**  
Your terminal prompt will now start with `(venv)`, like this:
```
(venv) C:\Projects\portfolio>
```
or on Mac/Linux:
```
(venv) ~/Projects/portfolio $
```

⚠️ **Every time you close and reopen your terminal, you must re-run the activate command before doing anything else in this project.**

---

## STEP 5 — Install Python Packages

With the virtual environment activated, install everything the project needs:

```bash
pip install -r requirements.txt
```

This will download and install Flask, the MySQL connector, the PDF parser, and all other dependencies.

It will print a lot of text — that is normal. Wait for it to finish (about 1–2 minutes).

**Check it worked:**
```bash
pip list
```
You should see Flask, mysql-connector-python, pdfplumber, and others in the list.

---

## STEP 6 — Create Your `.env` File

The `.env` file stores private settings like your database password. It is never uploaded to GitHub.

```bash
# Windows
copy .env.example .env

# Mac / Linux
cp .env.example .env
```

Now open the `.env` file in any text editor (VS Code, Notepad, etc.) and you will see:

```
SECRET_KEY=your-super-secret-key-change-this-immediately
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=portfolio_db
ADMIN_USERNAME=admin
ADMIN_PASSWORD=YourStrongPassword123!
FLASK_ENV=development
```

**Leave this file alone for now.** You will come back to fill in the Railway database details in Step 8.

---

## STEP 7 — Create a GitHub Account and Repository

You need a GitHub account to upload your code and connect to Railway.

### 7a. Create a GitHub Account

1. Go to https://github.com
2. Click **Sign up**
3. Enter your email, create a password, choose a username
4. Verify your email address

### 7b. Create a New Repository

1. Log in to GitHub
2. Click the **+** icon in the top-right corner → **New repository**
3. Fill in:
   - **Repository name:** `portfolio` (or any name you like)
   - **Description:** `My Spider-Verse Portfolio`
   - **Visibility:** Select **Public** (Railway's free plan requires public repos)
4. ⚠️ **Do NOT check** "Add a README file", "Add .gitignore", or "Choose a license" — the project already has these
5. Click **Create repository**

You will see a page with instructions. Keep this page open — you will need the URL in the next step.

---

## STEP 8 — Set Up Railway MySQL Database

Railway is a cloud platform that runs your database and your app on the internet. We set up the database first, then the app.

### 8a. Create a Railway Account

1. Go to https://railway.app
2. Click **Login** → **Login with GitHub**
3. Click **Authorize Railway** — this links your GitHub account to Railway

### 8b. Create a New Project with MySQL

1. Once logged in, click **New Project**
2. Click **Provision MySQL**
3. Railway will create a MySQL database in about 30 seconds
4. You will see a card labelled **MySQL** appear on the screen

### 8c. Get Your Database Credentials

1. Click on the **MySQL** card
2. Click the **Variables** tab
3. You will see these values (your actual values will be different):

   | Variable | Example Value |
   |----------|--------------|
   | `MYSQLHOST` | `monorail.proxy.rlwy.net` |
   | `MYSQLPORT` | `12345` |
   | `MYSQLUSER` | `root` |
   | `MYSQLPASSWORD` | `AbCdEfGhIjKlMnOp` |
   | `MYSQLDATABASE` | `railway` |

4. Click the **eye icon** next to `MYSQLPASSWORD` to reveal it
5. Keep this tab open — you will copy these values into your `.env` file now

### 8d. Update Your `.env` File

Open the `.env` file you created in Step 6 and update the MySQL section:

```
MYSQL_HOST=monorail.proxy.rlwy.net        ← paste your MYSQLHOST value
MYSQL_PORT=12345                           ← paste your MYSQLPORT value
MYSQL_USER=root                            ← paste your MYSQLUSER value
MYSQL_PASSWORD=AbCdEfGhIjKlMnOp           ← paste your MYSQLPASSWORD value
MYSQL_DATABASE=railway                     ← paste your MYSQLDATABASE value
```

Also set a strong secret key and admin password:

```
SECRET_KEY=spiderverse-abhijeet-super-secret-key-2025-xYz9AbC
ADMIN_USERNAME=admin
ADMIN_PASSWORD=Abhijeet@Spider2025!
FLASK_ENV=development
```

**What is SECRET_KEY?**  
It encrypts your login sessions so nobody can fake being an admin. Make it long and random. You can generate one at https://randomkeygen.com — copy any of the long strings shown.

Save the `.env` file.

---

## STEP 9 — Import the Database Schema and Data

The schema creates the empty tables. The sample data fills them with your information.

### 9a. Connect to Railway MySQL from Your Computer

You need a MySQL client tool. Choose one:

**Option A — MySQL Workbench (GUI, easiest for beginners):**
1. Download from https://dev.mysql.com/downloads/workbench/
2. Open MySQL Workbench
3. Click **+** to add a new connection
4. Fill in:
   - **Connection Name:** `Railway Portfolio`
   - **Hostname:** your `MYSQLHOST` value from Railway
   - **Port:** your `MYSQLPORT` value from Railway
   - **Username:** `root`
5. Click **Store in Vault** next to Password → enter your `MYSQLPASSWORD`
6. Click **OK** → then double-click the connection to open it

**Option B — Command line (if MySQL is installed locally):**
```bash
mysql -h YOUR_MYSQLHOST -P YOUR_MYSQLPORT -u root -p
# Type your MYSQLPASSWORD when prompted
```

**Option C — Railway's built-in query tool:**
1. On the Railway dashboard, click your **MySQL** service
2. Click the **Query** tab
3. You can run SQL directly here (paste the SQL from the files)

### 9b. Run schema.sql

This creates all the tables the app needs.

**In MySQL Workbench:**
1. Click **File** → **Open SQL Script**
2. Navigate to your `portfolio/database/schema.sql` file
3. Click **Open**
4. Click the yellow **lightning bolt** icon (Execute) or press Ctrl+Shift+Enter
5. You should see "10 table(s) created" type messages in the Output panel

**In command line:**
```bash
mysql -h YOUR_MYSQLHOST -P YOUR_MYSQLPORT -u root -p railway < database/schema.sql
```

**In Railway's Query tab:**
- Open `database/schema.sql` in a text editor
- Copy all the text
- Paste it into Railway's Query box
- Click **Run Query**

### 9c. Run sample_data.sql

This fills the tables with Abhijeet's projects, skills, certifications, and achievements.

**In MySQL Workbench:**
1. Click **File** → **Open SQL Script**
2. Open `database/sample_data.sql`
3. Click the yellow **lightning bolt** icon to run it

**In command line:**
```bash
mysql -h YOUR_MYSQLHOST -P YOUR_MYSQLPORT -u root -p railway < database/sample_data.sql
```

**In Railway's Query tab:**
- Open `database/sample_data.sql` in a text editor
- Copy all the text
- Paste and click **Run Query**

**How to check it worked:**  
Run this query to confirm your data is there:
```sql
SELECT COUNT(*) FROM projects;
SELECT COUNT(*) FROM skills;
SELECT COUNT(*) FROM certifications;
```
You should see 3, 21, and 3 respectively.

---

## STEP 10 — Test Locally

Before uploading to GitHub, let's make sure everything works on your computer.

Make sure your virtual environment is activated (you should see `(venv)` in your terminal prompt). If not, run:
```bash
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

Start the Flask server:
```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

Open your browser and visit **http://localhost:5000**

You should see the Spider-Verse portfolio with your projects and skills loaded from the Railway database!

**Test the admin dashboard:**  
Go to http://localhost:5000/admin  
Log in with:
- Username: whatever you set as `ADMIN_USERNAME` in `.env` (default: `admin`)
- Password: whatever you set as `ADMIN_PASSWORD` in `.env`

**Stop the server:** Press `Ctrl+C` in the terminal.

---

## STEP 11 — Add Your Resume PDF

Put your resume PDF in the `static/resume/` folder and rename it to `resume.pdf`:

```
portfolio/
└── static/
    └── resume/
        └── resume.pdf   ← place your file here
```

The **Download Resume** button on the portfolio will now serve this file.

---

## STEP 12 — Upload Code to GitHub

Now that everything works locally, upload the code to GitHub.

### 12a. Initialize Git and Make First Commit

In your terminal, inside the `portfolio` folder:

```bash
# Step 1: Start tracking this folder with Git
git init

# Step 2: Stage all files (prepare them for commit)
git add .

# Step 3: Create your first commit (a saved snapshot of your code)
git commit -m "Initial commit: Spider-Verse Portfolio by Abhijeet V S"
```

**What do these commands mean?**
- `git init` — tells Git to start watching this folder
- `git add .` — the dot means "add everything in the current folder"
- `git commit -m "..."` — saves a snapshot with a description message

### 12b. Connect to Your GitHub Repository

Go back to your GitHub repository page from Step 7b. You should see a section that says **"…or push an existing repository from the command line"**. It shows commands like:

```bash
git remote add origin https://github.com/YOUR-USERNAME/portfolio.git
git branch -M main
git push -u origin main
```

Run those exact commands in your terminal (copy them from GitHub, not from here, so you get your correct username):

```bash
git remote add origin https://github.com/YOUR-USERNAME/portfolio.git
git branch -M main
git push -u origin main
```

**What happens:**
- `git remote add origin ...` — tells Git where GitHub is (the remote)
- `git branch -M main` — names your branch "main"
- `git push -u origin main` — uploads your code to GitHub

**GitHub will ask for your username and password.**  

⚠️ **Important:** GitHub no longer accepts your account password for `git push`. You need a **Personal Access Token** instead:

1. On GitHub, click your profile picture (top right) → **Settings**
2. Scroll down → click **Developer settings** (bottom of the left sidebar)
3. Click **Personal access tokens** → **Tokens (classic)**
4. Click **Generate new token** → **Generate new token (classic)**
5. Give it a name: `portfolio-deploy`
6. Under **Expiration**, choose **No expiration** (or 90 days)
7. Under **Select scopes**, check **repo** (the first option)
8. Click **Generate token**
9. **Copy the token immediately** — you won't be able to see it again!

When Git asks for your password, paste this token instead of your account password.

**After the push, go to your GitHub repository page and refresh it.** You should see all your files listed there.

---

## STEP 13 — Deploy to Railway

Railway will host your Flask app on the internet. It reads your code from GitHub and runs it automatically.

### 13a. Add a Flask Service to Your Railway Project

1. Go to https://railway.app and open the project you created in Step 8
2. Click **New** (the + button in the top right of your project canvas)
3. Click **GitHub Repo**
4. If prompted, click **Configure GitHub App** → authorize Railway to access your repositories
5. Select your `portfolio` repository from the list
6. Click **Deploy Now**

Railway will now try to build and run your app. It reads the `Procfile` to know how to start it:
```
web: gunicorn wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 60
```

### 13b. Add Environment Variables to Railway

The app needs your database credentials and secret key. Go to:

1. Click on your **Flask service** (the new one, not the MySQL one) on the Railway canvas
2. Click the **Variables** tab
3. Click **New Variable** and add each one:

| Variable Name | Value |
|--------------|-------|
| `SECRET_KEY` | Your long random secret key |
| `MYSQL_HOST` | Your Railway MySQL `MYSQLHOST` value |
| `MYSQL_PORT` | Your Railway MySQL `MYSQLPORT` value |
| `MYSQL_USER` | `root` |
| `MYSQL_PASSWORD` | Your Railway MySQL `MYSQLPASSWORD` value |
| `MYSQL_DATABASE` | `railway` |
| `ADMIN_USERNAME` | `admin` |
| `ADMIN_PASSWORD` | Your strong admin password |
| `FLASK_ENV` | `production` |

**Tip:** You can also click **Raw Editor** and paste all variables at once in this format:
```
SECRET_KEY=your-secret-key-here
MYSQL_HOST=monorail.proxy.rlwy.net
MYSQL_PORT=12345
MYSQL_USER=root
MYSQL_PASSWORD=your-password-here
MYSQL_DATABASE=railway
ADMIN_USERNAME=admin
ADMIN_PASSWORD=YourStrongPassword!
FLASK_ENV=production
```

After adding variables, Railway automatically redeploys.

### 13c. Get Your Live URL

1. Click on your Flask service
2. Click the **Settings** tab
3. Under **Networking**, click **Generate Domain**
4. Railway gives you a URL like: `https://portfolio-production-abc1.up.railway.app`

🎉 **Your portfolio is now live on the internet!**

Open that URL in your browser. You should see the full Spider-Verse portfolio.

---

## STEP 14 — Add a Custom Domain (Optional)

If you own a domain like `abhijeetvs2308.com`, you can point it to your Railway app.

1. On Railway, go to your Flask service → **Settings** → **Networking**
2. Under **Custom Domain**, type your domain and click **Add**
3. Railway shows you a CNAME record to add to your domain's DNS settings
4. Log in to wherever you bought your domain (GoDaddy, Namecheap, Google Domains, etc.)
5. Find the DNS settings and add the CNAME record Railway gave you
6. DNS changes take 5–30 minutes to propagate

---

## STEP 15 — Upload Your Resume and Auto-Update the Portfolio

Your portfolio auto-updates from a PDF resume via the admin dashboard.

1. Go to your live URL + `/admin` — e.g. `https://portfolio-production-abc1.up.railway.app/admin`
2. Log in with your admin credentials
3. Click **Upload Resume** in the left sidebar
4. Drag and drop your PDF resume onto the upload area
5. Click **Upload & Parse Resume**
6. The system will extract your skills, projects, certifications, and achievements from the PDF and update the database automatically
7. Refresh your portfolio — the new information appears instantly

---

## STEP 16 — Updating Your Portfolio in the Future

### Method A: Use the Admin Dashboard (no coding required)

1. Go to `your-url.up.railway.app/admin`
2. Log in
3. Use the sidebar to add/edit/delete projects, skills, certifications, achievements
4. Changes appear instantly on the live site

### Method B: Push code changes to GitHub (auto-redeploys)

1. Make your code changes locally
2. Run:
   ```bash
   git add .
   git commit -m "Updated project descriptions"
   git push
   ```
3. Railway detects the push and automatically redeploys (takes about 1 minute)

### Method C: Upload a new resume PDF

1. Go to `/admin` → **Upload Resume**
2. Upload a new PDF
3. The database updates automatically with your latest information

---

## 🔧 Troubleshooting

### "No module named flask" when running python app.py
Your virtual environment is not activated. Run:
```bash
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### "Can't connect to MySQL" error locally
1. Check that your `.env` file has the correct Railway MySQL credentials
2. Make sure you are connected to the internet
3. Double-check that you copied the MYSQLHOST, MYSQLPORT, MYSQLPASSWORD from Railway correctly

### "Table 'railway.profile' doesn't exist"
You forgot to run `schema.sql`. Go back to Step 9b and run it now.

### Portfolio page loads but shows no projects / skills
You forgot to run `sample_data.sql`. Go back to Step 9c and run it now.

### Admin login says "Invalid credentials"
1. Check your `ADMIN_USERNAME` and `ADMIN_PASSWORD` in `.env` (local) or Railway environment variables (production)
2. The password you type must exactly match what is in `ADMIN_PASSWORD`

### "Authentication failed" when running git push
You need a Personal Access Token. Follow the instructions in Step 12b under "GitHub will ask for your username and password".

### Railway deployment shows "Build failed"
1. Click on the failed deployment in Railway → click **View Logs**
2. Read the error message at the bottom of the logs
3. Common cause: missing environment variables — go to Variables tab and check all 9 are set

### Railway app is running but shows 500 error
1. Click your Flask service on Railway → click **View Logs** (or the Logs tab)
2. Look for the Python error message
3. Most common cause: `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_PASSWORD` are wrong or the DB tables were never created

### Resume PDF download shows 404
Place your resume at `static/resume/resume.pdf` (exactly that filename), commit it to Git, and push to GitHub.

### The resume parser did not extract my information correctly
PDF parsing depends heavily on how your PDF was created. If results are poor:
1. Go to `/admin` → use the sidebar to manually add your projects, skills, etc.
2. Or try exporting your resume from Word/Google Docs as PDF — these formats parse better than scanned PDFs

### Port 5000 already in use (locally)
Something else is using port 5000. Either stop the other process, or start Flask on a different port:
```bash
# Set a different port
FLASK_RUN_PORT=5001 python app.py
```
Then visit http://localhost:5001 instead.

---

## ❓ Frequently Asked Questions

**Q: Do I need to know Python to use this portfolio?**  
No. Just follow the steps in order. The code is all written. You are just setting it up.

**Q: Is this free?**  
Yes. Railway's Starter plan includes $5 of free credits per month which is enough for a portfolio site. MySQL on Railway is also free to start.

**Q: What happens if Railway's free credits run out?**  
Railway will pause your services. You can add a credit card to continue, or export your code and host it elsewhere (Render.com also has a free tier).

**Q: How do I change the color scheme?**  
Open `static/css/style.css`. At the very top, inside `:root { ... }`, change:
- `--red: #E11D2E` → any color you want as the accent
- `--black: #0D0D0D` → the background color

**Q: How do I add a new project?**  
Go to `/admin` → **Projects** → **Add Project** → fill in the form → click **Create Project**. It appears on the portfolio immediately.

**Q: How do I change my name, bio, or contact details?**  
Either: upload a new resume PDF through `/admin` → **Upload Resume**, or edit the `profile` table directly via MySQL Workbench or Railway's Query tab.

**Q: How do I connect a custom domain like abhijeetvs2308.com?**  
See Step 14 above.

**Q: My git push asks for username and password but I used to log in with just a password.**  
GitHub requires Personal Access Tokens since August 2021. See Step 12b for how to create one.

**Q: I pushed to GitHub but Railway did not redeploy automatically.**  
On Railway, click your Flask service → **Settings** → make sure **Auto Deploy** is turned on (toggle it on).

**Q: Can I rename the repository?**  
Yes. On GitHub, go to your repo → **Settings** → **Repository name** → rename it → click **Rename**. Then update the remote URL on your computer:
```bash
git remote set-url origin https://github.com/YOUR-USERNAME/new-name.git
```

**Q: How do I see who contacted me through the form?**  
Go to `/admin` → **Messages** in the left sidebar.

**Q: How do I see how many people visited my portfolio?**  
Go to `/admin` → **Analytics** in the left sidebar.

**Q: How do I change the admin password?**  
On Railway, go to your Flask service → **Variables** tab → find `ADMIN_PASSWORD` → click the edit icon → type a new password → save. Railway will redeploy automatically.

**Q: Can I have multiple admin users?**  
Yes, but requires editing the database directly. Connect via MySQL Workbench and run:
```sql
INSERT INTO admin_users (username, password_hash) 
VALUES ('newuser', 'your-hashed-password');
```
To generate a hash, run in Python:
```python
from werkzeug.security import generate_password_hash
print(generate_password_hash('YourNewPassword123'))
```

**Q: The site works on Railway but the visitor counter always shows 0.**  
The counter records visits via a JavaScript API call. Make sure your browser is not blocking JavaScript. Also check the Railway logs for any `/api/record-visit` errors.

**Q: Can I use this portfolio for a different person?**  
Yes. Either run `sample_data.sql` with different data, or log in to `/admin` and update everything through the dashboard.

**Q: How do I delete the sample data and start fresh?**  
Connect to MySQL via MySQL Workbench and run:
```sql
DELETE FROM projects;
DELETE FROM skills;
DELETE FROM certifications;
DELETE FROM achievements;
DELETE FROM profile;
DELETE FROM education;
```
Then add your own data through the admin dashboard or upload your resume PDF.

---

## 🏗️ Architecture: How Everything Connects

```
┌─────────────────────────────────────────────────────────────────┐
│                        VISITOR'S BROWSER                        │
│  - Loads index.html from Railway                                │
│  - JavaScript runs and calls /api/projects, /api/skills, etc.  │
│  - Renders the Spider-Verse UI with live data                   │
└───────────────────────────┬─────────────────────────────────────┘
                            │  HTTP requests
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│               RAILWAY — FLASK APP (app.py)                       │
│                                                                 │
│  Routes:                                                        │
│  GET  /              → serves index.html                        │
│  GET  /api/projects  → returns JSON list of projects            │
│  GET  /api/skills    → returns JSON list of skills              │
│  POST /api/contact   → saves contact form message to DB         │
│  GET  /admin/        → admin dashboard (login required)         │
│  POST /admin/upload-resume → parses PDF, updates DB             │
└───────────────────────────┬─────────────────────────────────────┘
                            │  SQL queries
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│               RAILWAY — MYSQL DATABASE                          │
│                                                                 │
│  Tables:                                                        │
│  profile          → name, bio, email, LinkedIn, GitHub          │
│  education        → degree, institution, CGPA                   │
│  projects         → title, description, technologies, features  │
│  skills           → name, category, proficiency level           │
│  certifications   → name, issuer, date                          │
│  achievements     → title, description, date                    │
│  contacts         → messages from the contact form              │
│  visitors         → analytics (page views)                      │
│  resume_uploads   → history of uploaded PDFs                    │
│  admin_users      → admin login credentials                     │
└─────────────────────────────────────────────────────────────────┘
```

**What happens when someone loads your portfolio:**

1. Their browser requests `https://your-site.up.railway.app/`
2. Railway runs `app.py` which serves `templates/index.html`
3. The browser loads the HTML, then runs `static/js/main.js`
4. JavaScript calls `/api/projects` → Flask queries MySQL → returns JSON
5. JavaScript renders the project cards from that JSON
6. Same happens for skills, certifications, achievements, visitor count
7. The page is fully rendered with live data from the database

**What happens when you upload a resume:**

1. You go to `/admin/upload-resume` and upload a PDF
2. Flask saves the PDF to `uploads/resumes/`
3. `resume_parser/parser.py` reads the PDF with `pdfplumber`
4. The parser detects sections (Skills, Projects, Certifications, etc.)
5. It extracts structured data from each section
6. It inserts/updates rows in the MySQL tables
7. The portfolio immediately shows the new data

---

## 🔮 Future Improvements

- 📧 Email notifications when someone submits the contact form (using SendGrid)
- 🌍 Tamil language toggle
- 📸 Project image upload directly from the admin dashboard
- 📈 Charts in the analytics page (Chart.js)
- 🔗 GitHub API integration to auto-show your repositories
- 🤖 AI-powered bio generator using OpenAI API
- 📱 Progressive Web App (PWA) — lets users install it on their phone

---

## 📜 License

MIT License — free to use, modify, and share.

---

*Built with ❤️ and 🕷️ — "Anyone Can Wear The Mask"*
