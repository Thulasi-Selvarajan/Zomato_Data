# Import Streamlit library
import streamlit as st
# Import Pandas for data manipulation
import pandas as pd
# Import Plotly Express for interactive plots
import plotly.express as px
# Import Seaborn for statistical data visualization
import seaborn as sns
# Import Matplotlib for basic plotting
import matplotlib.pyplot as plt
# Import Image module from PIL for image processing
from PIL import Image
# Import Folium for creating interactive maps
import folium

# Load the data
@st.cache_resource  # Cache the data to improve performance
def load_data():
    return pd.read_csv("data_1.csv")

#streamlit page config.
st.set_page_config(page_title='Zomato Data Analysis', layout='wide',
                   initial_sidebar_state='expanded')

st.title(":red[Zomato Data Analysis and Visualization]")
#page setup
with st.sidebar:

    #image insertion
    image_path = (r"image.jpg")   
    image = Image.open(image_path)

    # Display the image using st.image()
    st.sidebar.image(image)

    st.write("## :red[Keep Food On Your Fingertips!]") 
 
    
#tabs 
st.write(":blue[Get Started Here!]")    
tab1,tab2,tab3=st.tabs(['Home','Map View','Data Visulization'])

with tab1:
    st.write("")
    st.write("")
    st.write('### :violet[Problem Statement]')
    st.write("* Zomato is a popular restaurant discovery and food delivery service.") 
    st.write("* Data analysis on the platform's data could be used to gain insights into customer preferences and behavior, as well as identify trends in the restaurant industry")
    st.write('* To perform the analysis various methodologies such as Data Exploration, Data Cleaning, Feature Selection And Deployment can be used')
    st.write("")
    st.write("")
    st.write('### :violet[Tools and Technologies used]')
    st.write('* Python')
    st.write('* Pandas')
    st.write('* Matplotlib')
    st.write('* Seaborn')
    st.write('* Plotly')
    st.write('* Streamlit')

with tab2:
    
    # Load the Folium map HTML file with explicit encoding
    with open("india_restaurants_map.html", "r", encoding="utf-8") as f:
        map_html = f.read() 
    #Display the HTML content using st.components.v1.html
    st.components.v1.html(map_html, width=600, height=400) 

