import pandas as pd
import matplotlib.pyplot as plt

overall = pd.read_csv("funnel_overall.csv")
by_source = pd.read_csv("funnel_by_source.csv")

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

stages = overall["stage"].str.capitalize().tolist()
users = overall["users"].tolist()
pct = overall["pct_of_start"].tolist()

colors_funnel = ["#1e3a8a", "#2563eb", "#60a5fa", "#93c5fd"]
y_pos = range(len(stages))

bars = axes[0].barh(y_pos, users, color=colors_funnel, height=0.6, zorder=3)
axes[0].set_yticks(y_pos)
axes[0].set_yticklabels(stages, fontsize=11)
axes[0].invert_yaxis()
axes[0].set_xlabel("Users", fontsize=11)
axes[0].set_title("Conversion Funnel: Visit → Purchase", fontsize=13, fontweight='bold')
axes[0].spines[['top','right']].set_visible(False)
axes[0].grid(axis='x', alpha=0.3, zorder=0)

for i, (bar, u, p) in enumerate(zip(bars, users, pct)):
    axes[0].text(bar.get_width() + max(users)*0.015, bar.get_y() + bar.get_height()/2,
                 f"{u:,} ({p:.1f}%)", va='center', fontsize=10, fontweight='bold')

for i in range(1, len(users)):
    drop = users[i-1] - users[i]
    drop_pct = round(100*drop/users[i-1], 1)
    axes[0].text(max(users)*0.55, i - 0.5, f"↓ -{drop:,} users (-{drop_pct}%)",
                 fontsize=9.5, color="#dc2626", ha='left', va='center', fontweight='bold')

by_source_sorted = by_source.sort_values("overall_conv", ascending=True)
colors_src = ["#dc2626" if x < 10 else "#2563eb" for x in by_source_sorted["overall_conv"]]

bars2 = axes[1].barh(by_source_sorted["source"], by_source_sorted["overall_conv"],
                      color=colors_src, height=0.6, zorder=3)
axes[1].set_xlabel("Overall Conversion Rate (%) — Visit to Purchase", fontsize=11)
axes[1].set_title("Conversion Rate by Traffic Source", fontsize=13, fontweight='bold')
axes[1].spines[['top','right']].set_visible(False)
axes[1].grid(axis='x', alpha=0.3, zorder=0)

for bar, val in zip(bars2, by_source_sorted["overall_conv"]):
    axes[1].text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                 f"{val}%", va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig("funnel_dashboard.png", dpi=150, bbox_inches="tight")
print("Saved funnel_dashboard.png")
plt.show()