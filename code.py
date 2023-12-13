# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Define functions for reading and transposing data
def read_data_excel(excel_url, sheet_name, new_cols, countries):
    """
    Reads data from an Excel file and performs necessary preprocessing.

    Parameters:
    - excel_url (str): URL of the Excel file.
    - sheet_name (str): Name of the sheet containing data.
    - new_cols (list): List of columns to select from the data.
    - countries (list): List of countries to include in the analysis.

    Returns:
    - data_read (DataFrame): Preprocessed data.
    - data_transpose (DataFrame): Transposed data.
    """
    data_read = pd.read_excel(excel_url, sheet_name=sheet_name, skiprows=3)
    data_read = data_read[new_cols]
    data_read.set_index('Country Name', inplace=True)
    data_read = data_read.loc[countries]

    return data_read, data_read.T


# API base url
api_base_url = "https://api.worldbank.org/v2/en/indicator"

# The Excel URL below indicates GDP growth (annual %)
excel_url_GDP = f'{api_base_url}/NY.GDP.MKTP.KD.ZG?downloadformat=excel'
# The Excel URL below indicates arable land (% of land area)
excel_url_arable_land = f'{api_base_url}/AG.LND.ARBL.ZS?downloadformat=excel'
# The Excel URL below indicates forest area (% of land area)
excel_url_forest_area = f'{api_base_url}/AG.LND.FRST.ZS?downloadformat=excel'
# The Excel URL below indicates Urban population growth (annual %)
excel_url_urban = f'{api_base_url}/SP.URB.GROW?downloadformat=excel'
# The Excel URL below indicates electricity production from oil, gas,
# and coal sources (% of total)
excel_url_electricity = f'{api_base_url}/EG.ELC.FOSL.ZS?downloadformat=excel'
# The Excel URL below indicates Agriculture, forestry, and fishing,
# value added (% of GDP)
excel_url_agriculture = f'{api_base_url}/NV.AGR.TOTL.ZS?downloadformat=excel'
# The Excel URL below indicates CO2 emissions (metric tons per capita)
excel_url_CO2 = f'{api_base_url}/EN.ATM.CO2E.PC?downloadformat=excel'

# Parameters for reading and transposing data
sheet_name = 'Data'
new_cols = ['Country Name', '2014', '2015', '2016', '2017', '2018',
            '2019', '2020', '2021', '2022']
countries = ['United States', 'China', 'Japan', 'Germany', 'India']

# Read and transpose arable land data
data_arable_land, data_arable_land_transpose = read_data_excel(
    excel_url_arable_land, sheet_name, new_cols, countries)
# Read and transpose forest area data
data_forest_area, data_forest_area_transpose = read_data_excel(
    excel_url_forest_area, sheet_name, new_cols, countries)
# Read and transpose GDP data
data_GDP, data_GDP_transpose = read_data_excel(
    excel_url_GDP, sheet_name, new_cols, countries)
# Read and transpose Urban population growth data
data_urban_read, data_urban_transpose = read_data_excel(
    excel_url_urban, sheet_name, new_cols, countries)
# Read and transpose electricity production data
data_electricity_read, data_electricity_transpose = read_data_excel(
    excel_url_electricity, sheet_name, new_cols, countries)
# Read and transpose agriculture data
data_agriculture_read, data_agriculture_transpose = read_data_excel(
    excel_url_agriculture, sheet_name, new_cols, countries)
# Read and transpose CO2 emissions data
data_CO2, data_CO2_transpose = read_data_excel(
    excel_url_CO2, sheet_name, new_cols, countries)

# Print the transposed data
print(data_GDP_transpose)

# Describe the statistics of GDP growth (annual %)
GDP_statistics = data_GDP_transpose.describe()
print(GDP_statistics)


def multiple_plot(x_data, y_data, xlabel, ylabel, title, labels, colors):
    """
    Plots multiple line plots.

    Parameters:
    - x_data (array-like): X-axis data.
    - y_data (list of array-like): Y-axis data for multiple lines.
    - xlabel (str): X-axis label.
    - ylabel (str): Y-axis label.
    - title (str): Plot title.
    - labels (list): List of labels for each line.
    - colors (list): List of colors for each line.
    """
    plt.figure(figsize=(8, 6))
    plt.title(title, fontsize=10)

    for i in range(len(y_data)):
        plt.plot(x_data, y_data[i], label=labels[i], color=colors[i])

    plt.xlabel(xlabel, fontsize=10)
    plt.ylabel(ylabel, fontsize=10)
    plt.legend(bbox_to_anchor=(1.02, 1))
    plt.tight_layout()
    plt.show()


