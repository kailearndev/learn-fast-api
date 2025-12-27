# FastAPI Todo App (Login + Calculator Demo)

Backend REST API sử dụng **FastAPI**  
Phục vụ mục đích học:

- Python backend cơ bản
- Cách tổ chức project theo module (giống NestJS / Go)
- Làm quen với layer: controller / service / repository / schema

---

## 🚀 Tech Stack

- Python 3.10+
- FastAPI
- Uvicorn
- Pydantic
- (sẽ thêm) Supabase (PostgreSQL + Auth)

---

## 📦 Installation

### 1️⃣ Clone project

```bash
git clone <repo-url>
cd fastapi-todo
```

### 2 Tạo virtual environment

## nếu chưa có virtual venv trên máy, cài đặt:

Linux/Mac:
sudo apt install python3-venv

Windows:
python -m pip install --user virtualenv

```bash
python -m venv venv
```

- Win:
  venv\Scripts\activate
- Mac / Linux:

  source venv/bin/activate

### 3 Cài đặt dependencies

##Install dependencies:

```bash
pip install -r requirements.txt
```

<!-- ```bash
pip install fastapi uvicorn

``` -->

### 4 Chạy project

```bash
python main.py # hoặc
python3 main.py

```

# uvicorn main:app --reload

```

- Mở trình duyệt truy cập http://127.0.0.1:8000
- Mở Swagger UI: http://127.0.0.1:8000/docs

---## 🛠 Project Structure

```

app/
├─ main.py # Entry point
├─ core/ # Code dùng chung toàn app
│ ├─ config.py # Config / env (sau này)
│ ├─ auth.py # Auth / JWT (sau này)
│ └─ supabase.py # Supabase client (sau này)
│
└─ modules/ # Feature-based modules
├─ calculator/
│ ├─ calculator.controller.py # Controller / Handler
│ ├─ calculator.service.py # Business logic
│ ├─ calculator.repository.py # Data / logic thấp
│ └─ calculator.schema.py # DTO / Validate
│
└─ todo/ # (sẽ làm tiếp)
├─ todo.controller.py
├─ todo.service.py
├─ todo.repository.py
└─ todo.schema.py

```

- `core/`: Chứa code dùng chung toàn app như config, auth, db client...
- `modules/`: Chứa các feature-based modules, mỗi module có controller, service, repository, schema riêng
- sẽ thêm supabase, auth, todo module sau
- nếu có supabase thì repository sẽ chứa logic thao tác db

### NOTE thứ tự tạo module

1. Tạo thư mục module trong `modules/`
2. Tạo theo thứ tự file:
   - `schema.py`: Định nghĩa DTO / Validate
   - `repository.py`: Logic thao tác data (với db thì viết query ở đây)
   - `service.py`: Business logic, gọi repository xử lý
   - `controller.py`: Định nghĩa route, gọi service xử lý
   thứ tự tạo file từ dưới lên trên sẽ dễ hơn vì service phụ thuộc repository, controller phụ thuộc service
   cách tạo này giúp tách biệt rõ ràng các layer, dễ bảo trì và mở rộng
   ngoài ra tạo file thì tạo router luôn trong controller để đăng ký route

3. Đăng ký router trong `main.py`
   "# learn-fast-api"
```
