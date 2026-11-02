# Final Project Guide

**Django & DRF — Beginner Level**
**Duration:** 2 weeks
**Pick:** 1 project from the 5 below

---

## How to Use This Guide

1. Read the **Overview** and **Features** of each project.
2. Pick the one that interests you most (or the one that challenges you the right amount).
3. Follow the **Week-by-Week Plan** — it tells you exactly what to build each week.
4. Use the **Models** table to create your database schema.
5. Use the **Endpoints** or **Pages** table to build your routes.
6. Submit according to the **Deliverables** at the end.

---

## Project Structure (All Projects)

Use this layout for every project:

```
my_project/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── myapp/
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py
│   ├── admin.py
│   ├── tests.py
│   ├── migrations/
│   ├── templates/       (UI projects only)
│   ├── static/          (UI projects only)
│   ├── serializers.py   (DRF projects only)
│   ├── views.py
│   └── urls.py
└── templates/           (UI projects — base.html lives here)
```

**Rules:**
- One project, one app. Keep it simple.
- `requirements.txt` must list every dependency.
- `README.md` is mandatory (see Deliverables).

---

---

# Project 1: Poll / Survey API

**Type:** DRF (REST API)

## Overview

Build a JSON API where users create polls with multiple-choice options, other users cast votes, and anyone can view live results.

## Features

- Create a poll with a question and 2–5 answer options
- Each option tracks how many votes it has received
- An authenticated user can vote **once** per poll (no duplicates)
- Polls have an open/closed status; only open polls accept votes
- Results endpoint returns vote counts and percentages per option
- Filter polls by status (open/closed) or by creator
- Pagination on the poll list endpoint (10 per page)
- Poll detail response nests its options and the voter's own vote (if they voted)

## Models

### Poll

| Field | Type | Notes |
|-------|------|-------|
| question | CharField (max 300) | The poll question |
| status | CharField (max 10) | Choices: `open`, `closed`. Default: `open` |
| creator | ForeignKey → User | `related_name='polls'` |
| created_at | DateTimeField | `auto_now_add=True` |

### Option

| Field | Type | Notes |
|-------|------|-------|
| poll | ForeignKey → Poll | `related_name='options'` |
| text | CharField (max 200) | The answer text |
| votes | PositiveIntegerField | Default: 0 |

### Vote

| Field | Type | Notes |
|-------|------|-------|
| poll | ForeignKey → Poll | `related_name='votes'` |
| option | ForeignKey → Option | `related_name='votes'` |
| voter | ForeignKey → User | `related_name='votes'` |
| created_at | DateTimeField | `auto_now_add=True` |

## Endpoints

| Method | URL | Auth | Description |
|--------|-----|------|-------------|
| GET | `/api/polls/` | Token | List polls (paginated, filterable by `?status=`) |
| GET | `/api/polls/{id}/` | Token | Poll detail with options + `my_vote` |
| POST | `/api/polls/` | Token | Create a poll |
| PATCH | `/api/polls/{id}/` | Token (creator only) | Update poll |
| DELETE | `/api/polls/{id}/` | Token (creator only) | Delete poll |
| POST | `/api/polls/{id}/vote/` | Token | Cast a vote |
| GET | `/api/polls/{id}/results/` | Token | Full results with percentages |

## Sample Requests & Responses

**Auth header (all endpoints):** `Authorization: Token a1b2c3d4e5f6...`

### `GET /api/polls/`

```bash
curl -H "Authorization: Token a1b2c3d4e5f6" "http://localhost:8000/api/polls/?status=open"
```

**200:**
```json
{
  "count": 3,
  "next": "http://localhost:8000/api/polls/?page=2&status=open",
  "previous": null,
  "results": [
    {
      "id": 1,
      "question": "Best language for web dev?",
      "status": "open",
      "creator": "jane",
      "created_at": "2026-11-01T10:30:00Z",
      "options": [
        {"id": 1, "text": "Python", "votes": 12},
        {"id": 2, "text": "JavaScript", "votes": 8}
      ]
    }
  ]
}
```

