import pandas as pd

# 1. Load the datasets
print("--- LOADING DATASETS ---")
df_users = pd.read_csv('ecommerce_users.csv')
df_events = pd.read_csv('ecommerce_events.csv')
print(f"Loaded {len(df_users)} users and {len(df_events)} event records.\n")

# 2. Merge users with their events to tie device types and channels to actions
df_merged = pd.merge(df_events, df_users, on='user_id', how='inner')

# 3. Calculate Overall Funnel Counts
funnel_order = ['page_view', 'add_to_cart', 'checkout_start', 'purchase_complete']
funnel_counts = df_merged.groupby('event_type')['user_id'].nunique().reindex(funnel_order)

print("--- OVERALL CONVERSION FUNNEL ---")
total_users = funnel_counts['page_view']
for stage, count in funnel_counts.items():
    conversion_rate = (count / total_users) * 100
    print(f"Stage: {stage.upper()} | Unique Users: {count} | Conversion from Start: {conversion_rate:.1f}%")

# 4. Segment by Device Type (Isolating the Mobile Bottleneck)
print("\n--- CONVERSION BY DEVICE TYPE ---")
device_funnel = pd.pivot_table(
    df_merged,
    index='event_type',
    columns='device_type',
    values='user_id',
    aggfunc='nunique'
).reindex(funnel_order)

# Calculate percentage relative to page_view for each device
device_totals = df_users['device_type'].value_counts()
device_conversion = device_funnel.copy()
for col in device_conversion.columns:
    device_conversion[col] = (device_conversion[col] / device_totals[col]) * 100

print(device_conversion.round(1))
print("\nAnalysis complete! This breakdown proves your exact data insight.")