# Display data
print(data_agriculture_read)
print(data_agriculture_transpose)


# The function below constructs a bar plot
def bar_plot(labels_array, width, y_data, y_label, label, title):
    # x is the range of values using the length of the label_array
    x = np.arange(len(labels_array))
    fig, ax = plt.subplots(figsize=(8, 6), dpi=200)

    plt.bar(x - width, y_data[0], width, label=label[0])
    plt.bar(x, y_data[1], width, label=label[1])
    plt.bar(x + width, y_data[2], width, label=label[2])
    plt.bar(x + width * 2, y_data[3], width, label=label[3])

    plt.title(title, fontsize=10)
    plt.ylabel(y_label, fontsize=10)
    plt.xlabel(None)
    plt.xticks(x, labels_array)

    plt.legend()
    ax.tick_params(bottom=False, left=True)
    plt.tight_layout()
    plt.show()
    return


# Each of the preprocessed and transposed dataframes are printed below
print(data_urban_read)
print(data_urban_transpose)


# Define a function to create a correlation heatmap
def correlation_heatmap(data, corr, title):
    """
    Displays a correlation heatmap for the given data.

    Parameters:
    - data (DataFrame): Input data.
    - corr (DataFrame): Correlation matrix.
    - title (str): Title for the heatmap.
    """
    plt.figure(figsize=(8, 6), dpi=200)
    plt.imshow(corr, cmap='magma', interpolation='none')
    plt.colorbar()

    # Show all ticks and label them with the dataframe column name
    plt.xticks(range(len(data.columns)),
               data.columns, rotation=90, fontsize=15)
    plt.yticks(range(len(data.columns)), data.columns, rotation=0, fontsize=15)

    plt.title(title, fontsize=20, fontweight='bold')

    # Loop over data dimensions and create text annotations
    labels = corr.values
    for i in range(labels.shape[0]):
        for j in range(labels.shape[1]):
            plt.text(j, i, '{:.2f}'.format(labels[i, j]),
                     ha="center", va="center", color="white")

    plt.show()


# Plot a multiple line plot for GDP growth (annual %)
x_data = data_GDP_transpose.index
y_data = [data_GDP_transpose['United States'],
          data_GDP_transpose['China'],
          data_GDP_transpose['Japan'],
          data_GDP_transpose['Germany'],
          data_GDP_transpose['India']]
xlabel = 'Years'
ylabel = '(%) GDP Growth'
labels = ['USA', 'China', 'Japan', 'Germany', 'India']
colors = ['purple', 'blue', 'green', 'yellow', 'red']
title = 'Annual (%) GDP Growth Countries'

# Plot the line plots for GDP of Countries
multiple_plot(x_data, y_data, xlabel, ylabel, title, labels, colors)

# The parameters for producing grouped bar plots of Agriculture,
# forestry, and fishing, value added (% of GDP)
labels_array = ['USA', 'China', 'Japan', 'Germany', 'India']
width = 0.2
y_data = [
    data_agriculture_read['2019'],
    data_agriculture_read['2020'],
    data_agriculture_read['2021'],
    data_agriculture_read['2022']
]
y_label = '% of GDP'
label = ['Year 2019', 'Year 2020', 'Year 2021', 'Year 2022']
title = 'Agriculture, forestry, and fishing, value added (% of GDP)'

# The parameters are passed into the defined function and
# produce the desired plot
bar_plot(labels_array, width, y_data, y_label, label, title)

# Parameters for producing scatter plots of Urban population growth (annual %)
labels_array = ['USA', 'China', 'Japan', 'Germany', 'India']
# Don't convert labels to integers, since they represent countries
x_data = labels_array
y_data = [
    data_urban_read['2014'],
    data_urban_read['2015'],
    data_urban_read['2016'],
    data_urban_read['2017'],
    data_urban_read['2018'],
    data_urban_read['2019'],
    data_urban_read['2020'],
    data_urban_read['2021'],
    data_urban_read['2022']
]
y_label = 'Urban growth'
label = ['Year 2014', 'Year 2015', 'Year 2016', 'Year 2017',
         'Year 2018', 'Year 2019', 'Year 2020', 'Year 2021',
         'Year 2022']
