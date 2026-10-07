import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(7)

n_visitors = 20000
start_date = datetime(2025, 6, 1)

p_visit_to_signup = 0.45
p_signup_to_cart  = 0.55
p_cart_to_purchase = 0.40

sources = np.random.choice(
    ["organic_search", "paid_ads", "social_media", "email", "direct"],
    size=n_visitors, p=[0.30, 0.25, 0.20, 0.15, 0.10]
)

device = np.random.choice(["mobile", "desktop", "tablet"], size=n_visitors, p=[0.55, 0.38, 0.07])

visit_dates = [start_date + timedelta(days=int(d), hours=np.random.randint(0,24))
               for d in np.random.randint(0, 30, n_visitors)]

user_ids = [f"U{i:07d}" for i in range(1, n_visitors+1)]

rows = []
for i in range(n_visitors):
    uid = user_ids[i]
    src = sources[i]
    dev = device[i]
    v_date = visit_dates[i]

    src_boost = {"organic_search": 1.05, "paid_ads": 0.85, "social_media": 0.75,
                 "email": 1.25, "direct": 1.10}[src]
    dev_boost = {"mobile": 0.85, "desktop": 1.20, "tablet": 0.95}[dev]

    rows.append({"user_id": uid, "source": src, "device": dev, "visit_date": v_date, "stage": "visit"})

    if np.random.rand() < min(p_visit_to_signup * src_boost * dev_boost, 0.95):
        s_date = v_date + timedelta(minutes=int(np.random.exponential(20)))
        rows.append({"user_id": uid, "source": src, "device": dev, "visit_date": s_date, "stage": "signup"})

        if np.random.rand() < min(p_signup_to_cart * src_boost * dev_boost, 0.95):
            c_date = s_date + timedelta(minutes=int(np.random.exponential(45)))
            rows.append({"user_id": uid, "source": src, "device": dev, "visit_date": c_date, "stage": "cart"})

            if np.random.rand() < min(p_cart_to_purchase * src_boost * dev_boost, 0.95):
                p_date = c_date + timedelta(minutes=int(np.random.exponential(30)))
                rows.append({"user_id": uid, "source": src, "device": dev, "visit_date": p_date, "stage": "purchase"})

df = pd.DataFrame(rows)
df = df.rename(columns={"visit_date": "event_timestamp"})
df.to_csv("funnel_events.csv", index=False)

print(df.head(12))
print("\nTotal events:", len(df))
print("\nEvent counts by stage:")
print(df["stage"].value_counts())