### `GET /api/polls/{id}/`

```bash
curl -H "Authorization: Token a1b2c3d4e5f6" "http://localhost:8000/api/polls/1/"
```

**200:**
```json
{
  "id": 1,
  "question": "Best language for web dev?",
  "status": "open",
  "creator": "jane",
  "created_at": "2026-11-01T10:30:00Z",
  "options": [
    {"id": 1, "text": "Python", "votes": 12},
    {"id": 2, "text": "JavaScript", "votes": 8}
  ],
  "my_vote": 1
}
```
> `my_vote` is `null` if the user hasn't voted.

### `POST /api/polls/`

```bash
curl -X POST \
  -H "Authorization: Token a1b2c3d4e5f6" \
  -H "Content-Type: application/json" \
  -d '{"question": "Favorite framework?", "options": ["Django", "Flask", "FastAPI"]}' \
  "http://localhost:8000/api/polls/"
```

**201:**
```json
{
  "id": 3,
  "question": "Favorite framework?",
  "status": "open",
  "creator": "jane",
  "created_at": "2026-11-02T14:22:00Z",
  "options": [
    {"id": 5, "text": "Django", "votes": 0},
    {"id": 6, "text": "Flask", "votes": 0},
    {"id": 7, "text": "FastAPI", "votes": 0}
  ]
}
```

**400** (too few options):
```json
{"options": ["Must have at least 2 options."]}
```

### `PATCH /api/polls/{id}/`

```bash
curl -X PATCH \
  -H "Authorization: Token a1b2c3d4e5f6" \
  -H "Content-Type: application/json" \
  -d '{"status": "closed"}' \
  "http://localhost:8000/api/polls/1/"
```

**200:**
```json
{
  "id": 1,
  "question": "Best language for web dev?",
  "status": "closed",
  "creator": "jane",
  "created_at": "2026-11-01T10:30:00Z",
  "options": [
    {"id": 1, "text": "Python", "votes": 12},
    {"id": 2, "text": "JavaScript", "votes": 8}
  ]
}
```

**403** (not the creator):
```json
{"detail": "Only the poll creator can update this poll."}
```

### `DELETE /api/polls/{id}/`

```bash
curl -X DELETE -H "Authorization: Token a1b2c3d4e5f6" "http://localhost:8000/api/polls/1/"
```

**204:** *(empty body)*

### `POST /api/polls/{id}/vote/`

```bash
curl -X POST \
  -H "Authorization: Token a1b2c3d4e5f6" \
  -H "Content-Type: application/json" \
  -d '{"option": 1}' \
  "http://localhost:8000/api/polls/1/vote/"
```

**201:**
```json
{"detail": "Vote recorded.", "poll_id": 1, "option_id": 1, "option_text": "Python"}
```

**400** (already voted):
```json
{"detail": "You have already voted on this poll."}
```

**400** (poll is closed):
```json
{"detail": "This poll is closed and no longer accepts votes."}
```

### `GET /api/polls/{id}/results/`

```bash
curl -H "Authorization: Token a1b2c3d4e5f6" "http://localhost:8000/api/polls/1/results/"
```

**200:**
```json
{
  "poll_id": 1,
  "question": "Best language for web dev?",
  "total_votes": 20,
  "results": [
    {"option_id": 1, "text": "Python", "votes": 12, "percentage": 60.0},
    {"option_id": 2, "text": "JavaScript", "votes": 8, "percentage": 40.0}
  ]
}
```

## Key DRF Concepts