with tab3:
    # Add a column with rupees as the currency
    def add_rupees_column(data):
        # Define conversion rates for currencies to INR
        conversion_rates = {
            'Dollar($)': 74.26,        # 1 USD = 74.26 INR
            'Brazilian Real(R$)': 13.12,    # 1 BRL = 13.12 INR
            'NewZealand($)': 50.85,    # 1 NZD = 50.85 INR
            # Add more conversion rates as needed
        }
        
        # Map currencies to conversion rates
        data['Conversion Rate'] = data['Currency'].map(conversion_rates)
        
        # Apply conversion to INR
        data['Average Cost in INR'] = data['Average Cost for two'] * data['Conversion Rate']
        
        return data

    # Plot comparing Indian currency with other countries' currency
    def currency_comparison_plot(data):
        currency_comparison_chart = px.bar(data, x='Country', y=['Average Cost for two', 'Average Cost in INR'],
                                            color='Currency', barmode='group',
                                            labels={'value': 'Average Cost'})
        currency_comparison_chart.update_layout(title="Average Cost Comparison by Country",
                                                yaxis_title="Average Cost",
                                                xaxis_title="Country")
        st.plotly_chart(currency_comparison_chart)
    
    # Plot top cuisines
    def top_cuisines_plot(data):
        top_cuisines = data['Cuisines'].value_counts().head(10)
        top_cuisines_chart = px.bar(top_cuisines, x=top_cuisines.index, y=top_cuisines.values, labels={'y': 'Count'})
        st.header("Top Cuisines")
        st.plotly_chart(top_cuisines_chart)

    # Plot top 5 countries with most restaurants
    def top_countries_plot(data):
        top_countries = data['Country'].value_counts().head(5)
        fig, ax = plt.subplots(figsize=(2,3))
        explode = [0, 0.3, 0.3, 0.3, 0.3]  # Explode the last slice
        ax.pie(top_countries, labels=top_countries.index, autopct='%0.2f%%', explode=explode,textprops={'fontsize': 4})
        ax.set_title("Pie chart of top 5 countries with most restaurants", fontsize=8)
        st.pyplot(fig)  # Show the plot using Streamlit   

    # Sidebar for selecting country and city
    def choose(data):
        st.header("Select Filters")
        selected_country = st.selectbox("Choose a country", data["Country"].unique())
        selected_city = st.selectbox("Choose cities", data[data["Country"] == selected_country]["City"].unique())
        return selected_country, selected_city

    # Plot cost vs rating
    def cost_rating_plot(data):
        cost_rating_chart = px.scatter(data, x='Average Cost for two', y='Aggregate rating', color='Rating text')
        st.header("Cost vs Rating")
        st.plotly_chart(cost_rating_chart)

     # Plot Aggregate rating distribution
    def rating_distribution_plot(data):
        plt.figure(figsize=(8, 6))  # Adjust the figure size as needed
        sns.countplot(x=data['Aggregate rating'], hue=data['Aggregate rating'], palette='viridis', legend=False)
        # Using the 'viridis' colormap
        plt.title('Countplot of Aggregate rating', fontsize=8)
        plt.xlabel('Aggregate rating', fontsize=8)
        plt.ylabel('Count', fontsize=8)
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        fig, ax = plt.gcf(), plt.gca()
        st.pyplot(fig)

   # Function to plot online delivery vs dine-in
    def online(data):
        # Group by country and count the occurrences of online delivery and dine-in
        online_delivery = data.groupby('Country')['Has Online delivery'].value_counts()

        # Extract the counts for online delivery and dine-in
        delivery_counts = online_delivery[:, 'Yes']
        dine_in_counts = online_delivery[:, 'No']

        # Create a pie chart
        labels = ['Online Delivery', 'Dine-in']
        sizes = [delivery_counts.sum(), dine_in_counts.sum()]
        explode = (0.1, 0)  # explode the 'Online Delivery' slice
        colors = ['#ff9999', '#66b3ff']  # specify colors
        fig, ax = plt.subplots(figsize=(4,2))  # set the figure size
        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%0.2f%%',textprops={'fontsize': 4})
        ax.set_title('Online Delivery vs. Dine-in', fontsize=8)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Show the pie chart
        st.pyplot(fig)

    # Function to display availability of online delivery
    def available(filtered_data):
        # Calculate the availability of online delivery in filtered data
        online_delivery_available = filtered_data["Has Online delivery"].value_counts(normalize=True) * 100

        # Create a pie chart
        labels = online_delivery_available.index
        sizes = online_delivery_available.values
        explode = (0.1, 0) if len(labels) == 2 else None  # Explode only if there are two categories
        colors = ['#ff9999', '#66b3ff']  # Specify colors

        fig, ax = plt.subplots(figsize=(4, 2))  # Set the figure size
        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%0.2f%%', textprops={'fontsize': 4})
        ax.set_title('Availability of Online Delivery', fontsize=8)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Show the pie chart
        st.pyplot(fig)

    # Function to find costly cuisines in India
    def costly_cuisines_in_india(data):
        # Filter data to include only restaurants in India
        india_data = data[data['Country'] == 'India']
        
        # Group by cuisine and calculate average cost
        cuisine_avg_cost = india_data.groupby('Cuisines')['Average Cost for two'].mean()
        
        # Sort by average cost in descending order
        costly_cuisines = cuisine_avg_cost.sort_values(ascending=False).head(5)
        
        return costly_cuisines

    # Function to display city-based information
    def city_information(data, city):
        city_data = data[data['City'] == city]
        
        # Display famous cuisines in the city
        st.write(f"### Famous cuisines in {city}:")
        famous_cuisines = city_data['Cuisines'].value_counts().head(3)
        st.write(famous_cuisines)
        
        # Display costlier cuisines in the city
        st.write(f"### Costlier cuisines in {city}:")
        costlier_cuisines = city_data.groupby('Cuisines')['Average Cost for two'].mean().sort_values(ascending=False).head(3)
        st.write(costlier_cuisines)
        
        # Display rating count in the city
        st.write(f"### Rating count in {city}:")
        rating_count = city_data['Aggregate rating'].value_counts()
        st.write(rating_count)
        
            # Function to filter data for restaurants in India
    def filter_data_for_india(data):
        return data[data['Country'] == 'India']

    # Function to prepare restaurant details for map markers
    def prepare_marker_details(data):
        marker_details = []
        for index, row in data.iterrows():
            marker = {
                'location': [row['Latitude'], row['Longitude']],
                'popup': f"<b>{row['Restaurant Name']}</b><br>"
                        f"Location: {row['Locality']}, {row['City']}<br>"
                        f"Cuisine: {row['Cuisines']}<br>"
                        f"Rating: {row['Aggregate rating']}<br>"
                        f"Average Cost for Two: {row['Average Cost for two']}"
                        f"Online Delivery: {'Yes' if row['Has Online delivery'] == 'Yes' else 'No'}"
            }
            marker_details.append(marker)
        return marker_details
    
                
    # Main function
    def main():
        
        # Load data
        data = load_data()

        # Add rupees column
        data = add_rupees_column(data)

        # Plot comparing Indian currency with other countries' currency
        currency_comparison_plot(data)

        # Display top cuisines plot
        top_cuisines_plot(data)

        # Plot top 5 countries with most restaurants
        top_countries_plot(data)

        online(data)
         
         
        # Find costly cuisines in India
        st.write("## Costly cuisines")
        costly_cuisines = costly_cuisines_in_india(data)
        st.write(costly_cuisines)
        
        # Filter based on the city
        st.write("## Filter based on the city")
        selected_city = st.selectbox("Select a city:", data['City'].unique())
        city_information(data, selected_city)
        
        
      
        #selecting country and city
        selected_country, selected_city= choose(data)

        # Filter data based on selected country and cities
        filtered_data = data[(data["Country"] == selected_country) & (data["City"]==(selected_city))]

        # Display top cuisines plot
        top_cuisines_plot(filtered_data)

        # Plot comparing Indian currency with other countries' currency
        currency_comparison_plot(filtered_data)

        # Display cost vs rating plot
        cost_rating_plot(filtered_data)

        # Display Aggregate rating distribution plot
        rating_distribution_plot(filtered_data)

        available(filtered_data)


       # Create a Folium Map centered on India
        india_map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

        # Add markers for each restaurant with popup labels
        marker_details = prepare_marker_details(data)
        for marker in marker_details:
            folium.Marker(location=marker['location'], popup=marker['popup']).add_to(india_map)

        # Save the map as HTML
        india_map.save('india_restaurants_map.html')
   

        

    if __name__ == "__main__":
     main()
