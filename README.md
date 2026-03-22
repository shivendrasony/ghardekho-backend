# GharDekho — Django Backend

Complete REST API backend built with Django 5 + DRF + JWT + PostgreSQL/SQLite.

---

## Quick Start (5 minutes)

### 1. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup environment file
```bash
cp .env.example .env
# No changes needed — SQLite works out of the box
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Seed sample data
```bash
python manage.py seed_data
```

### 6. Start the server
```bash
python manage.py runserver
```

API: http://localhost:8000
Admin: http://localhost:8000/admin

---

## Sample Login Credentials

| Role  | Email                    | Password  |
|-------|--------------------------|-----------|
| Admin | admin@ghardekho.in       | admin123  |
| Agent | rajesh@primerealty.in    | agent123  |
| Agent | priya@blrhomes.in        | agent123  |
| Buyer | amit@email.com           | buyer123  |
| Buyer | sneha@email.com          | buyer123  |

---

## Switch to PostgreSQL (Production)

```
# In .env:
USE_SQLITE=False
DB_NAME=ghardekho_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

Then run: `python manage.py migrate`

---

## API Endpoints

### Auth  /api/auth/
| POST /register/       | Register new user          |
| POST /login/          | Login — returns JWT tokens |
| POST /logout/         | Blacklist refresh token    |
| GET  /me/             | Get own profile            |
| PUT  /me/             | Update own profile         |
| POST /token/refresh/  | Get new access token       |
| GET  /agents/         | List all agents            |
| GET  /agents/{id}/    | Agent public profile       |

### Properties  /api/properties/
| GET    /                    | List + search + filter   |
| POST   /create/             | Post new property        |
| GET    /{id}/               | Property detail          |
| PUT    /{id}/               | Update (owner only)      |
| DELETE /{id}/               | Delete (owner only)      |
| GET    /featured/           | Featured listings        |
| GET    /my/                 | Own listings             |
| POST   /{id}/save/          | Save/unsave toggle       |
| GET    /saved/              | Saved properties         |
| GET    /admin/all/          | All listings (admin)     |
| PATCH  /admin/{id}/verify/  | Approve/reject listing   |

### Leads  /api/leads/
| POST  /                    | Submit inquiry (anyone)  |
| GET   /mine/               | Buyer's inquiries        |
| GET   /agent/              | Agent's leads            |
| PATCH /{id}/               | Update lead status       |
| POST  /visits/             | Schedule site visit      |
| PATCH /visits/{id}/status/ | Confirm/cancel visit     |

### Blog  /api/blog/
| GET  /              | List published posts     |
| GET  /featured/     | Featured posts           |
| GET  /categories/   | All categories           |
| GET  /{slug}/       | Post detail              |
| POST /create/       | Create post (admin)      |

---

## Connecting React Frontend

Update src/services/api.js in the React project:

```js
import axios from 'axios'

const api = axios.create({ baseURL: 'http://localhost:8000/api' })

api.interceptors.request.use(config => {
  const user = JSON.parse(localStorage.getItem('ghardekho_user') || '{}')
  if (user.token) config.headers.Authorization = `Bearer ${user.token}`
  return config
})

export default api
```

Replace mock data in React pages:
- Login → POST /api/auth/login/
- Properties list → GET /api/properties/
- Property detail → GET /api/properties/{id}/
- Post property → POST /api/properties/create/
- Inquiry → POST /api/leads/

