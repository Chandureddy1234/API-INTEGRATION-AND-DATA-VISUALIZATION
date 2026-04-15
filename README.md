# API-INTEGRATION-AND-DATA-VISUALIZATION

*COMPANY*: CODTECH IT SOLUTIONS

*NAME*: KALYAM CHANDU REDDY

*INTERN ID*: CTIS6413

*DOMAIN*: PYTHON PROGRAMMING

*DURATION*: 12 WEEKS

*MENTOR*: NEELA SANTHOSH KUMAR

Weather Analytics Dashboard (API Integration & Data Visualization)

This project focuses on building a **real-time Weather Analytics Dashboard** by integrating a public API and transforming raw data into meaningful visual insights. The objective was to demonstrate **API integration, data processing, and advanced visualization using Python**.

### 🔧 Project Implementation

The project was developed using **Python in Visual Studio Code**, leveraging key libraries such as:

* `requests` – for API communication
* `pandas` – for data manipulation
* `matplotlib` & `seaborn` – for advanced visualizations

The workflow begins by dynamically accepting a **city name as user input**, which is then converted into geographic coordinates using the **Open-Meteo Geocoding API**. These coordinates are used to fetch **hourly weather data** including temperature, humidity, and wind speed.

The raw JSON data is processed into a structured **Pandas DataFrame**, where additional features such as **date and hourly breakdown** are derived for deeper analysis.

### 📈 Dashboard Features

A fully customized **Power BI-style dashboard** is generated using Matplotlib and Seaborn, containing:

* **KPI Cards**

  * Average Temperature
  * Maximum Temperature
  * Minimum Temperature
  * Average Humidity

* **Time-Series Analysis**

  * Temperature trend over time
  * Humidity variation
  * Wind speed fluctuations

* **Distribution Analysis**

  * Temperature histogram with density curve

* **Advanced Visualization**

  * Hourly temperature heatmap showing patterns across days

The dashboard is carefully designed with **grid layouts, color themes, spacing optimization, and visual hierarchy** to ensure clarity and professional presentation.

### 💡 Key Highlights

* Real-time **API data integration (no static dataset used)**
* Clean and modular code structure (functions for each stage)
* Advanced visualization layout using **subplot grids**
* Exportable output (`weather_dashboard.png`) for reporting
* Handles errors such as invalid city input and API failures

### 🚀 Use Cases

This project demonstrates how raw API data can be transformed into actionable insights and can be applied in:

* Weather monitoring systems
* Smart city analytics
* Data visualization dashboards
* Real-time reporting tools

#OUTPUT 

<img width="2661" height="3002" alt="Image" src="https://github.com/user-attachments/assets/8fd86965-35eb-43f3-b200-90c3ccaba029" />
