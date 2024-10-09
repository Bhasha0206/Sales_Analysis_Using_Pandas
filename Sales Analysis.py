import pandas as pd
import os
import matplotlib.pyplot as plt

#Merging 12 months data into one dataset
df = pd.read_csv(r'C:\Users\moham\Downloads\Sales Analysis\Sales_Data\Sales_April_2019.csv')
files = [file for file in os.listdir(r'C:\Users\moham\Downloads\Sales Analysis\Sales_Data')]
complete_data = pd.DataFrame()
for file in files:
    df = pd.read_csv(r'C:\Users\moham\Downloads\Sales Analysis\Sales_Data\\'+file)
    complete_data = pd.concat([complete_data, df])
complete_data.to_csv("C:\\Users\\moham\\Downloads\\Sales Analysis\\Sales_Data\\complete_data.csv", index = False)

#Reading the updated data
cd = pd.read_csv(r'C:\Users\moham\Downloads\Sales Analysis\Sales_Data\complete_data.csv')
cd.head()

#Problem 1: What was the best month for sales? How much was earned that month?

#Adding month column to the data
cd['Month'] = cd['Order Date'].str[0:2]
cd.head()

#Cleaning data

#Dropping Nan Rows
nan_df = cd[cd.isna().any(axis=1)]
nan_df.head()
cd = cd.dropna(how='all')
cd.head()

#Finding Or and deleting it
cd = cd[cd['Order Date'].str[0:2]!='Or']

#Converting Month column into integer
cd['Month'] = cd['Month'].astype('int32')

#Adding a Sales column
cd['Quantity Ordered'] = pd.to_numeric(cd['Quantity Ordered'])
cd['Price Each'] = pd.to_numeric(cd['Price Each'])
cd['Sales'] = cd['Quantity Ordered'] * cd['Price Each']
cd.head()

#Finding the best month for sales
result = cd.groupby('Month').sum()

#Visualising using matplotlib
months = range(1,13)
plt.bar(months, result['Sales'])
plt.xticks(months)
plt.ylabel = ('Sales in USD')
plt.xlabel = ('Month')
plt.show()


#Problem 2: What city sold the most product?

#Adding a City column
def get_city(address):
    return address.split(',')[1]
def get_state(address):
    return address.split(',')[2].split(' ')[1]
cd['City'] = cd['Purchase Address'].apply(lambda x: get_city(x) + ' (' + get_state(x) + ')')
cd.head()

#Finding the city sold the most products
results = cd.groupby('City').sum()
results

#Visualising using matplotlib
cities = [city for city, df in cd.groupby('City')]
plt.bar(cities, results['Sales'])
plt.xticks(cities, rotation = 'vertical', size = '8')
plt.ylabel = ('Sales in USD')
plt.xlabel = ('City Name')
plt.show()


#Problem 3: What time should we display advertisements to maximize the likelihood of customer’s buying product?

#Converting Order Date column into datetime format
cd['Order Date'] = pd.to_datetime(cd['Order Date'], format='%m/%d/%y %H:%M')
cd['Order Date']

#Adding Hour and Minute Columns
cd['Hour'] = cd['Order Date'].dt.hour
cd['Minute'] = cd['Order Date'].dt.minute
cd.head()

#Visualising using matplotlib
hours = [hour for hour, df in cd.groupby('Hour')]
plt.plot(hours, cd.groupby(['Hour']).count())
plt.xticks(hours)
plt.ylabel = ('No.of orders')
plt.xlabel = ('Hour')
plt.grid()
plt.show()


#Problem 4: What products are most often sold together?

# Find duplicated 'Order ID' and show the first 20 rows
df = cd[cd['Order ID'].duplicated(keep=False)]
df.head(20)

# Join values from two rows into a single row for duplicated 'Order ID'
df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))

# Drop rows with duplicate values
df = df[['Order ID', 'Grouped']].drop_duplicates()

#Counting oairs of products
from itertools import combinations
from collections import Counter

count = Counter()
for row in df['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))

for key, value in count.most_common(10):
    print(key, value)
    

#Problem 5: What product sold the most? Why do you think it sold the most?

pg = cd.groupby('Product')
qo = pg['Quantity Ordered'].sum()

products = [product for product, df in pg]
plt.ylabel = ('# Ordered')
plt.bar(products, qo)
plt.xticks(products, rotation = "vertical", size = '8')

# Convert 'Price Each' to numeric
cd['Price Each'] = pd.to_numeric(cd['Price Each'], errors='coerce')

# Group by 'Product' and calculate the mean of 'Price Each'
prices = cd.groupby('Product')['Price Each'].mean()

# Assuming 'products' and 'qo' are already defined
fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(products, qo, color='g')
ax2.plot(products, prices, color='b')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered', color='g')
ax2.set_ylabel('Price ($)', color='b')
ax1.set_xticklabels(products, rotation='vertical', size=8)

plt.show()
