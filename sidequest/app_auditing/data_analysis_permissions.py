import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr, shapiro
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Load your dataset
df = pd.read_csv("vr_app_permissions.csv")

# Optional: inspect
print(df.head())

print("Descriptive Statistics:")
print(df[['Total_Permissions', 'EyeTracking_Consent_Prompts']].describe())

# Shapiro-Wilk test
shapiro_perm = shapiro(df['Total_Permissions'])
shapiro_eye = shapiro(df['EyeTracking_Consent_Prompts'])

print(f"Shapiro-Wilk for Total_Permissions: p = {shapiro_perm.pvalue:.4f}")
print(f"Shapiro-Wilk for EyeTracking_Consent_Prompts: p = {shapiro_eye.pvalue:.4f}")

# Spearman correlation if non-normal
corr, p = spearmanr(df['Total_Permissions'], df['EyeTracking_Consent_Prompts'])

print(f"Spearman correlation: ρ = {corr:.3f}, p = {p:.4f}")

# Fit linear regression model
model = smf.ols("EyeTracking_Consent_Prompts ~ Total_Permissions", data=df).fit()
print(model.summary())

# Scatterplot with regression line
sns.lmplot(x="Total_Permissions", y="EyeTracking_Consent_Prompts", data=df, ci=95)
plt.title("Permissions vs Eye-Tracking Consent Prompts")
plt.xlabel("Total Permissions")
plt.ylabel("Eye-Tracking Consent Prompts")
plt.tight_layout()
plt.savefig("consent_prompt.pdf")
plt.show()
