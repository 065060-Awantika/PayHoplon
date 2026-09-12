import streamlit as st
import pandas as pd
import plotly.express as px
import random
import uuid
import textwrap
from datetime import datetime, timedelta

# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="PayHoplon",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# HELPER FOR HTML
# =============================================================================

def render_html(html):
    st.markdown(
        textwrap.dedent(html),
        unsafe_allow_html=True
    )

# =============================================================================
# DARK PROFESSIONAL THEME
# =============================================================================

render_html("""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);

/* ============================================================
   COLORS
   ============================================================ */

:root {
    --bg: #071014;
    --bg-dark: #050D10;
    --panel: #101C22;
    --panel-2: #14242A;
    --border: #263B42;
    --text: #F1F7F5;
    --muted: #8EA4A6;

    --green: #2DD4A8;
    --green-dark: #159C7E;

    --amber: #F2B84B;
    --red: #F06A73;
    --purple: #9B8AFB;
}

/* ============================================================
   GLOBAL
   ============================================================ */

html,
body,
.stApp,
[class*="css"],
.stMarkdown,
.stText,
p,
span,
label,
button,
input,
textarea,
select,
div {
    font-family: 'Inter',
    sans-serif !important;
}

.stApp {
    background:
        radial-gradient(
            circle at 78% 4%,
            rgba(45,212,168,.10),
            transparent 28%
        ),
        radial-gradient(
            circle at 30% 40%,
            rgba(25,100,90,.07),
            transparent 35%
        ),
        #071014 !important;

    color: #F1F7F5 !important;
}

.block-container {
    max-width: 1450px !important;
    padding: 1.3rem 2rem 3rem !important;
}

/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #09171B 0%,
            #061114 100%
        ) !important;

    border-right: 1px solid #1D3339 !important;
}

section[data-testid="stSidebar"] > div {
    background: transparent !important;
}

section[data-testid="stSidebar"] * {
    color: #DDE9E6 !important;
}

section[data-testid="stSidebar"] input {
    background: #111E23 !important;
    color: #F1F7F5 !important;
    border: 1px solid #2A4047 !important;
}

section[data-testid="stSidebar"]
[data-baseweb="select"] > div {
    background: #111E23 !important;
    border-color: #2A4047 !important;
}

section[data-testid="stSidebar"]
[data-baseweb="select"] span {
    color: #E4EFEC !important;
}

section[data-testid="stSidebar"]
.stNumberInput button {
    background: #17272D !important;
    color: #DCE9E5 !important;
    border-color: #2A4047 !important;
}

section[data-testid="stSidebar"]
.stSlider [role="slider"] {
    background: #2DD4A8 !important;
}

.sidebar-brand {
    padding: 5px 2px 24px;
}

.brand-row {
    display: flex;
    align-items: center;
    gap: 12px;
}

.shield {
    width: 46px;
    height: 46px;
    border-radius: 14px;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 23px;

    background:
        linear-gradient(
            145deg,
            #16483D,
            #0A2925
        );

    border: 1px solid #267C68;

    box-shadow:
        0 0 25px rgba(45,212,168,.12);
}

.brand-name {
    font-size: 1.4rem;
    font-weight: 800;
    color: #F4FAF8 !important;
    letter-spacing: -.03em;
}

.brand-sub {
    font-size: .64rem;
    color: #6F888A !important;
    margin-top: 2px;
    letter-spacing: .04em;
}

.sidebar-section {
    color: #6F8588 !important;
    font-size: .70rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .08em;
    margin: 20px 0 10px;
}

.guardrail-note {
    margin-top: 20px;
    padding: 15px;

    border: 1px solid #20383B;
    border-radius: 14px;

    background:
        linear-gradient(
            135deg,
            rgba(45,212,168,.08),
            rgba(17,29,34,.7)
        );

    color: #91A8A9 !important;
    font-size: .74rem;
    line-height: 1.5;
}

/* ============================================================
   TOP BAR
   ============================================================ */

.topbar {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    margin-bottom: 8px;
}

.user-pill {
    display: flex;
    align-items: center;
    gap: 8px;

    padding: 7px 11px;

    border-radius: 999px;

    background: #101D22;

    border: 1px solid #263A40;

    color: #A8B9B9 !important;

    font-size: .75rem;
}

.user-dot {
    width: 25px;
    height: 25px;
    border-radius: 50%;

    display: flex;
    align-items: center;
    justify-content: center;

    background: #1C8069;

    color: white !important;
    font-weight: 700;
}

/* ============================================================
   HERO
   ============================================================ */

.hero {
    position: relative;
    overflow: hidden;

    padding: 28px 30px;

    border-radius: 20px;

    border: 1px solid #1F383D;

    background:
        radial-gradient(
            circle at 82% 0%,
            rgba(45,212,168,.12),
            transparent 28%
        ),
        linear-gradient(
            135deg,
            #0D1C21,
            #081419
        );

    box-shadow:
        0 15px 45px rgba(0,0,0,.20);

    margin-bottom: 20px;
}

.hero-kicker {
    color: #6FA99E !important;
    font-size: .76rem;
    font-weight: 600;
    letter-spacing: .05em;
    margin-bottom: 6px;
}

.hero-title {
    font-size: 2.5rem;
    line-height: 1;
    font-weight: 800;
    letter-spacing: -.05em;
    color: #F4FAF8 !important;
}

.hero-title .accent {
    color: #2DD4A8 !important;
}

.hero-sub {
    max-width: 720px;
    color: #94A9AA !important;
    font-size: .92rem;
    line-height: 1.55;
    margin-top: 12px;
}

.hero-right {
    position: absolute;
    right: 34px;
    top: 32px;

    width: 220px;

    border-left: 2px solid #2DD4A8;

    padding-left: 18px;
}

.hero-right b {
    color: #E5F0ED !important;
    font-size: .85rem;
}

.hero-right span {
    color: #2DD4A8 !important;
    font-size: .82rem;
    font-weight: 700;
}

/* ============================================================
   KPI CARDS
   ============================================================ */

.kpi {
    position: relative;

    min-height: 108px;

    padding: 18px;

    border-radius: 16px;

    border: 1px solid #263B42;

    background:
        linear-gradient(
            145deg,
            #122027,
            #0D191F
        );

    box-shadow:
        0 7px 25px rgba(0,0,0,.16);

    overflow: hidden;
}

.kpi.green {
    border-color: rgba(45,212,168,.42);
}

.kpi.amber {
    border-color: rgba(242,184,75,.38);
}

.kpi.purple {
    border-color: rgba(155,138,251,.38);
}

.kpi-label {
    color: #8EA3A5 !important;
    font-size: .69rem;
    font-weight: 700;
    margin-bottom: 8px;
}

.kpi-value {
    color: #F3F8F6 !important;
    font-size: 1.65rem;
    font-weight: 800;
    letter-spacing: -.03em;
}

.kpi-delta {
    color: #6DA89B !important;
    font-size: .67rem;
    margin-top: 6px;
}

.kpi-icon {
    position: absolute;

    right: 17px;
    top: 16px;

    width: 36px;
    height: 36px;

    border-radius: 50%;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 17px;
}

.icon-green {
    background: rgba(45,212,168,.12);
    color: #2DD4A8 !important;
}

.icon-amber {
    background: rgba(242,184,75,.12);
    color: #F2B84B !important;
}

.icon-purple {
    background: rgba(155,138,251,.12);
    color: #9B8AFB !important;
}

.icon-slate {
    background: rgba(145,165,167,.10);
    color: #B7C5C6 !important;
}

/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {
    min-height: 43px !important;

    border-radius: 11px !important;

    font-weight: 700 !important;

    background: #17272D !important;

    color: #DCE9E5 !important;

    border: 1px solid #2A4148 !important;

    box-shadow: none !important;
}

.stButton > button:hover {
    border-color: #2DD4A8 !important;
    color: #2DD4A8 !important;
    background: #142D2B !important;
}

button[kind="primary"] {
    background:
        linear-gradient(
            135deg,
            #2DD4A8,
            #159C7E
        ) !important;

    color: #03120E !important;

    border: none !important;

    box-shadow:
        0 5px 20px rgba(45,212,168,.18) !important;
}

button[kind="primary"]:hover {
    background:
        linear-gradient(
            135deg,
            #42DFB7,
            #20B18F
        ) !important;

    color: #02100C !important;
}

/* ============================================================
   TABS
   ============================================================ */

div[data-baseweb="tab-list"] {
    gap: 4px !important;
    background: transparent !important;
    border-bottom: 1px solid #21363C !important;
}

button[data-baseweb="tab"] {
    color: #7E9597 !important;
    font-weight: 700 !important;
    background: transparent !important;
    padding: 12px 16px !important;
}

button[data-baseweb="tab"]:hover {
    color: #C0CFCD !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #2DD4A8 !important;
}

div[data-baseweb="tab-highlight"] {
    background: #2DD4A8 !important;
    height: 3px !important;
}

/* ============================================================
   PANELS
   ============================================================ */

.panel {
    border: 1px solid #263B42;

    border-radius: 16px;

    background:
        linear-gradient(
            145deg,
            #101D23,
            #0D181E
        );

    padding: 18px;
}

.panel-title {
    color: #EAF3F0 !important;
    font-weight: 800;
    font-size: 1rem;
}

.panel-sub {
    color: #7E9698 !important;
    font-size: .75rem;
    margin-top: 3px;
}

/* ============================================================
   EXPANDERS
   ============================================================ */

div[data-testid="stExpander"] {
    background: #101C22 !important;
    border: 1px solid #263B42 !important;
    border-radius: 13px !important;
    margin-bottom: 8px !important;
}

div[data-testid="stExpander"] summary,
div[data-testid="stExpander"] summary span,
div[data-testid="stExpander"] p {
    color: #DDE9E6 !important;
}

/* ============================================================
   ALERTS
   ============================================================ */

div[data-testid="stAlert"] {
    background: #102229 !important;
    color: #AFC3C2 !important;
    border: 1px solid #28424A !important;
    border-radius: 12px !important;
}

div[data-testid="stAlert"] p,
div[data-testid="stAlert"] span {
    color: #AFC3C2 !important;
}

/* ============================================================
   DATAFRAME
   ============================================================ */

div[data-testid="stDataFrame"] {
    border: 1px solid #263B42 !important;
    border-radius: 12px !important;
    overflow: hidden;
}

/* ============================================================
   CAPTIONS / TEXT
   ============================================================ */

.stMarkdown p,
.stMarkdown li {
    color: #B5C5C5;
}

[data-testid="stCaptionContainer"] p {
    color: #748C8F !important;
}

hr {
    border-color: #20343A !important;
}

/* ============================================================
   HIDE STREAMLIT CHROME
   ============================================================ */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 900px) {

    .hero-right {
        display: none;
    }

    .hero-title {
        font-size: 1.9rem;
    }

    .block-container {
        padding: 1rem !important;
    }

}

</style>
""")

