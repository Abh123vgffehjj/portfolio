# API Reference

All endpoints are prefixed with `/api`.

## Public Endpoints

### GET /api/profile
Returns the portfolio owner's profile data.

**Response:**
```json
{
  "id": 1,
  "full_name": "Abhijeet V S",
  "role": "AI & IoT Developer",
  "subtitle": "Computer Science Engineering Student",
  "summary": "...",
  "email": "abhijeetvs@email.com",
  "linkedin": "https://linkedin.com/in/abhijeetvs2308",
  "github": "https://github.com/Abh123vgffehjj",
  "animated_roles": ["AI Developer", "IoT Innovator", "..."],
  "resume_filename": "resume.pdf"
}
```

---

### GET /api/education
Returns all education entries.

**Response:** Array of education objects.
```json
[
  {
    "id": 1,
    "degree": "Bachelor of Engineering (Computer Science and Engineering)",
    "institution": "Loyola-ICAM College of Engineering and Technology (LICET)",
    "cgpa": "8.54 / 10",
    "start_year": 2024,
    "expected_graduation": "2028",
    "description": "..."
  }
]
```

---

### GET /api/skills
Returns all skills, grouped by category and as a flat list.

**Response:**
```json
{
  "grouped": {
    "Programming": [ { "id": 1, "name": "Python", "category": "Programming", "proficiency": 90 } ],
    "Web": [ ... ]
  },
  "all": [ ... ]
}
```

---

### GET /api/projects
Returns all projects. Supports optional query params:
- `?category=IoT` — filter by category
- `?search=helmet` — search title/description/technologies

**Response:** Array of project objects.
```json
[
  {
    "id": 1,
    "title": "Mine Safety Smart Helmet",
    "description": "...",
    "technologies": ["ESP32", "Python", "Flask"],
    "features": ["Real-time monitoring", "Fall detection"],
    "achievement": "Presented at IIT Madras",
    "category": "IoT",
    "is_featured": true,
    "github_url": null,
    "live_url": null
  }
]
```

---

### GET /api/projects/:id
Returns a single project by ID.

---

### GET /api/certifications
Returns all certifications ordered by display_order.

---

### GET /api/achievements
Returns all achievements ordered by display_order.

---

### GET /api/visitor-count
Returns total visitor count.

**Response:** `{ "count": 142 }`

---

### POST /api/record-visit
Records a page visit for analytics.

**Body:** `{ "page": "/" }`

**Response:** `{ "ok": true }`

---

### POST /api/contact
Submits a contact form message.

**Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "message": "Hello! I'd love to collaborate."
}
```

**Success Response:** `{ "success": true, "message": "Message sent successfully!" }`

**Error Response (400):**
```json
{
  "success": false,
  "errors": ["Please enter a valid email address."]
}
```

---

## Admin Endpoints (require session login)

All admin routes require being logged in at `/admin/login`.

| Method | Route | Action |
|--------|-------|--------|
| GET | `/admin/` | Dashboard |
| GET/POST | `/admin/login` | Login page |
| GET | `/admin/logout` | Logout |
| GET/POST | `/admin/upload-resume` | Resume upload |
| GET | `/admin/projects` | List projects |
| GET/POST | `/admin/projects/add` | Add project |
| GET/POST | `/admin/projects/edit/:id` | Edit project |
| POST | `/admin/projects/delete/:id` | Delete project |
| GET | `/admin/skills` | List skills |
| POST | `/admin/skills/add` | Add skill |
| POST | `/admin/skills/delete/:id` | Delete skill |
| GET | `/admin/certifications` | List certs |
| POST | `/admin/certifications/add` | Add cert |
| POST | `/admin/certifications/delete/:id` | Delete cert |
| GET | `/admin/achievements` | List achievements |
| POST | `/admin/achievements/add` | Add achievement |
| POST | `/admin/achievements/delete/:id` | Delete achievement |
| GET | `/admin/contacts` | List messages |
| POST | `/admin/contacts/delete/:id` | Delete message |
| GET | `/admin/analytics` | Visitor analytics |
