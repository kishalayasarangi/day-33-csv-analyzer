import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os
import sys
from pathlib import Path

# ============================================
# CSV Data Analyzer
# Day 33 — 120 Days of Code | NIT Rourkela
# ============================================

def load_csv(filepath):
    try:
        df = pd.read_csv(filepath)
        print(f"\n✅ Loaded: {filepath}")
        print(f"   Rows: {len(df):,} | Columns: {len(df.columns)}")
        return df
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return None
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return None

def basic_info(df, filename):
    print("\n" + "=" * 55)
    print("  BASIC INFO")
    print("=" * 55)
    print(f"  File     : {filename}")
    print(f"  Rows     : {len(df):,}")
    print(f"  Columns  : {len(df.columns)}")
    print(f"  Size     : {df.memory_usage(deep=True).sum() / 1024:.1f} KB")

    print("\n  Columns:")
    for col in df.columns:
        dtype = str(df[col].dtype)
        nulls = df[col].isnull().sum()
        null_pct = (nulls / len(df) * 100)
        print(f"  {col:<25} {dtype:<12} {nulls} nulls ({null_pct:.1f}%)")

def numeric_analysis(df):
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if not numeric_cols:
        print("\n  No numeric columns found.")
        return

    print("\n" + "=" * 55)
    print("  NUMERIC ANALYSIS")
    print("=" * 55)

    for col in numeric_cols:
        data = df[col].dropna()
        if len(data) == 0:
            continue

        print(f"\n  📊 {col}")
        print(f"     Count  : {len(data):,}")
        print(f"     Mean   : {data.mean():.4f}")
        print(f"     Median : {data.median():.4f}")
        print(f"     Std Dev: {data.std():.4f}")
        print(f"     Min    : {data.min():.4f}")
        print(f"     Max    : {data.max():.4f}")
        print(f"     Range  : {data.max() - data.min():.4f}")

        q1 = data.quantile(0.25)
        q3 = data.quantile(0.75)
        iqr = q3 - q1
        outliers = data[(data < q1 - 1.5 * iqr) | (data > q3 + 1.5 * iqr)]
        print(f"     Q1     : {q1:.4f}")
        print(f"     Q3     : {q3:.4f}")
        print(f"     IQR    : {iqr:.4f}")
        print(f"     Outliers: {len(outliers)}")

def categorical_analysis(df):
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    if not cat_cols:
        return

    print("\n" + "=" * 55)
    print("  CATEGORICAL ANALYSIS")
    print("=" * 55)

    for col in cat_cols:
        data = df[col].dropna()
        unique = data.nunique()
        print(f"\n  📝 {col}")
        print(f"     Unique values: {unique}")
        print(f"     Most common:")
        for val, count in data.value_counts().head(5).items():
            pct = count / len(data) * 100
            bar = '█' * int(pct / 5)
            print(f"     {str(val):<20} {count:>6} ({pct:.1f}%) {bar}")

