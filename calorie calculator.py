import streamlit as st

st.set_page_config(
    page_title="CalorieWise | Calorie Calculator",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at 8% 5%, rgba(16, 185, 129, 0.10), transparent 24%),
                radial-gradient(circle at 95% 10%, rgba(59, 130, 246, 0.09), transparent 24%),
                linear-gradient(180deg, #f8fbff 0%, #f4f8f7 100%);
            color: #172033;
        }

        .block-container {
            max-width: 1100px;
            padding-top: 2.2rem;
            padding-bottom: 3rem;
        }

        .hero {
            background: linear-gradient(135deg, #ffffff 0%, #eefbf6 100%);
            border: 1px solid rgba(16, 185, 129, 0.16);
            border-radius: 28px;
            padding: 32px;
            margin-bottom: 24px;
            box-shadow: 0 14px 40px rgba(15, 23, 42, 0.07);
        }

        .hero-kicker {
            color: #0f9f72;
            font-weight: 800;
            font-size: 14px;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        .hero h1 {
            margin: 0;
            font-size: 48px;
            line-height: 1.05;
            color: #102033;
            font-weight: 900;
        }

        .hero p {
            margin: 12px 0 0 0;
            color: #536174;
            font-size: 17px;
            line-height: 1.6;
            max-width: 780px;
        }

        .card {
            background: rgba(255, 255, 255, 0.92);
            border: 1px solid rgba(15, 23, 42, 0.08);
            border-radius: 22px;
            padding: 24px;
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.055);
            margin-bottom: 18px;
        }

        .card-title {
            font-size: 21px;
            font-weight: 850;
            color: #162235;
            margin-bottom: 4px;
        }

        .card-subtitle {
            color: #6a7688;
            font-size: 14px;
            margin-bottom: 18px;
        }

        .result-card {
            background: linear-gradient(145deg, #0f9f72 0%, #0b7d5a 100%);
            color: white;
            border-radius: 24px;
            padding: 28px;
            box-shadow: 0 16px 36px rgba(15, 159, 114, 0.23);
            margin-top: 8px;
        }

        .result-label {
            color: rgba(255,255,255,0.78);
            font-size: 14px;
            font-weight: 700;
        }

        .result-number {
            font-size: 42px;
            font-weight: 900;
            line-height: 1.05;
            margin: 5px 0 4px 0;
        }

        .result-caption {
            color: rgba(255,255,255,0.88);
            font-size: 14px;
        }

        .info-pill {
            display: inline-block;
            padding: 7px 11px;
            border-radius: 999px;
            background: #e9f9f3;
            color: #0d8c66;
            font-weight: 800;
            font-size: 12px;
            margin-right: 6px;
            margin-bottom: 6px;
        }

        .interpretation {
            background: #f8fafc;
            border-left: 4px solid #0f9f72;
            border-radius: 14px;
            padding: 16px 18px;
            color: #445066;
            line-height: 1.65;
            margin-top: 16px;
        }

        .footer-note {
            color: #778398;
            font-size: 12px;
            text-align: center;
            margin-top: 18px;
        }

        div[data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid rgba(15, 23, 42, 0.07);
            border-radius: 18px;
            padding: 16px;
        }

        .stButton > button {
            border-radius: 14px !important;
            min-height: 48px !important;
            font-weight: 800 !important;
        }

        @media (max-width: 768px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
            .hero {
                padding: 24px;
                border-radius: 22px;
            }
            .hero h1 {
                font-size: 34px;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Helper functions
# -----------------------------
def calculate_bmr(sex: str, weight_kg: float, height_cm: float, age: int) -> float:
    """Mifflin-St Jeor BMR estimate."""
    if sex == "Male":
        return (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    return (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161


ACTIVITY_LEVELS = {
    "Sedentary — little exercise": 1.20,
    "Lightly active — 1–3 days/week": 1.375,
    "Moderately active — 3–5 days/week": 1.55,
    "Very active — 6–7 days/week": 1.725,
    "Extra active — intense training/physical job": 1.90,
}

GOALS = {
    "Maintain weight": 0,
    "Gentle fat loss": -300,
    "Gentle weight gain": 300,
}


def interpretation_text(goal: str, maintenance: float) -> str:
    target = max(maintenance + GOALS[goal], 0)

    if goal == "Maintain weight":
        return (
            f"Your estimated maintenance intake is about **{maintenance:,.0f} kcal/day**. "
            "Eating around this level may help maintain your current weight, although real-world needs vary."
        )

    if goal == "Gentle fat loss":
        return (
            f"A gentle starting target could be around **{target:,.0f} kcal/day**, "
            "using a modest adjustment from your estimated maintenance. "
            "Track how you feel and how your weight changes over time rather than relying on one calculation."
        )

    return (
        f"A gentle starting target could be around **{target:,.0f} kcal/day**, "
        "using a modest adjustment from your estimated maintenance. "
        "Progress depends on food quality, training, sleep, and individual factors."
    )


# -----------------------------
# Header
# -----------------------------
st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">🥗 Simple nutrition tool</div>
        <h1>CalorieWise</h1>
        <p>
            Estimate your daily calorie requirement using a few basic personal and
            activity details. The result is an educational estimate—not a diagnosis.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Input section
# -----------------------------
left, right = st.columns([1.15, 0.85], gap="large")

with left:
    st.markdown(
        """
        <div class="card">
            <div class="card-title">👤 Your details</div>
            <div class="card-subtitle">Enter your information below.</div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)

    with c1:
        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=25,
            step=1,
            help="For adults 18 and above.",
        )

        height = st.number_input(
            "Height (cm)",
            min_value=100.0,
            max_value=230.0,
            value=165.0,
            step=0.5,
        )

    with c2:
        sex = st.selectbox("Sex", ["Female", "Male"])

        weight = st.number_input(
            "Weight (kg)",
            min_value=25.0,
            max_value=300.0,
            value=60.0,
            step=0.5,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="card">
            <div class="card-title">🏃 Activity & goal</div>
            <div class="card-subtitle">Choose the options that best match your routine.</div>
        """,
        unsafe_allow_html=True,
    )

    activity = st.selectbox("Activity level", list(ACTIVITY_LEVELS.keys()))

    goal = st.radio(
        "Your goal",
        list(GOALS.keys()),
        horizontal=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    calculate = st.button(
        "✨ Calculate My Calories",
        type="primary",
        use_container_width=True,
    )

with right:
    st.markdown(
        """
        <div class="card">
            <div class="card-title">💡 How it works</div>
            <div class="card-subtitle">A simple 2-step estimate.</div>
            <span class="info-pill">1. BMR</span>
            <span class="info-pill">2. Activity adjustment</span>
            <p style="color:#596579; line-height:1.7; margin-top:12px;">
                We first estimate your Basal Metabolic Rate (BMR), then multiply it
                by an activity factor to estimate your Total Daily Energy Expenditure (TDEE).
            </p>
            <div style="background:#f8fafc; padding:14px; border-radius:14px; color:#5d6a7d; line-height:1.55;">
                <b>Tip:</b> Use the result as a starting point. Your actual calorie
                needs can differ because of body composition, health, training, and other factors.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="card">
            <div class="card-title">🔒 Simple by design</div>
            <div class="card-subtitle">No database. No account. No complicated setup.</div>
            <p style="color:#596579; line-height:1.7; margin-bottom:0;">
                This project uses only Python variables, dictionaries, functions,
                Streamlit components, and session-free calculations.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------
# Results
# -----------------------------
if calculate:
    bmr = calculate_bmr(sex, weight, height, age)
    maintenance = bmr * ACTIVITY_LEVELS[activity]
    target = max(maintenance + GOALS[goal], 0)

    st.markdown(
        """
        <div class="card-title" style="margin-top:22px; margin-bottom:10px;">
            📊 Your result
        </div>
        """,
        unsafe_allow_html=True,
    )

    r1, r2, r3 = st.columns(3)

    with r1:
        st.metric("🔥 BMR", f"{bmr:,.0f} kcal/day")

    with r2:
        st.metric("⚡ Maintenance", f"{maintenance:,.0f} kcal/day")

    with r3:
        st.metric("🎯 Goal estimate", f"{target:,.0f} kcal/day")

    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-label">YOUR ESTIMATED DAILY TARGET</div>
            <div class="result-number">{target:,.0f} kcal</div>
            <div class="result-caption">
                Based on your selected goal: <b>{goal}</b>
            </div>
            <div class="interpretation">
                {interpretation_text(goal, maintenance)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("📌 See your calculation details"):
        st.write(f"**Age:** {age} years")
        st.write(f"**Sex:** {sex}")
        st.write(f"**Height:** {height:.1f} cm")
        st.write(f"**Weight:** {weight:.1f} kg")
        st.write(f"**Activity:** {activity}")
        st.write(f"**Goal:** {goal}")
        st.write(f"**Activity factor:** {ACTIVITY_LEVELS[activity]:.3f}")

    st.info(
        "This calculator provides a general estimate for educational purposes. "
        "It is not medical advice and should not replace guidance from a qualified "
        "doctor or registered dietitian, especially for pregnancy, eating disorders, "
        "chronic illness, or other special health needs."
    )

else:
    st.markdown(
        """
        <div class="card" style="text-align:center; padding:36px; margin-top:22px;">
            <div style="font-size:42px;">🥗</div>
            <div class="card-title">Ready to calculate?</div>
            <div style="color:#69758a; line-height:1.6;">
                Fill in your details and click <b>Calculate My Calories</b>
                to see your estimated daily calorie requirement.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="footer-note">
        CalorieWise • Python + Streamlit • No database required
    </div>
    """,
    unsafe_allow_html=True,
)
