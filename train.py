# ╔══════════════════════════════════════════════════════════════════╗
# ║         STUDENT PERFORMANCE — FULL ML PIPELINE                  ║
# ║         VS Code Ready  |  Run with:  python pipeline.py         ║
# ║         Dataset : Student_Performance.csv  (10,000 rows)        ║
# ║         Target  : Performance Index → Binary Classification     ║
# ║         Split   : 80% Train | 20% Test                          ║
# ╚══════════════════════════════════════════════════════════════════╝
#
# SETUP (run once in your terminal)
# ──────────────────────────────────────────────────────────────────
#   pip install pandas numpy matplotlib seaborn scikit-learn scipy
#
# FOLDER STRUCTURE
# ──────────────────────────────────────────────────────────────────
#   your_project/
#   ├── pipeline.py                  ← this file
#   ├── Student_Performance.csv      ← your dataset (same folder)
#   └── outputs/                     ← charts saved here (auto-created)
# ──────────────────────────────────────────────────────────────────

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix,
    classification_report, RocCurveDisplay
)
import warnings
warnings.filterwarnings("ignore")

# ── Output folder for charts ───────────────────────────────────────
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save(fig, name):
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"   💾 Saved → {path}")

# ══════════════════════════════════════════════════════════════════
# STEP 1 ── DATA UNDERSTANDING
# ══════════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print("  STEP 1 : DATA UNDERSTANDING")
print("=" * 65)

# ── Load dataset ───────────────────────────────────────────────────
CSV_PATH = "Student_Performance.csv"   # ← change path if needed
df = pd.read_csv(CSV_PATH)

print(f"\n📌 Dataset loaded  : {CSV_PATH}")
print(f"   Shape           : {df.shape}")

print("\n📌 First 5 rows :")
print(df.head().to_string())

print("\n📌 Data Types :")
print(df.dtypes.to_string())

print("\n📌 Missing Values :")
missing     = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
print(pd.DataFrame({"Count": missing, "Percent (%)": missing_pct}).to_string())

print(f"\n📌 Duplicate Rows  : {df.duplicated().sum()}")

print("\n📌 Summary Statistics :")
print(df.describe().to_string())

print("\n📌 Unique values per column :")
print(df.nunique().to_frame("Unique Values").to_string())

print("\n📌 Extracurricular Activities values :",
      df["Extracurricular Activities"].unique().tolist())

# ── Distribution plots ─────────────────────────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
axes = axes.flatten()
for i, col in enumerate(df.columns):
    if col == "Extracurricular Activities":
        df[col].value_counts().plot(
            kind="bar", ax=axes[i],
            color=["steelblue", "tomato"], edgecolor="white"
        )
        axes[i].set_xticklabels(axes[i].get_xticklabels(), rotation=0)
    else:
        axes[i].hist(df[col], bins=20, color="steelblue", edgecolor="white")
        axes[i].set_ylabel("Count")
    axes[i].set_title(col, fontsize=10, fontweight="bold")

plt.suptitle("Step 1 — Feature Distributions", fontsize=14, fontweight="bold")
plt.tight_layout()
save(fig, "01_feature_distributions.png")


# ══════════════════════════════════════════════════════════════════
# STEP 2 ── DATA CLEANING
# ══════════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print("  STEP 2 : DATA CLEANING")
print("=" * 65)

# 2a. Remove duplicates
before = len(df)
df = df.drop_duplicates().reset_index(drop=True)
print(f"\n🗑️  Duplicates removed  : {before - len(df)}")
print(f"   Rows remaining     : {len(df)}")

# 2b. Missing values — your dataset has 0, but handled for safety
num_cols_fill = [
    "Hours Studied", "Previous Scores", "Sleep Hours",
    "Sample Question Papers Practiced", "Performance Index"
]
for col in num_cols_fill:
    if df[col].isnull().sum() > 0:
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)
        print(f"   ✔ {col}: filled with median ({median_val:.2f})")

print("\n📌 Missing values after cleaning :")
print(df.isnull().sum().to_string())

