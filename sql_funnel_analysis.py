import sqlite3
import pandas as pd

df = pd.read_csv("funnel_events.csv")

conn = sqlite3.connect(":memory:")
df.to_sql("funnel_events", conn, index=False, if_exists="replace")

query_overall = """
WITH stage_counts AS (
    SELECT
        stage,
        COUNT(DISTINCT user_id) AS users
    FROM funnel_events
    GROUP BY stage
)
SELECT
    stage,
    users,
    ROUND(100.0 * users / (SELECT users FROM stage_counts WHERE stage = 'visit'), 2) AS pct_of_start
FROM stage_counts
ORDER BY
    CASE stage
        WHEN 'visit' THEN 1
        WHEN 'signup' THEN 2
        WHEN 'cart' THEN 3
        WHEN 'purchase' THEN 4
    END;
"""

overall = pd.read_sql_query(query_overall, conn)
print("=== OVERALL FUNNEL ===")
print(overall.to_string(index=False))

query_by_source = """
SELECT
    source,
    COUNT(DISTINCT CASE WHEN stage='visit' THEN user_id END) AS visit,
    COUNT(DISTINCT CASE WHEN stage='signup' THEN user_id END) AS signup,
    COUNT(DISTINCT CASE WHEN stage='cart' THEN user_id END) AS cart,
    COUNT(DISTINCT CASE WHEN stage='purchase' THEN user_id END) AS purchase
FROM funnel_events
GROUP BY source
ORDER BY visit DESC;
"""

by_source = pd.read_sql_query(query_by_source, conn)
by_source["signup_rate"] = round(100*by_source["signup"]/by_source["visit"], 1)
by_source["cart_rate"] = round(100*by_source["cart"]/by_source["signup"], 1)
by_source["purchase_rate"] = round(100*by_source["purchase"]/by_source["cart"], 1)
by_source["overall_conv"] = round(100*by_source["purchase"]/by_source["visit"], 1)

print("\n=== FUNNEL BY TRAFFIC SOURCE ===")
print(by_source.to_string(index=False))

overall.to_csv("funnel_overall.csv", index=False)
by_source.to_csv("funnel_by_source.csv", index=False)
conn.close()