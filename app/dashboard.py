import requests
import pandas as pd
import plotly.express as px
import gradio as gr
from .config import API_BASE_URL


def safe_get(path: str):
    r = requests.get(f"{API_BASE_URL}{path}", timeout=10)
    r.raise_for_status()
    return r.json()


def load_data():
    latest = safe_get("/events/latest?limit=200")
    summary = safe_get("/summary")
    routes = safe_get("/routes")
    stops = safe_get("/stops")
    return latest, summary, routes, stops


def format_risk_badge(risk_band: str) -> str:
    risk = str(risk_band).lower()
    if risk == "high":
        return "🔴 High"
    if risk == "medium":
        return "🟡 Medium"
    return "🟢 Low"


def kpi_card(value: str, label: str) -> str:
    return f"""
<div class="kpi-card">
    <div class="kpi-value">{value}</div>
    <div class="kpi-label">{label}</div>
</div>
"""


def build_dashboard(route_filter, stop_filter):
    latest, summary, _, _ = load_data()
    df = pd.DataFrame(latest)

    empty_fig = px.bar(title="No data available")

    if df.empty:
        return (
            kpi_card("0", "Total Events"),
            kpi_card("0", "Bunching Events"),
            kpi_card("0", "Gap Events"),
            kpi_card("0.000", "Avg Bunching Probability"),
            "## System Status\nNo live events available yet.",
            pd.DataFrame(),
            pd.DataFrame(),
            empty_fig,
            empty_fig,
            empty_fig,
            """
<div class="insight-card">
    <div class="insight-title">Route Insight</div>
    <div class="insight-body">No route insight available.</div>
</div>
""",
            """
<div class="insight-card">
    <div class="insight-title">AI Insight — Model Gemini 2.5 Flash</div>
    <div class="insight-body">No AI explanation available.</div>
</div>
""",
        )

    if route_filter != "All":
        df = df[df["route_id"] == route_filter]
    if stop_filter != "All":
        df = df[df["stop_name"] == stop_filter]

    if df.empty:
        return (
            kpi_card(str(summary.get("total_events", 0)), "Total Events"),
            kpi_card(str(summary.get("bunching_events", 0)), "Bunching Events"),
            kpi_card(str(summary.get("gap_events", 0)), "Gap Events"),
            kpi_card(str(round(float(summary.get("avg_bunching_probability", 0)), 3)), "Avg Bunching Probability"),
            "## System Status\nNo events match the selected filters.",
            pd.DataFrame(),
            pd.DataFrame(),
            empty_fig,
            empty_fig,
            empty_fig,
            """
<div class="insight-card">
    <div class="insight-title">Route Insight</div>
    <div class="insight-body">No route insight for this selection.</div>
</div>
""",
            """
<div class="insight-card">
    <div class="insight-title">AI Insight — Model Gemini 2.5 Flash</div>
    <div class="insight-body">No AI explanation for this selection.</div>
</div>
""",
        )

    total_events = kpi_card(str(summary.get("total_events", 0)), "Total Events")
    bunching_events = kpi_card(str(summary.get("bunching_events", 0)), "Bunching Events")
    gap_events = kpi_card(str(summary.get("gap_events", 0)), "Gap Events")
    avg_prob = kpi_card(str(round(float(summary.get("avg_bunching_probability", 0)), 3)), "Avg Bunching Probability")

    system_status_md = f"""
## System Status

**Total events processed:** {summary.get("total_events", 0)}  
**Bunching events detected:** {summary.get("bunching_events", 0)}  
**Gap events detected:** {summary.get("gap_events", 0)}  
**Average delay:** {round(float(summary.get("avg_delay_sec", 0)), 2)} sec  
**Average bunching probability:** {round(float(summary.get("avg_bunching_probability", 0)), 3)}
"""

    preview_cols = [
        "route_id",
        "bus_id",
        "stop_name",
        "headway_min",
        "status",
        "bunching_probability",
        "risk_band",
        "recommended_action",
        "hold_time_sec",
    ]
    preview_cols = [c for c in preview_cols if c in df.columns]
    preview_df = df[preview_cols].head(20).copy()

    if "headway_min" in preview_df.columns:
        preview_df["headway_min"] = preview_df["headway_min"].round(2)
    if "bunching_probability" in preview_df.columns:
        preview_df["bunching_probability"] = preview_df["bunching_probability"].round(3)
    if "risk_band" in preview_df.columns:
        preview_df["risk_band"] = preview_df["risk_band"].apply(format_risk_badge)

    top_cols = [
        "route_id",
        "stop_name",
        "headway_min",
        "status",
        "bunching_probability",
        "risk_band",
        "recommended_action",
        "hold_time_sec",
    ]
    top_cols = [c for c in top_cols if c in df.columns]
    top_risk_df = (
        df[top_cols]
        .sort_values("bunching_probability", ascending=False)
        .head(5)
        .copy()
    )

    if "headway_min" in top_risk_df.columns:
        top_risk_df["headway_min"] = top_risk_df["headway_min"].round(2)
    if "bunching_probability" in top_risk_df.columns:
        top_risk_df["bunching_probability"] = top_risk_df["bunching_probability"].round(3)
    if "risk_band" in top_risk_df.columns:
        top_risk_df["risk_band"] = top_risk_df["risk_band"].apply(format_risk_badge)

    status_counts = df["status"].value_counts().reset_index()
    status_counts.columns = ["status", "count"]
    fig_status = px.bar(
        status_counts,
        x="status",
        y="count",
        title="Service Status Distribution",
    )
    fig_status.update_layout(height=360)

    bunching_df = df[df["status"] == "bunching"]
    if bunching_df.empty:
        fig_bunching = px.bar(title="No bunching events in selection")
        fig_bunching.update_layout(height=360)
    else:
        hotspot_df = bunching_df["stop_name"].value_counts().reset_index()
        hotspot_df.columns = ["stop_name", "count"]
        fig_bunching = px.bar(
            hotspot_df,
            x="stop_name",
            y="count",
            title="Bunching Hotspots",
        )
        fig_bunching.update_layout(height=360, xaxis_tickangle=-35)

    risk_df = df.groupby("stop_name", as_index=False)["bunching_probability"].mean()
    fig_risk = px.bar(
        risk_df,
        x="stop_name",
        y="bunching_probability",
        title="Average Bunching Probability by Stop",
    )
    fig_risk.update_layout(height=360, xaxis_tickangle=-35)

    top = df.sort_values("bunching_probability", ascending=False).iloc[0]

    route_insight_md = f"""
<div class="insight-card">
    <div class="insight-title">Route Insight</div>
    <div class="insight-body">
        <b>Route:</b> {top.get('route_id', 'N/A')}<br>
        <b>Stop:</b> {top.get('stop_name', 'N/A')}<br>
        <b>Status:</b> {top.get('status', 'N/A')}<br>
        <b>Headway:</b> {round(float(top.get('headway_min', 0) or 0), 2)} min<br>
        <b>Bunching probability:</b> {round(float(top.get('bunching_probability', 0) or 0), 3)}<br>
        <b>Risk band:</b> {format_risk_badge(top.get('risk_band', 'Low'))}<br>
        <b>Recommended action:</b> {top.get('recommended_action', 'N/A')}<br>
        <b>Hold time:</b> {int(top.get('hold_time_sec', 0) or 0)} sec
    </div>
</div>
"""

    explanation_text = top.get("ai_explanation", "No AI explanation available.")
    ai_md = f"""
<div class="insight-card ai-card">
    <div class="insight-title">AI Insight — Model Gemini 2.5 Flash</div>
    <div class="insight-body">{explanation_text}</div>
</div>
"""

    return (
        total_events,
        bunching_events,
        gap_events,
        avg_prob,
        system_status_md,
        preview_df,
        top_risk_df,
        fig_status,
        fig_bunching,
        fig_risk,
        route_insight_md,
        ai_md,
    )