# 2c. Standardise categorical text
df["Extracurricular Activities"] = (
    df["Extracurricular Activities"].str.strip().str.title()
)
print("\n✅ Extracurricular Activities cleaned:",
      df["Extracurricular Activities"].unique().tolist())
print("\n✅ Data cleaning complete. Shape:", df.shape)


# ══════════════════════════════════════════════════════════════════
# STEP 3 ── OUTLIER DETECTION & REMOVAL
# ══════════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print("  STEP 3 : OUTLIER DETECTION")
print("=" * 65)

continuous_cols = [
    "Hours Studied", "Previous Scores", "Sleep Hours",
    "Sample Question Papers Practiced", "Performance Index"
]

# ── Boxplots BEFORE ────────────────────────────────────────────────
fig, axes = plt.subplots(1, 5, figsize=(20, 4))
for ax, col in zip(axes, continuous_cols):
    sns.boxplot(y=df[col], ax=ax, color="lightcoral",
                flierprops=dict(marker="o", markersize=3))
    ax.set_title(col, fontsize=9, fontweight="bold")
plt.suptitle("Step 3 — Boxplots BEFORE Outlier Removal",
             fontsize=13, fontweight="bold")
plt.tight_layout()
save(fig, "02_boxplot_before.png")

# ── Remove outliers using IQR (3 × IQR fence) ─────────────────────
before = len(df)
mask   = pd.Series([True] * len(df), index=df.index)
for col in continuous_cols:
    Q1  = df[col].quantile(0.25)
    Q3  = df[col].quantile(0.75)
    IQR = Q3 - Q1
    mask &= df[col].between(Q1 - 3 * IQR, Q3 + 3 * IQR)

df = df[mask].reset_index(drop=True)
print(f"\n🗑️  Outlier rows removed : {before - len(df)}")
print(f"   Rows remaining      : {len(df)}")

# ── Boxplots AFTER ─────────────────────────────────────────────────
fig, axes = plt.subplots(1, 5, figsize=(20, 4))
for ax, col in zip(axes, continuous_cols):
    sns.boxplot(y=df[col], ax=ax, color="lightgreen",
                flierprops=dict(marker="o", markersize=3))
    ax.set_title(col, fontsize=9, fontweight="bold")
plt.suptitle("Step 3 — Boxplots AFTER Outlier Removal",
             fontsize=13, fontweight="bold")
plt.tight_layout()
save(fig, "03_boxplot_after.png")


# ══════════════════════════════════════════════════════════════════
# STEP 4 ── FEATURE ENGINEERING
# ══════════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print("  STEP 4 : FEATURE ENGINEERING")
print("=" * 65)

df["Study_Sleep_Ratio"]   = df["Hours Studied"] / (df["Sleep Hours"] + 1)
df["Total_Preparation"]   = (df["Hours Studied"] +
                              df["Sample Question Papers Practiced"])
df["Score_Per_StudyHour"] = df["Previous Scores"] / (df["Hours Studied"] + 1)

print("✅ New features created:")
print("   • Study_Sleep_Ratio   = Hours Studied / (Sleep Hours + 1)")
print("   • Total_Preparation   = Hours Studied + Sample Question Papers Practiced")
print("   • Score_Per_StudyHour = Previous Scores / (Hours Studied + 1)")

# ── Binary target from Performance Index (median = 55) ────────────
threshold = df["Performance Index"].median()
df["Performance_Class"] = (df["Performance Index"] >= threshold).astype(int)

print(f"\n🎯 Target : Performance_Class")
print(f"   Threshold (median) : {threshold:.1f}")
print(f"\n   Class distribution :")
vc = df["Performance_Class"].value_counts().rename(
    {0: "Low  (0) < 55", 1: "High (1) ≥ 55"}
)
print(vc.to_string())

# ── Class distribution bar ─────────────────────────────────────────
fig, ax = plt.subplots(figsize=(5, 3))
df["Performance_Class"].value_counts().plot(
    kind="bar", color=["tomato", "steelblue"], edgecolor="white", ax=ax
)
ax.set_title("Target Class Distribution", fontweight="bold")
ax.set_xticklabels(["High (1) ≥ 55", "Low (0) < 55"], rotation=0)
ax.set_ylabel("Count")
plt.tight_layout()
save(fig, "04_class_distribution.png")

