# 📊 Nifty 50 Stock Market Analysis Dashboard

## 🚀 Project Overview

This project is an end-to-end **Stock Market Analysis Dashboard** built using:

* 🐍 Python (Data Processing & Analysis)
* 🗄️ PostgreSQL (Data Storage)
* 📊 Power BI (Business Intelligence Dashboard)
* 🌐 Streamlit (Interactive Web App)

The project analyzes **Nifty 50 stocks** to identify:

* Top & worst performing stocks
* Volatility trends
* Sector-wise performance
* Correlation between stocks
* Monthly gainers & losers

---

## 🧩 Project Architecture

```
Data Source → Data Cleaning (Jupyter Notebook)
           → PostgreSQL Database
           → Streamlit App (Visualization)
           → Power BI Dashboard
```

---

## 📁 Files in Repository

### 1️⃣ `Data_Extraction_Transformation.ipynb`

* Data cleaning and preprocessing
* Feature engineering:

  * Daily returns
  * Monthly returns
  * Financial year mapping
* Prepares dataset for database storage

---

### 2️⃣ `app.py`

A **Streamlit dashboard** that provides:

#### 🔹 Key Features

* 📌 Total Stocks, Green Stocks, Red Stocks
* 📈 Top 10 Performing Stocks (Yearly Returns)
* 📉 Bottom 10 Performing Stocks
* ⚡ Volatility Analysis (Top 10 most volatile stocks)
* 📊 Cumulative Return (Top 5 stocks)
* 🏭 Sector-wise Performance
* 🔥 Correlation Heatmap
* 📅 Monthly Top 5 Gainers & Losers

#### 🔹 Tech Used

* Pandas, NumPy
* Matplotlib, Seaborn
* Plotly (interactive charts)
* SQLAlchemy (DB connection)
* Streamlit UI

---

### 3️⃣ `Stock_Pro.pbix`

Power BI Dashboard containing:

* Interactive filtering
* Monthly performance visualization
* Sector insights
* Top/Bottom stock comparison
* Business-level insights for decision making

---

## 🗄️ Database Setup (PostgreSQL)

Make sure PostgreSQL is running and update credentials in `app.py`:

```python
engine = create_engine(
    "postgresql+psycopg2://username:password@localhost:5432/Stock_Db"
)
```

### Required Tables:

* `stock_data`
* `sector_df_data`

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/stock-analysis-dashboard.git
cd stock-analysis-dashboard
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If requirements file not available:

```bash
pip install streamlit pandas numpy matplotlib seaborn plotly sqlalchemy psycopg2
```

---

### 3️⃣ Run Streamlit App

```bash
streamlit run app.py
```

---

## 📊 Key Insights Generated

* 📈 Identifies **top performing stocks** based on yearly return
* 📉 Detects **loss-making stocks**
* ⚡ Measures **volatility using standard deviation**
* 🔗 Shows **correlation between stocks**
* 🏭 Highlights **best/worst sectors**
* 📅 Tracks **monthly gainers & losers trends**

---

## 🎯 Use Cases

* 📊 Stock market analysis
* 💼 Investment decision support
* 📉 Risk analysis (volatility & correlation)
* 📈 Portfolio optimization insights

---

## ⚠️ Known Issues / Improvements

* Database dependency (PostgreSQL required)
* Credentials are hardcoded (should use `.env`)
* Large datasets may impact performance
* UI can be enhanced further

---

## 🔮 Future Enhancements

* ✅ Add live stock data (API integration)
* ✅ Deploy Streamlit app online
* ✅ Add predictive analytics (ML models)
* ✅ User authentication system
* ✅ Real-time dashboard updates

---

## 👩‍💻 Author

**Vinodhini**

* 💡 Skills: Python, Data Analysis, Power BI, SQL, Streamlit
* 📊 Passionate about Data & Stock Market Analytics

---

## ⭐ If you like this project

Give it a ⭐ on GitHub and share your feedback!
