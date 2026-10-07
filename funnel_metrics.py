import pandas as pd
import json

overall = pd.read_csv("funnel_overall.csv")

stages = overall["stage"].tolist()
users = overall["users"].tolist()

stage_to_stage = []
for i in range(1, len(stages)):
    prev_stage, curr_stage = stages[i-1], stages[i]
    prev_users, curr_users = users[i-1], users[i]
    conv_rate = round(100 * curr_users / prev_users, 2)
    drop_rate = round(100 - conv_rate, 2)
    dropped_users = prev_users - curr_users
    stage_to_stage.append({
        "from_stage": prev_stage,
        "to_stage": curr_stage,
        "users_entering": prev_users,
        "users_advancing": curr_users,
        "users_dropped": dropped_users,
        "conversion_rate_pct": conv_rate,
        "drop_off_rate_pct": drop_rate
    })

df_transitions = pd.DataFrame(stage_to_stage)
print(df_transitions.to_string(index=False))

weakest = df_transitions.loc[df_transitions["drop_off_rate_pct"].idxmax()]
print(f"\n>>> WEAKEST STAGE: {weakest['from_stage']} -> {weakest['to_stage']}")
print(f">>> Drop-off rate: {weakest['drop_off_rate_pct']}% ({weakest['users_dropped']} users lost)")

avg_purchase_value = 55.00
improvement_pp = 10
new_rate = (weakest["conversion_rate_pct"] + improvement_pp) / 100
additional_users_advancing = int(weakest["users_entering"] * new_rate) - weakest["users_advancing"]

downstream_rate = 1.0
found = False
for t in stage_to_stage:
    if t["from_stage"] == weakest["from_stage"]:
        found = True
        continue
    if found:
        downstream_rate *= t["conversion_rate_pct"] / 100

additional_purchases = int(additional_users_advancing * downstream_rate)
additional_revenue = round(additional_purchases * avg_purchase_value, 2)

impact = {
    "weakest_transition": f"{weakest['from_stage']} -> {weakest['to_stage']}",
    "current_drop_off_pct": float(weakest["drop_off_rate_pct"]),
    "hypothetical_improvement_pp": int(improvement_pp),
    "additional_users_advancing": int(additional_users_advancing),
    "estimated_additional_purchases": int(additional_purchases),
    "assumed_avg_order_value": float(avg_purchase_value),
    "estimated_additional_revenue": float(additional_revenue)
}

print("\n=== BUSINESS IMPACT ESTIMATE ===")
for k,v in impact.items():
    print(f"{k}: {v}")

df_transitions.to_csv("funnel_transitions.csv", index=False)
with open("funnel_impact.json", "w") as f:
    json.dump(impact, f, indent=2)