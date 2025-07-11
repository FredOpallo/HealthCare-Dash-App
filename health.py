import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# Loading the data
def load_data():
    data = pd.read_csv('Assets/healthcare.csv')
    data['Billing Amount'] = pd.to_numeric(data['Billing Amount'], errors='coerce')
    data['Date of Admission'] = pd.to_datetime(data['Date of Admission'])
    data['YearMonth'] = data['Date of Admission'].dt.to_period('M')
    return data

data = load_data()
num_records = len(data)
avg_billing = round(data['Billing Amount'].mean(), 2)

# Creating web app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# App layout and Design
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1('HealthCare Dashboard', className="text-center my-5 display-4", style={'color': '#007bff'}), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.Div(f"Total Patient Records: {num_records}", className="text-center my-3 top-text bg-light p-3 rounded shadow-sm"), width=6),
        dbc.Col(html.Div(f"Average Billing Amount: {avg_billing}", className="text-center my-3 top-text bg-light p-3 rounded shadow-sm"), width=6)
    ], className="mb-5"),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Patient Demographics", className="card-title mb-3"),
                    dcc.Dropdown(
                        id="gender-filter",
                        options=[{"label": gender, "value": gender} for gender in data['Gender'].unique()],
                        value=None,
                        placeholder="Select Gender",
                        className="mb-3"
                    ),
                    dcc.Graph(id="age-distribution", className="dash-graph")
                ])
            ], className="shadow-sm")
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Medical Condition Distribution", className="card-title mb-3"),
                    dcc.Graph(id="condition-distribution", className="dash-graph")
                ])
            ], className="shadow-sm")
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Insurance Provider Comparison", className="card-title mb-3"),
                    dcc.Graph(id="insurance-comparison", className="dash-graph")
                ])
            ], className="shadow-sm")
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Billing Amount Distribution", className="card-title mb-3"),
                    dcc.Slider(
                        id="billing-slider",
                        min=data['Billing Amount'].min(),
                        max=data['Billing Amount'].max(),
                        value=data['Billing Amount'].median(),
                        marks={int(value): f"${int(value):,}" for value in data['Billing Amount'].quantile([0, 0.25, 0.5, 0.75, 1]).values},
                        step=100,
                        tooltip={"placement": "bottom", "always_visible": True},
                        className="mb-3"
                    ),
                    dcc.Graph(id="billing-distribution", className="dash-graph")
                ])
            ], className="shadow-sm")
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Trends in Admission", className="card-title mb-3"),
                    dcc.RadioItems(
                        id="chart-type",
                        options=[{"label": "Line Chart", 'value': 'line'}, {"label": "Bar Chart", 'value': 'bar'}],
                        value='line',
                        inline=True,
                        className='mb-4'
                    ),
                    dcc.Dropdown(
                        id="condition-filter",
                        options=[{'label': condition, 'value': condition} for condition in data['Medical Condition'].unique()],
                        value=None,
                        placeholder="Select a Condition",
                        className="mb-3"
                    ),
                    dcc.Graph(id="admission-trends", className="dash-graph")
                ])
            ], className="shadow-sm")
        ], width=12)
    ])
], fluid=True)

# Callbacks

@app.callback(
    Output('age-distribution', 'figure'),
    Input('gender-filter', 'value')
)
def update_distribution(selected_gender):
    filtered_df = data[data['Gender'] == selected_gender] if selected_gender else data
    if filtered_df.empty:
        return {}
    fig = px.histogram(
        filtered_df,
        x='Age',
        nbins=10,
        title='Age Distribution By Gender',
        color_discrete_sequence=['blue', 'red']
    )
    return fig

@app.callback(
    Output('condition-distribution', 'figure'),
    Input('gender-filter', 'value')
)
def update_medical_condition(selected_gender):
    filtered_df = data[data["Gender"] == selected_gender] if selected_gender else data
    fig = px.pie(filtered_df, names="Medical Condition", title="Medical Condition Distribution")
    return fig

@app.callback(
    Output('insurance-comparison', 'figure'),
    Input('gender-filter', 'value')
)
def update_insurance(selected_gender):
    filtered_df = data[data['Gender'] == selected_gender] if selected_gender else data
    fig = px.bar(
        filtered_df,
        x="Insurance Provider", y="Billing Amount", color="Medical Condition",
        barmode="group",
        title="Insurance Provider Price Comparison",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    return fig

@app.callback(
    Output("billing-distribution", "figure"),
    [Input("gender-filter", "value"),
     Input("billing-slider", "value")]
)
def update_billing(selected_gender, slider_value):
    filtered_df = data[data['Gender'] == selected_gender] if selected_gender else data
    # Show billing amounts within +/- $100 of slider value
    filtered_df = filtered_df[
        (filtered_df['Billing Amount'] >= slider_value - 100) &
        (filtered_df['Billing Amount'] <= slider_value + 100)
    ]
    fig = px.histogram(filtered_df, x="Billing Amount", nbins=10, title="Billing Amount Distribution")
    return fig

@app.callback(
    Output("admission-trends", "figure"),
    [Input("chart-type", "value"),
     Input("condition-filter", "value")]
)
def update_admission(chart_type, selected_condition):
    filtered_df = data[data['Medical Condition'] == selected_condition] if selected_condition else data
    trend_df = filtered_df.groupby("YearMonth").size().reset_index(name="Count")
    trend_df["YearMonth"] = trend_df["YearMonth"].astype(str)
    if chart_type == "line":
        fig = px.line(trend_df, x="YearMonth", y="Count", title="Admission Trends over Time")
    else:
        fig = px.bar(trend_df, x="YearMonth", y="Count", title="Admission Trends Over Time")
    return fig

if __name__ == "__main__":
    app.run(debug=True)
