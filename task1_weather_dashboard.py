# task1_weather_dashboard.py

import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import urllib3

urllib3.disable_warnings()

sns.set_theme(style="whitegrid", context="talk")
plt.rcParams["grid.alpha"] = 0.3

# -----------------------------
# GET CITY COORDINATES
# -----------------------------
def get_city():

    city = input("\nEnter City Name: ")

    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 1
    }

    response = requests.get(geo_url, params=params, verify=False)
    data = response.json()

    if "results" not in data:
        print("City not found")
        return None, None, None

    lat = data["results"][0]["latitude"]
    lon = data["results"][0]["longitude"]
    name = data["results"][0]["name"]

    return lat, lon, name


# -----------------------------
# FETCH WEATHER DATA
# -----------------------------
def fetch_weather(lat, lon):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "wind_speed_10m"
        ],
        "timezone": "auto"
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10,
            verify=False
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:

        print("Error fetching weather data:", e)
        return None


# -----------------------------
# PROCESS DATA
# -----------------------------
def process_data(data):

    hourly = data["hourly"]

    df = pd.DataFrame({
        "Datetime": pd.to_datetime(hourly["time"]),
        "Temperature": hourly["temperature_2m"],
        "Humidity": hourly["relative_humidity_2m"],
        "WindSpeed": hourly["wind_speed_10m"]
    })

    df["Hour"] = df["Datetime"].dt.hour
    df["Date"] = df["Datetime"].dt.date

    return df


