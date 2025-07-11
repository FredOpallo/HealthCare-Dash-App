# HealthCare Dashboard

A modern interactive dashboard for visualizing healthcare data using [Dash](https://dash.plotly.com/) and [Plotly].  
This dashboard provides insights into patient demographics, medical conditions, insurance provider comparisons, billing distributions, and admission trends.

## Features

- **Patient Demographics:** View age distribution by gender.
- **Medical Condition Distribution:** Visualize the proportion of medical conditions.
- **Insurance Provider Comparison:** Compare billing amounts across insurance providers.
- **Billing Amount Distribution:** Explore billing amounts with interactive filtering.
- **Admission Trends:** Analyze admission trends over time by condition and chart type.

## Technologies Used

- Python 3
- Dash & Dash Bootstrap Components
- Plotly
- Pandas

## Setup Instructions

1. **Clone the repository or copy the files to your machine.**

2. **Install dependencies:**
   ```bash
   pip install dash dash-bootstrap-components plotly pandas
   ```

3. **Add your healthcare data:**
   - Place your CSV file at `Assets/healthcare.csv`.
   - Ensure columns include: `Gender`, `Age`, `Medical Condition`, `Insurance Provider`, `Billing Amount`, `Date of Admission`.

4. **(Optional) Customize styling:**
   - Edit `assets/custom.css` for custom styles.

5. **Run the dashboard:**
   ```bash
   python health.py
   ```
   - The app will be available at [http://127.0.0.1:8050](http://127.0.0.1:8050).

## File Structure

```
healthCare/
│
├── health.py
├── Assets/
│   └── healthcare.csv
├── assets/
│   └── custom.css
└── README.md
```

## Screenshots

![Dashboard Screenshot](assets/dashboard_screenshot.png) <!-- Add screenshot if available -->

## License

This project is for educational and demonstration purposes.

## Author

Created by Elvis Fred Opallo but it was a guided project from Youtube Channel "Code with Josh".