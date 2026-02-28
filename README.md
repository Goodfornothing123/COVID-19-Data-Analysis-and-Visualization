# COVID-19 Global Data Analysis & Visualization Dashboard

## 📌 Project Overview
This project is a high-performance, interactive web-based dashboard designed to track and analyze the global impact of COVID-19. It provides real-time insights into cases, mortality rates, and vaccination progress across the globe using data from reliable sources.

**Author:** Md Shamshad Shamim

## ✨ Key Features
- **Real-time Global Metrics**: Total Cases, Deaths, Vaccinations, and Case Fatality Rates.
- **Interactive Daily Trends**: 7-day moving averages of new cases for multi-country comparison.
- **Global Heatmaps**: Geographic visualization of the pandemic spread.
- **Vaccination Analysis**: Tracking the percentage of fully vaccinated populations.
- **Positivity vs. Testing**: Correlation analysis between testing capacity and positivity rates.
- **Premium UI**: Dark-themed, glassmorphic design for a modern aesthetic.

## 🛠️ Technology Stack
- **Language**: Python 3.x
- **Frontend/Dashboard**: Streamlit
- **Data Manipulation**: Pandas, NumPy
- **Visualizations**: Plotly Express, Plotly Graph Objects
- **Data Source**: Our World in Data (OWID)

## 🚀 How to Run
1. **Clone the project** or download the files into a folder.
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Launch the Dashboard**:
   ```bash
   streamlit run app.py
   ```

## ☁️ Deployment on Streamlit Cloud
1.  Upload all these files to your **GitHub** repository.
2.  Go to [share.streamlit.io](https://share.streamlit.io/).
3.  Connect your GitHub account.
4.  Select your repository, branch (`main`), and main file path (`app.py`).
5.  Click **Deploy**! Streamlit will automatically read `requirements.txt` and set up the environment.

## 📊 Data Insights
The dashboard utilizes the Our World in Data (OWID) dataset, which is updated daily. It focuses on:
- **Trend Smoothing**: Using 7-day averages to remove reporting noise.
- **Relative Metrics**: Normalizing data (per hundred, per thousand) for fair country comparisons.
- **Interactive Filtering**: Dynamic sidebars for intuitive data exploration.

---
*Produced by Md Shamshad Shamim for academic submission.*