- `ModelViewSet` for polls; custom `@action` for vote and results
- Nested serializers (options inside poll detail)
- `SerializerMethodField` for `my_vote` and percentage calculation
- Custom permission class `IsPollCreator` for update/delete
- Business logic in the vote action (check poll is open, check user hasn't voted)
- `DjangoFilterBackend` for status filtering
- `PageNumberPagination` (page size 10)

## Week-by-Week Plan

### Week 1

| Day | Task |
|-----|------|
| Mon | Create project + app. Define all 3 models. Run migrations. |
| Tue | Write serializers: `OptionSerializer`, `PollSerializer` (nested options). |
| Wed | Build `PollViewSet` with CRUD. Wire up `DefaultRouter`. Test in browsable API. |
| Thu | Set up `TokenAuthentication` + `IsAuthenticated`. Create test users + tokens. |
| Fri | Add `DjangoFilterBackend` (filter by status) + `PageNumberPagination`. |

### Week 2

| Day | Task |
|-----|------|
| Mon | Implement `@action vote/` with all business logic (open check, duplicate check, increment option votes). |
| Tue | Implement `@action results/` with percentage calculation. |
| Wed | Write `IsPollCreator` permission class. Apply to `partial_update` and `destroy`. |
| Thu | Proceed |
| Fri | Write README. Polish. Final test run. Push to GitHub. |

## Deliverables

- [ ] Working API with all 7 endpoints functional
- [ ] Custom permission class (`IsPollCreator`)
- [ ] README with: setup instructions, endpoint table, sample curl commands, sample JSON responses
- [ ] GitHub repo (public or private, shared with instructor)

---

---

# Project 2: Restaurant Menu & Order API

**Type:** DRF (REST API)

## Overview

Build a JSON API where a restaurant manages its menu items and customers place orders. Staff can add/edit/remove menu items, mark them as available or sold out, and manage order status. Customers browse the menu and place orders.

## Features

- **Two roles:** `staff` (manage menu + view all orders) and `customer` (browse menu + place orders)
- Menu items have: name, description, price, category, availability flag
- Categories: `appetizers`, `mains`, `desserts`, `drinks`
- Customers place orders with multiple items (each with a quantity)
- Order total is calculated server-side
- Orders have a status workflow: `pending` → `preparing` → `ready` → `served`
- Staff can only advance status forward (no going back)
- Menu is public (no auth to browse); orders and menu management require auth
- Filter menu by category; filter orders by status
- Pagination on list endpoints

## Models

### MenuItem

| Field | Type | Notes |
|-------|------|-------|
| name | CharField (max 200) | |
| description | TextField | |
| price | DecimalField (max 8, decimals 2) | |
| category | CharField (max 20) | Choices: `appetizers`, `mains`, `desserts`, `drinks` |
| is_available | BooleanField | Default: `True` |
| created_at | DateTimeField | `auto_now_add=True` |

### Order

| Field | Type | Notes |
|-------|------|-------|
| customer | ForeignKey → User | `related_name='orders'` |
| table_number | PositiveIntegerField | |
| status | CharField (max 20) | Choices: `pending`, `preparing`, `ready`, `served`. Default: `pending` |
| created_at | DateTimeField | `auto_now_add=True` |

### OrderItem

| Field | Type | Notes |
|-------|------|-------|
| order | ForeignKey → Order | `related_name='items'` |
| menu_item | ForeignKey → MenuItem | |
| quantity | PositiveIntegerField | Min: 1 |

> **Note:** `total` is computed in the serializer (sum of `price × quantity` for all items). Not stored in the DB.

## Endpoints

| Method | URL | Auth | Description |
|--------|-----|------|-------------|
| GET | `/api/menu/` | None | List menu items (filterable by `?category=`) |
| GET | `/api/menu/{id}/` | None | Retrieve a menu item |
| POST | `/api/menu/` | Staff | Create a menu item |
| PATCH | `/api/menu/{id}/` | Staff | Update a menu item (e.g., mark sold out) |
| DELETE | `/api/menu/{id}/` | Staff | Remove a menu item |
| POST | `/api/orders/` | Customer | Place an order |
| GET | `/api/orders/` | Staff | List orders (filterable by `?status=`) |
| GET | `/api/orders/{id}/` | Staff or owner | Retrieve an order |
| PATCH | `/api/orders/{id}/` | Staff | Update order status |

## Sample Requests & Responses

### `GET /api/menu/`

```bash
curl "http://localhost:8000/api/menu/?category=appetizers"
```

**200:**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Bruschetta",
      "description": "Tomato, basil, garlic on toasted baguette",
      "price": "8.50",
      "category": "appetizers",
      "is_available": true
    },
    {
      "id": 2,
      "name": "Calamari",
      "description": "Crispy fried squid with lemon aioli",
      "price": "12.00",
      "category": "appetizers",
      "is_available": false
    }
  ]
}
```

### `POST /api/menu/`

```bash
curl -X POST \
  -H "Authorization: Token sTaFfT0k3n..." \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Margherita Pizza",
    "description": "San Marzano tomato, fresh mozzarella, basil",
    "price": "14.00",
    "category": "mains",
    "is_available": true
  }' \
  "http://localhost:8000/api/menu/"