# =============================================================================
# VENDORS
# =============================================================================

def seed_vendors():

    return [

        {
            "vendor": "Sundar Steel Traders",
            "upi_id": "sundarsteel@upi",
            "verified": True,
            "category": "Raw Material"
        },

        {
            "vendor": "Ganga Logistics",
            "upi_id": "gangalog@upi",
            "verified": True,
            "category": "Logistics"
        },

        {
            "vendor": "Nova Packaging Co.",
            "upi_id": "novapack@upi",
            "verified": True,
            "category": "Packaging"
        },

        {
            "vendor": "QuickFix Electricals",
            "upi_id": "quickfixelec@upi",
            "verified": True,
            "category": "Maintenance"
        },

        {
            "vendor": "Shadow Enterprises",
            "upi_id": "shadowent@upi",
            "verified": False,
            "category": "Unknown"
        },

        {
            "vendor": "Raghav Textiles",
            "upi_id": "raghavtex@upi",
            "verified": True,
            "category": "Raw Material"
        }

    ]


# =============================================================================
# SESSION STATE
# =============================================================================

if "vendors" not in st.session_state:

    st.session_state.vendors = seed_vendors()


if "invoices" not in st.session_state:

    st.session_state.invoices = []


if "ledger" not in st.session_state:

    st.session_state.ledger = []


