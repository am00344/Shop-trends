import pandas as pd
import numpy as np
import seaborn as sns
from datetime import datetime, timedelta


sns.set_theme(style="whitegrid")
np.random.seed(42)


print("Ingesting raw transactional data...")


menu_items = {
    'Iced Oat Latte': ('Drink', 5.50, 1.20),
    'Americano': ('Drink', 3.75, 0.40),
    'Chai Latte': ('Drink', 4.75, 0.90),
    'Blueberry Biscuit': ('Food', 4.25, 1.10),
    'Breakfast Sandwich': ('Food', 6.50, 2.30),
    'Avocado Toast': ('Food', 7.00, 2.50)
}


base_date = datetime(2026, 9, 21, 7, 0, 0) # Midterms week starts
raw_records = []

for i in range(1, 301):
    # Randomly assign a time slot based on campus rush patterns
    day_offset = np.random.randint(0, 7)
    # Peak hours: 8-10 AM (Morning rush) and 2-4 PM (Midterm study sessions)
    hour_pool = [8, 9, 14, 15] if np.random.rand() < 0.65 else [7, 10, 11, 12, 13, 16, 17]
    hour = np.random.choice(hour_pool)
    minute = np.random.randint(0, 60)
    
    timestamp = base_date + timedelta(days=day_offset, hours=hour, minutes=minute)
    

    item = np.random.choice(list(menu_items.keys()))
    if np.random.rand() < 0.15:
        item = item.upper() if np.random.rand() < 0.5 else item.lower()
        
    quantity = np.random.choice([1, 2, 3], p=[0.75, 0.20, 0.05])
    raw_records.append({"Transaction_ID": i, "Timestamp": timestamp, "Item_Ordered": item, "Quantity": quantity})

df_raw = pd.DataFrame(raw_records)


print("Cleaning data and standardizing schema...")


df_raw['Item_Ordered'] = df_raw['Item_Ordered'].str.title()


menu_df = pd.DataFrame.from_dict(menu_items, orient='index', columns=['Category', 'Price', 'COGS']).reset_index()
menu_df = menu_df.rename(columns={'index': 'Item_Ordered'})

df = pd.merge(df_raw, menu_df, on='Item_Ordered', how='left')


df['Gross_Revenue'] = df['Price'] * df['Quantity']
df['Total_Cost'] = df['COGS'] * df['Quantity']
df['Net_Profit'] = df['Gross_Revenue'] - df['Total_Cost']

# Extract precise operational dimensions
df['Hour_of_Day'] = df['Timestamp'].dt.hour
df['Day_Name'] = df['Timestamp'].dt.day_name()


print("\n📊 --- BUSINESS METRICS SUMMARY ---")
total_rev = df['Gross_Revenue'].sum()
total_profit = df['Net_Profit'].sum()
avg_ticket = df.groupby('Transaction_ID')['Gross_Revenue'].sum().mean()

print(f"Total Gross Revenue: ${total_rev:,.2f}")
print(f"Total Net Profit:    ${total_profit:,.2f}")
print(f"Average Ticket Size: ${avg_ticket:,.2f}")


item_perf = df.groupby('Item_Ordered').agg(
    Units_Sold=('Quantity', 'sum'),
    Total_Revenue=('Gross_Revenue', 'sum'),
    Total_Profit=('Net_Profit', 'sum')
).sort_values(by='Total_Profit', ascending=False)

print("\n Item Performance Breakdown:")
print(item_perf)