```

**201:**
```json
{
  "id": 15,
  "name": "Margherita Pizza",
  "description": "San Marzano tomato, fresh mozzarella, basil",
  "price": "14.00",
  "category": "mains",
  "is_available": true
}
```

**403** (customer tries to create):
```json
{"detail": "Staff access required."}
```

### `POST /api/orders/`

```bash
curl -X POST \
  -H "Authorization: Token cUst0m3rT0k..." \
  -H "Content-Type: application/json" \
  -d '{
    "table_number": 7,
    "items": [
      {"menu_item": 1, "quantity": 2},
      {"menu_item": 15, "quantity": 1}
    ]
  }' \
  "http://localhost:8000/api/orders/"
```

**201:**
```json
{
  "id": 3,
  "table_number": 7,
  "status": "pending",
  "items": [
    {"menu_item": 1, "name": "Bruschetta", "quantity": 2, "unit_price": "8.50", "line_total": "17.00"},
    {"menu_item": 15, "name": "Margherita Pizza", "quantity": 1, "unit_price": "14.00", "line_total": "14.00"}
  ],
  "total": "31.00",
  "created_at": "2026-11-02T18:30:00Z"
}
```

**400** (item is sold out):
```json
{"items": [{"menu_item": 2, "error": "Calamari is not available."}]}
```

### `PATCH /api/orders/{id}/`

```bash
curl -X PATCH \
  -H "Authorization: Token sTaFfT0k3n..." \
  -H "Content-Type: application/json" \
  -d '{"status": "preparing"}' \
  "http://localhost:8000/api/orders/3/"