if "guardrails" not in st.session_state:

    st.session_state.guardrails = {

        "budget_cap": 50000,

        "auto_approve_ceiling": 20000,

        "blacklist": [
            "Shadow Enterprises"
        ],

        "duplicate_window_days": 7

    }


MANUAL_MINUTES_PER_INVOICE = 8

VENDOR_NAMES = [
    v["vendor"]
    for v in st.session_state.vendors
]


# =============================================================================
# GENERATE INVOICE
# =============================================================================

def generate_invoice():

    vendor = random.choice(
        st.session_state.vendors
    )

    amount = random.choice([

        random.randint(2000, 18000),

        random.randint(2000, 18000),

        random.randint(20000, 45000),

        random.randint(55000, 90000)

    ])


    # 15% duplicate chance

    duplicate_test = (

        random.random() < 0.15

        and len(st.session_state.invoices) > 0

    )


    if duplicate_test:

        previous = random.choice(
            st.session_state.invoices[-5:]
        )

        vendor = next(

            v
            for v in st.session_state.vendors

            if v["vendor"] == previous["vendor"]

        )

        amount = previous["amount"]


    return {

        "invoice_id":
            f"INV-{uuid.uuid4().hex[:6].upper()}",

        "vendor":
            vendor["vendor"],

        "upi_id":
            vendor["upi_id"],

        "verified_vendor":
            vendor["verified"],

        "amount":
            amount,

        "date":
            datetime.now()
            - timedelta(
                minutes=random.randint(0, 120)
            )

    }


# =============================================================================
# UPI TRANSACTION MATCH
# =============================================================================

def find_matching_upi_txn(invoice):

    # Simulate 90% UPI match success

    if random.random() < 0.90:

        txn = {

            "txn_id":
                f"UPI-{uuid.uuid4().hex[:8].upper()}",

            "amount":
                invoice["amount"],

            "upi_id":
                invoice["upi_id"],

            "status":
                "ready"

        }

        st.session_state.ledger.append(txn)

        return txn


    return None


# =============================================================================
# RULE ENGINE
# =============================================================================