title = 'Urban population growth (annual %)'
colors = ['red', 'magenta', 'blue', 'yellow',
          'green', 'purple', 'cyan', 'orange', 'brown']


# Create a dataframe for Japan using selected indicators
data_Japan = {
    'Urban pop. growth': data_urban_transpose['Japan'],
    'Electricity production': data_electricity_transpose['Japan'],
    'Agric. forestry and Fisheries': data_agriculture_transpose['Japan'],
    'CO2 Emissions': data_CO2_transpose['Japan'],
    'Forest Area': data_forest_area_transpose['Japan'],
    'GDP Annual Growth': data_GDP_transpose['Japan']
}
df_Japan = pd.DataFrame(data_Japan)

# Display the dataframe and correlation matrix
print(df_Japan)
corr_Japan = df_Japan.corr()
print(corr_Japan)

# Display the correlation heatmap for Japan
correlation_heatmap(df_Japan, corr_Japan, 'Japan')

# Create a dataframe for China using selected indicators
data_China = {
    'Urban pop. growth': data_urban_transpose['China'],
    'Electricity production': data_electricity_transpose['China'],
    'Agric. forestry and Fisheries': data_agriculture_transpose['China'],
    'CO2 Emissions': data_CO2_transpose['China'],
    'Forest Area': data_forest_area_transpose['China'],
    'GDP Annual Growth': data_GDP_transpose['China']
}
df_Chaina = pd.DataFrame(data_China)

# Display the dataframe and correlation matrix
print(df_Chaina)
corr_Chaina = df_Chaina.corr()
print(corr_Chaina)

# Display the correlation heatmap for China
correlation_heatmap(df_Chaina, corr_Chaina, 'China')

# Plot a multiple line plot for Electricity Production (annual %)
# for selected countries
x_data_electricity = data_electricity_transpose.index
y_data_electricity = [data_electricity_transpose[country]
                      for country in countries]
xlabel_electricity = 'Years'
ylabel_electricity = '(%) Electricity Production'
labels_electricity = countries
colors_electricity = ['orange', 'pink', 'cyan', 'purple', 'green',
                      'red', 'blue', 'yellow', 'brown', 'gray', 'teal',
                      'magenta', 'purple', 'orange', 'blue']
title = 'Annual (%) of Electricity Production of different Countries'

# Plot the line plots for Electricity Production of selected countries
multiple_plot(x_data_electricity, y_data_electricity, xlabel_electricity,
              ylabel_electricity, title,
              labels_electricity, colors_electricity)

# Plot a multiple line plot for Urban land (annual %) for selected countries
x_data_urban_land = data_arable_land_transpose.index
y_data_urban_land = [data_arable_land_transpose[country]
                     for country in countries]
xlabel_urban_land = 'Years'
ylabel_urban_land = '(%) Urban land'
labels_urban_land = countries
colors_urban_land = ['orange', 'pink', 'cyan', 'purple', 'green', 'red',
                     'blue', 'yellow', 'brown', 'gray', 'teal',
                     'magenta', 'purple', 'orange', 'blue']
title_urban_land = 'Annual (%) of Urban land of different Countries'

# Plot the line plots for Urban land of selected countries
multiple_plot(x_data_urban_land, y_data_urban_land, xlabel_urban_land,
              ylabel_urban_land, title_urban_land,
              labels_electricity, colors_urban_land)

# The parameters for producing Greenhouse Gas Emissions by Countries
labels_array = ['USA', 'China', 'Japan', 'Germany', 'India']
width = 0.2
y_data = [
    data_CO2['2019'],
    data_CO2['2020'],
    data_CO2['2021'],
    data_CO2['2022']
]
y_label = 'CO2 Emissions (metric tons per capita'
label = ['Year 2019', 'Year 2020', 'Year 2021', 'Year 2022']
title = 'Greenhouse Gas Emissions by Countries)'

# The parameters are passed into the defined function and
# produce the desired plot
bar_plot(labels_array, width, y_data, y_label, label, title)
