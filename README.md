
# 💱 Currency Converter | Real-Time Streamlit App

A professional, interactive **currency converter web application** built using **Streamlit**, designed for seamless real-time conversion and insightful trend analysis. This project utilizes the **ExchangeRate API** and **Plotly visualizations** to provide accurate results and a clean, responsive user experience.

---

## 🧠 Objective

To develop a responsive and easy-to-use application that:

* **Converts currencies instantly** using real-time exchange rates
* **Visualizes trends** with advanced financial charting
* Displays a **live rate table** with reverse calculations
* Provides a **minimal, modern interface** compatible with dark mode

---

## 📌 Key Features

* 🔄 **Real-time currency conversion** across global currencies
* 📊 **Interactive charts**: Line, Area, Candlestick, and OHLC using Plotly
* 🧮 **Swap function** to reverse base and target currencies instantly
* 📈 **Volatility, average rate, and trend summaries**
* 📅 **Select time ranges** (7, 15, or 30 days) for historical analysis
* 📋 **Live exchange table** with reverse rates
* 🌙 **Dark-mode optimized layout** using custom CSS
* ⚡ **Streamlit caching** to reduce API calls and speed up rendering

---

## 🧰 Tech Stack

* **Streamlit** – Frontend and interactivity
* **ExchangeRate API** – Real-time exchange rates
* **Plotly** – Responsive and interactive charting
* **Pandas** – Data manipulation and time series formatting
* **Requests** – REST API handling and error checking

---

## 📁 Project Structure

```
currency-converter/
│
├── currency_converter.py         # Main Streamlit app
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
└── screenshots/                  # App preview images
    ├── dashboard.png
    ├── analytics_chart.png
    └── rates_table.png
```

---

## 📸 Screenshots

### 💻 Main Dashboard

<img width="1910" height="870" alt="Screenshot 2025-07-10 005033" src="https://github.com/user-attachments/assets/11958863-71cd-46e0-a9c3-0fbe9af39887" />

### 📈 Exchange Rate Trend View

<img width="1815" height="1009" alt="Screenshot 2025-07-10 005127" src="https://github.com/user-attachments/assets/a3977e39-ea40-4394-9925-021203c17ed3" />

### 📋 Live Rates Table

<img width="1808" height="1034" alt="Screenshot 2025-07-10 005141" src="https://github.com/user-attachments/assets/8230b153-3e3c-440d-95bc-208033fedd12" />

---



## 🌐 Deployment

### 🚀 Deploy to Streamlit Cloud

1. **Fork or upload** this repo to your GitHub
2. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your GitHub repo
4. Set `currency_converter.py` as the main file
5. Click **Deploy**

---

## ⚙️ Configuration Options

* **Add new currencies**: Edit the `CURRENCY_DATA` dictionary
* **Change chart durations**: Modify `chart_duration` in the dropdown options
* **Refresh frequency**: Adjust `@st.cache_data(ttl=...)`
* **Styling**: Customize via embedded HTML/CSS in Streamlit markdown blocks

---

## 🧠 How It Works

1. User selects **source** and **target** currencies
2. App fetches the **latest exchange rates** via API
3. Performs real-time **conversion and calculations**
4. Retrieves **historical time series** for plotting
5. Displays **interactive charts and live rates** with reverse lookups

---

## 👤 Project By

**Naman Agrawal**
Feel free to reach out and connect with me on [LinkedIn](https://www.linkedin.com/in/naman-agrawal-8671aa27b/) for collaboration or feedback.

---