def generate_charts(df, output_dir="charts"):
    os.makedirs(output_dir, exist_ok=True)
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()

    plt.style.use('dark_background')
    charts_made = []

    # Histogram for each numeric column
    for col in numeric_cols[:4]:
        fig, ax = plt.subplots(figsize=(8, 5))
        data = df[col].dropna()
        ax.hist(data, bins=30, color='#7c3aed', edgecolor='#1e1e3a', alpha=0.85)
        ax.set_title(f'Distribution of {col}', color='white', fontsize=14)
        ax.set_xlabel(col, color='#a0a0b0')
        ax.set_ylabel('Frequency', color='#a0a0b0')
        ax.tick_params(colors='#606070')
        fig.patch.set_facecolor('#0f0f1a')
        ax.set_facecolor('#0a0a0a')
        path = f"{output_dir}/{col}_histogram.png"
        plt.savefig(path, bbox_inches='tight', dpi=100)
        plt.close()
        charts_made.append(path)

    # Bar chart for categorical columns
    for col in cat_cols[:2]:
        top = df[col].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(10, 5))
        colors = ['#7c3aed', '#10b981', '#f59e0b', '#ef4444', '#3b82f6',
                  '#ec4899', '#8b5cf6', '#14b8a6', '#f97316', '#06b6d4']
        bars = ax.barh(top.index.astype(str), top.values,
                       color=colors[:len(top)])
        ax.set_title(f'Top values in {col}', color='white', fontsize=14)
        ax.set_xlabel('Count', color='#a0a0b0')
        ax.tick_params(colors='#a0a0b0')
        fig.patch.set_facecolor('#0f0f1a')
        ax.set_facecolor('#0a0a0a')
        path = f"{output_dir}/{col}_barchart.png"
        plt.savefig(path, bbox_inches='tight', dpi=100)
        plt.close()
        charts_made.append(path)

    # Correlation heatmap
    if len(numeric_cols) >= 2:
        fig, ax = plt.subplots(figsize=(8, 6))
        corr = df[numeric_cols].corr()
        im = ax.imshow(corr, cmap='RdPu', vmin=-1, vmax=1)
        ax.set_xticks(range(len(numeric_cols)))
        ax.set_yticks(range(len(numeric_cols)))
        ax.set_xticklabels(numeric_cols, rotation=45, ha='right', color='#a0a0b0', fontsize=9)
        ax.set_yticklabels(numeric_cols, color='#a0a0b0', fontsize=9)
        for i in range(len(numeric_cols)):
            for j in range(len(numeric_cols)):
                ax.text(j, i, f'{corr.iloc[i, j]:.2f}',
                        ha='center', va='center', color='white', fontsize=8)
        plt.colorbar(im, ax=ax)
        ax.set_title('Correlation Heatmap', color='white', fontsize=14)
        fig.patch.set_facecolor('#0f0f1a')
        ax.set_facecolor('#0a0a0a')
        path = f"{output_dir}/correlation_heatmap.png"
        plt.savefig(path, bbox_inches='tight', dpi=100)
        plt.close()
        charts_made.append(path)

    return charts_made

def generate_report(df, filename, charts):
    report = []
    report.append(f"# CSV Analysis Report")
    report.append(f"**File:** {filename}")
    report.append(f"**Rows:** {len(df):,} | **Columns:** {len(df.columns)}")
    report.append(f"\n## Columns")
    for col in df.columns:
        report.append(f"- `{col}` ({df[col].dtype})")
    report.append(f"\n## Numeric Summary")
    numeric = df.select_dtypes(include=['number'])
    if not numeric.empty:
        report.append(numeric.describe().to_string())
    report.append(f"\n## Charts Generated")
    for c in charts:
        report.append(f"- {c}")

    with open("report.md", "w") as f:
        f.write("\n".join(report))
    print("\n  📄 Report saved: report.md")

def create_sample_csv():
    import random
    data = {
        'student_id': range(1, 101),
        'name': [f'Student_{i}' for i in range(1, 101)],
        'age': [random.randint(18, 25) for _ in range(100)],
        'branch': random.choices(
            ['Mechanical', 'CSE', 'ECE', 'Civil', 'Chemical'],
            k=100
        ),
        'cgpa': [round(random.uniform(5.0, 10.0), 2) for _ in range(100)],
        'attendance': [random.randint(50, 100) for _ in range(100)],
        'projects': [random.randint(0, 10) for _ in range(100)],
        'placement': random.choices(['Placed', 'Not Placed'], weights=[60, 40], k=100)
    }
    df = pd.DataFrame(data)
    df.to_csv('sample_students.csv', index=False)
    print("  ✅ Created sample_students.csv")
    return 'sample_students.csv'

def main():
    print("=" * 55)
    print("  CSV Data Analyzer — Day 33 of 120")
    print("=" * 55)
    print("\n  Options:")
    print("  1. Analyze a CSV file")
    print("  2. Generate and analyze sample data")

    choice = input("\n  Choose (1/2): ").strip()

    if choice == '1':
        filepath = input("  Enter CSV file path: ").strip()
    elif choice == '2':
        filepath = create_sample_csv()
    else:
        print("  Invalid choice!")
        return

    df = load_csv(filepath)
    if df is None:
        return

    basic_info(df, filepath)
    numeric_analysis(df)
    categorical_analysis(df)

    print("\n" + "=" * 55)
    print("  Generating charts...")
    charts = generate_charts(df)
    print(f"  ✅ {len(charts)} charts saved in charts/ folder")

    generate_report(df, filepath, charts)

    print("\n" + "=" * 55)
    print("  Analysis complete!")
    print("  Check the charts/ folder for visualizations")
    print("  Check report.md for the full report")
    print("=" * 55)

main()