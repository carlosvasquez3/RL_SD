import pandas as pd
import plotly.graph_objects as go
import colorcet as cc
import math

def generate_learning_plots(df: pd.DataFrame, max_lines_per_plot=4, title_prefix="Average return"):
    """
    Generate learning curves for reinforcement learning agent performance.
    
    Parameters:
    df: DataFrame with columns ['Epsilon_Level', 'Rho_Level', 'Repetition', 'Run', 'Return']
    max_lines_per_plot: Maximum number of treatment combinations per subplot
    title_prefix: Prefix for plot titles
    """
    
    # Group data and calculate statistics
    grouped_data = df.groupby(["Epsilon_Level", "Rho_Level", "Run"])["Return"]
    mean_return = grouped_data.mean()
    lower_ci = grouped_data.quantile(0.025)
    upper_ci = grouped_data.quantile(0.975)

    summary_df = pd.DataFrame({
        "mean_return": mean_return,
        "upper_ci": upper_ci,
        "lower_ci": lower_ci
    }).reset_index()

    # Treatment combinations
    treatment_groups = sorted(
        summary_df.groupby(["Epsilon_Level", "Rho_Level"]).groups.keys(),
        key=lambda x: (x[1], x[0])  # Sort by rho, then epsilon
    )

    total_plots = math.ceil(len(treatment_groups) / max_lines_per_plot)

    # Color palette
    palette = cc.glasbey_light[:max_lines_per_plot * total_plots]
    rgba_colors = [f'rgba({int(c[1:3],16)},{int(c[3:5],16)},{int(c[5:7],16)},0.15)' for c in palette]
    line_colors = [f'rgb({int(c[1:3],16)},{int(c[3:5],16)},{int(c[5:7],16)})' for c in palette]

    for plot_idx in range(total_plots):
        fig = go.Figure()
        subset_groups = treatment_groups[plot_idx * max_lines_per_plot:(plot_idx + 1) * max_lines_per_plot]

        for line_idx, (epsilon_level, rho_level) in enumerate(subset_groups):
            group_data = summary_df[(summary_df["Epsilon_Level"] == epsilon_level) & 
                                  (summary_df["Rho_Level"] == rho_level)]
            group_name = f"ϵ={epsilon_level}, ρ={rho_level}"

            color_idx = plot_idx * max_lines_per_plot + line_idx
            fill_color = rgba_colors[color_idx % len(rgba_colors)]
            line_color = line_colors[color_idx % len(line_colors)]

            # Confidence intervals
            fig.add_trace(go.Scatter(
                x=group_data["Run"].tolist() + group_data["Run"].tolist()[::-1],
                y=group_data["upper_ci"].tolist() + group_data["lower_ci"].tolist()[::-1],
                fill='toself', fillcolor=fill_color,
                line=dict(color='rgba(255,255,255,0)'),
                showlegend=False,
                legendgroup=group_name
            ))

            # Main learning curve
            fig.add_trace(go.Scatter(
                x=group_data["Run"], y=group_data["mean_return"],
                mode='lines', name=group_name,
                line=dict(width=2, color=line_color),
                legendgroup=group_name
            ))

        # Plot aesthetics
        fig.update_layout(
            title=f"<b>{title_prefix} — Subplot {plot_idx+1}</b>",
            title_x=0.5,
            title_font=dict(size=26),
            xaxis=dict(
                title="Run",
                title_font=dict(size=24),
                tickfont=dict(size=24)
            ),
            yaxis=dict(
                title="Average return (y)",
                title_font=dict(size=24),
                tickfont=dict(size=24)
            ),
            legend_title_font=dict(size=20),
            legend=dict(
                font=dict(size=24),
                title_side="top",
                yanchor="top", y=1,
                xanchor="left", x=1.02,
                orientation="v"
            ),
            template="plotly_white"
        )

        fig.show()