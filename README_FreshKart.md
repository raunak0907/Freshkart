
# 🛒 FreshKart – Smart Grocery Ordering Web App

![FreshKart Banner](https://i.imgur.com/CEa8j3B.png)

> A full-stack grocery store application built with Flask, SQLite, HTML5, Bootstrap5, and custom JavaScript. Inspired by platforms like Blinkit & BigBasket, **FreshKart** brings a responsive, modern UI, real-time cart management, secure login system, PDF invoices, and much more.

---

## 🚀 Demo

🌐 Live Deployment (optional): [https://freshkart-demo.vercel.app](#)

📽️ Preview Screenshots:

| 🏠 Homepage | 🛒 Product Listing | 🧾 Checkout & Invoice |
|------------|-------------------|------------------------|
| ![](https://i.imgur.com/M4Q2fXO.png) | ![](https://i.imgur.com/JQ7sd5T.png) | ![](https://i.imgur.com/8Vm3Txk.png) |

---

## 🧰 Tech Stack

| Layer            | Technology                        |
|------------------|-----------------------------------|
| **Frontend**     | HTML5, CSS3, Bootstrap 5, JS      |
| **Backend**      | Flask (Python)                    |
| **Database**     | SQLite (ORM ready)                |
| **PDF Generator**| ReportLab                         |
| **Session Mgmt** | Flask-Login, Flask Sessions       |
| **Deployment**   | Render / Railway / Localhost      |

---

## 🧠 Key Features

- 🔐 **User Authentication** (Register, Login, Forgot Password)
- 🛍️ **Real-time Cart System** with Add/Remove functionality
- 🧾 **PDF Invoice Generation** on Checkout
- ✅ **Stock & Discount Handling**
- 💬 **Flash Notifications** for all actions
- 📦 **Product Categories, Brands, and Sorting**
- 📱 **Fully Responsive UI** with smooth UX
- 📊 **Admin-ready structure** (CRUD support coming)
- 🌈 **Glassmorphism UI** on login/register (modern feel)
- 📥 **Order Confirmation with animation**

---

## 📁 Folder Structure

```bash
freshkart/
├── static/
│   ├── css/
│   ├── js/
│   └── invoices/
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── products.html
│   ├── cart.html
│   ├── checkout.html
│   ├── order_confirmation.html
│   └── auth/
│       ├── login.html
│       ├── register.html
│       ├── forgot_password.html
│       └── reset_password.html
├── db/
│   └── freshkart.db
├── create_db.py
├── app.py
└── requirements.txt
```

---

## ⚙️ Installation & Setup

### 🖥️ Localhost

1. **Clone the repository**

```bash
git clone https://github.com/your-username/freshkart.git
cd freshkart
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Run DB setup**

```bash
python create_db.py
```

4. **Run the app**

```bash
python app.py
```

> App will be available at: `http://127.0.0.1:5000/`

---

## 💼 Resume Value

| Skill Demonstrated         | Description |
|---------------------------|-------------|
| ✅ Full-Stack Architecture | Flask + SQL + Bootstrap + REST |
| ✅ UI/UX Best Practices    | Responsive, animated, accessible |
| ✅ Authentication & Security | Hashing-ready login + forgot/reset flow |
| ✅ PDF + Files Handling    | Real-world business logic |
| ✅ Deployment Readiness    | Vercel, Render, Railway-compatible |
| ✅ Documentation           | This README shows your professionalism |

---

## 🔮 Future Enhancements

- 🔄 API Layer with Flask-RESTful
- 🧾 Email PDF invoice via Flask-Mail
- 🔍 Advanced Search, Filters, Pagination
- 🛡️ Password Hashing & OAuth Login (Google/Facebook)
- 📊 Admin Dashboard & Analytics

---

## 📞 Connect With Me

> 👤 **Raunak Rathor**  
📧 `2005raunakrathor@gmail.com`  
🔗 [LinkedIn](https://www.linkedin.com/in/raunak-rathor-3b8625323) | [LeetCode](https://leetcode.com/u/__ronyyyy/)