def run_rule_engine(invoice):

    g = st.session_state.guardrails

    reasons = []

    passed = True


    # ---------------------------------------------------------
    # 1. Vendor verification
    # ---------------------------------------------------------

    if not invoice["verified_vendor"]:

        passed = False

        reasons.append(
            "Vendor not on verified list"
        )


    # ---------------------------------------------------------
    # 2. Blacklist check
    # ---------------------------------------------------------

    if invoice["vendor"] in g["blacklist"]:

        passed = False

        reasons.append(

            f"Vendor '{invoice['vendor']}' "
            f"is blacklisted"

        )


    # ---------------------------------------------------------
    # 3. Budget cap
    # ---------------------------------------------------------

    if invoice["amount"] > g["budget_cap"]:

        passed = False

        reasons.append(

            f"Amount ₹{invoice['amount']:,} "
            f"exceeds budget cap "
            f"₹{g['budget_cap']:,}"

        )


    # ---------------------------------------------------------
    # 4. Duplicate detection
    # ---------------------------------------------------------

    cutoff = (

        invoice["date"]

        - timedelta(
            days=g["duplicate_window_days"]
        )

    )


    for past in st.session_state.invoices:

        if (

            past["vendor"]
            == invoice["vendor"]

            and past["amount"]
            == invoice["amount"]

            and past["date"] >= cutoff

            and past["decision"]
            in (

                "Auto-Approved & Released",

                "Manually Approved"

            )

        ):

            passed = False

            reasons.append(

                f"Possible duplicate of "
                f"{past['invoice_id']} "
                f"(same vendor + amount)"

            )

            break


    # ---------------------------------------------------------
    # 5. UPI ledger match
    # ---------------------------------------------------------

    matched_txn = find_matching_upi_txn(
        invoice
    )


    if matched_txn is None:

        passed = False

        reasons.append(

            "No matching UPI transaction "
            "found in ledger"

        )


    # ---------------------------------------------------------
    # 6. Autonomy ceiling
    # ---------------------------------------------------------

    autonomous = (

        passed

        and invoice["amount"]
        <= g["auto_approve_ceiling"]

    )


    if passed and not autonomous:

        reasons.append(

            f"Passed all checks but above "
            f"auto-approve ceiling "
            f"(₹{g['auto_approve_ceiling']:,}) "
            f"— routed for quick sign-off"

        )


    # ---------------------------------------------------------
    # FINAL DECISION
    # ---------------------------------------------------------

    if passed and autonomous:

        decision = (
            "Auto-Approved & Released"
        )

    elif passed and not autonomous:

        decision = (
            "Cleared — Awaiting Sign-off"
        )

    else:

        decision = (
            "Flagged for Review"
        )


    return (
        decision,
        reasons,
        matched_txn
    )


# =============================================================================
# INGEST
# =============================================================================

def ingest_and_process():

    invoice = generate_invoice()

    decision, reasons, txn = (
        run_rule_engine(invoice)
    )

    invoice["decision"] = decision

    invoice["reasons"] = reasons

    invoice["txn_id"] = (

        txn["txn_id"]

        if txn

        else None

    )

    st.session_state.invoices.append(
        invoice
    )


def batch_ingest(n):

    for _ in range(n):

        ingest_and_process()


# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:

    render_html("""

    <div class="sidebar-brand">

        <div class="brand-row">

            <div class="shield">
                🛡️
            </div>

            <div>

                <div class="brand-name">
                    PayHoplon
                </div>

                <div class="brand-sub">
                    GUARDRAILS FOR SMARTER PAYMENTS
                </div>

            </div>

        </div>

    </div>

    """)


    render_html("""

    <div class="sidebar-section">
        Simulation Controls
    </div>

    """)


    g = st.session_state.guardrails


    g["budget_cap"] = st.number_input(

        "Budget Cap per Invoice (₹)",

        min_value=5000,

        max_value=200000,

        value=g["budget_cap"],

        step=5000

    )


    g["auto_approve_ceiling"] = (
        st.number_input(

            "Fully Autonomous Ceiling (₹)",

            min_value=1000,

            max_value=g["budget_cap"],

            value=min(
                g["auto_approve_ceiling"],
                g["budget_cap"]
            ),

            step=1000

        )
    )


    g["blacklist"] = st.multiselect(

        "Blacklist Vendors",

        VENDOR_NAMES,

        default=g["blacklist"]

    )


    g["duplicate_window_days"] = (
        st.slider(

            "Duplicate Check Window (Days)",

            1,

            30,

            g["duplicate_window_days"]

        )
    )


    render_html("""

    <div class="guardrail-note">

        💡

        <b style="color:#DCE8E5 !important;">
            Set once.
        </b>

        <br>

        The agent operates inside these
        limits — no exceptions or manual
        overrides unless you change
        the guardrails here.

    </div>

    """)


    st.markdown("<br>", unsafe_allow_html=True)


    if st.button(
        "↻  Reset Simulation",
        use_container_width=True
    ):

        st.session_state.invoices = []

        st.session_state.ledger = []

        st.rerun()


# =============================================================================
# TOP BAR
# =============================================================================

render_html("""

<div class="topbar">

    <div class="user-pill">

        <span class="user-dot">
            A
        </span>

        Awantika&nbsp;⌄

    </div>

</div>

""")


# =============================================================================
# HERO
# =============================================================================

render_html("""

<div class="hero">

    <div class="hero-kicker">
        WELCOME TO
    </div>

    <div class="hero-title">
        Pay<span class="accent">Hoplon</span>
    </div>

    <div class="hero-sub">

        Autonomous invoice reconciliation
        &amp; UPI payment release, operating
        safely inside the guardrails you
        control.

    </div>

    <div class="hero-right">

        <b>
            Automate.<br>
            Protect.
        </b>

        <br>

        <span>
            Pay with Confidence.
        </span>

    </div>

</div>

""")


