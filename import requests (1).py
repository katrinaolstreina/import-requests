import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from playwright.sync_api import sync_playwright

def get_data_with_playwright(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Headless browser mode
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(5000)  # Wait for JavaScript content to load
        html = page.content()
        browser.close()
        return pd.read_html(html)[0]

# Link
start_date = '2024-09-23'
end_date = '2024-09-29'
imbalance_url = f'https://baltic.transparency-dashboard.eu/node/44?start_date={start_date}T00:00&end_date={end_date}T00:00&output_time_zone=EET&mode=table'
print("url is:",imbalance_url)
activations_url= f"https://baltic.transparency-dashboard.eu/node/35?start_date={start_date}T00:00&end_date={end_date}T00:00&output_time_zone=EET&mode=table"

# imbalance_url='https://baltic.transparency-dashboard.eu/node/44?start_date=2024-09-23T00:00&end_date=2024-09-29T00:00&output_time_zone=EET&mode=table'

# imbalance_url = 'https://baltic.transparency-dashboard.eu/node/44?mode=table'
# activations_url = 'https://baltic.transparency-dashboard.eu/node/35?mode=table'


imbalance_data = get_data_with_playwright(imbalance_url)
activations_data = get_data_with_playwright(activations_url)

print(imbalance_data.head())
print(activations_data.head())

# print(activations_data.columns)
# print(activations_data['Timestamp'])


# Convert the 'From' and 'To' columns to datetime for easier plotting and filtering
imbalance_data['MWh'] = pd.to_datetime(imbalance_data['MWh'])
activations_data[('MWh', 'Timestamp')] = pd.to_datetime(activations_data[('MWh', 'Timestamp')])

# Filter data between the required time period (2024-09-23 to 2024-09-29)
start = datetime(2024, 9, 23)
end = datetime(2024, 9, 29)
imbalance_filtered = imbalance_data[(imbalance_data['MWh'] >= start) & (imbalance_data['MWh'] <= end)]
activations_filtered = activations_data[(activations_data[('MWh', 'Timestamp')] >= start) & (activations_data[('MWh', 'Timestamp')] <= end)]


print(imbalance_filtered)


# Plotting the imbalance and activations for the Baltics
plt.figure(figsize=(10,6))

# Plot imbalance
plt.plot(imbalance_filtered['MWh'], imbalance_filtered['Baltics'], label='Imbalance', color='blue')

# Plot activations (upward and downward)
plt.plot(activations_filtered[('MWh', 'Timestamp')], activations_filtered[('Baltics', 'Upward')], label='Upward Activation', color='green')
plt.plot(activations_filtered[('MWh', 'Timestamp')], activations_filtered[('Baltics', 'Downward')], label='Downward Activation', color='red')

# Labels and title
plt.xlabel('Time')
plt.ylabel('MWh')
plt.title('Imbalance and Activation Actions in the Baltics (2024-09-23 to 2024-09-29)')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)

# Show the plot
plt.tight_layout()
plt.show()



# # # Assessment of regulation activities
# # # The imbalance should decrease after the activation actions. We can check this by observing if
# # # imbalance values tend to decrease after upward/downward activations.
# # # imbalance_change = imbalance_filtered['Baltics'].diff()
# # # activations_upward = activations_filtered['Baltics Upward']
# # # activations_downward = activations_filtered['Baltics Downward']

# # # assessment = "Assessment: In cases where upward or downward activations were applied, we"
