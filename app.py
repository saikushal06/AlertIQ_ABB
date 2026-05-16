import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=8000, key="live_refresh")

st.set_page_config(
    page_title="ALERTIQ | ABB Accelerator",
    page_icon="⚡",
    layout="wide"
)
# ---------------- SESSION STATE ----------------
if "emergency" not in st.session_state:
    st.session_state.emergency = False

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top left, #152033 0%, #070B12 38%, #05070B 100%);
    color: white;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #101827, #0B111C);
}

.hero {
    padding: 28px;
    border-radius: 24px;
    background: linear-gradient(135deg, rgba(239,68,68,0.22), rgba(37,99,235,0.18), rgba(17,24,39,0.95));
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 0 35px rgba(0,0,0,0.35);
    margin-bottom: 24px;
}

.hero-title {
    font-size: 48px;
    font-weight: 900;
    letter-spacing: 1px;
}

.hero-sub {
    font-size: 18px;
    color: #CBD5E1;
}

.card {
    padding: 22px;
    border-radius: 22px;
    background: linear-gradient(145deg, #111827, #0B1120);
    border: 1px solid rgba(148,163,184,0.2);
    box-shadow: 0 0 28px rgba(0,0,0,0.45);
}

.metric-title {
    color: #94A3B8;
    font-size: 14px;
}

.metric-value {
    color: white;
    font-size: 34px;
    font-weight: 900;
}

.safe-box {
    border-left: 7px solid #22C55E;
    box-shadow: 0 0 18px rgba(34,197,94,0.25);
}

.warning-box {
    border-left: 7px solid #F59E0B;
    box-shadow: 0 0 18px rgba(245,158,11,0.25);
}

.critical-box {
    border-left: 7px solid #EF4444;
    box-shadow: 0 0 22px rgba(239,68,68,0.45);
}

.safe-text { color: #22C55E; font-weight: 800; }
.warning-text { color: #F59E0B; font-weight: 800; }
.critical-text { color: #EF4444; font-weight: 800; }

.copilot {
    padding: 22px;
    border-radius: 22px;
    background: linear-gradient(135deg, rgba(239,68,68,0.25), rgba(15,23,42,0.96));
    border: 1px solid rgba(239,68,68,0.35);
    box-shadow: 0 0 30px rgba(239,68,68,0.22);
}

.factory-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
}

.factory-tile {
    padding: 22px;
    border-radius: 22px;
    background: #0B1120;
    border: 1px solid rgba(255,255,255,0.14);
    text-align: center;
    min-height: 145px;
}

.tile-title {
    font-size: 20px;
    font-weight: 800;
}

.tile-score {
    font-size: 34px;
    font-weight: 900;
}

.old-hmi {
    background: #1F2937;
    border: 1px dashed #EF4444;
    padding: 18px;
    border-radius: 18px;
}

.new-hmi {
    background: #052E16;
    border: 1px solid #22C55E;
    padding: 18px;
    border-radius: 18px;
}
            .live-indicator{
background:rgba(255,0,0,0.15);
border:1px solid #ff4444;
padding:10px 18px;
border-radius:14px;
display:inline-block;
font-weight:700;
color:#ff6666;
animation:pulse 1.2s infinite;
margin-top:10px;
}

@keyframes pulse{
0%{opacity:0.5;}
50%{opacity:1;}
100%{opacity:0.5;}
}
            .machine-card{
background:rgba(10,20,40,0.92);
padding:25px;
border-radius:22px;
margin-bottom:25px;
border-left:6px solid #22c55e;
box-shadow:0 0 25px rgba(34,197,94,0.15);
transition:all 0.35s ease;
animation:fadeUp 0.5s ease;
}

.machine-card:hover{
transform:translateY(-6px) scale(1.01);
box-shadow:0 0 35px rgba(59,130,246,0.35);
}

.warning-card{
border-left:6px solid #f59e0b;
box-shadow:0 0 25px rgba(245,158,11,0.22);
}

.critical-card{
border-left:6px solid #ef4444;
box-shadow:0 0 35px rgba(239,68,68,0.35);
animation:criticalPulse 1.2s infinite;
}

@keyframes criticalPulse{
0%{box-shadow:0 0 15px rgba(239,68,68,0.2);}
50%{box-shadow:0 0 40px rgba(239,68,68,0.7);}
100%{box-shadow:0 0 15px rgba(239,68,68,0.2);}
}

@keyframes fadeUp{
from{
opacity:0;
transform:translateY(20px);
}
to{
opacity:1;
transform:translateY(0px);
}
}
            .factory-card{
background:rgba(10,20,40,0.72);
backdrop-filter:blur(12px);
border:1px solid rgba(255,255,255,0.08);
border-radius:22px;
padding:24px;
transition:all 0.35s ease;
overflow:hidden;
position:relative;
}

.factory-card:hover{
transform:translateY(-6px) scale(1.02);
box-shadow:0 0 35px rgba(59,130,246,0.25);
}

.factory-card::before{
content:'';
position:absolute;
top:0;
left:-100%;
width:100%;
height:100%;
background:linear-gradient(
90deg,
transparent,
rgba(255,255,255,0.08),
transparent
);
transition:0.6s;
}

.factory-card:hover::before{
left:100%;
}
            .critical-banner{
margin-top:18px;
margin-bottom:22px;
padding:18px;
border-radius:18px;
background:linear-gradient(
90deg,
rgba(127,29,29,0.92),
rgba(239,68,68,0.18)
);
border:1px solid rgba(239,68,68,0.45);
font-size:20px;
font-weight:800;
color:#FECACA;
box-shadow:0 0 35px rgba(239,68,68,0.35);
animation:bannerPulse 1.2s infinite;
}

@keyframes bannerPulse{
0%{
transform:scale(1);
box-shadow:0 0 20px rgba(239,68,68,0.25);
}
50%{
transform:scale(1.01);
box-shadow:0 0 45px rgba(239,68,68,0.55);
}
100%{
transform:scale(1);
box-shadow:0 0 20px rgba(239,68,68,0.25);
}
}
</style>
""", unsafe_allow_html=True)

# ---------------- DATA ----------------
machines = ["Boiler Unit", "Conveyor Motor", "Cooling Pump", "Packaging Arm", "Compressor", "Power Panel"]

def create_data():
    data = []

    for machine in machines:
        temp = np.random.randint(35, 95)
        vibration = round(np.random.uniform(0.8, 6.8), 2)
        pressure = np.random.randint(25, 90)
        energy = np.random.randint(45, 145)

        if st.session_state.emergency and machine in ["Cooling Pump", "Compressor"]:
            temp = np.random.randint(96, 125)
            vibration = round(np.random.uniform(7.5, 10.5), 2)
            pressure = np.random.randint(88, 115)
            energy = np.random.randint(150, 195)

        risk = 0
        risk += 35 if temp > 90 else 18 if temp > 70 else 5
        risk += 30 if vibration > 7 else 15 if vibration > 4.8 else 4
        risk += 20 if pressure > 85 else 10 if pressure > 65 else 3
        risk += 15 if energy > 145 else 8 if energy > 105 else 2

        if risk >= 75:
            status = "Critical"
        elif risk >= 45:
            status = "Warning"
        else:
            status = "Safe"

        data.append({
            "Machine": machine,
            "Temperature": temp,
            "Vibration": vibration,
            "Pressure": pressure,
            "Energy": energy,
            "Risk Score": risk,
            "Status": status
        })

    return pd.DataFrame(data)

df = create_data()

# ---------------- AI LOGIC ----------------
def recommendation(row):
    issues = []

    if row["Temperature"] > 90:
        issues.append("overheating")
    if row["Vibration"] > 7:
        issues.append("abnormal vibration")
    if row["Pressure"] > 85:
        issues.append("pressure instability")
    if row["Energy"] > 145:
        issues.append("energy overload")

    if row["Status"] == "Critical":
        return f"Immediate action required. {row['Machine']} shows {', '.join(issues)}. Stop operation, isolate the unit, and schedule urgent maintenance."
    elif row["Status"] == "Warning":
        return f"{row['Machine']} shows early risk signals. Schedule preventive inspection and monitor trend changes."
    return f"{row['Machine']} is stable. Continue normal monitoring."

def copilot_message(df):
    top = df.sort_values("Risk Score", ascending=False).iloc[0]
    if top["Status"] == "Critical":
        return f"🚨 Focus first on {top['Machine']}. It is the highest-risk unit with risk score {top['Risk Score']}. ALERTIQ compressed multiple sensor alerts into one actionable incident."
    elif top["Status"] == "Warning":
        return f"⚠️ Preventive action recommended for {top['Machine']}. Risk score is {top['Risk Score']}. Early intervention can prevent downtime."
    return "✅ Factory state is stable. No urgent operator action required."

def status_class(status):
    return status.lower() + "-box"

def text_class(status):
    return status.lower() + "-text"

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙ Control Panel")
role = st.sidebar.selectbox("User Role", ["Operator", "Engineer", "Manager", "Demo Mode"])

if st.sidebar.button("🚨 Simulate Factory Emergency"):
    st.session_state.emergency = True

if st.sidebar.button("✅ Reset Factory"):
    st.session_state.emergency = False

st.sidebar.write("Time:", datetime.now().strftime("%H:%M:%S"))
st.sidebar.info("Prototype uses simulated industrial sensor data.")

# ---------------- HERO ----------------
st.markdown("""
<div class="hero">
    <div class="hero-title">⚡ ALERTIQ</div>
    <div class="hero-sub">
    Situation-Aware AI Copilot for Next-Generation Industrial HMI
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("""
<div class="live-indicator">
🔴 LIVE AI MONITORING ACTIVE
</div>
""", unsafe_allow_html=True)
# ---------------- METRICS ----------------
critical = len(df[df["Status"] == "Critical"])
warning = len(df[df["Status"] == "Warning"])
safe = len(df[df["Status"] == "Safe"])
avg_risk = round(df["Risk Score"].mean(), 1)
if critical > 0:
    st.markdown(f"""
    <div class="critical-banner">
    🚨 GLOBAL FACTORY ALERT:
    {critical} critical industrial incident(s) detected.
    Immediate operator intervention required.
    </div>
    """, unsafe_allow_html=True)


m1, m2, m3, m4 = st.columns(4)

for col, title, value in [
    (m1, "Machines Online", len(df)),
    (m2, "Critical Incidents", critical),
    (m3, "Warnings", warning),
    (m4, "Average Risk", avg_risk)
]:
    with col:
        st.markdown(f"""
        <div class="card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

st.write("")

# ---------------- COPILOT ----------------
st.markdown(f"""
<div class="copilot">
<h3>🤖 ALERTIQ Operator Copilot</h3>
<p>{copilot_message(df)}</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------------- DIGITAL TWIN ----------------
st.subheader("🏭 Digital Twin Factory View")

cols = st.columns(3)

for index, row in df.iterrows():
    status = row["Status"]

    if status == "Critical":
        emoji = "🔴"
        box_type = "error"
    elif status == "Warning":
        emoji = "🟡"
        box_type = "warning"
    else:
        emoji = "🟢"
        box_type = "success"

    with cols[index % 3]:
        if box_type == "error":
            st.error(
                f"""
                {emoji} **{row['Machine']}**

                Status: **{row['Status']}**

                Risk Score: **{row['Risk Score']}**
                """
            )
        elif box_type == "warning":
            st.warning(
                f"""
                {emoji} **{row['Machine']}**

                Status: **{row['Status']}**

                Risk Score: **{row['Risk Score']}**
                """
            )
        else:
            st.success(
                f"""
                {emoji} **{row['Machine']}**

                Status: **{row['Status']}**

                Risk Score: **{row['Risk Score']}**
                """
            )

            # ---------------- AI INCIDENT TIMELINE ----------------
st.subheader("🧠 AI Incident Timeline")

top_machine = df.sort_values("Risk Score", ascending=False).iloc[0]



if top_machine["Status"] == "Critical":
    st.error(f"""
    **AI Incident Detected: {top_machine['Machine']} Failure Risk**

    19:42:01 → Temperature spike detected  
    19:42:04 → Vibration anomaly correlated  
    19:42:07 → Pressure instability confirmed  
    19:42:10 → ALERTIQ compressed multiple alarms into one incident  
    19:42:13 → Operator action generated: Stop unit and inspect immediately
    """)

elif top_machine["Status"] == "Warning":
    st.warning(f"""
    **Early Risk Pattern Detected: {top_machine['Machine']}**

    19:42:01 → Minor sensor deviation detected  
    19:42:04 → Risk score increased  
    19:42:07 → Preventive inspection recommended  
    19:42:10 → Operator notified before failure occurs
    """)

else:
    st.success("""
    **No active incident detected**

    19:42:01 → Sensors normal  
    19:42:04 → No correlation risk found  
    19:42:07 → Factory state stable  
    19:42:10 → Continue normal monitoring
    """)

    # ---------------- PREDICTIVE MAINTENANCE ----------------
st.subheader("🔮 Predictive Maintenance Intelligence")

top_machine = df.sort_values("Risk Score", ascending=False).iloc[0]

failure_probability = min(98, int(top_machine["Risk Score"] + np.random.randint(5, 18)))
failure_eta = max(3, int(60 - top_machine["Risk Score"] * 0.45))

if top_machine["Status"] == "Critical":
    st.error(f"""
    **Machine at Highest Risk:** {top_machine['Machine']}

    **Failure Probability:** {failure_probability}%  
    **Estimated Time Before Failure:** {failure_eta} minutes  
    **AI Confidence:** 94%

    ALERTIQ predicts a high chance of operational failure if immediate action is not taken.
    """)
elif top_machine["Status"] == "Warning":
    st.warning(f"""
    **Machine Under Observation:** {top_machine['Machine']}

    **Failure Probability:** {failure_probability}%  
    **Estimated Risk Window:** {failure_eta} minutes  
    **AI Confidence:** 82%

    Preventive inspection is recommended before the condition becomes critical.
    """)
else:
    st.success(f"""
    **Factory Health Stable**

    **Failure Probability:** {failure_probability}%  
    **AI Confidence:** 76%

    No immediate maintenance risk detected.
    """)

    # ---------------- LIVE SENSOR GRAPH ----------------
st.subheader("📈 Live Sensor Monitoring")

selected_machine = st.selectbox(
    "Select Machine",
    df["Machine"].tolist()
)

live_data = pd.DataFrame({
    "Time": list(range(10)),
    "Temperature": np.random.randint(40, 120, 10),
    "Vibration": np.random.randint(1, 10, 10),
})

fig_live = px.line(
    live_data,
    x="Time",
    y=["Temperature", "Vibration"],
    markers=True,
    title=f"Realtime Sensor Activity - {selected_machine}"
)

fig_live.update_layout(
    paper_bgcolor="#050816",
    plot_bgcolor="#050816",
    font_color="white",
    title_font_size=22
)

st.plotly_chart(fig_live, width='stretch')
# ---------------- ROLE VIEWS ----------------
if role == "Operator":
    st.subheader("👷 Operator View - Action Priority")

    for _, row in df.sort_values("Risk Score", ascending=False).iterrows():
        st.markdown(f"""
        <div class="factory-card machine-card {row['Status'].lower()}-card">
            <h3>{row['Machine']}</h3>
            <p>Status: <span class="{text_class(row['Status'])}">{row['Status']}</span></p>
            <p>Risk Score: <b>{row['Risk Score']}</b></p>
            <p><b>AI Action:</b> {recommendation(row)}</p>
        </div>
        """, unsafe_allow_html=True)

elif role == "Engineer":
    st.subheader("🛠 Engineer View - Sensor Intelligence")

    st.dataframe(df, width='stretch')

    fig = px.bar(
        df,
        x="Machine",
        y="Risk Score",
        color="Status",
        title="AI Risk Score by Machine",
        text="Risk Score"
    )
    st.plotly_chart(fig, width='stretch')

    selected = st.selectbox("Deep Dive Machine", df["Machine"])
    row = df[df["Machine"] == selected].iloc[0]

    sensor_df = pd.DataFrame({
        "Sensor": ["Temperature", "Vibration", "Pressure", "Energy"],
        "Value": [row["Temperature"], row["Vibration"], row["Pressure"], row["Energy"]]
    })

    fig2 = px.line(
        sensor_df,
        x="Sensor",
        y="Value",
        markers=True,
        title=f"Sensor Signature - {selected}"
    )
    st.plotly_chart(fig2, width='stretch')

    st.info(recommendation(row))

elif role == "Manager":
    st.subheader("📊 Manager View - Executive Health")

    c1, c2 = st.columns(2)

    with c1:
        fig = px.pie(df, names="Status", title="Factory Health Distribution")
        st.plotly_chart(fig, width='stretch')

    with c2:
        st.write("### Business Impact")
        st.success("Reduced alarm noise using incident compression")
        st.info("Improves operator decision speed")
        st.warning("Supports predictive maintenance planning")

    st.write("### Top Risk Machines")
    st.dataframe(
        df.sort_values("Risk Score", ascending=False)[["Machine", "Status", "Risk Score"]],
        width='stretch'
    )

else:
    st.subheader("🎬 Demo Mode - Old HMI vs ALERTIQ")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="old-hmi">
        <h3>❌ Traditional HMI</h3>
        <p>ALARM 01: TEMP HIGH</p>
        <p>ALARM 02: VIBRATION HIGH</p>
        <p>ALARM 03: PRESSURE HIGH</p>
        <p>ALARM 04: ENERGY SPIKE</p>
        <p>Operator must manually understand priority.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        top = df.sort_values("Risk Score", ascending=False).iloc[0]
        st.markdown(f"""
        <div class="new-hmi">
        <h3>✅ ALERTIQ HMI</h3>
        <p><b>Incident Cluster:</b> {top['Machine']}</p>
        <p><b>Status:</b> {top['Status']}</p>
        <p><b>AI Action:</b> {recommendation(top)}</p>
        <p>Noise converted into one decision-ready insight.</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<br><center style="color:#94A3B8;">
ALERTIQ | ABB Accelerator 2026 | Theme: Next-gen Control System Interface
</center>
""", unsafe_allow_html=True)