def launch_dashboard():
    _, _, routes, stops = load_data()

    route_options = ["All"] + routes
    stop_options = ["All"] + stops

    custom_css = """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    body, .gradio-container {
        font-family: 'Inter', sans-serif !important;
    }

    .gradio-container {
        max-width: 1400px !important;
        margin: 0 auto !important;
    }

    h1 {
        font-size: 42px !important;
        font-weight: 700 !important;
        letter-spacing: -1px !important;
        margin-bottom: 10px !important;
    }

    h2 {
        font-size: 24px !important;
        font-weight: 600 !important;
        margin-top: 8px !important;
        margin-bottom: 10px !important;
    }

    .gr-markdown p {
        line-height: 1.7 !important;
        font-size: 15px !important;
    }

    .kpi-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 18px 20px;
        min-height: 100px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.18);
    }

    .kpi-value {
        font-size: 30px;
        font-weight: 700;
        line-height: 1.1;
        margin-bottom: 8px;
    }

    .kpi-label {
        font-size: 14px;
        opacity: 0.8;
        font-weight: 500;
    }

    .insight-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 20px 22px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.18);
        white-space: normal !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        line-height: 1.8 !important;
        font-size: 16px !important;
    }

    .insight-title {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 14px;
    }

    .insight-body {
        font-size: 16px;
        line-height: 1.8;
        white-space: normal !important;
        word-break: break-word;
    }

    .ai-card {
        margin-top: 8px;
    }

    .block {
        border-radius: 18px !important;
    }
    """

    with gr.Blocks(
        title="Dublin Bus AI-Assisted Reliability Dashboard",
        theme=gr.themes.Soft(),
        css=custom_css,
    ) as demo:
        gr.Markdown("""
# Dublin Bus AI-Assisted Reliability Dashboard

Live operational intelligence system for detection, prediction, recommendations, and AI explanations.
""")

        with gr.Row():
            route_filter = gr.Dropdown(
                choices=route_options,
                value="All",
                label="Route Filter",
                scale=1,
            )
            stop_filter = gr.Dropdown(
                choices=stop_options,
                value="All",
                label="Stop Filter",
                scale=1,
            )

        with gr.Row():
            total_events_box = gr.Markdown()
            bunching_events_box = gr.Markdown()
            gap_events_box = gr.Markdown()
            avg_prob_box = gr.Markdown()

        system_status_md = gr.Markdown()

        gr.Markdown("---")
        gr.Markdown("## Latest Events")
        preview_df = gr.Dataframe(label="Latest Events Preview")

        gr.Markdown("## Operational Priority Queue")
        top_risk_df = gr.Dataframe(label="Top 5 Critical Events")

        gr.Markdown("---")
        with gr.Row():
            status_plot = gr.Plot()
            bunching_plot = gr.Plot()

        risk_plot = gr.Plot()

        gr.Markdown("---")
        route_insight_md = gr.Markdown()
        ai_md = gr.Markdown()

        refresh_btn = gr.Button("Refresh Now", variant="primary")

        outputs = [
            total_events_box,
            bunching_events_box,
            gap_events_box,
            avg_prob_box,
            system_status_md,
            preview_df,
            top_risk_df,
            status_plot,
            bunching_plot,
            risk_plot,
            route_insight_md,
            ai_md,
        ]

        refresh_btn.click(
            fn=build_dashboard,
            inputs=[route_filter, stop_filter],
            outputs=outputs,
        )

        demo.load(
            fn=build_dashboard,
            inputs=[route_filter, stop_filter],
            outputs=outputs,
        )

        timer = gr.Timer(3.0)
        timer.tick(
            fn=build_dashboard,
            inputs=[route_filter, stop_filter],
            outputs=outputs,
        )

    demo.launch()


if __name__ == "__main__":
    launch_dashboard()