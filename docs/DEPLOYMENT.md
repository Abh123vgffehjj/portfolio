# Deployment Guide

## Local Development

```bash
# 1. Clone
git clone https://github.com/YOUR-USERNAME/portfolio.git
cd portfolio

# 2. Virtual env
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install deps
pip install -r requirements.txt

# 4. Environment
cp .env.example .env
# Edit .env with your MySQL credentials

# 5. Database
mysql -u root -p portfolio_db < database/schema.sql
mysql -u root -p portfolio_db < database/sample_data.sql

# 6. Run
python app.py
# Visit http://localhost:5000
```

---

## Vercel + Railway Production Deployment

### 1. Set up Railway MySQL

```
railway.app → New Project → Provision MySQL
Copy: Host, Port, User, Password, Database
Run schema.sql and sample_data.sql via Railway's Query tab
```

### 2. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/USERNAME/portfolio.git
git push -u origin main
```

### 3. Deploy on Vercel

```
vercel.com → New Project → Import from GitHub → Deploy
```

### 4. Set Vercel Environment Variables

In Vercel project → Settings → Environment Variables:

```
SECRET_KEY          = <long-random-string>
MYSQL_HOST          = <railway-host>
MYSQL_PORT          = <railway-port>
MYSQL_USER          = <railway-user>
MYSQL_PASSWORD      = <railway-password>
MYSQL_DATABASE      = railway
ADMIN_USERNAME      = admin
ADMIN_PASSWORD      = <strong-password>
FLASK_ENV           = production
```

### 5. Redeploy

Vercel → Deployments → Redeploy (to pick up env vars)

---

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | Yes | Flask session encryption key. Use 50+ random characters. |
| `MYSQL_HOST` | Yes | Database host (localhost or cloud host) |
| `MYSQL_PORT` | Yes | Database port (usually 3306) |
| `MYSQL_USER` | Yes | Database username |
| `MYSQL_PASSWORD` | Yes | Database password |
| `MYSQL_DATABASE` | Yes | Database name |
| `ADMIN_USERNAME` | Yes | Username for /admin login |
| `ADMIN_PASSWORD` | Yes | Password for /admin login |
| `FLASK_ENV` | Yes | `development` or `production` |

---

## Supported Hosted MySQL Providers

| Provider | Free Tier | Notes |
|----------|-----------|-------|
| Railway | Yes (hobby) | Easiest to set up, recommended |
| Aiven | Yes (free tier) | Good for production |
| PlanetScale | Yes | MySQL-compatible, serverless |
| TiDB Cloud | Yes | MySQL-compatible |
| Clever Cloud | Yes | European hosting |

---

## Security Checklist Before Going Live

- [ ] Change `SECRET_KEY` to a long random string (never use defaults)
- [ ] Change `ADMIN_PASSWORD` to something strong
- [ ] Remove debug mode (`FLASK_ENV=production`)
- [ ] `.env` is in `.gitignore` (it is by default)
- [ ] Admin URL (`/admin`) is not publicly advertised
- [ ] MySQL user has only the permissions it needs (not root in production)
