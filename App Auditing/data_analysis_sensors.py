import pandas as pd
import statsmodels.formula.api as smf
import scikit_posthocs as sp
import matplotlib.pyplot as plt
import seaborn as sns

# Load your CSV data
df = pd.read_csv("vr_app_permissions.csv")
df = df[df.User_Ratings < 1000].reset_index(drop=True)
plt.figure(figsize=(10, 6))
sns.boxplot(x="App_Genre", y="User_Ratings", data=df, palette="Set2")

plt.title("Distribution of Eye-Tracking Consent Prompts by App Genre")
plt.xlabel("App Genre")
plt.ylabel("Number of Consent Prompts")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