# =============================================================================
# CALCULATE KPIs
# =============================================================================

df = pd.DataFrame(
    st.session_state.invoices
)

total = len(df)


auto = (

    (
        df["decision"]
        == "Auto-Approved & Released"
    ).sum()

    if total

    else 0

)


cleared = (

    (
        df["decision"]
        == "Cleared — Awaiting Sign-off"
    ).sum()

    if total

    else 0

)


flagged = (

    (
        df["decision"]
        == "Flagged for Review"
    ).sum()

    if total

    else 0

)


released_amt = (

    df.loc[
        df["decision"]
        == "Auto-Approved & Released",
        "amount"
    ].sum()

    if total

    else 0

)


processed_amt = (

    df["amount"].sum()

    if total

    else 0

)


minutes_saved = (
    auto
    * MANUAL_MINUTES_PER_INVOICE
)

hours_saved = (
    minutes_saved / 60
)


# =============================================================================
# KPI ROW
# =============================================================================

k1, k2, k3, k4, k5 = st.columns(5)


with k1:

    render_html(f"""

    <div class="kpi green">

        <div class="kpi-icon icon-green">
            ▣
        </div>

        <div class="kpi-label">
            INVOICES PROCESSED
        </div>

        <div class="kpi-value">
            {total}
        </div>

        <div class="kpi-delta">
            ↑ +0% vs last run
        </div>

    </div>

    """)


with k2:

    percentage = (
        f"{auto / total * 100:.0f}%"
        if total
        else "0%"
    )

    render_html(f"""

    <div class="kpi green">

        <div class="kpi-icon icon-green">
            ✓
        </div>

        <div class="kpi-label">
            AUTONOMOUSLY RELEASED
        </div>

        <div class="kpi-value">
            {auto}
        </div>

        <div class="kpi-delta">
            ↑ {percentage} of total
        </div>

    </div>

    """)


with k3:

    percentage = (
        f"{flagged / total * 100:.0f}%"
        if total
        else "0%"
    )

    render_html(f"""

    <div class="kpi amber">

        <div class="kpi-icon icon-amber">
            !
        </div>

        <div class="kpi-label">
            FLAGGED FOR REVIEW
        </div>

        <div class="kpi-value">
            {flagged}
        </div>

        <div
            class="kpi-delta"
            style="color:#D5A64B !important;"
        >
            ↑ {percentage} of total
        </div>

    </div>

    """)


with k4:

    render_html(f"""

    <div class="kpi purple">

        <div class="kpi-icon icon-purple">
            ₹
        </div>

        <div class="kpi-label">
            ₹ AUTO-RELEASED
        </div>

        <div class="kpi-value">
            ₹{released_amt:,.0f}
        </div>

        <div
            class="kpi-delta"
            style="color:#A99CF2 !important;"
        >
            of ₹{processed_amt:,.0f}
            processed
        </div>

    </div>

    """)


with k5:

    render_html(f"""

    <div class="kpi">

        <div class="kpi-icon icon-slate">
            ◷
        </div>

        <div class="kpi-label">
            TIME SAVED
        </div>

        <div class="kpi-value">
            {hours_saved:.1f} hrs
        </div>

        <div class="kpi-delta">
            ↑ {minutes_saved:.0f} min
            @ {MANUAL_MINUTES_PER_INVOICE}
            min/invoice
        </div>

    </div>

    """)


st.markdown(
    "<div style='height:15px'></div>",
    unsafe_allow_html=True
)


# =============================================================================
# ACTION BUTTONS
# =============================================================================

b1, b2, spacer = st.columns(
    [1.15, .95, 3.3]
)


with b1:

    if st.button(

        "▶  Ingest next invoice",

        type="primary",

        use_container_width=True

    ):

        ingest_and_process()

        st.rerun()


with b2:

    if st.button(

        "⏩  Batch ingest ×10",

        use_container_width=True

    ):

        batch_ingest(10)

        st.rerun()


st.markdown(
    "<div style='height:10px'></div>",
    unsafe_allow_html=True
)


# =============================================================================
# TABS
# =============================================================================

tab1, tab2, tab3, tab4 = st.tabs([

    "▣  Live Feed",

    "⚠  Exception Queue",

    "▦  Vendor Master",

    "▥  Analytics"

])


# =============================================================================
# LIVE FEED
# =============================================================================

