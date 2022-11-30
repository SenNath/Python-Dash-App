# Python-Dash-App

Use the following instructions to run the dash application.

1. Create a virtual environment in the root folder

Commands:
 
virtualenv venv
source venv/bin/activate


2. Install Python dependencies

Command:
pip install -r requirements.txt


3. Run the application

Command:
python index.py

4. Use the below link to access the dash web application

Link:
http://localhost:8000/


## About The Assignment

Genomic Data Analysis and Visualization Web Application

1. Data:

There are 4 datasets (chronos.csv, cn.csv, expression.csv and metadata.csv).

● chronos.csv - contains the chronos data<br /> 
● cn.csv - contains the copy number data<br /> 
● expression.csv - contains the expression data<br /> 
● metadata.csv - contains description about the data available in the rest 3 files

Apart from metadata.csv, all 3 datasets contain 100 gene names as identifiers in the columns and 908 sample IDs as identifiers in the rows.

2. Tasks:

Data Overview -

a. Allow user to select the dataset.<br /> 
b. Upon selection, display the dataset as an interactive table (preferably with options to search/sort/download data).<br /> 
c. Display all summary statistics for the selected dataset - like number of rows, number of columns.<br /> 

Data Visualization -

a. Scatter plot

i. The webapp should allow the user to select genes from datasets and plot 2D scatter plots between 2 variables(expression/copy_number/chronos) for any pair of genes.<br /> 
ii. The user should be able to filter and color data points using metadata information available in the file “metadata.csv”.<br /> 
iii. The visualization could be interactive

b. Boxplot/violin plot

i. User should be able to select a gene and a variable
(expression/chronos/copy_number) and generate a boxplot to display its distribution across multiple categories as defined by user selected variable (a column from the metadata file).

