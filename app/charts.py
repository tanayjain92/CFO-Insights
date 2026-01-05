import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from .metrics import metric_over_time, multi_metrics_over_time

# Single metric plot
def plot_metric_over_time(conn, metric, start_year=None, end_year=None, title=None):
    df = metric_over_time(conn, metric, start_year, end_year)

    # error check -
    if "error" in df.columns or df.empty:
        return None, df

    # matplotlib plot -
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df["year"], df[metric], marker="o", linestyle="-", linewidth=2, color="#007AFF")
    ax.set_xlabel("Year", fontsize=12)
    if title is None:
        title = f"{metric.replace('_', ' ').title()} Over Time"
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter('{x:,.0f}'))
    ax.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    return fig, df

# Multiple metrics plot
def plot_multi_metrics(conn, metrics, start_year=None, end_year=None, title="Financial Comparison"):
    df = multi_metrics_over_time(conn, metrics, start_year, end_year)
    
    if "error" in df.columns or df.empty:
        return None, df
    
    # plot -    
    fig, ax = plt.subplots(figsize=(10, 6))
    for metric in metrics:
        ax.plot(df["year"], df[metric], marker="o", label=metric.replace("_", " ").title())
    ax.set_xlabel("Year")
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter('{x:,.0f}'))
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    return fig, df