with tab1:

    if total == 0:

        left, right = st.columns(
            [3.2, 1]
        )


        # ---------------------------------------------------------
        # LIVE FEED EMPTY
        # ---------------------------------------------------------

        with left:

            render_html("""

            <div class="panel">

                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                ">

                    <div>

                        <div class="panel-title">
                            ▣ &nbsp; Live Invoice Feed
                        </div>

                        <div class="panel-sub">
                            Invoices are processed in real time
                            with rule-based guardrails.
                        </div>

                    </div>


                    <div style="
                        padding:7px 11px;
                        border-radius:999px;
                        background:rgba(45,212,168,.10);
                        border:1px solid rgba(45,212,168,.25);
                        color:#2DD4A8 !important;
                        font-size:.68rem;
                        font-weight:700;
                    ">

                        ● Live Simulation

                    </div>

                </div>


                <div style="
                    margin-top:20px;
                    height:205px;
                    border:1px solid #273B42;
                    border-radius:12px;
                    background:#0C171D;

                    display:flex;
                    flex-direction:column;

                    align-items:center;
                    justify-content:center;
                ">

                    <div style="
                        font-size:30px;
                        opacity:.7;
                    ">
                        ▤
                    </div>


                    <div style="
                        font-size:1rem;
                        font-weight:700;
                        color:#E4EEEB !important;
                        margin-top:8px;
                    ">

                        No invoices yet

                    </div>


                    <div style="
                        font-size:.75rem;
                        color:#71898C !important;
                        margin-top:7px;
                    ">

                        Click “Ingest next invoice”
                        or “Batch ingest ×10”
                        to populate the feed.

                    </div>

                </div>

            </div>

            """)


        # ---------------------------------------------------------
        # GUARDRAILS IN ACTION
        # ---------------------------------------------------------

        with right:

            render_html("""

            <div class="panel">

                <div class="panel-title">
                    🛡️ &nbsp; Guardrails in Action
                </div>

                <div class="panel-sub">
                    Real-time checks before any
                    payment is released.
                </div>


                <div style="
                    margin-top:18px;
                    line-height:2.05;
                    font-size:.74rem;
                ">

                    <div style="color:#B9C9C7 !important;">
                        🟢 &nbsp;
                        Invoice amount within budget cap
                    </div>

                    <div style="color:#B9C9C7 !important;">
                        🟢 &nbsp;
                        Vendor not in blacklist
                    </div>

                    <div style="color:#B9C9C7 !important;">
                        🟢 &nbsp;
                        Duplicate invoice check
                    </div>

                    <div style="color:#B9C9C7 !important;">
                        🟢 &nbsp;
                        UPI ID verification
                    </div>

                    <div style="color:#B9C9C7 !important;">
                        🟢 &nbsp;
                        Accounting record match
                    </div>

                    <div style="color:#B9C9C7 !important;">
                        🟢 &nbsp;
                        Category &amp; policy compliance
                    </div>

                </div>


                <div style="
                    margin-top:18px;
                    padding-top:13px;
                    border-top:1px solid #26383E;
                ">

                    <span style="
                        color:#2DD4A8 !important;
                    ">
                        ━━━━
                    </span>

                    <span style="
                        color:#70878A !important;
                        font-size:.68rem;
                    ">

                        Prevention today.<br>
                        &nbsp;&nbsp;&nbsp;&nbsp;
                        Fewer exceptions tomorrow.

                    </span>

                </div>

            </div>

            """)


    else:

        # ---------------------------------------------------------
        # EXPORT
        # ---------------------------------------------------------

        export_df = df.drop(
            columns=["reasons"]
        ).copy()


        export_df["date"] = (
            export_df["date"]
            .dt.strftime("%Y-%m-%d %H:%M")
        )


        st.download_button(

            "⬇  Export invoice log (CSV)",

            export_df.to_csv(
                index=False
            ),

            file_name=
            "payhoplon_invoice_log.csv",

            mime="text/csv"

        )


        # ---------------------------------------------------------
        # INVOICE CARDS
        # ---------------------------------------------------------

        for inv in reversed(
            st.session_state.invoices
        ):

            if (
                inv["decision"]
                == "Auto-Approved & Released"
            ):

                icon = "🟢"

            elif (
                inv["decision"]
                == "Cleared — Awaiting Sign-off"
            ):

                icon = "🟡"

            else:

                icon = "🔴"


            with st.expander(

                f"{icon}  "
                f"{inv['invoice_id']} — "
                f"{inv['vendor']} — "
                f"₹{inv['amount']:,} — "
                f"**{inv['decision']}**"

            ):

                st.write(

                    f"**UPI ID:** "
                    f"{inv['upi_id']}  |  "
                    f"**Matched txn:** "
                    f"{inv['txn_id'] or 'None'}"

                )


                st.write(

                    f"**Timestamp:** "
                    f"{inv['date'].strftime('%d %b, %I:%M %p')}"

                )


                if inv["reasons"]:

                    st.write(
                        "**Agent reasoning:**"
                    )

                    for reason in inv["reasons"]:

                        st.write(
                            f"- {reason}"
                        )

                else:

                    st.write(

                        "**Agent reasoning:** "
                        "All checks passed cleanly — "
                        "released without human involvement."

                    )


# =============================================================================
# EXCEPTION QUEUE
# =============================================================================

