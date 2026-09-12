import streamlit as st
import pandas as pd
import plotly.express as px
import random
import uuid
from datetime import datetime, timedelta

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="PayHoplon",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# DARK FINTECH THEME
# ============================================================

st.markdown("""
<style>

/* =========================================================
   MAIN BACKGROUND
   ========================================================= */

.stApp {
    background:
        radial-gradient(
            circle at 80% 0%,
            rgba(45, 212, 168, 0.10),
            transparent 28%
        ),
        radial-gradient(
            circle at 25% 50%,
            rgba(30, 100, 90, 0.07),
            transparent 30%
        ),
        #071014 !important;

    color: #F1F7F5 !important;
}

.block-container {
    max-width: 1450px !important;
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
}


/* =========================================================
   GLOBAL TEXT
   ========================================================= */

.stApp p,
.stApp span,
.stApp label,
.stApp li {
    color: #D5E1DF !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #F3F8F6 !important;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #09171B 0%,
            #061114 100%
        ) !important;

    border-right: 1px solid #1D3339 !important;
}

section[data-testid="stSidebar"] * {
    color: #DDE9E6 !important;
}

section[data-testid="stSidebar"] label {
    color: #90A7A9 !important;
    font-weight: 600 !important;
}

section[data-testid="stSidebar"] input {
    background: #111F24 !important;
    color: #FFFFFF !important;
    border: 1px solid #2A4047 !important;
}

section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #111F24 !important;
    border-color: #2A4047 !important;
}

section[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #FFFFFF !important;
}

section[data-testid="stSidebar"] .stNumberInput button {
    background: #17272D !important;
    color: #DDE9E6 !important;
    border-color: #2A4047 !important;
}

section[data-testid="stSidebar"] .stSlider [role="slider"] {
    background: #2DD4A8 !important;
}

section[data-testid="stSidebar"] hr {
    border-color: #21363C !important;
}


/* =========================================================
   SIDEBAR TITLE
   ========================================================= */

section[data-testid="stSidebar"] h1 {
    color: #F4FAF8 !important;
    font-size: 1.5rem !important;
    font-weight: 800 !important;
}

section[data-testid="stSidebar"] .stCaption {
    color: #6F888A !important;
}


/* =========================================================
   BUTTONS
   ========================================================= */

.stButton > button {
    min-height: 43px !important;

    border-radius: 11px !important;

    background: #16272D !important;

    color: #E6F0ED !important;

    border: 1px solid #2A4249 !important;

    font-weight: 700 !important;

    box-shadow: none !important;
}

.stButton > button:hover {
    background: #14302D !important;

    border-color: #2DD4A8 !important;

    color: #2DD4A8 !important;
}

button[kind="primary"] {
    background:
        linear-gradient(
            135deg,
            #2DD4A8,
            #159C7E
        ) !important;

    color: #03130F !important;

    border: none !important;

    box-shadow:
        0 6px 20px rgba(45,212,168,.16) !important;
}

button[kind="primary"]:hover {
    background:
        linear-gradient(
            135deg,
            #43DFB7,
            #20B38F
        ) !important;

    color: #02100C !important;
}


/* =========================================================
   METRIC CARDS
   ========================================================= */

div[data-testid="stMetric"] {

    background:
        linear-gradient(
            145deg,
            #122127,
            #0C181E
        ) !important;

    border: 1px solid #294047 !important;

    border-radius: 16px !important;

    padding: 18px !important;

    min-height: 110px !important;

    box-shadow:
        0 8px 25px rgba(0,0,0,.18) !important;
}

div[data-testid="stMetricLabel"] {
    color: #8EA4A6 !important;
}

div[data-testid="stMetricLabel"] * {
    color: #8EA4A6 !important;
    font-weight: 600 !important;
}

div[data-testid="stMetricValue"] {
    color: #F4FAF8 !important;
}

div[data-testid="stMetricValue"] * {
    color: #F4FAF8 !important;
    font-weight: 800 !important;
}

div[data-testid="stMetricDelta"] {
    color: #2DD4A8 !important;
}

div[data-testid="stMetricDelta"] * {
    color: #2DD4A8 !important;
}


/* =========================================================
   TABS
   ========================================================= */

div[data-baseweb="tab-list"] {
    background: transparent !important;

    border-bottom: 1px solid #21363C !important;

    gap: 4px !important;
}

button[data-baseweb="tab"] {
    background: transparent !important;

    color: #809698 !important;

    font-weight: 700 !important;

    padding: 12px 16px !important;
}

button[data-baseweb="tab"] * {
    color: #809698 !important;
}

button[data-baseweb="tab"]:hover {
    color: #C2D0CE !important;
}

button[data-baseweb="tab"]:hover * {
    color: #C2D0CE !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #2DD4A8 !important;
}

button[data-baseweb="tab"][aria-selected="true"] * {
    color: #2DD4A8 !important;
}

div[data-baseweb="tab-highlight"] {
    background-color: #2DD4A8 !important;

    height: 3px !important;
}


/* =========================================================
   EXPANDERS
   ========================================================= */

div[data-testid="stExpander"] {
    background: #101D23 !important;

    border: 1px solid #263C43 !important;

    border-radius: 13px !important;

    margin-bottom: 8px !important;
}

div[data-testid="stExpander"] summary {
    color: #E5EFEC !important;
}

div[data-testid="stExpander"] summary * {
    color: #E5EFEC !important;
}


/* =========================================================
   ALERTS
   ========================================================= */

div[data-testid="stAlert"] {
    background: #102229 !important;

    border: 1px solid #29444B !important;

    border-radius: 12px !important;
}

div[data-testid="stAlert"] * {
    color: #B9C9C7 !important;
}


/* =========================================================
   CAPTIONS
   ========================================================= */

[data-testid="stCaptionContainer"] p {
    color: #7D9698 !important;
}


/* =========================================================
   DOWNLOAD BUTTON
   ========================================================= */

.stDownloadButton button {
    background: #16272D !important;

    color: #DDE9E5 !important;

    border: 1px solid #2A4249 !important;

    border-radius: 10px !important;
}

.stDownloadButton button:hover {
    border-color: #2DD4A8 !important;

    color: #2DD4A8 !important;
}


/* =========================================================
   DATAFRAME
   ========================================================= */

div[data-testid="stDataFrame"] {
    border: 1px solid #263C43 !important;

    border-radius: 12px !important;

    overflow: hidden !important;
}


/* =========================================================
   SLIDER
   ========================================================= */

.stSlider [role="slider"] {
    background-color: #2DD4A8 !important;
}


/* =========================================================
   DIVIDER
   ========================================================= */

hr {
    border-color: #20353B !important;
}


/* =========================================================
   STREAMLIT HEADER / FOOTER
   ========================================================= */

header {
    background: transparent !important;
}

#MainMenu {
    visibility: hidden !important;
}

footer {
    visibility: hidden !important;
}


/* =========================================================
   RESPONSIVE
   ========================================================= */

@media (max-width: 900px) {

    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# VENDOR MASTER
# ============================================================

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


# ============================================================
# SESSION STATE
# ============================================================

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
        "blacklist": ["Shadow Enterprises"],
        "duplicate_window_days": 7
    }


MANUAL_MINUTES_PER_INVOICE = 8

VENDOR_NAMES = [
    vendor["vendor"]
    for vendor in st.session_state.vendors
]


# ============================================================
# INVOICE GENERATION
# ============================================================

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


# ============================================================
# UPI TRANSACTION
# ============================================================

def find_matching_upi_txn(invoice):

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


# ============================================================
# RULE ENGINE
# ============================================================

def run_rule_engine(invoice):

    g = st.session_state.guardrails

    reasons = []

    passed = True

    # --------------------------------------------------------
    # Vendor verification
    # --------------------------------------------------------

    if not invoice["verified_vendor"]:

        passed = False

        reasons.append(
            "Vendor not on verified list"
        )

    # --------------------------------------------------------
    # Blacklist
    # --------------------------------------------------------

    if invoice["vendor"] in g["blacklist"]:

        passed = False

        reasons.append(
            f"Vendor '{invoice['vendor']}' is blacklisted"
        )

    # --------------------------------------------------------
    # Budget
    # --------------------------------------------------------

    if invoice["amount"] > g["budget_cap"]:

        passed = False

        reasons.append(

            f"Amount ₹{invoice['amount']:,} "
            f"exceeds budget cap "
            f"₹{g['budget_cap']:,}"

        )

    # --------------------------------------------------------
    # Duplicate
    # --------------------------------------------------------

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

            and past["date"]
            >= cutoff

            and past["decision"] in [

                "Auto-Approved & Released",

                "Manually Approved"

            ]

        ):

            passed = False

            reasons.append(

                f"Possible duplicate of "
                f"{past['invoice_id']} "
                f"(same vendor + amount)"

            )

            break

    # --------------------------------------------------------
    # UPI match
    # --------------------------------------------------------

    matched_txn = find_matching_upi_txn(
        invoice
    )

    if matched_txn is None:

        passed = False

        reasons.append(
            "No matching UPI transaction found in ledger"
        )

    # --------------------------------------------------------
    # Autonomy ceiling
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Final decision
    # --------------------------------------------------------

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


# ============================================================
# PROCESS INVOICE
# ============================================================

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


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🛡️ PayHoplon")

    st.caption(
        "GUARDRAILS FOR SMARTER PAYMENTS"
    )

    st.divider()

    st.markdown("### Simulation Controls")

    g = st.session_state.guardrails

    g["budget_cap"] = st.number_input(
        "Budget Cap per Invoice (₹)",
        min_value=5000,
        max_value=200000,
        value=g["budget_cap"],
        step=5000
    )

    g["auto_approve_ceiling"] = st.number_input(
        "Fully Autonomous Ceiling (₹)",
        min_value=1000,
        max_value=g["budget_cap"],
        value=min(
            g["auto_approve_ceiling"],
            g["budget_cap"]
        ),
        step=1000
    )

    g["blacklist"] = st.multiselect(
        "Blacklist Vendors",
        VENDOR_NAMES,
        default=g["blacklist"]
    )

    g["duplicate_window_days"] = st.slider(
        "Duplicate Check Window (Days)",
        1,
        30,
        g["duplicate_window_days"]
    )

    st.divider()

    st.info(
        "💡 Set once. The agent operates "
        "inside these limits."
    )

    if st.button(
        "↻ Reset Simulation",
        use_container_width=True
    ):

        st.session_state.invoices = []

        st.session_state.ledger = []

        st.rerun()


# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns(
    [4, 1]
)

with header_left:

    st.caption(
        "WELCOME TO"
    )

    st.markdown(
        "<h1 style='margin-bottom:0;'>"
        "Pay<span style='color:#2DD4A8;'>Hoplon</span>"
        "</h1>",
        unsafe_allow_html=True
    )

    st.write(
        "Autonomous invoice reconciliation & "
        "UPI payment release, operating safely "
        "inside the guardrails you control."
    )


with header_right:

    st.markdown(
        "### 🛡️"
    )

    st.caption(
        "Automate.\nProtect."
    )

    st.markdown(
        "**Pay with Confidence.**"
    )


st.divider()


# ============================================================
# DATAFRAME
# ============================================================

df = pd.DataFrame(
    st.session_state.invoices
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

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
    minutes_saved
    / 60
)


# ============================================================
# KPI CARDS
# ============================================================

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric(
    "Invoices Processed",
    total
)

k2.metric(
    "Autonomously Released",
    auto,
    (
        f"{auto / total * 100:.0f}% of total"
        if total
        else None
    )
)

k3.metric(
    "Flagged for Review",
    flagged,
    (
        f"{flagged / total * 100:.0f}% of total"
        if total
        else None
    )
)

k4.metric(
    "₹ Auto-Released",
    f"₹{released_amt:,.0f}",
    (
        f"of ₹{processed_amt:,.0f} processed"
        if total
        else None
    )
)

k5.metric(
    "Time Saved",
    f"{hours_saved:.1f} hrs",
    (
        f"{minutes_saved:.0f} min @ "
        f"{MANUAL_MINUTES_PER_INVOICE} min/invoice"
    )
)


st.markdown("")


# ============================================================
# ACTION BUTTONS
# ============================================================

button1, button2, empty = st.columns(
    [1.2, 1, 3]
)

with button1:

    if st.button(
        "▶ Ingest Next Invoice",
        type="primary",
        use_container_width=True
    ):

        ingest_and_process()

        st.rerun()


with button2:

    if st.button(
        "⏩ Batch Ingest ×10",
        use_container_width=True
    ):

        batch_ingest(10)

        st.rerun()


st.markdown("")


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs([

    "▣ Live Feed",

    "⚠ Exception Queue",

    "▦ Vendor Master",

    "▥ Analytics"

])


# ============================================================
# LIVE FEED
# ============================================================

with tab1:

    if total == 0:

        left, right = st.columns(
            [3, 1]
        )

        with left:

            st.subheader(
                "▣ Live Invoice Feed"
            )

            st.caption(
                "Invoices are processed in real time "
                "with rule-based guardrails."
            )

            st.info(
                "No invoices yet.\n\n"
                "Click **Ingest Next Invoice** or "
                "**Batch Ingest ×10** to populate "
                "the feed."
            )


        with right:

            st.subheader(
                "🛡️ Guardrails in Action"
            )

            st.caption(
                "Real-time checks before payment release."
            )

            st.success(
                "✓ Invoice amount within budget"
            )

            st.success(
                "✓ Vendor verification"
            )

            st.success(
                "✓ Duplicate invoice check"
            )

            st.success(
                "✓ UPI ID matching"
            )

            st.success(
                "✓ Accounting record match"
            )

            st.success(
                "✓ Policy compliance"
            )


    else:

        export_df = df.drop(
            columns=["reasons"]
        ).copy()

        export_df["date"] = (
            export_df["date"]
            .dt.strftime("%Y-%m-%d %H:%M")
        )

        st.download_button(

            "⬇ Export Invoice Log",

            export_df.to_csv(
                index=False
            ),

            file_name=
            "payhoplon_invoice_log.csv",

            mime="text/csv"

        )

        st.markdown("")


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

            elif (
                inv["decision"]
                == "Manually Approved"
            ):

                icon = "🔵"

            else:

                icon = "🔴"


            with st.expander(

                f"{icon} "
                f"{inv['invoice_id']} | "
                f"{inv['vendor']} | "
                f"₹{inv['amount']:,} | "
                f"{inv['decision']}"

            ):

                st.write(
                    f"**UPI ID:** "
                    f"{inv['upi_id']}"
                )

                st.write(
                    f"**Matched Transaction:** "
                    f"{inv['txn_id'] or 'None'}"
                )

                st.write(
                    f"**Timestamp:** "
                    f"{inv['date'].strftime('%d %b %Y, %I:%M %p')}"
                )

                if inv["reasons"]:

                    st.write(
                        "**Agent Reasoning:**"
                    )

                    for reason in inv["reasons"]:

                        st.write(
                            f"• {reason}"
                        )

                else:

                    st.success(
                        "All checks passed cleanly. "
                        "Payment released autonomously."
                    )


# ============================================================
# EXCEPTION QUEUE
# ============================================================

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
            "✓ No exceptions pending."
        )


    else:

        for inv in exceptions:

            c1, c2, c3 = st.columns(
                [3, 1, 1]
            )

            with c1:

                st.write(

                    f"**{inv['invoice_id']}** — "
                    f"{inv['vendor']} — "
                    f"₹{inv['amount']:,}"

                )

                st.caption(
                    " • ".join(
                        inv["reasons"]
                    )
                )


            with c2:

                if st.button(

                    "✓ Approve",

                    key=
                    f"approve_{inv['invoice_id']}",

                    use_container_width=True

                ):

                    inv["decision"] = (
                        "Manually Approved"
                    )

                    st.rerun()


            with c3:

                if st.button(

                    "✕ Reject",

                    key=
                    f"reject_{inv['invoice_id']}",

                    use_container_width=True

                ):

                    inv["decision"] = (
                        "Rejected"
                    )

                    st.rerun()


# ============================================================
# VENDOR MASTER
# ============================================================

with tab3:

    st.subheader(
        "▦ Vendor Master"
    )

    st.caption(
        "Verified payment destinations "
        "and vendor risk status."
    )

    vendor_df = pd.DataFrame(
        st.session_state.vendors
    ).copy()

    vendor_df["verified"] = (
        vendor_df["verified"]
        .map({
            True: "✓ Verified",
            False: "⚠ Unverified"
        })
    )

    st.dataframe(

        vendor_df,

        use_container_width=True,

        hide_index=True

    )


# ============================================================
# ANALYTICS
# ============================================================

with tab4:

    if total == 0:

        st.info(

            "Run the simulation first. "
            "Batch Ingest ×10 is the fastest "
            "way to generate analytics."

        )

    else:

        chart_df = (
            df
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


        # ------------------------------------------------------
        # ROW 1
        # ------------------------------------------------------

        col1, col2 = st.columns(2)


        # ------------------------------------------------------
        # DECISION BREAKDOWN
        # ------------------------------------------------------

        with col1:

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

            fig = px.pie(

                decision_counts,

                names="Decision",

                values="Count",

                hole=0.55,

                title="Decision Breakdown",

                color="Decision",

                color_discrete_map=
                color_map,

                template="plotly_dark"

            )

            fig.update_layout(

                paper_bgcolor="#101C22",

                plot_bgcolor="#101C22",

                font_color="#D8E3E1",

                title_font_color="#F1F7F5",

                legend_font_color="#AFC0BE",

                margin=dict(
                    t=55,
                    l=10,
                    r=10,
                    b=10
                )

            )

            st.plotly_chart(

                fig,

                use_container_width=True

            )


        # ------------------------------------------------------
        # CUMULATIVE RELEASE
        # ------------------------------------------------------

        with col2:

            fig = px.line(

                chart_df,

                x="seq",

                y="cumulative_released",

                markers=True,

                title=
                "Cumulative ₹ Auto-Released",

                labels={

                    "seq":
                        "Invoice #",

                    "cumulative_released":
                        "₹ Released"

                },

                template="plotly_dark"

            )

            fig.update_traces(

                line_color="#2DD4A8",

                line_width=3,

                marker=dict(
                    size=6,
                    color="#2DD4A8"
                )

            )

            fig.update_layout(

                paper_bgcolor="#101C22",

                plot_bgcolor="#101C22",

                font_color="#D8E3E1",

                title_font_color="#F1F7F5",

                margin=dict(
                    t=55,
                    l=10,
                    r=10,
                    b=10
                )

            )

            fig.update_xaxes(
                gridcolor="#20343A",
                zeroline=False
            )

            fig.update_yaxes(
                gridcolor="#20343A",
                zeroline=False
            )

            st.plotly_chart(

                fig,

                use_container_width=True

            )


        # ------------------------------------------------------
        # ROW 2
        # ------------------------------------------------------

        col3, col4 = st.columns(2)


        # ------------------------------------------------------
        # AMOUNT DISTRIBUTION
        # ------------------------------------------------------

        with col3:

            fig = px.histogram(

                chart_df,

                x="amount",

                nbins=15,

                title=
                "Invoice Amount Distribution",

                labels={
                    "amount":
                        "Invoice Amount (₹)"
                },

                template="plotly_dark"

            )

            fig.update_traces(
                marker_color="#2DD4A8"
            )

            fig.add_vline(

                x=
                st.session_state
                .guardrails[
                    "budget_cap"
                ],

                line_dash="dash",

                line_color="#F06A73",

                annotation_text=
                "Budget Cap"

            )

            fig.add_vline(

                x=
                st.session_state
                .guardrails[
                    "auto_approve_ceiling"
                ],

                line_dash="dash",

                line_color="#2DD4A8",

                annotation_text=
                "Auto Ceiling"

            )

            fig.update_layout(

                paper_bgcolor="#101C22",

                plot_bgcolor="#101C22",

                font_color="#D8E3E1",

                title_font_color="#F1F7F5",

                margin=dict(
                    t=55,
                    l=10,
                    r=10,
                    b=10
                )

            )

            st.plotly_chart(

                fig,

                use_container_width=True

            )


        # ------------------------------------------------------
        # VENDOR VOLUME
        # ------------------------------------------------------

        with col4:

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

            fig = px.bar(

                vendor_summary,

                x="total_amount",

                y="vendor",

                orientation="h",

                title=
                "Volume by Vendor",

                labels={

                    "total_amount":
                        "₹ Total Processed",

                    "vendor":
                        ""

                },

                template="plotly_dark"

            )

            fig.update_traces(
                marker_color="#2DD4A8"
            )

            fig.update_layout(

                paper_bgcolor="#101C22",

                plot_bgcolor="#101C22",

                font_color="#D8E3E1",

                title_font_color="#F1F7F5",

                margin=dict(
                    t=55,
                    l=10,
                    r=10,
                    b=10
                )

            )

            st.plotly_chart(

                fig,

                use_container_width=True

            )


        # ------------------------------------------------------
        # EXCEPTION REASONS
        # ------------------------------------------------------

        reasons = []

        for inv in st.session_state.invoices:

            for reason in inv["reasons"]:

                if "budget cap" in reason:

                    reasons.append(
                        "Over Budget Cap"
                    )

                elif "blacklisted" in reason:

                    reasons.append(
                        "Blacklisted Vendor"
                    )

                elif "not on verified list" in reason:

                    reasons.append(
                        "Unverified Vendor"
                    )

                elif "duplicate" in reason.lower():

                    reasons.append(
                        "Possible Duplicate"
                    )

                elif "No matching UPI" in reason:

                    reasons.append(
                        "No Matching UPI"
                    )

                elif "ceiling" in reason:

                    reasons.append(
                        "Above Auto Ceiling"
                    )


        if reasons:

            reason_df = (

                pd.Series(reasons)

                .value_counts()

                .reset_index()

            )

            reason_df.columns = [
                "Reason",
                "Count"
            ]

            fig = px.bar(

                reason_df,

                x="Count",

                y="Reason",

                orientation="h",

                title=
                "Why Invoices Were Flagged",

                template="plotly_dark"

            )

            fig.update_traces(
                marker_color="#F06A73"
            )

            fig.update_layout(

                showlegend=False,

                paper_bgcolor="#101C22",

                plot_bgcolor="#101C22",

                font_color="#D8E3E1",

                title_font_color="#F1F7F5",

                margin=dict(
                    t=55,
                    l=10,
                    r=10,
                    b=10
                )

            )

            st.plotly_chart(

                fig,

                use_container_width=True

            )

        else:

            st.success(

                "No exception reasons yet — "
                "every invoice so far has cleared cleanly."

            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Control today. Confidence tomorrow. "
    " | PayHoplon • Bitmela Launchpad Ideathon"
)