# ── Correlation heatmap ────────────────────────────────────────────
corr_df = df.drop(columns=["Extracurricular Activities",
                            "Performance Index"], errors="ignore")
fig, ax = plt.subplots(figsize=(10, 7))
sns.heatmap(corr_df.corr(), annot=True, fmt=".2f",
            cmap="coolwarm", linewidths=0.5, ax=ax)
ax.set_title("Feature Correlation Heatmap", fontweight="bold")
plt.tight_layout()
save(fig, "05_correlation_heatmap.png")


# ══════════════════════════════════════════════════════════════════
# STEP 5 ── ENCODING
# ══════════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print("  STEP 5 : ENCODING")
print("=" * 65)

le = LabelEncoder()
df["Extracurricular_Enc"] = le.fit_transform(df["Extracurricular Activities"])
mapping = dict(zip(le.classes_, le.transform(le.classes_)))
print(f"\n✅ Extracurricular Activities encoded : {mapping}")
print("   (No → 0,  Yes → 1)")


# ══════════════════════════════════════════════════════════════════
# STEP 6 ── FEATURE SCALING & TRAIN / TEST SPLIT
# ══════════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print("  STEP 6 : FEATURE SCALING  (80 / 20 split)")
print("=" * 65)

FEATURE_COLS = [
    "Hours Studied",
    "Previous Scores",
    "Sleep Hours",
    "Sample Question Papers Practiced",
    "Extracurricular_Enc",
    "Study_Sleep_Ratio",
    "Total_Preparation",
    "Score_Per_StudyHour",
]

X = df[FEATURE_COLS].copy()
y = df["Performance_Class"]

# ── 80 / 20 stratified split ───────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size    = 0.20,
    random_state = 42,
    stratify     = y
)

print(f"\n   Total samples  : {len(df)}")
print(f"   Train samples  : {len(X_train)}  ({len(X_train)/len(df)*100:.0f}%)")
print(f"   Test  samples  : {len(X_test)}   ({len(X_test)/len(df)*100:.0f}%)")

# ── StandardScaler ─────────────────────────────────────────────────
scaler     = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)   # fit on train only
X_test_sc  = scaler.transform(X_test)        # apply same scale to test

print(f"\n✅ StandardScaler applied.")
print(f"   X_train shape  : {X_train_sc.shape}")
print(f"   X_test  shape  : {X_test_sc.shape}")

scaled_preview = pd.DataFrame(X_train_sc, columns=FEATURE_COLS)
print("\n📌 Scaled feature stats (mean ≈ 0, std ≈ 1) :")
print(scaled_preview.describe().round(3).to_string())


# ══════════════════════════════════════════════════════════════════
# STEP 7 ── MODEL BUILDING
# ══════════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print("  STEP 7 : MODEL BUILDING")
print("=" * 65)

# Model 1 : Logistic Regression
lr_model = LogisticRegression(max_iter=1000, random_state=42, C=1.0)
lr_model.fit(X_train_sc, y_train)
print("✅ Model 1 : Logistic Regression  — trained")

# Model 2 : Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train_sc, y_train)
print("✅ Model 2 : Random Forest         — trained")


# ══════════════════════════════════════════════════════════════════
# STEP 8 ── MODEL EVALUATION
# ══════════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print("  STEP 8 : MODEL EVALUATION")
print("=" * 65)

def evaluate(name, model, X, y_true):
    y_pred  = model.predict(X)
    y_proba = model.predict_proba(X)[:, 1]
    return {
        "Model"    : name,
        "Accuracy" : accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred),
        "Recall"   : recall_score(y_true, y_pred),
        "F1-Score" : f1_score(y_true, y_pred),
        "ROC-AUC"  : roc_auc_score(y_true, y_proba),
        "_pred"    : y_pred,
        "_proba"   : y_proba,
        "_cm"      : confusion_matrix(y_true, y_pred),
        "_report"  : classification_report(
                         y_true, y_pred,
                         target_names=["Low (0)", "High (1)"])
    }

