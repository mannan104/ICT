import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt

st.set_page_config(page_title="ICT for Structural Safety", page_icon="🏗️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
html, body, [class*="css"] {font-family:'Poppins',sans-serif;}
.stApp{
background: radial-gradient(circle at top left,#00d4ff22,#0000 30%),
            radial-gradient(circle at bottom right,#00ffa322,#0000 30%),
            #0A192F;
}
.block-container {padding-top:1rem;}
.hero{
padding:30px;border-radius:24px;text-align:center;
background:linear-gradient(135deg,#00D4FF,#007CF0);
color:white;
}
.team{
padding:20px;border-radius:20px;
background:rgba(255,255,255,0.08);
border:1px solid rgba(255,255,255,0.15);
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>🏗️ ICT FOR STRUCTURAL SAFETY</h1>
<h3>Live Beam Deflection Visualizer</h3>
<p>Real-Time Structural Analysis Dashboard</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 👨‍💻 Project Team")
team = pd.DataFrame({
"Name":["Abdul Mannan","Muhammad Bin Akarma","Muneeb Azhar","Ahmed Ali","Hammad Fida"],
"Registration No":["25-ME-55","25-ME-59","25-ME-03","25-ME-115","25-ME-27"]
})
st.dataframe(team, use_container_width=True)

st.sidebar.header("Beam Parameters")
materials = {"Steel":200e9,"Aluminum":69e9,"Concrete":30e9,"Wood":12e9}
material = st.sidebar.selectbox("Material", list(materials))
E = materials[material]
L = st.sidebar.slider("Beam Length (m)",1.0,20.0,10.0)
P = st.sidebar.slider("Point Load (N)",100,10000,3000)
I = st.sidebar.slider("Moment of Inertia (m⁴)",0.000001,0.01,0.0005)

delta = (P*L**3)/(48*E*I)
allowable = L/360

c1,c2,c3,c4 = st.columns(4)
c1.metric("Length", f"{L:.2f} m")
c2.metric("Load", f"{P} N")
c3.metric("Material", material)
c4.metric("Deflection", f"{delta:.6f} m")

status = "SAFE" if delta <= allowable else "CRITICAL"
st.success("✅ SAFE") if status=="SAFE" else st.error("❌ CRITICAL")

gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=delta*1000,
    title={"text":"Deflection (mm)"},
    gauge={"axis":{"range":[0,max(1,allowable*1000)]}}
))
st.plotly_chart(gauge, use_container_width=True)

col1,col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(6,2))
    ax.plot([0,L],[0,0], lw=8)
    ax.scatter([0,L],[0,0], s=200)
    ax.arrow(L/2,0.5,0,-0.4, head_width=0.3, head_length=0.1)
    ax.axis("off")
    ax.set_title("Beam Model")
    st.pyplot(fig)

with col2:
    x = np.linspace(0,L,300)
    y = -delta*np.sin(np.pi*x/L)
    fig2, ax2 = plt.subplots(figsize=(6,3))
    ax2.plot(x,y,lw=3)
    ax2.fill_between(x,y,0,alpha=0.3)
    ax2.grid(True)
    ax2.set_title("Deflection Curve")
    st.pyplot(fig2)

st.latex(r"\delta = \frac{PL^3}{48EI}")

results = pd.DataFrame({
    "Parameter":["Material","Length","Load","Deflection","Allowable","Status"],
    "Value":[material,L,P,delta,allowable,status]
})
st.dataframe(results, use_container_width=True)

st.download_button(
    "Download Report CSV",
    results.to_csv(index=False),
    "beam_report.csv",
    "text/csv"
)

st.progress(min(int((delta/max(allowable,1e-9))*100),100))

st.markdown("---")
st.markdown("### Features")
st.markdown("""
- Real-Time Beam Deflection Analysis
- Material Database
- Safety Monitoring
- Interactive Dashboard
- Downloadable Report
- Structural Visualization
""")
