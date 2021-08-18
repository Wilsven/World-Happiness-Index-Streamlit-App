import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns

# Read data
df = pd.read_csv('world-happiness-report-2021.csv')

# Display title
st.title('World Happiness Index 2021:')
# Also display title in the sidebar
st.sidebar.title('World Happiness Index 2021')

# Place a fancy image lol
url = 'https://images.pexels.com/photos/573259/pexels-photo-573259.jpeg?cs=srgb&dl=pexels-matheus-bertelli-573259.jpg' \
      '&fm=jpg '
st.image(url, caption='World Happiness Dataset')

# Add country select filter
country_list = ['All', 'Western Europe', 'South Asia', 'Southeast Asia', 'East Asia',
                'North America and ANZ', 'Middle East and North Africa',
                'Latin America and Caribbean', 'Central and Eastern Europe',
                'Commonwealth of Independent States', 'Sub-Saharan Africa']

select = st.sidebar.selectbox('Filter the region here:',
                              country_list,
                              key='1')
# Add ladder score slider
score = st.sidebar.slider('Adjust ladder score slider:',
                          min_value=0,
                          max_value=10,
                          value=(0, 10))

# Create first mask to filter for selected regions
mask1 = df['Regional indicator'] == select

if select == 'All':
    df_filtered = df
else:
    df_filtered = df[mask1]

# Create mask 2 to filter for scores equal to or higher
mask2 = df['Ladder score'].between(*score)
df_filtered = df_filtered[mask2]

# Display dataframe
st.write(df_filtered)

# Display number of observations, updates dynamically
number_of_results = df_filtered.shape[0]
st.markdown(f'*Available Results: {number_of_results}*')

# Scatter chart
fig = px.scatter(df_filtered,
                 x='Logged GDP per capita',
                 y='Healthy life expectancy',
                 size='Ladder score',
                 color='Regional indicator',
                 hover_name='Country name',
                 size_max=10)

st.subheader('Healthy Life Expectancy vs Logged GDP per Capita:')
st.write(fig)

# Bar chart
st.subheader('Bar chart of Country\'s Ladder Score:')
st.write(px.bar(df_filtered, y='Ladder score', x='Country name'))

# Seaborn correlation heatmap
df_corr = df_filtered.corr()

# Define fig size
plt.figure(figsize=(8, 8))

# Create corr heatmap
fig1 = plt.figure()
ax = sns.heatmap(df_corr,
                 vmin=-1,
                 vmax=1,
                 center=0,
                 cmap=sns.diverging_palette(20, 220, n=200),
                 square=True)

ax.set_xticklabels(ax.get_xticklabels(),
                   rotation=45,
                   horizontalalignment='right')

st.subheader('Correlation Heatmap of Features:')
st.pyplot(fig1)