# -----------------------------
# CREATE DASHBOARD
# -----------------------------
def create_dashboard(df, city):

    avg_temp  = round(df["Temperature"].mean(), 2)
    max_temp  = df["Temperature"].max()
    min_temp  = df["Temperature"].min()
    avg_hum   = round(df["Humidity"].mean(), 2)
    avg_wind  = round(df["WindSpeed"].mean(), 2)

    # ── global style ──────────────────────────────────────────
    sns.set_theme(style="whitegrid", context="notebook")
    plt.rcParams.update({
        "axes.spines.top":   False,
        "axes.spines.right": False,
        "grid.alpha":        0.25,
        "grid.linestyle":    "--",
    })

    BG = "#F4F6F9"
    fig = plt.figure(figsize=(22, 22), facecolor=BG)

    # 4-column grid: rows = [KPI, trend1, trend2, heatmap]
    grid = fig.add_gridspec(
        nrows=4,
        ncols=4,
        height_ratios=[0.42, 1.15, 1.15, 1.5],
        hspace=0.70,
        wspace=0.38,
    )

    fig.suptitle(
        f"Weather Analytics Dashboard  —  {city}",
        fontsize=26,
        fontweight="bold",
        color="#1A237E",
        y=0.975,
    )

    # ── KPI boxes (one per column) ────────────────────────────
    kpi_items = [
        ("Avg Temp",     f"{avg_temp}°C",  "#E53935", "#FFEBEE"),
        ("Max Temp",     f"{max_temp}°C",  "#FF6D00", "#FFF3E0"),
        ("Min Temp",     f"{min_temp}°C",  "#1E88E5", "#E3F2FD"),
        ("Avg Humidity", f"{avg_hum}%",    "#00897B", "#E0F2F1"),
    ]

    for col, (label, value, clr, bg) in enumerate(kpi_items):
        ax = fig.add_subplot(grid[0, col])
        ax.set_facecolor(bg)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_edgecolor(clr)
            spine.set_linewidth(2.2)
        ax.text(0.5, 0.70, label, ha="center", va="center",
                fontsize=13, color="#444444", fontweight="bold",
                transform=ax.transAxes)
        ax.text(0.5, 0.30, value, ha="center", va="center",
                fontsize=24, color=clr, fontweight="bold",
                transform=ax.transAxes)

    # ── helper: clean date x-axis ─────────────────────────────
    def fmt_date_axis(ax):
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        ax.tick_params(axis="x", rotation=30, labelsize=10)
        ax.set_xlabel("")

    # ── Temperature Trend ─────────────────────────────────────
    ax1 = fig.add_subplot(grid[1, :2])
    ax1.set_facecolor("#FFF9F9")
    sns.lineplot(data=df, x="Datetime", y="Temperature",
                 color="#E53935", linewidth=2.2, ax=ax1)
    ax1.fill_between(df["Datetime"], df["Temperature"],
                     df["Temperature"].min(), alpha=0.15, color="#E53935")
    ax1.set_title("Temperature Trend (°C)", fontsize=14,
                  fontweight="bold", pad=12)
    ax1.set_ylabel("Temperature (°C)", fontsize=11)
    fmt_date_axis(ax1)

    # ── Humidity Trend ────────────────────────────────────────
    ax2 = fig.add_subplot(grid[1, 2:])
    ax2.set_facecolor("#F5F9FF")
    sns.lineplot(data=df, x="Datetime", y="Humidity",
                 color="#1E88E5", linewidth=2.2, ax=ax2)
    ax2.fill_between(df["Datetime"], df["Humidity"],
                     df["Humidity"].min(), alpha=0.15, color="#1E88E5")
    ax2.set_title("Humidity Trend (%)", fontsize=14,
                  fontweight="bold", pad=12)
    ax2.set_ylabel("Humidity (%)", fontsize=11)
    fmt_date_axis(ax2)

    # ── Wind Speed Trend ──────────────────────────────────────
    ax3 = fig.add_subplot(grid[2, :2])
    ax3.set_facecolor("#F5FFF7")
    sns.lineplot(data=df, x="Datetime", y="WindSpeed",
                 color="#43A047", linewidth=2.2, ax=ax3)
    ax3.fill_between(df["Datetime"], df["WindSpeed"],
                     df["WindSpeed"].min(), alpha=0.15, color="#43A047")
    ax3.set_title("Wind Speed Trend (km/h)", fontsize=14,
                  fontweight="bold", pad=12)
    ax3.set_ylabel("Wind Speed (km/h)", fontsize=11)
    fmt_date_axis(ax3)

    # ── Temperature Distribution ──────────────────────────────
    ax4 = fig.add_subplot(grid[2, 2:])
    ax4.set_facecolor("#FFFBF0")
    sns.histplot(df["Temperature"], bins=20, kde=True,
                 color="#FB8C00", edgecolor="white", ax=ax4)
    ax4.set_title("Temperature Distribution (°C)", fontsize=14,
                  fontweight="bold", pad=12)
    ax4.set_xlabel("Temperature (°C)", fontsize=11)
    ax4.set_ylabel("Count", fontsize=11)

    # ── Hourly Temperature Heatmap ────────────────────────────
    pivot = df.pivot_table(
        values="Temperature",
        index="Hour",
        columns="Date",
    ).sort_index()

    ax5 = fig.add_subplot(grid[3, :])
    sns.heatmap(
        pivot,
        cmap="coolwarm",
        ax=ax5,
        linewidths=0.4,
        linecolor="#DDDDDD",
        cbar_kws={"label": "Temperature (°C)", "shrink": 0.75,
                  "pad": 0.02},
    )
    ax5.set_title("Hourly Temperature Heatmap", fontsize=14,
                  fontweight="bold", pad=12)
    ax5.set_xlabel("Date", fontsize=11)
    ax5.set_ylabel("Hour of Day", fontsize=11)
    ax5.tick_params(axis="x", rotation=30, labelsize=10)
    ax5.tick_params(axis="y", labelsize=9)

    # ── save & show ───────────────────────────────────────────
    plt.savefig(
        "weather_dashboard.png",
        dpi=150,
        bbox_inches="tight",
        facecolor=fig.get_facecolor(),
    )
    plt.show()
    print("\nDashboard saved as weather_dashboard.png")


# -----------------------------
# MAIN
# -----------------------------
def main():

    print("\nWeather Dashboard\n")

    lat, lon, city = get_city()

    if lat is None:
        return

    data = fetch_weather(lat, lon)

    if data is None:
        return

    df = process_data(data)

    create_dashboard(df, city)


if __name__ == "__main__":
    main()