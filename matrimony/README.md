
# Marry Matrimony Web App 

A fully functional matrimonial web application built using **Python Flask** and **MySQL**, designed to help users find their life partner. Users can register, upload profiles with photos, express interest in others, and view matched profiles. 

##  Tech Stack

- **Frontend**: HTML, CSS, Jinja2
- **Backend**: Python (Flask)
- **Database**: MySQL


---

## Features

-  User Registration with profile photo
-  Login/Logout authentication
-  Editable profile (name, age, phone, gender, religion, etc.)
-  Gender-based match feed (e.g., male sees only females)
-  View matched profiles like a social media feed
-  Express interest / connection requests
-  View profile details (non-editable)
-  Delete Account option
-  Filter by age, location, and searc


---

## Project Structure

```
matrimony/
│
├── static/
│   └── uploads/              
│   └── style.css             
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── register.html
│   ├── dash.html
│   ├── profile.html
│   └── view_profile.html
│
├── mat.py                    
└── README.md                 



## ⚙️ Setup Instructions

1. **Clone the repo**:
```bash
git clone https://github.com/Gopinath-C3/Marry_matrimony.git
cd Marry_matrimony
```

2. **Install dependencies**:
```bash
pip install flask flask-mysqldb
```

3. **Set up MySQL database**:
```sql
CREATE DATABASE matrimony;

USE matrimony;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    age INT,
    gender VARCHAR(20),
    location VARCHAR(100),
    religion VARCHAR(50),
    language_preference VARCHAR(50),
    bio TEXT,
    phone VARCHAR(20),
    profile_photo VARCHAR(255)
);


4. **Run the app**:
```bash
python mat.py
```

Visit `http://127.0.0.1:5000` in your browser.



## Security Notes

- Passwords are currently stored in plain text (not secure for production).
- Email and phone number are checked for uniqueness.
- Input validation needs to be enhanced for production usage.

---

## Future Improvements

- Password encryption (e.g., bcrypt)
- Email verification
- Chat functionality between users
- Admin dashboard for monitoring