with tab2:

    exceptions = [

        inv

        for inv
        in st.session_state.invoices

        if inv["decision"]
        == "Flagged for Review"

    ]


    if not exceptions:

        st.success(

            "No exceptions pending. "
            "Everything either auto-released "
            "or cleared for sign-off."

        )


    else:

        for inv in exceptions:

            c1, c2, c3 = st.columns(
                [3, 1, 1]
            )


            with c1:

                st.markdown(

                    f"**{inv['invoice_id']}** — "
                    f"{inv['vendor']} — "
                    f"₹{inv['amount']:,}"

                )

                st.caption(

                    " · ".join(
                        inv["reasons"]
                    )

                )


            with c2:

                if st.button(

                    "✓  Approve",

                    key=
                    f"appr_{inv['invoice_id']}",

                    use_container_width=True

                ):

                    inv["decision"] = (
                        "Manually Approved"
                    )

                    st.rerun()


            with c3:

                if st.button(

                    "✕  Reject",

                    key=
                    f"rej_{inv['invoice_id']}",

                    use_container_width=True

                ):

                    inv["decision"] = (
                        "Rejected"
                    )

                    st.rerun()


# =============================================================================
# VENDOR MASTER
# =============================================================================

with tab3:

    render_html("""

    <div class="panel">

        <div class="panel-title">
            ▦ &nbsp; Vendor Master
        </div>

        <div class="panel-sub">
            Verified payment destinations
            and vendor risk status.
        </div>

    </div>

    """)


    vendor_df = pd.DataFrame(
        st.session_state.vendors
    ).copy()


    vendor_df["verified"] = (
        vendor_df["verified"]
        .map({

            True:
                "✓ Verified",

            False:
                "⚠ Unverified"

        })
    )


    st.dataframe(

        vendor_df,

        use_container_width=True,

        hide_index=True

    )


# =============================================================================
# ANALYTICS
# =============================================================================

