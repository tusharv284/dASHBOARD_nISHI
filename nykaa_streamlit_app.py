
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Nykaa Discounting & Premium Perception",
    page_icon="💄",
    layout="wide"
)

# Dark theme via custom CSS (works even if viewer uses light mode)
DARK_BG = "#050814"
CARD_BG = "#0b1020"
ACCENT = "#e91e63"
TEXT = "#f5f5f5"
MUTED = "#9e9e9e"

st.markdown(f"""
    <style>
    .stApp {{
        background-color: {DARK_BG};
        color: {TEXT};
    }}
    .metric-card {{
        background-color: {CARD_BG};
        padding: 1rem 1.2rem;
        border-radius: 0.7rem;
        border: 1px solid #1f2937;
    }}
    .metric-label {{
        font-size: 0.85rem;
        color: {MUTED};
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }}
    .metric-value {{
        font-size: 1.4rem;
        font-weight: 600;
        color: {TEXT};
    }}
    .metric-delta-pos {{
        font-size: 0.8rem;
        color: #4ade80;
    }}
    .metric-delta-neg {{
        font-size: 0.8rem;
        color: #f97373;
    }}
    .section-title {{
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.2rem;
        color: {TEXT};
    }}
    .section-sub {{
        font-size: 0.85rem;
        color: {MUTED};
        margin-bottom: 0.8rem;
    }}
    </style>
""", unsafe_allow_html=True)

st.markdown("""
# Nykaa: Is Discounting Killing Premium Brand Perception?
""")

with st.expander("📌 How to read this dashboard", expanded=False):
    st.write("""This executive view is organized to answer three questions:
    1. Is discounting increasing short‑term revenue?
    2. Is it damaging long‑term customer quality?
    3. What should Nykaa change in its discount strategy?

    Use the tabs below to move from **diagnostics → segmentation → prediction → strategy**.
    """)

# Sidebar controls
st.sidebar.header("Simulation Controls")

selected_period = st.sidebar.selectbox(
    "Analysis window", ["Last 30 days", "Last 90 days", "Last 180 days", "Last 365 days"], index=1
)

discount_shift = st.sidebar.slider(
    "Change discount frequency", -30, 30, 0, help="Simulate % change in overall discount frequency"
)

discount_intensity = st.sidebar.slider(
    "Change average discount %", -20, 20, 0, help="Simulate % change in average discount depth"
)

st.sidebar.markdown("---")
selected_segment = st.sidebar.selectbox(
    "Focus segment",
    ["All", "Full‑Price Loyalists", "Smart Shoppers", "Discount Addicts", "Deal Chasers"],
)

st.sidebar.markdown("""---
**Premium Brand Risk Index** is a composite score (0‑100) based on:
- Full‑price purchase rate
- Brand switching
- AOV erosion
- Discount dependency growth
""")

# --------- Dummy data generators (replace with real models/data) ---------
np.random.seed(42)

# Example headline metrics influenced by sliders (simple elasticities for demo)
base_revenue = 100.0
base_margin = 32.0
base_risk = 58.0

revenue_impact = 1 + (discount_shift * 0.12 + discount_intensity * 0.18) / 100
margin_impact = 1 - (discount_shift * 0.08 + discount_intensity * 0.25) / 100
risk_impact = 1 + (discount_shift * 0.25 + discount_intensity * 0.3) / 100

rev_value = base_revenue * revenue_impact
margin_value = base_margin * margin_impact
risk_value = min(max(base_risk * risk_impact, 0), 100)

