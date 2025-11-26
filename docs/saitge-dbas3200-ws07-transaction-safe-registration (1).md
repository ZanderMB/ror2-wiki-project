![alt text](image.png)

---

### *DBAS 3200 – Data-Driven Application Programming*

**Instructor:** Davis Boudreau
**Week:** 7
**Title:** Transaction-Safe Event Registration with Django
**Workshop Type:** Guided Activity
**Estimated Time:** 3 hours

---

# **0. Assignment Details**

| Field              | Value                                             |
| ------------------ | ------------------------------------------------- |
| **Course**         | DBAS 3200 – Data-Driven Application Programming   |
| **Workshop**       | 07 – Transaction-Safe Event Registration          |
| **Instructor**     | Davis Boudreau                                    |
| **Tools Required** | Docker, VS Code, PostgreSQL, pgAdmin, Django      |
| **Pre-Requisites** | Workshop 06 (Docker Django Setup), MP1            |
| **Deliverables**   | README.md reflections + blank file in Brightspace |

---

# **1. Overview / Purpose / Objectives**

## **Purpose**

This workshop teaches you how to design **safe, real-world multi-step transactional workflows** using Django, PostgreSQL, and Docker. You will build a complete workflow for registering attendees for events, ensuring:

* no overbooking
* no duplicate registrations
* no partial updates
* clear user feedback
* database consistency under concurrency

This work prepares you for **MP2**, **MP3**, and the **Final Project**.

---

## **Objectives**

After completing this workshop, you will be able to:

* Apply Django's `@transaction.atomic` decorator to guarantee all-or-nothing operations.
* Lock rows with `select_for_update()` to avoid race conditions.
* Create a reusable **service layer** to enforce business rules.
* Validate user input and display helpful error messages.
* Build event listing, event registration, and registration success pages.
* Verify transactional integrity using pgAdmin.
* Document reasoning in a README.md professional reflection.

---

# **2. Learning Outcomes Addressed**

This workshop develops:

* **Outcome 1:** Implement a Data Access Layer (ORM).
* **Outcome 4:** Manipulate data within applications (CRUD).
* **Outcome 5:** Exercise application-level transactional control.
* **Outcome 6:** Develop professional workflow practices.

---

# **3. Conceptual Background (Deep Framing)**

## **A) What is a Transaction?**

A transaction is a set of operations that must either **all succeed** or **all fail**.

Example:

* Check event capacity
* Create attendee
* Create registration
* Update seats_taken

Without transaction safety → **data corruption**.

---

## **B) Why Use Application-Level Control?**

Databases enforce structural rules.
Applications enforce **business rules**.

Examples:

* “Don’t allow duplicate registrations.”
* “Event cannot exceed capacity.”
* “Seats_taken must reflect the number of registrations.”

---

## **C) Why Row Locking (`select_for_update`) Matters**

Without row locks:

* Two users both see “1 seat left”
* Both try to register
* Both succeed
* Capacity becomes negative

With row locks:

* One request locks the event row
* Second waits
* Only one proceeds

---

## **D) Importance of User Feedback**

Don’t leave users confused.

Typical necessary messages:

* “Event is full.”
* “You are already registered.”
* “Both name and email are required.”
* “Registration successful!”

This improves UX and makes your app production-quality.

---

# **4. Activity Tasks / Instructions**

---

# **Step 0 — Start Docker Stack**

```bash
make up
make web
```

Verify:

