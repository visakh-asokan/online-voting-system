# 🗳 Online Voting System

A web-based voting system built using Django that allows users to securely vote and admins to manage elections.

---

## 🚀 Features

### 👤 User

* Register with college email
* Login & Logout
* View elections (Active / Upcoming / Closed)
* Vote (only once per election)
* View results after election ends
* Change password

### 🛠 Admin

* Create elections
* Add/Delete candidates
* Stop voting
* Delete elections
* View real-time results

---

## 🧠 Tech Stack

* Backend: Django (Python)
* Frontend: HTML, CSS, JavaScript
* Database: SQLite

---

## 📂 Project Structure


online_voting_system/
│
├── voting/
├── voting_system/
├── manage.py
├── requirements.txt
└── README.md


---

## ⚙️ Setup Instructions


git clone <your-repo-link>
cd online_voting_system

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver

---

## 🌐 Usage

* User login: `/login/`
* Admin dashboard: `/admin-dashboard/`
* Django admin: `/admin/`

---

## 🔐 Security Features

* One user → one vote
* Email validation
* Role-based access control
* Login authentication

---

## 📌 Future Improvements

* OTP verification
* Blockchain-based voting
* Live result updates
* Email notifications

---

## 👨‍💻 Author

Visakh A