# Headline KPI row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Revenue (Indexed)</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{rev_value:0.1f}</div>', unsafe_allow_html=True)
    delta = (revenue_impact - 1) * 100
    css = "metric-delta-pos" if delta >= 0 else "metric-delta-neg"
    st.markdown(f'<div class="{css}">{delta:+0.1f}% vs baseline</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Gross Margin %</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{margin_value:0.1f}%</div>', unsafe_allow_html=True)
    delta = (margin_impact - 1) * 100
    css = "metric-delta-pos" if delta >= 0 else "metric-delta-neg"
    st.markdown(f'<div class="{css}">{delta:+0.1f} pts vs baseline</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Revenue from Discounted Orders</div>', unsafe_allow_html=True)
    disc_share = 62 + discount_shift * 0.4 + discount_intensity * 0.7
    st.markdown(f'<div class="metric-value">{disc_share:0.1f}%</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-delta-neg">High discount dependency</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Premium Brand Risk Index</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{risk_value:0.0f} / 100</div>', unsafe_allow_html=True)
    risk_tag = "Elevated" if risk_value >= 60 else "Stable"
    css = "metric-delta-neg" if risk_value >= 60 else "metric-delta-pos"
    st.markdown(f'<div class="{css}">{risk_tag} premium erosion risk</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Tabs = the 4 layers
layer1, layer2, layer3, layer4 = st.tabs([
    "1. Discount Dependency",
    "2. Customer Segments",
    "3. Predictive Models",
    "4. Decision Engine",
])

# ---------- Layer 1: Discount dependency diagnostics ----------
with layer1:
    st.markdown('<div class="section-title">Discount Dependency KPIs</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Are we buying short‑term revenue at the cost of margin and premium perception?</div>', unsafe_allow_html=True)

    # Sample monthly time‑series
    months = pd.date_range(end=pd.Timestamp.today(), periods=12, freq="M")
    df_disc = pd.DataFrame({
        "Month": months,
        "Discounted Revenue %": np.linspace(55, 68, 12) + np.random.normal(0, 1.2, 12),
        "Average Discount %": np.linspace(18, 24, 12) + np.random.normal(0, 0.6, 12),
        "Full‑Price Purchase Rate": np.linspace(45, 34, 12) + np.random.normal(0, 1.0, 12),
    })

    c1, c2 = st.columns([2, 1.3])

    with c1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_disc["Month"], y=df_disc["Discounted Revenue %"],
            mode="lines+markers", name="Revenue from Discounted Orders",
            line=dict(color=ACCENT, width=2)
        ))
        fig.add_trace(go.Scatter(
            x=df_disc["Month"], y=df_disc["Full‑Price Purchase Rate"],
            mode="lines+markers", name="Full‑Price Purchase Rate",
            line=dict(color="#4ade80", width=2)
        ))
        fig.update_layout(
            template="plotly_dark",
            plot_bgcolor=CARD_BG,
            paper_bgcolor=CARD_BG,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=20, r=20, t=40, b=20),
            height=360,
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Premium Erosion Signals</div>', unsafe_allow_html=True)
        st.write("• Full‑price rate trending down over last 6 months")
        st.write("• Revenue increasingly concentrated in sale periods")
        st.write("• Higher brand switching post mega‑sales")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    c3, c4 = st.columns(2)

    with c3:
        # Simple elasticity view
        discounts = np.array([0, 10, 20, 30])
        revenue_curve = 100 * (1 + 0.015 * discounts - 0.0002 * discounts ** 2)
        margin_curve = 32 * (1 - 0.018 * discounts)
        df_elastic = pd.DataFrame({
            "Discount %": discounts,
            "Revenue Index": revenue_curve,
            "Margin %": margin_curve,
        })
        fig2 = px.line(
            df_elastic.melt(id_vars="Discount %", value_vars=["Revenue Index", "Margin %"]),
            x="Discount %", y="value", color="variable",
            template="plotly_dark", markers=True,
            color_discrete_map={"Revenue Index": ACCENT, "Margin %": "#4ade80"},
        )
        fig2.update_layout(
            plot_bgcolor=CARD_BG,
            paper_bgcolor=CARD_BG,
            height=330,
            legend_title="",
        )
        st.plotly_chart(fig2, use_container_width=True)

    with c4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Key Insight</div>', unsafe_allow_html=True)
        st.write("• Revenue peaks around 15‑20% discount before margins fall sharply.")
        st.write("• Above this, Nykaa is likely over‑discounting for limited incremental volume.")
        st.write("• This is the starting point for defining the optimal discount band.")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- Layer 2: Customer segmentation ----------
