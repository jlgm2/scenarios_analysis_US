import pandas as pd
import plotly.express as px
import plotly.graph_objects as go  # Correct import for go
import streamlit as st

# Streamlit Sidebar for Data Source Selection
st.sidebar.title("Filters")

# Region Selection Box
region = st.sidebar.selectbox(
    "Select Region:",
    options=['U.S.', 'Europe (Germany)', 'Asia (Japan)']
)

# Map region to appropriate file path
if region == 'U.S.':
    file_path = 'scenarios_results_data_US.csv'
elif region == 'Europe (Germany)':
    file_path = 'scenarios_results_data_EU.csv'
else:  # Asia (Japan)
    file_path = 'scenarios_results_data_Asia.csv'

# Load the dataset based on selected region
data = pd.read_csv(file_path)

# Rename columns for consistency
data = data.rename(columns=lambda x: x.strip())

# Define columns for environmental impact indicators
impact_columns = [
    "Climate change (total), kg CO2 eq", "Acidification, mol H+ eq",
    "Climate change (biogenic), kg CO2 eq", "Climate change (fossil), kg CO2 eq",
    "human toxicity: non-carcinogenic , inorganics, CTUh",
    "ionising radiation: human health , kg Bq U235eq", "land use, (dimensionless)",
    "material resources: metals/minerals, kg Sb-eq", "ozone depletion, kg CFC11-eq",
    "particulate matter formation, disease incidence",
    "photochemical oxidant formation: human health, kg NMVOC-eq",
    "water use , m3 world eq depriv"
]

# Dropdown for Building Savings
building_savings = st.sidebar.selectbox(
    "Select Building Savings:",
    options=['Not considered', 'Considered']
)

# Dropdown for Environmental Impact Indicator
impact_indicator = st.sidebar.selectbox(
    "Select Environmental Impact Indicator:",
    options=impact_columns
)

# Filter dataset based on user selection for building savings
if building_savings == "Not considered":
    building_savings_data = 0
else:
    building_savings_data = 1

filtered_data = data[data['Building savings'] == building_savings_data]

# Generate the Plotly Chart
fig = px.scatter(
    data_frame=filtered_data,
    x=impact_indicator,
    y="Cost, USD2023",
    color="Alkali sorbent",  # Color by Alkali sorbent
    hover_name="Label",
    labels={"x": impact_indicator, "y": "Cost (USD2023)"},
    title=f"{impact_indicator} vs Cost (Building Savings: {building_savings})",
)

# Enhance chart aesthetics
fig.update_traces(
    marker=dict(size=12, opacity=0.8)  # Bigger data points
)

# Add horizontal and vertical lines as separate traces to include in the legend
# Horizontal line at Y = 10000
fig.add_trace(
    go.Scatter(
        x=[min(filtered_data[impact_indicator]), max(filtered_data[impact_indicator])],
        y=[10000, 10000],
        mode='lines',
        line=dict(color="red", width=2, dash="dash"),
        name="100 USD per tonne of CO2",
        showlegend=True  # This will show the line in the legend
    )
)

# Vertical line at X = 0
fig.add_trace(
    go.Scatter(
        x=[0, 0],
        y=[min(filtered_data["Cost, USD2023"]), max(filtered_data["Cost, USD2023"])],
        mode='lines',
        line=dict(color="blue", width=2, dash="dash"),
        name="Carbon Neutrality",
        showlegend=True  # This will show the line in the legend
    )
)

# Update layout with visible gridlines
fig.update_layout(
    plot_bgcolor="white",
    xaxis=dict(
        gridcolor="lightgrey",  # Grey gridlines for X axis
        zerolinecolor="grey",
        title_font=dict(size=14, family="Arial", color="black"),
        showgrid=True,  # Ensure grid lines are visible on x-axis
        gridwidth=1  # Set gridline width
    ),
    yaxis=dict(
        gridcolor="lightgrey",  # Grey gridlines for Y axis
        zerolinecolor="grey",
        title_font=dict(size=14, family="Arial", color="black"),
        showgrid=True,  # Ensure grid lines are visible on y-axis
        gridwidth=1  # Set gridline width
    ),
    legend_title="Alkali Sorbent",
    title_font=dict(size=18, family="Arial"),
    font=dict(size=12, family="Arial"),
    height=800,  # Adjust height for a more reasonable size
    width=800,   # Adjust width to match the height and make it more square
    legend=dict(
        orientation="h",  # Horizontal legend
        yanchor="top",
        y=-0.1,  # Move the legend further down
        xanchor="center",
        x=0.5
    )
)

# Streamlit main page content
st.title(f"Environmental Impact Dashboard - {region}")
st.plotly_chart(fig)
