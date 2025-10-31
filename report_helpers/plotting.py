import pandas as pd
import plotly.graph_objects as go
import colorcet as cc

def generate_learning_plots(df: pd.DataFrame, title="RL Agent Learning"):
    """
    Generate learning curves for reinforcement learning agent performance.
    
    Parameters:
    df: DataFrame with columns ['Epsilon_Level', 'Rho_Level', 'Repetition', 'Run', 'Return']
    title: Title for the plot
    """
    
    grouped_data = df.groupby(["Epsilon_Level", "Rho_Level", "Run"])["Return"]
    mean_return = grouped_data.mean()
    lower_ci = grouped_data.quantile(0.025)
    upper_ci = grouped_data.quantile(0.975)

    summary_df = pd.DataFrame({
        "mean_return": mean_return,
        "upper_ci": upper_ci,
        "lower_ci": lower_ci
    }).reset_index()

    treatment_groups = sorted(
        summary_df.groupby(["Epsilon_Level", "Rho_Level"]).groups.keys(),
        key=lambda x: (x[1], x[0])
    )

    palette = cc.glasbey_light[:len(treatment_groups)]
    rgba_colors = [f'rgba({int(c[1:3],16)},{int(c[3:5],16)},{int(c[5:7],16)},0.15)' for c in palette]
    line_colors = [f'rgb({int(c[1:3],16)},{int(c[3:5],16)},{int(c[5:7],16)})' for c in palette]

    fig = go.Figure()

    for line_idx, (epsilon_level, rho_level) in enumerate(treatment_groups):
        group_data = summary_df[
            (summary_df["Epsilon_Level"] == epsilon_level) & 
            (summary_df["Rho_Level"] == rho_level)
        ]
        
        group_name = fr"$\Large \epsilon = {epsilon_level},\; \rho = {rho_level}$"

        fill_color = rgba_colors[line_idx % len(rgba_colors)]
        line_color = line_colors[line_idx % len(line_colors)]

        fig.add_trace(go.Scatter(
            x=group_data["Run"].tolist() + group_data["Run"].tolist()[::-1],
            y=group_data["upper_ci"].tolist() + group_data["lower_ci"].tolist()[::-1],
            fill='toself',
            fillcolor=fill_color,
            line=dict(color='rgba(255,255,255,0)'),
            showlegend=False,
            legendgroup=group_name
        ))

        fig.add_trace(go.Scatter(
            x=group_data["Run"],
            y=group_data["mean_return"],
            mode='lines',
            name=group_name,
            line=dict(width=2.5, color=line_color),
            legendgroup=group_name
        ))

    x_ticks = list(range(0, int(summary_df["Run"].max()) + 1, 100))
    x_ticktext = [fr"$\Large {val}$" for val in x_ticks]

    y_min = round(summary_df["mean_return"].min(), 1)
    y_max = round(summary_df["mean_return"].max(), 1)
    y_ticks = list(pd.Series(
        [round(val, 1) for val in 
         list(pd.Series(range(int(y_min), int(y_max) + 1, 10))) if val >= y_min and val <= y_max]
    ).drop_duplicates())
    y_ticktext = [fr"$\Large {val}$" for val in y_ticks]

    fig.update_layout(
        title=r"$\huge \textbf{" + title + r"}$",
        title_x=0.5,
        xaxis=dict(
            title=r"$\Large \mathit{Run}$",
            title_font=dict(size=26),
            tickfont=dict(size=22),
            tickmode="array",
            tickvals=x_ticks,
            ticktext=x_ticktext,
            automargin=True
        ),
        yaxis=dict(
            title=None,
            tickfont=dict(size=22),
            tickmode="array",
            tickvals=y_ticks,
            ticktext=y_ticktext,
            automargin=True
        ),
        legend=dict(
            font=dict(size=22),
            title_side="top",
            yanchor="top", y=1,
            xanchor="left", x=1.02,
            orientation="v",
            bgcolor="rgba(255,255,255,0.85)"
        ),
        margin=dict(l=100, r=120, t=100, b=80),
        template="plotly_white",
        font=dict(size=22)
    )

    fig.add_annotation(
        text=r"$\Large \bar{\mathit{y}}\; (\mathit{Average\ return})$",
        x=-0.08,
        y=0.5,
        xref="paper",
        yref="paper",
        textangle=-90,
        showarrow=False,
        font=dict(size=26)
    )

    fig.show()