with layer2:
    st.markdown('<div class="section-title">Customer Segments & Quality</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Do heavy‑discount customers dilute long‑term value?</div>', unsafe_allow_html=True)

    segments = ["Full‑Price Loyalists", "Smart Shoppers", "Discount Addicts", "Deal Chasers"]
    df_seg = pd.DataFrame({
        "Segment": segments,
        "6M LTV": [4200, 3100, 1900, 900],
        "90D Retention %": [78, 65, 48, 22],
        "Churn Probability": [0.12, 0.22, 0.38, 0.61],
        "Margin per Customer": [31, 28, 17, 9],
        "Brand Loyalty Index": [0.86, 0.71, 0.44, 0.21],
        "Discount Dependency": [0.10, 0.35, 0.82, 0.95],
    })

    if selected_segment != "All":
        df_view = df_seg[df_seg["Segment"] == selected_segment]
    else:
        df_view = df_seg.copy()

    st.dataframe(
        df_view.style.format({
            "6M LTV": "₹{:.0f}",
            "90D Retention %": "{:.0f}%",
            "Churn Probability": "{:.0%}",
            "Margin per Customer": "₹{:.0f}",
            "Brand Loyalty Index": "{:.2f}",
            "Discount Dependency": "{:.0%}",
        }),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:
        fig3 = px.bar(
            df_seg,
            x="Segment",
            y="6M LTV",
            color="Segment",
            template="plotly_dark",
            color_discrete_sequence=[ACCENT, "#4ade80", "#f97373", "#facc15"],
        )
        fig3.update_layout(
            plot_bgcolor=CARD_BG,
            paper_bgcolor=CARD_BG,
            showlegend=False,
            height=340,
        )
        st.plotly_chart(fig3, use_container_width=True)

    with c2:
        fig4 = px.scatter(
            df_seg,
            x="Discount Dependency",
            y="6M LTV",
            size="Margin per Customer",
            color="Segment",
            template="plotly_dark",
            color_discrete_sequence=[ACCENT, "#4ade80", "#f97373", "#facc15"],
        )
        fig4.update_layout(
            plot_bgcolor=CARD_BG,
            paper_bgcolor=CARD_BG,
            height=340,
        )
        st.plotly_chart(fig4, use_container_width=True)

# ---------- Layer 3: Predictive models layer ----------
with layer3:
    st.markdown('<div class="section-title">Predictive Signals</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Forward‑looking view of LTV, churn, and incremental revenue from discounting.</div>', unsafe_allow_html=True)

    tab_a, tab_b, tab_c, tab_d, tab_e = st.tabs([
        "LTV vs Discount", "Churn Risk", "Next Purchase", "Uplift", "Elasticity Sim"
    ])

    with tab_a:
        st.write("Predicted LTV drops as discount dependency rises, indicating premium dilution risk for over‑incentivized cohorts.")
        dep = np.linspace(0, 1, 20)
        ltv = 4500 * (1 - 0.55 * dep + 0.08 * dep ** 2)
        df_ltv = pd.DataFrame({"Discount Dependency": dep, "Predicted LTV": ltv})
        fig = px.line(df_ltv, x="Discount Dependency", y="Predicted LTV", template="plotly_dark", markers=True,
                      color_discrete_sequence=[ACCENT])
        fig.update_layout(plot_bgcolor=CARD_BG, paper_bgcolor=CARD_BG, height=340)
        st.plotly_chart(fig, use_container_width=True)

    with tab_b:
        st.write("Churn probability spikes when discount‑heavy customers do not see deals for 60‑90 days.")
        days = np.arange(0, 120, 10)
        churn = 0.08 + 0.003 * days
        churn_disc = 0.12 + 0.006 * days
        df_c = pd.DataFrame({"Days Since Last Discount": days, "Low Discount Users": churn, "High Discount Users": churn_disc})
        fig = px.line(df_c.melt(id_vars="Days Since Last Discount"),
                      x="Days Since Last Discount", y="value", color="variable",
                      template="plotly_dark",
                      color_discrete_sequence=["#4ade80", ACCENT])
        fig.update_layout(plot_bgcolor=CARD_BG, paper_bgcolor=CARD_BG, height=340, legend_title="")
        st.plotly_chart(fig, use_container_width=True)

    with tab_c:
        st.write("Discount‑addicted cohorts delay purchases outside sale windows, leading to lumpy, promotion‑driven demand.")
        days = np.arange(1, 60)
        next_purchase_full = 18 + np.random.gamma(3, 1.2, len(days))
        next_purchase_disc = 22 + np.random.gamma(4, 1.4, len(days))
        df_np = pd.DataFrame({"Customer Type": np.repeat(["Low Discount", "High Discount"], len(days)),
                              "Days to Next Purchase": np.concatenate([next_purchase_full, next_purchase_disc])})
        fig = px.histogram(df_np, x="Days to Next Purchase", color="Customer Type", barmode="overlay",
                           template="plotly_dark", nbins=25,
                           color_discrete_sequence=["#4ade80", ACCENT])
        fig.update_layout(plot_bgcolor=CARD_BG, paper_bgcolor=CARD_BG, height=340)
        st.plotly_chart(fig, use_container_width=True)

    with tab_d:
        st.write("Uplift view separates true incremental revenue from cannibalized orders that would have happened without discounts.")
        cohorts = ["Full‑Price Loyalists", "Smart Shoppers", "Discount Addicts", "Deal Chasers"]
        uplift = [0.06, 0.14, 0.28, 0.40]
        cannibal = [0.72, 0.55, 0.40, 0.25]
        df_u = pd.DataFrame({"Segment": cohorts, "True Incremental Revenue %": uplift, "Cannibalized Revenue %": cannibal})
        fig = px.bar(df_u.melt(id_vars="Segment"), x="Segment", y="value", color="variable", barmode="group",
                     template="plotly_dark", color_discrete_sequence=["#4ade80", ACCENT])
        fig.update_layout(plot_bgcolor=CARD_BG, paper_bgcolor=CARD_BG, height=340, legend_title="")
        st.plotly_chart(fig, use_container_width=True)

    with tab_e:
        st.write("Use the sliders on the left to simulate revenue, margin, and risk impact of changing discount frequency and depth.")
        st.write("This view links promo policy directly to brand health and profitability.")

# ---------- Layer 4: Executive decision engine ----------
with layer4:
    st.markdown('<div class="section-title">Strategic Recommendation Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Translate diagnostics and predictions into an actionable discount playbook.</div>', unsafe_allow_html=True)

    df_strategy = pd.DataFrame({
        "Segment": [
            "High LTV + Low Discount (Full‑Price Loyalists)",
            "High LTV + High Discount (Smart Shoppers)",
            "Low LTV + High Discount (Discount Addicts)",
            "New Customers",
        ],
        "Recommended Discount Strategy": [
            "Protect premium. Minimal blanket discounts; focus on early access, exclusive launches, and loyalty tiers instead of price cuts.",
            "Gradually taper discount depth (‑5 to ‑10 pts) while adding non‑price benefits like samples, bundles, and experiences.",
            "Stop always‑on deals. Restrict to tightly targeted win‑back offers; push upsell to mid‑tier and private‑label brands.",
            "Use controlled onboarding offers (first‑order voucher, shipping perks) capped at 1‑2 events, then migrate to value‑based loyalty.",
        ],
        "Brand Risk Impact": [
            "Strengthens premium perception and raises Premium Brand Risk Index ceiling.",
            "Reduces conditioning while preserving top‑line.",
            "Prevents further margin leakage from low‑quality cohorts.",
            "Avoids creating a generation of discount‑addicted new users.",
        ],
    })

    st.dataframe(df_strategy, use_container_width=True, hide_index=True)

    st.markdown("---")

    st.markdown("""**Board‑Level Framing**  
"Discounting is not just a revenue lever; it is a customer conditioning tool. Our analysis indicates that beyond a certain frequency and depth, discounting reduces long‑term LTV and raises churn risk. A targeted, segment‑specific discount strategy can expand contribution margin while protecting Nykaa's premium brand perception.""")
