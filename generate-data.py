import random
import pandas as pd
from datetime import datetime, timedelta

# Set random seed for consistent, reproducible results
random.seed(42)

num_users = 2500
devices = ['Desktop', 'Mobile']
channels = ['Organic Search', 'Paid Ads', 'Social Media']

# 1. Generate User Profiles
users = []
for i in range(1, num_users + 1):
    users.append({
        'user_id': f'U_{i:04d}',
        'device_type': random.choices(devices, weights=[0.35, 0.65])[0], # 65% mobile traffic
        'acquisition_channel': random.choices(channels, weights=[0.5, 0.3, 0.2])[0],
        'signup_date': datetime(2026, 1, 1) + timedelta(days=random.randint(0, 90))
    })

df_users = pd.DataFrame(users)

# 2. Generate Event Logs simulating the Funnel
events = []
event_id_counter = 1

for _, row in df_users.iterrows():
    user_id = row['user_id']
    device = row['device_type']
    signup_time = row['signup_date']
    
    session_id = f'S_{user_id}'
    
    # Stage 1: Page View (100% of users)
    events.append({
        'event_id': event_id_counter,
        'user_id': user_id,
        'session_id': session_id,
        'event_type': 'page_view',
        'timestamp': signup_time
    })
    event_id_counter += 1

    # Stage 2: Add to Cart (65% conversion)
    if random.random() < 0.65:
        events.append({
            'event_id': event_id_counter,
            'user_id': user_id,
            'session_id': session_id,
            'event_type': 'add_to_cart',
            'timestamp': signup_time + timedelta(minutes=random.randint(1, 8))
        })
        event_id_counter += 1

        # Stage 3: Checkout Start (55% conversion)
        if random.random() < 0.55:
            events.append({
                'event_id': event_id_counter,
                'user_id': user_id,
                'session_id': session_id,
                'event_type': 'checkout_start',
                'timestamp': signup_time + timedelta(minutes=random.randint(9, 20))
            })
            event_id_counter += 1

            # Stage 4: Purchase Complete (The Bottleneck!)
            purchase_prob = 0.40 if device == 'Mobile' else 0.75
            
            if random.random() < purchase_prob:
                events.append({
                    'event_id': event_id_counter,
                    'user_id': user_id,
                    'session_id': session_id,
                    'event_type': 'purchase_complete',
                    'timestamp': signup_time + timedelta(minutes=random.randint(21, 35))
                })
                event_id_counter += 1

df_events = pd.DataFrame(events)

# 3. Export to CSV files for your data analysis workflow
df_users.to_csv('ecommerce_users.csv', index=False)
df_events.to_csv('ecommerce_events.csv', index=False)

print("Success! Custom e-commerce dataset generated: 'ecommerce_users.csv' and 'ecommerce_events.csv'")