```

**200:**
```json
{
  "id": 3,
  "table_number": 7,
  "status": "preparing",
  "total": "31.00",
  "created_at": "2026-11-02T18:30:00Z"
}
```

**400** (invalid status transition):
```json
{"status": ["Cannot move from 'served' to 'pending'."]}
```

### `GET /api/orders/{id}/` (customer views own order)

```bash
curl -H "Authorization: Token cUst0m3rT0k..." "http://localhost:8000/api/orders/3/"
```

**200:**
```json
{
  "id": 3,
  "table_number": 7,
  "status": "preparing",
  "items": [
    {"name": "Bruschetta", "quantity": 2, "unit_price": "8.50", "line_total": "17.00"},
    {"name": "Margherita Pizza", "quantity": 1, "unit_price": "14.00", "line_total": "14.00"}
  ],
  "total": "31.00",
  "created_at": "2026-11-02T18:30:00Z"
}
```

**403** (customer views someone else's order):
```json
{"detail": "You can only view your own orders."}
```

## Key DRF Concepts

- `ModelSerializer` with nested writable fields (order items in the create serializer)
- `SerializerMethodField` for computed `line_total` and `total`
- Custom permission classes: `IsStaff`, `IsOwnerOrStaff`
- `DjangoFilterBackend` for category and status filtering
- `PageNumberPagination`
- Business logic in `perform_create` (check item availability, validate status transitions)
- `DecimalField` for money
- Separate read/write serializers for orders (customer sees less data than staff)
- Role-based auth: add a `role` field (CharField: `staff` / `customer`) to your custom user or use `is_staff`

## Week-by-Week Plan

### Week 1

| Day | Task |
|-----|------|
| Mon | Create project + app. Define models: `MenuItem`, `Order`, `OrderItem`. Migrations. |
| Tue | Write serializers: `MenuItemSerializer`, `OrderItemSerializer`, `OrderSerializer` (nested items, computed total). |
| Wed | Build `MenuItemViewSet` (public read, staff write). Build `OrderViewSet` (create for customers, list/detail for staff). |
| Thu | Set up `TokenAuthentication`. Create a `role` field. Write `IsStaff` and `IsOwnerOrStaff` permissions. |
| Fri | Wire up router. Test all endpoints in browsable API. Add `DjangoFilterBackend`. |

### Week 2

| Day | Task |
|-----|------|
| Mon | Implement order creation logic: validate all items are available, compute total server-side. |
| Tue | Implement status workflow: validate transitions (pending→preparing→ready→served only). |
| Wed | Add pagination. Add `?category=` filter on menu. Add `?status=` filter on orders. |
| Thu | Proceed |
| Fri | Write README. Polish. Push to GitHub. |

## Deliverables

- [ ] Working API with all 9 endpoints functional
- [ ] Role-based permissions (`IsStaff`, `IsOwnerOrStaff`)
- [ ] README with: setup instructions, endpoint table, sample curl commands, sample JSON responses
- [ ] GitHub repo

---

---

# Project 3: Library Management System

**Type:** Django UI (server-rendered)


## Overview

Build a web app to manage books, members, and the full issue/return workflow with due-date tracking and an overdue dashboard.

## Features

- Add, list, and view books (title, author, ISBN, copies)
- Register and list members
- Issue a book to a member (select member, set due date)
- Return a book (mark as returned, update available count)
- Dashboard showing total books, members, currently issued, overdue count
- Overdue page listing all past-due issues
- Search books by title, author, or ISBN
- Admin panel customized for quick management

## Models

### Book

| Field | Type | Notes |
|-------|------|-------|
| title | CharField (max 200) | |
| author | CharField (max 100) | |
| isbn | CharField (max 13) | `unique=True` |
| copies | PositiveIntegerField | Total copies. Default: 1 |
| available | PositiveIntegerField | Currently available. Default: 1 |
| created_at | DateTimeField | `auto_now_add=True` |

### Member

| Field | Type | Notes |
|-------|------|-------|
| name | CharField (max 100) | |
| email | EmailField | `unique=True` |
| joined_at | DateTimeField | `auto_now_add=True` |

### Issue

| Field | Type | Notes |
|-------|------|-------|
| book | ForeignKey → Book | `related_name='issues'` |
| member | ForeignKey → Member | `related_name='issues'` |
| issued_date | DateField | `auto_now_add=True` |
| due_date | DateField | Set by the librarian |
| returned_date | DateField | `null=True, blank=True` |
| is_returned | BooleanField | Default: `False` |

## Pages

| Page | URL | Description |
|------|-----|-------------|
| Dashboard | `/` | Stats: total books, total members, currently issued, overdue count |
| Book List | `/books/` | All books with search by title/author/ISBN |
| Add Book | `/books/add/` | Form: title, author, ISBN, copies |
| Book Detail | `/books/{id}/` | Book info + full issue/return history |
| Member List | `/members/` | All registered members |
| Add Member | `/members/add/` | Form: name, email |
| Issue Book | `/books/{id}/issue/` | Form: select member, set due date |
| Return Book | `/issues/{id}/return/` | Confirm and mark as returned |
| Overdue | `/overdue/` | All issues past due date, highlighted in red |

## Key Django Concepts

- Model relationships (ForeignKey from Issue → Book, Issue → Member)
- Django forms with validation (due date must be after today)
- Template conditionals for status display (overdue = red, available = green)
- QuerySet aggregation (`Count`, `Sum`) for dashboard stats
- Template inheritance (`base.html` → child templates)
- Class-based views or function-based views (your choice)

## Week-by-Week Plan

### Week 1

| Day | Task |
|-----|------|
| Mon | Create project + app. Define all 3 models. Migrations. |
| Tue | Build Book List page (table with title, author, ISBN, available count). Build Add Book form. |
| Wed | Build Book Detail page (info + issue history). Build Member List + Add Member. |
| Thu | Set up `base.html` with navigation. Apply template inheritance to all pages. |
| Fri | Proceed... |

### Week 2

| Day | Task |
|-----|------|
| Mon | Issue Book page: form to select member + due date. Business logic: check `available > 0`, decrement on issue. |
| Tue | Return Book page: confirm, set `returned_date`, increment `available`. |
| Wed | Overdue page: query `due_date < today AND is_returned = False`. Highlight in red. |
| Thu | Dashboard: use `Count` and filter queries to show 4 stats. Add search to book list. |
| Fri | Write README with screenshots. Polish CSS. Push to GitHub. |

## Deliverables

- [ ] Working app with full issue/return flow
- [ ] Dashboard with live stats
- [ ] Overdue page with red highlighting
- [ ] Search functionality on book list
- [ ] README with: setup instructions, screenshots of all pages
- [ ] GitHub repo

---

---

# Project 4: Event Registration Platform

**Type:** Django UI (server-rendered)

## Overview

Build a web app where organizers create events and attendees register with capacity enforcement. Organizers can view their registered attendees and manage their events.

## Features

- Organizers create events (title, description, location, start/end time, max attendees)
- Public event list showing upcoming events with spots remaining
- Event detail page with a registration form
- Capacity enforcement: reject registration if event is full
- "My Events" page for the logged-in organizer
- Attendee list (organizer only) showing who registered
- Cancel registration (frees up a spot)
- Filter events by location
- Pagination on event list (5 per page)
- Flash messages for success/error feedback

## Models

### Event

| Field | Type | Notes |
|-------|------|-------|
| title | CharField (max 200) | |
| description | TextField | |
| location | CharField (max 200) | |
| start_time | DateTimeField | |
| end_time | DateTimeField | Must be after `start_time` |
| max_attendees | PositiveIntegerField | Default: 50 |
| organizer | ForeignKey → User | `related_name='events'` |
| created_at | DateTimeField | `auto_now_add=True` |

### Registration

| Field | Type | Notes |
|-------|------|-------|
| event | ForeignKey → Event | `related_name='registrations'` |
| attendee_name | CharField (max 100) | |
| attendee_email | EmailField | |
| registered_at | DateTimeField | `auto_now_add=True` |

## Pages

| Page | URL | Description |
|------|-----|-------------|
| Event List | `/` | All upcoming events, paginated, filterable by `?location=` |
| Event Detail | `/events/{id}/` | Full event info + registration form + spots remaining |
| Create Event | `/events/create/` | Form for organizers (login required) |
| My Events | `/events/my/` | Events the logged-in user organized |
| Attendee List | `/events/{id}/attendees/` | Table of registered attendees (organizer only) |
| Cancel Registration | `/registrations/{id}/cancel/` | Remove a registration |

## Key Django Concepts

- DateTime validation (end time must be after start time)
- Business logic in views: check capacity before allowing registration
- `QuerySet.annotate(Count('registrations'))` to show spots remaining
- `LoginRequiredMixin` for organizer-only pages
- Django messages framework for success/error feedback
- URL query params for filtering (`?location=NYC`)
- Pagination on the event list
- Template conditionals (show "Full" badge if no spots left)

## Week-by-Week Plan

### Week 1

| Day | Task |
|-----|------|
| Mon | Create project + app. Define models: `Event`, `Registration`. Migrations. |
| Tue | Build Event List page (paginated, 5/page). Build Event Detail page. |
| Wed | Build Create Event form with DateTime validation. Set up login/register views. |
| Thu | Set up `base.html` with nav. Apply template inheritance. Basic CSS. |
| Fri | Build "My Events" page (filter by `request.user`). Test all pages. |

### Week 2

| Day | Task |
|-----|------|
| Mon | Registration form on event detail (name + email). Capacity check in view. |
| Tue | Attendee List page (organizer only, table format). Cancel Registration with confirmation. |
| Wed | Location filter via query params. Messages framework (success on register, error if full). |
| Thu | Test to check: registration succeeds, registration rejected when full, organizer can see attendees, non-organizer cannot. |
| Fri | Write README with screenshots. Polish UI. Push to GitHub. |

## Deliverables

- [ ] Working app with full registration flow
- [ ] Capacity enforcement (no over-registration)
- [ ] Organizer-only attendee view
- [ ] Location filter working
- [ ] README with: setup instructions, screenshots
- [ ] GitHub repo (public)

---


# Project 5 : Movie Watchlist & Review

**Type:** Django UI (you build a real website with pages)

## What You're Building

A website where users track movies they want to watch, have watched, or are currently watching. They can write a review and give a star rating (1–5). You can see the average rating for each movie, filter by genre, and search by title.

Think of it like a personal version of IMDb

## What You Need to Build (Features)

- Add a movie (title, year, genre, a short description)
- Each movie belongs to a genre (Action, Comedy, Drama, Horror, Sci-Fi, Documentary)
- Mark a movie's status: `watchlist` (want to watch), `watching`, or `watched`
- Write a review for a movie you've watched (your opinion + a star rating from 1 to 5)
- Each movie can have multiple reviews (from different users)
- Show the **average rating** on the movie card (calculated from all its reviews)
- List all movies as cards (title, year, genre, average rating, status badge)
- Filter by genre (dropdown)
- Filter by status (dropdown: all / watchlist / watching / watched)
- Search by title
- Movie detail page: full info + all reviews + a form to add your own review
- Edit a movie (change status, update info)
- Delete a movie (with confirmation)
- "My Movies" page: only the movies YOU added
- Pagination: 6 movies per page (card grid)

## Your Models (2 relationships)

### Table: Genre

| Column | Type | Notes |
|--------|------|-------|
| name | CharField (max 50) | Must be unique. Like "Action", "Comedy" |

### Table: Movie

| Column | Type | Notes |
|--------|------|-------|
| title | CharField (max 200) | |
| year | PositiveIntegerField | Like 2019 |
| description | TextField | A short blurb (2–3 sentences) |
| genre | **ForeignKey → Genre** | Which genre this movie is |
| status | CharField (max 15) | `watchlist`, `watching`, or `watched`. Default: `watchlist` |
| owner | ForeignKey → User | Who added this movie |
| created_at | DateTimeField | Set automatically |

### Table: Review

| Column | Type | Notes |
|--------|------|-------|
| movie | **ForeignKey → Movie** | Which movie this review is for |
| user | ForeignKey → User | Who wrote the review |
| rating | PositiveSmallIntegerField | 1 to 5 |
| text | TextField | Your written opinion |
| created_at | DateTimeField | Set automatically |


## Your Pages

| Page | URL | What it shows |
|------|-----|---------------|
| Home / Movie List | `/` | All movies as cards in a grid. Each card shows: title, year, genre badge, average rating (stars), status badge. Filter bar at top. 6 per page. |
| Movie Detail | `/movies/{id}/` | Full movie info + a list of all reviews (avatar, name, stars, text, date) + a form at the bottom to write your own review. |
| Add Movie | `/movies/add/` | A form: title, year, genre (dropdown), description, status (dropdown). |
| Edit Movie | `/movies/{id}/edit/` | Same form, pre-filled. Most people will use this to change the status (e.g., from "watchlist" to "watched"). |
| Delete Movie | `/movies/{id}/delete/` | "Are you sure? This will also delete all its reviews." → Yes / No. |
| My Movies | `/my-movies/` | Only the movies YOU added. Same card layout. |
| Genre List | `/genres/` | All genres with a count next to each (e.g., "Action — 14 movies"). |

## The Filter Bar (on the Home page)

At the top of the card grid:
- A dropdown: **All genres / Action / Comedy / Drama / Horror / Sci-Fi / Documentary**
- A dropdown: **All / Watchlist / Watching / Watched**
- A text input: **Search by title**

All three work together. If they pick "Sci-Fi" + "Watched" + type "inter", you show only watched Sci-Fi movies whose title contains "inter".

## What You'll Practice

| Concept | What it means in plain words |
|---------|------------------------------|
| ForeignKey (two of them) | "This movie belongs to this genre" and "This review belongs to this movie." |
| `annotate(Avg(...))` | Add a calculated number (average rating) to each object in your list without a separate query. |
| `QuerySet.filter()` | Chain filters for the filter bar: `.filter(genre__name='Sci-Fi').filter(status='watched')` |
| `Q` objects | For the title search: `filter(Q(title__icontains=search))` |
| `LoginRequiredMixin` | Only logged-in users can add/edit/delete movies or write reviews. |
| Template conditionals | Show a green "Watched" badge, a yellow "Watching" badge, or a blue "Watchlist" badge. |
| `DeleteView` with cascade | When you delete a movie, its reviews are deleted too (that's what `on_delete=CASCADE` does). |
| Pagination with cards | 6 movies per page in a CSS grid. |

## Your 2-Week Plan

### Week 1: Build the pages

| Day | What to do |
|-----|-----------|
| **Mon** | Create project + app. Write all 3 models. Run migrations. Add some genres in the admin (Action, Comedy, Drama, Horror, Sci-Fi, Documentary). |
| **Tue** | Build the Add Movie form. Build the Movie List page. Show movies as cards (title, year, genre, status). No rating yet. No filters yet. |
| **Wed** | Build the Movie Detail page. Show the movie info. Add a simple list of reviews below it (just the text and rating for now). |
| **Thu** | Set up login/register. Add `LoginRequiredMixin` to add/edit/delete. Make sure users only see their own movies on "My Movies." |
| **Fri** | Create `base.html` with a nav bar (Home, My Movies, Genres, Add Movie, Logout). Make all templates extend it. Add CSS for the card grid. |

### Week 2: Add ratings, filters, and polish

| Day | What to do |
|-----|-----------|
| **Mon** | Build the "Write a Review" form on the Movie Detail page (rating: 1–5 dropdown, text: textarea). Save it. Show it in the review list. |
| **Tue** | Add `annotate(Avg('reviews__rating'))` to the Movie List queryset. Display the average as stars on each card (e.g., ★★★★☆ 4.2). |
| **Wed** | Add the filter bar (genre dropdown + status dropdown + search input). Read `request.GET` and apply the filters in your view. |
| **Thu** | Build the Edit Movie page (mostly for changing status). Build the Delete confirmation. Build the Genre List page with counts. Add pagination (6 per page). |
| **Fri** | Write your README with screenshots. Polish the CSS (make the cards look nice, style the badges and stars). Push to GitHub. You're done. |

## What to Turn In

- [ ] A working website where you can add movies, write reviews, and see average ratings
- [ ] Filter bar working (genre + status + search all work together)
- [ ] Average rating displayed on cards and detail page
- [ ] "My Movies" page showing only your movies
- [ ] A README with: how to run it, screenshots of every page
- [ ] A GitHub repo with all your code

---

---
# Deploy your final project online✅

<!-- ## Updated Quick Comparison

| # | Project | Type | Core Skills | Difficulty |
|---|---------|------|-------------|------------|
| 1 | Poll / Survey API | DRF | Nested serializers, `@action`, Custom permissions | Easy–Medium |
| 2 | Restaurant Menu & Order API | DRF | Role-based permissions, Nested writable fields, Status workflow | Medium |
| 3 | Library Management | Django UI | Relationships, Aggregation, Business logic, Admin | Medium |
| 4 | Event Registration | Django UI | DateTime validation, Annotate, Messages, Capacity logic | Easy–Medium |
| 5 | Movie Watchlist & Review | Django UI | Two ForeignKeys, `annotate(Avg)`, Filtering, Card layout | Easy–Medium |

## Updated "How to Pick"

| If you want… | Pick this |
|-------------|-----------|
| The easiest API project | **#1** — Poll / Survey |
| The most "real" API project | **#2** — Restaurant Menu & Order |
| A website with two relationships and ratings | **#5** — Movie Watchlist & Review |
| The easiest website project | **#4** — Event Registration |
| A website with real business logic (issue/return) | **#3** — Library Management |
 -->
