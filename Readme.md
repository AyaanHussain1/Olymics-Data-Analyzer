# Olympics Data Analyzer

🔗 **Live Demo:** [https://olymics-data-analyzer-sys.streamlit.app/]

An interactive data analytics dashboard exploring over a century of Olympic Games history, covering 271,000+ athlete records from 1896 to 2016.

## Overview

This project turns a large, raw historical dataset into an interactive exploration tool. Rather than a single static analysis, the dashboard lets a user drill down into Olympic history from four different angles — overall medal tallies, global participation trends, country-specific performance, and individual athlete demographics — all through dynamic filters rather than fixed charts.

## How It Works

1. **Data** — Combined two datasets: `athlete_events` (271,116 records covering 134,732 unique athletes across 66 sports) and `noc_regions` (country/region mapping for National Olympic Committees).
2. **Preprocessing** — Filtered to Summer Olympics only, merged region names onto each record via NOC codes, removed duplicate entries, and one-hot encoded medal types (Gold/Silver/Bronze) for aggregation.
3. **Analysis Modules** — Built a dedicated helper library (`helper.py`) with reusable functions for:
   - **Medal Tally** — Filterable by year and/or country, with automatic totals
   - **Overall Analysis** — Trends in participating nations, events, and athletes over time, plus a sport-by-year heatmap of event counts
   - **Country-Wise Analysis** — A selected country's medal trajectory over time, its strongest sports (heatmap), and its top 10 athletes
   - **Athlete-Wise Analysis** — Age distribution of medalists by medal type, and male vs. female participation trends over the decades
4. **Visualization** — Used Plotly for interactive line charts and Matplotlib/Seaborn for heatmaps and distribution plots.
5. **Deployment** — Built as a multi-page Streamlit app with sidebar navigation, letting users switch between analysis modes and apply filters (year, country, sport) without reloading the page.

## Tech Stack

- **Language:** Python
- **Data Handling:** Pandas, NumPy
- **Visualization:** Plotly, Matplotlib, Seaborn
- **App/Deployment:** Streamlit

## Project Structure

```
olympics-data-analyzer/
├── app.py               # Streamlit dashboard (main entry point)
├── preprocesser.py      # Data cleaning and merging logic
├── helper.py            # Reusable analysis functions for each dashboard view
├── athlete_events.xls   # Raw athlete/event records
├── noc_regions.xls      # NOC-to-region mapping
└── requirements.txt     # Python dependencies
```

## Installation & Usage

```bash
# Clone the repository
git clone https://github.com/AyaanHussain1/olympics-data-analyzer.git
cd olympics-data-analyzer

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Results

The dashboard successfully condenses 120 years of Olympic history into four interactive, filterable views, letting users explore trends (e.g. the rise in female participation, or a specific country's historical medal performance) that would be difficult to see in the raw dataset alone.

## License

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

This project is built for educational and portfolio purposes, using a publicly available historical Olympics dataset.
