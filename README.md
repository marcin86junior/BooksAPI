# BooksAPI

**BooksAPI** is an application for managing books.

---

## 📋 Main Requirements

- Python 3.10
- Django 5.2
- djangorestframework 3.16.0

---

## 🛠️ Local installation

### 1. Prepare the environment

```bash
mkdir Zadanie_2_BooksAPI
cd Zadanie_2_BooksAPI
git clone https://github.com/marcin86junior/BooksAPI.git .
cd Zadanie_2_BooksAPI
python -m venv .venv
```

### 2. Activate the environment
- **Windows (PowerShell)**:
  ```bash
  .venv\Scripts\activate
  ```
- **Linux/macOS**:
  ```bash
  source .venv/bin/activate
  ```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure the environment
Copy the `.env.template` file and fill in the appropriate data:

```bash
cp .env.template .env
```
⚠️ **Do not add `.env` file to the repository!** Use `.env.template` as template.

### 5. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
### 6. Create a superuser
```bash
python manage.py createsuperuser
```
### 7. Run the server
```bash
python manage.py runserver
```

### 8. Run test
```bash
python manage.py test
```

---

## 🐳 Run via Docker
### 1. Build the image
```bash
docker-compose up -d --build
```
### 2. Run the container
```bash
docker-compose up
```

---

## 🌐 Avaiable adresses
- App: http://127.0.0.1:8000/
- Swagger: http://127.0.0.1:8000/swagger/
- Admin: http://127.0.0.1:8000/admin/