with tab4:

    if total == 0:

        st.info(

            "Ingest some invoices first — "
            "try Batch ingest ×10 for a full "
            "dataset to chart."

        )


    else:

        chart_df = df.copy()


        chart_df = (

            chart_df

            .sort_values("date")

            .reset_index(drop=True)

        )


        chart_df["cumulative_released"] = (

            chart_df.where(

                chart_df["decision"]
                == "Auto-Approved & Released"

            )["amount"]

            .fillna(0)

            .cumsum()

        )


        chart_df["seq"] = range(

            1,

            len(chart_df) + 1

        )


        # ---------------------------------------------------------
        # DECISION BREAKDOWN
        # ---------------------------------------------------------

        row1c1, row1c2 = st.columns(2)


        with row1c1:

            decision_counts = (

                chart_df["decision"]

                .value_counts()

                .reset_index()

            )


            decision_counts.columns = [

                "Decision",
                "Count"

            ]


            color_map = {

                "Auto-Approved & Released":
                    "#2DD4A8",

                "Cleared — Awaiting Sign-off":
                    "#F2B84B",

                "Flagged for Review":
                    "#F06A73",

                "Manually Approved":
                    "#8FB7FF",

                "Rejected":
                    "#718083"

            }


            fig_pie = px.pie(

                decision_counts,

                names="Decision",

                values="Count",

                title=
                "Decision breakdown",

                hole=.58,

                color="Decision",

                color_discrete_map=
                color_map,

                template="plotly_dark"

            )


            fig_pie.update_layout(

                paper_bgcolor="#101C22",

                plot_bgcolor="#101C22",

                font_color="#C9D6D4",

                title_font_color="#EAF3F0",

                legend_font_color="#AFC0BE",

                margin=dict(
                    t=55,
                    l=10,
                    r=10,
                    b=10
                )

            )


            fig_pie.update_traces(

                textinfo="percent",

                marker=dict(
                    line=dict(
                        color="#101C22",
                        width=2
                    )
                )

            )


            st.plotly_chart(

                fig_pie,

                use_container_width=True

            )


        # ---------------------------------------------------------
        # CUMULATIVE RELEASE
        # ---------------------------------------------------------

        with row1c2:

            fig_cum = px.line(

                chart_df,

                x="seq",

                y="cumulative_released",

                title=
                "Cumulative ₹ auto-released",

                labels={

                    "seq":
                        "Invoice #",

                    "cumulative_released":
                        "₹ released"

                },

                markers=True,

                template="plotly_dark"

            )


            fig_cum.update_traces(

                line_color="#2DD4A8",

                line_width=3,

                marker=dict(
                    size=6,
                    color="#2DD4A8"
                )

            )


            fig_cum.update_layout(

                paper_bgcolor="#101C22",

                plot_bgcolor="#101C22",

                font_color="#C9D6D4",

                title_font_color="#EAF3F0",

                margin=dict(
                    t=55,
                    l=10,
                    r=10,
                    b=10
                )

            )


            fig_cum.update_xaxes(

                gridcolor="#20343A",

                zeroline=False

            )


            fig_cum.update_yaxes(

                gridcolor="#20343A",

                zeroline=False

            )


            st.plotly_chart(

                fig_cum,

                use_container_width=True

            )


        # ---------------------------------------------------------
        # INVOICE DISTRIBUTION + VENDOR VOLUME
        # ---------------------------------------------------------

        row2c1, row2c2 = st.columns(2)


        with row2c1:

            fig_hist = px.histogram(

                chart_df,

                x="amount",

                nbins=15,

                title=
                "Invoice amount distribution",

                labels={
                    "amount":
                        "Invoice amount (₹)"
                },

                template="plotly_dark"

            )


            fig_hist.update_traces(

                marker_color="#2DD4A8"

            )


            fig_hist.add_vline(

                x=
                st.session_state
                .guardrails["budget_cap"],

                line_dash="dash",

                line_color="#F06A73",

                annotation_text=
                "Budget cap"

            )


            fig_hist.add_vline(

                x=
                st.session_state
                .guardrails[
                    "auto_approve_ceiling"
                ],

                line_dash="dash",

                line_color="#2DD4A8",

                annotation_text=
                "Auto ceiling"

            )


            fig_hist.update_layout(

                paper_bgcolor="#101C22",

                plot_bgcolor="#101C22",

                font_color="#C9D6D4",

                title_font_color="#EAF3F0",

                margin=dict(
                    t=55,
                    l=10,
                    r=10,
                    b=10
                )

            )


            fig_hist.update_xaxes(

                gridcolor="#20343A",

                zeroline=False

            )


            fig_hist.update_yaxes(

                gridcolor="#20343A",

                zeroline=False

            )


            st.plotly_chart(

                fig_hist,

                use_container_width=True

            )


        with row2c2:

            vendor_summary = (

                chart_df

                .groupby("vendor")

                .agg(

                    invoices=(
                        "invoice_id",
                        "count"
                    ),

                    total_amount=(
                        "amount",
                        "sum"
                    )

                )

                .reset_index()

                .sort_values(
                    "total_amount",
                    ascending=True
                )

            )


            fig_vendor = px.bar(

                vendor_summary,

                x="total_amount",

                y="vendor",

                orientation="h",

                title=
                "Volume by vendor (₹ processed)",

                labels={

                    "total_amount":
                        "₹ total processed",

                    "vendor":
                        ""

                },

                template="plotly_dark"

            )


            fig_vendor.update_traces(

                marker_color="#2DD4A8"

            )


            fig_vendor.update_layout(

                paper_bgcolor="#101C22",

                plot_bgcolor="#101C22",

                font_color="#C9D6D4",

                title_font_color="#EAF3F0",

                margin=dict(
                    t=55,
                    l=10,
                    r=10,
                    b=10
                )

            )


            fig_vendor.update_xaxes(

                gridcolor="#20343A",

                zeroline=False

            )


            fig_vendor.update_yaxes(

                gridcolor="#20343A",

                zeroline=False

            )


            st.plotly_chart(

                fig_vendor,

                use_container_width=True

            )


        # ---------------------------------------------------------
        # EXCEPTION REASONS
        # ---------------------------------------------------------

        all_reasons = []


        for inv in st.session_state.invoices:

            for reason in inv["reasons"]:

                if "budget cap" in reason:

                    all_reasons.append(
                        "Over budget cap"
                    )

                elif "blacklisted" in reason:

                    all_reasons.append(
                        "Blacklisted vendor"
                    )

                elif "not on verified list" in reason:

                    all_reasons.append(
                        "Unverified vendor"
                    )

                elif "duplicate" in reason.lower():

                    all_reasons.append(
                        "Possible duplicate"
                    )

                elif "No matching UPI" in reason:

                    all_reasons.append(
                        "No matching UPI transaction"
                    )

                elif "ceiling" in reason:

                    all_reasons.append(
                        "Above auto-approve ceiling"
                    )

                else:

                    all_reasons.append(
                        reason
                    )


        if all_reasons:

            reason_df = (

                pd.Series(all_reasons)

                .value_counts()

                .reset_index()

            )


            reason_df.columns = [

                "Reason",
                "Count"

            ]


            fig_reasons = px.bar(

                reason_df,

                x="Count",

                y="Reason",

                orientation="h",

                title=
                "Why invoices got flagged / routed for review",

                template="plotly_dark"

            )


            fig_reasons.update_traces(

                marker_color="#F06A73"

            )


            fig_reasons.update_layout(

                showlegend=False,

                paper_bgcolor="#101C22",

                plot_bgcolor="#101C22",

                font_color="#C9D6D4",

                title_font_color="#EAF3F0",

                margin=dict(
                    t=55,
                    l=10,
                    r=10,
                    b=10
                )

            )


            fig_reasons.update_xaxes(

                gridcolor="#20343A",

                zeroline=False

            )


            fig_reasons.update_yaxes(

                gridcolor="#20343A",

                zeroline=False

            )


            st.plotly_chart(

                fig_reasons,

                use_container_width=True

            )


        else:

            st.success(

                "No exception reasons yet — "
                "every invoice so far has cleared cleanly."

            )


# =============================================================================
# FOOTER
# =============================================================================

render_html("""

<div style="
    margin-top:30px;
    padding-top:16px;
    border-top:1px solid #1D3036;

    display:flex;
    justify-content:space-between;

    color:#61787B !important;

    font-size:.68rem;
">

    <span>
        “Control today. Confidence tomorrow.”
    </span>

    <span>
        PayHoplon &nbsp;|&nbsp;
        Bitmela Launchpad Ideathon 🌱
    </span>

</div>

""")