lr_res = evaluate("Logistic Regression", lr_model, X_test_sc, y_test)
rf_res = evaluate("Random Forest",       rf_model, X_test_sc, y_test)

# ── Print detailed reports ─────────────────────────────────────────
for res in [lr_res, rf_res]:
    print(f"\n{'─'*50}")
    print(f"  {res['Model']}")
    print(f"{'─'*50}")
    print(f"  Accuracy  : {res['Accuracy']:.4f}")
    print(f"  Precision : {res['Precision']:.4f}")
    print(f"  Recall    : {res['Recall']:.4f}")
    print(f"  F1-Score  : {res['F1-Score']:.4f}")
    print(f"  ROC-AUC   : {res['ROC-AUC']:.4f}")
    print(f"\n  Classification Report:\n{res['_report']}")

# ── Summary comparison table ───────────────────────────────────────
summary = pd.DataFrame([
    {k: v for k, v in r.items() if not k.startswith("_")}
    for r in [lr_res, rf_res]
]).set_index("Model").round(4)

print("\n📊 FINAL COMPARISON TABLE")
print(summary.to_string())

# ── Confusion Matrices ─────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
for ax, res in zip(axes, [lr_res, rf_res]):
    sns.heatmap(
        res["_cm"],
        annot       = True,
        fmt         = "d",
        cmap        = "Blues",
        ax          = ax,
        linewidths  = 0.5,
        xticklabels = ["Low (0)", "High (1)"],
        yticklabels = ["Low (0)", "High (1)"]
    )
    ax.set_title(f"Confusion Matrix\n{res['Model']}", fontweight="bold")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")

plt.suptitle("Step 8 — Confusion Matrices", fontsize=14, fontweight="bold")
plt.tight_layout()
save(fig, "06_confusion_matrices.png")

# ── ROC Curves ────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 6))
RocCurveDisplay.from_predictions(
    y_test, lr_res["_proba"],
    name  = f"Logistic Regression  (AUC = {lr_res['ROC-AUC']:.3f})",
    ax    = ax, color="steelblue"
)
RocCurveDisplay.from_predictions(
    y_test, rf_res["_proba"],
    name  = f"Random Forest        (AUC = {rf_res['ROC-AUC']:.3f})",
    ax    = ax, color="tomato"
)
ax.plot([0, 1], [0, 1], "k--", label="Random Baseline")
ax.set_title("ROC Curve — Model Comparison", fontweight="bold", fontsize=13)
ax.legend(loc="lower right")
plt.tight_layout()
save(fig, "07_roc_curve.png")

# ── Feature Importance (Random Forest) ────────────────────────────
importances = (
    pd.Series(rf_model.feature_importances_, index=FEATURE_COLS)
    .sort_values(ascending=True)
)
fig, ax = plt.subplots(figsize=(9, 5))
colors  = ["#2196F3" if v >= importances.median() else "#90CAF9"
           for v in importances]
importances.plot(kind="barh", ax=ax, color=colors, edgecolor="white")
for i, v in enumerate(importances):
    ax.text(v + 0.001, i, f"{v:.3f}", va="center", fontsize=9)
ax.set_title("Feature Importance — Random Forest", fontweight="bold", fontsize=13)
ax.set_xlabel("Importance Score")
plt.tight_layout()
save(fig, "08_feature_importance.png")

# ── Logistic Regression Coefficients ──────────────────────────────
coef_series = (
    pd.Series(lr_model.coef_[0], index=FEATURE_COLS)
    .sort_values(ascending=True)
)
fig, ax = plt.subplots(figsize=(9, 5))
colors  = ["tomato" if v < 0 else "steelblue" for v in coef_series]
coef_series.plot(kind="barh", ax=ax, color=colors, edgecolor="white")
ax.axvline(0, color="black", linewidth=0.8)
ax.set_title("Logistic Regression — Feature Coefficients",
             fontweight="bold", fontsize=13)
ax.set_xlabel("Coefficient Value")
plt.tight_layout()
save(fig, "09_lr_coefficients.png")

print("\n" + "=" * 65)
print("  ✅  All charts saved to the  outputs/  folder")
print("  🏁  Pipeline Complete!")
print("=" * 65)