* Django → [http://localhost:8000](http://localhost:8000)
* pgAdmin → [http://localhost:5050](http://localhost:5050)

---

# **Step 1 — Create/Update Django Models**

Create `events/models.py`:

```python
from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    location = models.CharField(maxmaxlength=150, blank=True, null=True)
    capacity = models.PositiveIntegerField(default=50)
    seats_taken = models.PositiveIntegerField(default=0)

    @property
    def seats_available(self):
        return self.capacity - self.seats_taken

    def __str__(self):
        return f"{self.title} ({self.date})"


class Attendee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.name} <{self.email}>"


class Registration(models.Model):
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("attendee", "event")
```

Run:

```bash
make makemigrations
make migrate
```

---

# **Step 2 — Implement Transactional Service Layer**

Create `events/services.py`:

```python
from django.db import transaction, IntegrityError
from .models import Event, Attendee, Registration

class RegistrationService:

    @transaction.atomic
    def register_attendee_for_event(self, name, email, event_id):
        attendee, _ = Attendee.objects.get_or_create(
            email=email,
            defaults={"name": name}
        )

        event = Event.objects.select_for_update().get(id=event_id)

        if event.seats_available <= 0:
            raise ValueError("Event is full. No seats available.")

        try:
            Registration.objects.create(attendee=attendee, event=event)
        except IntegrityError:
            raise ValueError("You are already registered for this event.")

        event.seats_taken += 1
        event.save()

        return {"attendee": attendee.name, "event": event.title}
```

---

# **Step 3 — Build Views and URL Routing**

### `events/views.py`

```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event
from .services import RegistrationService

def event_list_view(request):
    events = Event.objects.all().order_by("date")
    return render(request, "events/event_list.html", {"events": events})


def register_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    error = None

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()

        if not name or not email:
            error = "Both name and email are required."
        else:
            service = RegistrationService()
            try:
                service.register_attendee_for_event(name, email, event.id)
                return redirect("events:event_register_success", event_id=event.id)
            except ValueError as e:
                error = str(e)

    return render(request, "events/register.html", {"event": event, "error": error})


def register_success_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, "events/register_success.html", {"event": event})
```

---

### `events/urls.py`

```python
from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path("", views.event_list_view, name="event_list"),
    path("<int:event_id>/register/", views.register_view, name="event_register"),
    path("<int:event_id>/register/success/", views.register_success_view, name="event_register_success"),
]
```

Add to main URLs:

`core/core/urls.py`:

```python
path("events/", include("events.urls", namespace="events")),
```

---

# **Step 4 — Build Templates**

Create folder:

```
templates/
    base.html
    events/
        event_list.html
        register.html
        register_success.html
```

### **base.html**

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8" />
    <title>{% block title %}Event App{% endblock %}</title>
</head>
<body>

<header>
  <h1>Event Management System</h1>
  <nav><a href="{% url 'events:event_list' %}">Events</a></nav>
  <hr>
</header>

<main>
{% block content %}{% endblock %}
</main>

</body>
</html>
```

---

### **event_list.html**

```html
{% extends "base.html" %}
{% block title %}Events{% endblock %}
{% block content %}
<h2>Event List</h2>

{% for event in events %}
  <div>
    <h3>{{ event.title }}</h3>
    <p>Date: {{ event.date }}</p>
    <p>Seats: {{ event.seats_taken }} / {{ event.capacity }}</p>

    {% if event.seats_available > 0 %}
      <a href="{% url 'events:event_register' event.id %}">Register</a>
    {% else %}
      <strong>Event Full</strong>
    {% endif %}
  </div>
  <hr>
{% endfor %}
{% endblock %}
```

---

### **register.html**

```html
{% extends "base.html" %}
{% block title %}Register{% endblock %}
{% block content %}

<h2>Register for {{ event.title }}</h2>

{% if error %}
  <p style="color:red;">{{ error }}</p>
{% endif %}

<form method="POST">
  {% csrf_token %}
  <label>Name:</label><br>
  <input name="name" /><br><br>

  <label>Email:</label><br>
  <input name="email" type="email" /><br><br>

  <button type="submit">Submit Registration</button>
</form>

{% endblock %}
```

---

### **register_success.html**

```html
{% extends "base.html" %}
{% block title %}Success{% endblock %}
{% block content %}
<h2>Registration Successful!</h2>
<p>You are registered for <strong>{{ event.title }}</strong>.</p>
<a href="{% url 'events:event_list' %}">Return to Event List</a>
{% endblock %}
```

---

# **Step 5 — Create Events Using ALL THREE METHODS**

## **Method A — Django Admin (Recommended)**

1. Visit:
   [http://localhost:8000/admin](http://localhost:8000/admin)
2. Log in
3. Click **Events**
4. Create:

| Title           | Date       | Capacity |
| --------------- | ---------- | -------- |
| Tech Conference | 2025-03-10 | 4        |
| Web Summit      | 2025-04-05 | 2        |
| Workshop Day    | 2025-05-12 | 1        |

---

## **Method B — Seed Script**

Create:

**`seed_events.py`**

```python
from events.models import Event
from datetime import date

def run():
    Event.objects.create(title="Tech Conference", date=date(2025,3,10), capacity=4)
    Event.objects.create(title="Web Summit", date=date(2025,4,5), capacity=2)
    Event.objects.create(title="Workshop Day", date=date(2025,5,12), capacity=1)
    print("Seed events created!")
```

Run:

```bash
python manage.py shell < seed_events.py
```

---

## **Method C — Django Shell**

```bash
make web
python manage.py shell
```

```python
from events.models import Event
from datetime import date

Event.objects.create(title="Tech Conference", date=date(2025,3,10), capacity=4)
Event.objects.create(title="Web Summit", date=date(2025,4,5), capacity=2)
Event.objects.create(title="Workshop Day", date=date=2025,5,12), capacity=1)
```

---

# **Step 6 — Test the Workflow**

---

## **6B — Test Registration Flow (Detailed)**

### 1. Visit Events List Page

[http://localhost:8000/events/](http://localhost:8000/events/)

### 2. Click **Register** on an event

You will be taken to:

```
/events/<event_id>/register/
```

### 3. Fill in the form

Example:

```
Name: Alice Johnson
Email: alice@example.com
```

### 4. Submit and expect

**Redirect to success page:**

```
/events/<event_id>/register/success/
```

### 5. Return to event list and verify updated seats_taken

---

## **6C — Test Error Scenarios (Detailed)**

### **1. Missing fields**

Submit blank name or email:

Expected:

```
Both name and email are required.
```

---

### **2. Duplicate registration**

Register once successfully.
Register again with same email.

Expected:

```
You are already registered for this event.
```

---

### **3. Full event**

Set capacity to 1.
Register once.
Register again.

Expected:

```
Event is full. No seats available.
```

---

## **6D — Inspect Data in pgAdmin (Detailed)**

### 1. Visit pgAdmin

[http://localhost:5050](http://localhost:5050)

### 2. Navigate to tables:

```
events_event
events_attendee
events_registration
```

### 3. Verify:

* seats_taken incremented appropriately
* Attendee row inserted
* Registration row inserted
* No duplicates
* No corruption

---

# **Step 7 — README.md Reflection**

Create `README.md`:

```markdown
# DBAS3200 – Workshop 07 Reflection

## 1. Why do we need @transaction.atomic?
<answer>

## 2. How does select_for_update prevent overbooking?
<answer>

## 3. What rules come from the database vs the application layer?
<answer>

## 4. How does user feedback improve the registration flow?
<answer>

## 5. What failure scenarios did you test?
<answer>

## 6. How would this change if payments were added?
<answer>
```

---

# **Step 8 — Brightspace Submission**

### Students must submit:

### **1. Blank file (reflection.txt)**

Contents:

```
Reflection answers are in the Brightspace comment box.
```

### **2. Paste reflection answers in Brightspace comments**

---

# **Step 9 — Deliverables**

| Deliverable            | Location                            |
| ---------------------- | ----------------------------------- |
| Models                 | `events/models.py`                  |
| Services               | `events/services.py`                |
| Views + URLs           | `events/views.py`, `events/urls.py` |
| Templates              | `templates/events/`                 |
| README.md              | project root                        |
| Brightspace blank file | Brightspace                         |
| Reflection answers     | Brightspace comments                |

---

# **Evaluation Rubric**

| Category                 | Description                        | Weight |
| ------------------------ | ---------------------------------- | ------ |
| Technical Implementation | Correct, transaction-safe workflow | 40%    |
| User Experience          | Fully functional forms + feedback  | 25%    |
| Documentation            | README reflections                 | 20%    |
| Professionalism          | Git hygiene, structure             | 15%    |

---
