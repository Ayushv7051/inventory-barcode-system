# Inventory Barcode System

A complete barcode-based inventory management system built with **Streamlit** (frontend), **Flask** (backend), and **MySQL** (database). This project enables real-time product tracking, inventory management, and barcode scanning.

---

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Database Setup](#database-setup)
- [Running the Project](#running-the-project)
- [How to Use](#how-to-use)
- [Project Files](#project-files)
- [Useful Links](#useful-links)

---

## ✨ Features

### Frontend (Streamlit)
- **Role-Based Access Control**: Staff and Admin roles with different permissions
- **Real-Time Barcode Scanning**: Camera integration for barcode detection
- **Product Management**: Create, update, and delete products
- **Inventory Adjustment**: Increase/decrease stock quantities
- **Search Functionality**: Search products by name or barcode
- **Live Dashboard**: View scanned products with running totals

### Backend (Flask API)
- RESTful API endpoints for product management
- Database operations (CRUD)
- Real-time inventory tracking
- Product search with filtering

### Database (MySQL)
- Structured product table with unique barcode indexing
- Automatic timestamps for audit trail
- Sample data included

---

## 📁 Project Structure

```
inventory-barcode-system/
├── app.py                    # Main Streamlit app with login & role-based routing
├── straam.py                 # Product scanner & inventory management interface
├── reader.py                 # Continuous barcode reader (read-only mode)
├── barcode.py                # Flask backend API server
├── check.py                  # Database connection test script
├── database_schema.sql       # MySQL database schema & sample data
└── README.md                 # This file
```

---

## 🔧 Prerequisites

Ensure you have the following installed on your system:

- **Python 3.8+**
- **MySQL Server** (or MariaDB)
- **pip** (Python package manager)

### Required Python Libraries:
- `streamlit` - Web framework for frontend
- `flask` - Backend API framework
- `mysql-connector-python` - MySQL database connector
- `opencv-python` (cv2) - Camera & barcode detection
- `pyzbar` - Barcode decoding
- `pandas` - Data handling
- `requests` - HTTP requests

---

## 📥 Installation & Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/Ayushv7051/inventory-barcode-system.git
cd inventory-barcode-system
```

### Step 2: Create Python Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

Or manually install:
```bash
pip install streamlit flask mysql-connector-python opencv-python pyzbar pandas requests
```

---

## 🗄️ Database Setup

### Step 1: Start MySQL Server
Ensure MySQL is running on your system.

### Step 2: Create Database
Open MySQL client or phpMyAdmin and execute the SQL script:

```bash
# Using MySQL command line
mysql -u root -p < database_schema.sql
```

Or copy-paste the contents of `database_schema.sql` in your MySQL client.

**Database Credentials (Update in code if different):**
- Host: `localhost`
- User: `root`
- Password: `` (empty by default)
- Database: `inventory_db`

### Step 3: Verify Database
Test the database connection:
```bash
python check.py
```

You should see product data printed if the connection is successful.

---

## 🚀 Running the Project

### Method 1: Run All Components (Recommended)

**Terminal 1 - Start Flask Backend API:**
```bash
python barcode.py
```
The API will start on `http://localhost:5000`

**Terminal 2 - Start Streamlit Frontend:**
```bash
streamlit run app.py
```
The app will open in your browser at `http://localhost:8501`

### Method 2: Individual Components

**Start Backend Only:**
```bash
python barcode.py
```

**Start Reader (Read-Only Mode):**
```bash
streamlit run reader.py
```

**Start Scanner (Edit Mode):**
```bash
streamlit run straam.py
```

---

## 💻 How to Use

### Login Page
1. Open the Streamlit app at `http://localhost:8501`
2. Enter credentials:
   - **Username**: `staff` | **Password**: `1234` → Access to Reader mode
   - **Username**: `admin` or `normal staff` | **Password**: `admin123` → Access to Scanner mode

### Scanner Mode (Straam)
- **Start Camera**: Click to activate barcode scanning
- **Scan Barcode**: Point camera at barcode (uses OpenCV detection)
- **Create Product**: Add new product if not found in database
- **Update Details**: Modify existing product information
- **Adjust Inventory**: Increase/decrease stock quantities
- **Search**: Find products by name or barcode

### Reader Mode (Read-Only)
- **Scan Products**: Same as Scanner but without edit permissions
- **View History**: See all scanned products in a table
- **Calculate Total**: Automatic running total of scanned items
- **Clear History**: Reset scanned items list

---

## 📂 Project Files Description

| File | Purpose |
|------|---------|
| `app.py` | Login system with role-based authentication & module routing |
| `straam.py` | Interactive barcode scanner with inventory management UI |
| `reader.py` | Read-only continuous barcode reader with live dashboard |
| `barcode.py` | Flask REST API backend with database operations |
| `check.py` | Database connectivity test utility |
| `database_schema.sql` | MySQL schema with sample product data |

---

## 🔗 Useful Links

- **Repository**: [GitHub - inventory-barcode-system](https://github.com/Ayushv7051/inventory-barcode-system)
- **Streamlit Docs**: [https://docs.streamlit.io](https://docs.streamlit.io)
- **Flask Docs**: [https://flask.palletsprojects.com](https://flask.palletsprojects.com)
- **MySQL Docs**: [https://dev.mysql.com/doc](https://dev.mysql.com/doc)
- **OpenCV Docs**: [https://docs.opencv.org](https://docs.opencv.org)
- **PyZBar Docs**: [https://github.com/NaturalHistoryMuseum/pyzbar](https://github.com/NaturalHistoryMuseum/pyzbar)

---

## 📝 Sample Test Data

The database comes with 5 sample products:

| Barcode | Product Name | Quantity | Price |
|---------|-------------|----------|-------|
| 12345678 | Product A | 50 | ₹299.99 |
| 87654321 | Product B | 30 | ₹499.99 |
| 11111111 | Product C | 100 | ₹199.99 |
| 22222222 | Product D | 20 | ₹799.99 |
| 33333333 | Product E | 75 | ₹99.99 |

Use these barcodes to test the scanning functionality!

---

## ⚙️ Configuration

### Update Database Credentials:
Edit the connection details in these files:
- `barcode.py` (Line ~6-10)
- `reader.py` (Line ~8-13)
- `check.py` (Line ~3-8)

Change:
```python
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",  # Change here
    database="inventory_db"
)
```

### Change Streamlit Port:
```bash
streamlit run app.py --server.port 8000
```

### Change Flask Port:
Edit `barcode.py` last line:
```python
app.run(host="0.0.0.0", port=5000, debug=True)  # Change 5000 to your port
```

---

## 📸 Features Highlight

✅ **Real-time Barcode Scanning** with OpenCV  
✅ **Role-Based Access Control** (Staff/Admin)  
✅ **CRUD Operations** for Products  
✅ **Live Inventory Tracking**  
✅ **Search & Filter** Functionality  
✅ **MySQL Database** with Proper Indexing  
✅ **REST API** Backend  
✅ **Responsive UI** with Streamlit  

---

## 🐛 Troubleshooting

### Camera Not Working?
- Check if your device has a camera
- Grant camera permissions to Python
- Try: `cv2.VideoCapture(0)` - use index 1 or 2 if 0 doesn't work

### Database Connection Error?
- Ensure MySQL is running
- Check credentials in code
- Run `python check.py` to test connection

### Barcode Not Detecting?
- Ensure good lighting conditions
- Place barcode at optimal angle (parallel to camera)
- Try using sample barcode: `12345678`

### Port Already in Use?
- Change port in app configuration
- Or kill existing process: `lsof -ti:5000 | xargs kill`

---

## 📧 Contact & Support

For issues, suggestions, or contributions:
- GitHub Issues: [Submit Issue](https://github.com/Ayushv7051/inventory-barcode-system/issues)
- GitHub Profile: [@Ayushv7051](https://github.com/Ayushv7051)

---

**Happy Barcode Scanning! 📦✨**
