"""
PayHoplon — Autonomous Invoice-to-UPI Payment Agent (Prototype)
Bitmela Launchpad Ideathon | Track: Agentic Payments

This is a working simulation: it generates synthetic invoices and a synthetic
UPI transaction ledger, runs them through a rule engine (guardrails), and
autonomously decides whether to release payment or flag for human review —
mirroring exactly what PayHoplon would do against real UPI/accounting data.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import uuid
from datetime import datetime, timedelta

st.set_page_config(page_title="PayHoplon", page_icon="🛡️", layout="wide")

# ---------------------------------------------------------------------------
# SESSION STATE / SEED DATA
# ---------------------------------------------------------------------------

def seed_vendors():
    return [
        {"vendor": "Sundar Steel Traders", "upi_id": "sundarsteel@upi", "verified": True, "category": "Raw Material"},
        {"vendor": "Ganga Logistics", "upi_id": "gangalog@upi", "verified": True, "category": "Logistics"},
        {"vendor": "Nova Packaging Co.", "upi_id": "novapack@upi", "verified": True, "category": "Packaging"},
        {"vendor": "QuickFix Electricals", "upi_id": "quickfixelec@upi", "verified": True, "category": "Maintenance"},
        {"vendor": "Shadow Enterprises", "upi_id": "shadowent@upi", "verified": False, "category": "Unknown"},
        {"vendor": "Raghav Textiles", "upi_id": "raghavtex@upi", "verified": True, "category": "Raw Material"},
    ]

if "vendors" not in st.session_state:
    st.session_state.vendors = seed_vendors()
if "invoices" not in st.session_state:
    st.session_state.invoices = []          # processed invoice records
if "ledger" not in st.session_state:
    st.session_state.ledger = []             # simulated UPI transaction ledger
if "guardrails" not in st.session_state:
    st.session_state.guardrails = {
        "budget_cap": 50000,
        "auto_approve_ceiling": 20000,   # below this + all checks pass -> fully autonomous
        "blacklist": ["Shadow Enterprises"],
        "duplicate_window_days": 7,
    }

# Assumption used for the "time saved" ROI metric — a business owner/accountant
# manually checking, matching, and approving one invoice takes ~this long.
MANUAL_MINUTES_PER_INVOICE = 8

VENDOR_NAMES = [v["vendor"] for v in st.session_state.vendors]

# ---------------------------------------------------------------------------
# SYNTHETIC DATA GENERATION (stands in for a real invoicing / UPI API feed)
# ---------------------------------------------------------------------------

def generate_invoice():
    vendor = random.choice(st.session_state.vendors)
    # Weighted amount distribution: mostly normal, occasionally over cap
    amount = random.choice([
        random.randint(2000, 18000),
        random.randint(2000, 18000),
        random.randint(20000, 45000),
        random.randint(55000, 90000),   # will breach budget cap sometimes
    ])
    # 15% chance of being an exact duplicate of a recent invoice (fraud/error case)
    is_duplicate_test = random.random() < 0.15 and len(st.session_state.invoices) > 0
    if is_duplicate_test:
        prior = random.choice(st.session_state.invoices[-5:])
        vendor = next(v for v in st.session_state.vendors if v["vendor"] == prior["vendor"])
        amount = prior["amount"]

    invoice = {
        "invoice_id": f"INV-{uuid.uuid4().hex[:6].upper()}",
        "vendor": vendor["vendor"],
        "upi_id": vendor["upi_id"],
        "verified_vendor": vendor["verified"],
        "amount": amount,
        "date": datetime.now() - timedelta(minutes=random.randint(0, 120)),
    }
    return invoice


def find_matching_upi_txn(invoice):
    """Simulates checking the UPI transaction ledger for a matching debit-ready record.
    In production this would call the bank/UPI statement API. Here we simulate that
    ~90% of invoices have a clean corresponding ledger entry, 10% don't match (data gap)."""
    if random.random() < 0.90:
        txn = {
            "txn_id": f"UPI-{uuid.uuid4().hex[:8].upper()}",
            "amount": invoice["amount"],
            "upi_id": invoice["upi_id"],
            "status": "ready",
        }
        st.session_state.ledger.append(txn)
        return txn
    return None

# ---------------------------------------------------------------------------
# RULE ENGINE — THE CORE OF PAYHOPLON
# ---------------------------------------------------------------------------

def run_rule_engine(invoice):
    g = st.session_state.guardrails
    reasons = []
    passed = True

    # 1. Vendor verification
    if not invoice["verified_vendor"]:
        passed = False
        reasons.append("Vendor not on verified list")

    # 2. Blacklist check
    if invoice["vendor"] in g["blacklist"]:
        passed = False
        reasons.append(f"Vendor '{invoice['vendor']}' is blacklisted")

    # 3. Budget cap
    if invoice["amount"] > g["budget_cap"]:
        passed = False
        reasons.append(f"Amount ₹{invoice['amount']:,} exceeds budget cap ₹{g['budget_cap']:,}")

    # 4. Duplicate detection (same vendor + amount within window)
    cutoff = invoice["date"] - timedelta(days=g["duplicate_window_days"])
    for past in st.session_state.invoices:
        if (past["vendor"] == invoice["vendor"]
                and past["amount"] == invoice["amount"]
                and past["date"] >= cutoff
                and past["decision"] in ("Auto-Approved & Released", "Manually Approved")):
            passed = False
            reasons.append(f"Possible duplicate of {past['invoice_id']} (same vendor + amount)")
            break

    # 5. UPI ledger match
    matched_txn = find_matching_upi_txn(invoice)
    if matched_txn is None:
        passed = False
        reasons.append("No matching UPI transaction found in ledger")

    # 6. Autonomy ceiling — even clean invoices above ceiling get a light-touch flag
    autonomous = passed and invoice["amount"] <= g["auto_approve_ceiling"]

    if passed and not autonomous:
        reasons.append(f"Passed all checks but above auto-approve ceiling (₹{g['auto_approve_ceiling']:,}) — routed for quick sign-off")

    if passed and autonomous:
        decision = "Auto-Approved & Released"
    elif passed and not autonomous:
        decision = "Cleared — Awaiting Sign-off"
    else:
        decision = "Flagged for Review"

    return decision, reasons, matched_txn


def ingest_and_process():
    invoice = generate_invoice()
    decision, reasons, txn = run_rule_engine(invoice)
    invoice["decision"] = decision
    invoice["reasons"] = reasons
    invoice["txn_id"] = txn["txn_id"] if txn else None
    st.session_state.invoices.append(invoice)


def batch_ingest(n):
    for _ in range(n):
        ingest_and_process()

# ---------------------------------------------------------------------------
# SIDEBAR — GUARDRAIL CONFIGURATION (the "trust settings" the business owner sets once)
# ---------------------------------------------------------------------------

st.sidebar.title("🛡️ PayHoplon Guardrails")
st.sidebar.caption("Set once. The agent operates inside these limits — no exceptions, no manual overrides unless you change them here.")

g = st.session_state.guardrails
g["budget_cap"] = st.sidebar.number_input("Hard budget cap per invoice (₹)", min_value=5000, max_value=200000, value=g["budget_cap"], step=5000)
g["auto_approve_ceiling"] = st.sidebar.number_input("Fully autonomous ceiling (₹)", min_value=1000, max_value=g["budget_cap"], value=min(g["auto_approve_ceiling"], g["budget_cap"]), step=1000)
g["blacklist"] = st.sidebar.multiselect("Blacklisted vendors", VENDOR_NAMES, default=g["blacklist"])
g["duplicate_window_days"] = st.sidebar.slider("Duplicate-check window (days)", 1, 30, g["duplicate_window_days"])

st.sidebar.divider()
if st.sidebar.button("🔄 Reset simulation", use_container_width=True):
    st.session_state.invoices = []
    st.session_state.ledger = []
    st.rerun()

# ---------------------------------------------------------------------------
# MAIN DASHBOARD
# ---------------------------------------------------------------------------

st.title("🛡️ PayHoplon")
st.caption("An agent that doesn't just watch your money — it manages it. Autonomous invoice reconciliation + UPI payment release, inside guardrails you control.")

col_a, col_b, col_c = st.columns([1, 1, 2])
with col_a:
    if st.button("📥 Ingest next invoice", type="primary", use_container_width=True):
        ingest_and_process()
with col_b:
    if st.button("⏩ Batch ingest ×10", use_container_width=True):
        batch_ingest(10)

df = pd.DataFrame(st.session_state.invoices)

# KPIs
total = len(df)
auto = (df["decision"] == "Auto-Approved & Released").sum() if total else 0
cleared = (df["decision"] == "Cleared — Awaiting Sign-off").sum() if total else 0
flagged = (df["decision"].isin(["Flagged for Review"])).sum() if total else 0
released_amt = df.loc[df["decision"] == "Auto-Approved & Released", "amount"].sum() if total else 0
processed_amt = df["amount"].sum() if total else 0
# Time saved: every invoice that didn't need a human touch (auto-released) saves the full manual time
minutes_saved = auto * MANUAL_MINUTES_PER_INVOICE
hours_saved = minutes_saved / 60

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Invoices processed", total)
k2.metric("Autonomously released", auto, f"{(auto/total*100):.0f}% of total" if total else None)
k3.metric("Flagged for review", flagged, f"{(flagged/total*100):.0f}% of total" if total else None)
k4.metric("₹ auto-released", f"₹{released_amt:,.0f}", f"of ₹{processed_amt:,.0f} processed" if total else None)
k5.metric("⏱ Time saved", f"{hours_saved:.1f} hrs", f"{minutes_saved:.0f} min @ {MANUAL_MINUTES_PER_INVOICE} min/invoice")

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(["📋 Live Feed", "🚩 Exception Queue", "🏢 Vendor Master", "📊 Analytics"])

with tab1:
    if total == 0:
        st.info("Click **Ingest next invoice** (or **Batch ingest ×10** to populate faster) and watch PayHoplon decide in real time.")
    else:
        export_df = df.drop(columns=["reasons"]).copy()
        export_df["date"] = export_df["date"].dt.strftime("%Y-%m-%d %H:%M")
        st.download_button(
            "⬇️ Export invoice log (CSV)",
            export_df.to_csv(index=False),
            file_name="payhoplon_invoice_log.csv",
            mime="text/csv",
        )
        for inv in reversed(st.session_state.invoices):
            color = {"Auto-Approved & Released": "🟢", "Cleared — Awaiting Sign-off": "🟡", "Flagged for Review": "🔴"}[inv["decision"]]
            with st.expander(f"{color} {inv['invoice_id']} — {inv['vendor']} — ₹{inv['amount']:,} — **{inv['decision']}**"):
                st.write(f"**UPI ID:** {inv['upi_id']}  |  **Matched txn:** {inv['txn_id'] or 'None'}")
                st.write(f"**Timestamp:** {inv['date'].strftime('%d %b, %I:%M %p')}")
                if inv["reasons"]:
                    st.write("**Agent reasoning:**")
                    for r in inv["reasons"]:
                        st.write(f"- {r}")
                else:
                    st.write("**Agent reasoning:** All checks passed cleanly — released without human involvement.")

with tab2:
    exceptions = [inv for inv in st.session_state.invoices if inv["decision"] == "Flagged for Review"]
    if not exceptions:
        st.success("No exceptions pending. Everything either auto-released or cleared for sign-off.")
    else:
        for inv in exceptions:
            c1, c2, c3 = st.columns([3, 1, 1])
            with c1:
                st.write(f"**{inv['invoice_id']}** — {inv['vendor']} — ₹{inv['amount']:,}")
                st.caption(" · ".join(inv["reasons"]))
            with c2:
                if st.button("✅ Approve", key=f"appr_{inv['invoice_id']}"):
                    inv["decision"] = "Manually Approved"
                    st.rerun()
            with c3:
                if st.button("❌ Reject", key=f"rej_{inv['invoice_id']}"):
                    inv["decision"] = "Rejected"
                    st.rerun()

with tab3:
    st.dataframe(pd.DataFrame(st.session_state.vendors), use_container_width=True, hide_index=True)

with tab4:
    if total == 0:
        st.info("Ingest some invoices first — try **Batch ingest ×10** for a full dataset to chart.")
    else:
        chart_df = df.copy()
        chart_df = chart_df.sort_values("date").reset_index(drop=True)
        chart_df["cumulative_released"] = chart_df.where(
            chart_df["decision"] == "Auto-Approved & Released"
        )["amount"].fillna(0).cumsum()
        chart_df["seq"] = range(1, len(chart_df) + 1)

        row1c1, row1c2 = st.columns(2)

        with row1c1:
            decision_counts = chart_df["decision"].value_counts().reset_index()
            decision_counts.columns = ["Decision", "Count"]
            color_map = {
                "Auto-Approved & Released": "#22c55e",
                "Cleared — Awaiting Sign-off": "#eab308",
                "Flagged for Review": "#ef4444",
                "Manually Approved": "#3b82f6",
                "Rejected": "#6b7280",
            }
            fig_pie = px.pie(
                decision_counts, names="Decision", values="Count",
                title="Decision breakdown", hole=0.45,
                color="Decision", color_discrete_map=color_map,
            )
            fig_pie.update_traces(textinfo="percent+label")
            st.plotly_chart(fig_pie, use_container_width=True)

        with row1c2:
            fig_cum = px.line(
                chart_df, x="seq", y="cumulative_released",
                title="Cumulative ₹ auto-released over time",
                labels={"seq": "Invoice #", "cumulative_released": "₹ released (cumulative)"},
                markers=True,
            )
            fig_cum.update_traces(line_color="#22c55e")
            st.plotly_chart(fig_cum, use_container_width=True)

        row2c1, row2c2 = st.columns(2)

        with row2c1:
            fig_hist = px.histogram(
                chart_df, x="amount", nbins=15, title="Invoice amount distribution",
                labels={"amount": "Invoice amount (₹)"},
            )
            fig_hist.add_vline(
                x=st.session_state.guardrails["budget_cap"], line_dash="dash",
                line_color="red", annotation_text="Budget cap",
            )
            fig_hist.add_vline(
                x=st.session_state.guardrails["auto_approve_ceiling"], line_dash="dash",
                line_color="green", annotation_text="Auto ceiling",
            )
            st.plotly_chart(fig_hist, use_container_width=True)

        with row2c2:
            vendor_summary = chart_df.groupby("vendor").agg(
                invoices=("invoice_id", "count"), total_amount=("amount", "sum")
            ).reset_index().sort_values("total_amount", ascending=True)
            fig_vendor = px.bar(
                vendor_summary, x="total_amount", y="vendor", orientation="h",
                title="Volume by vendor (₹ processed)",
                labels={"total_amount": "₹ total processed", "vendor": ""},
            )
            st.plotly_chart(fig_vendor, use_container_width=True)

        # Exception reason frequency — flatten the reasons lists
        all_reasons = []
        for inv in st.session_state.invoices:
            for r in inv["reasons"]:
                # bucket by the first few words so similar reasons group together
                if "budget cap" in r:
                    all_reasons.append("Over budget cap")
                elif "blacklisted" in r:
                    all_reasons.append("Blacklisted vendor")
                elif "not on verified list" in r:
                    all_reasons.append("Unverified vendor")
                elif "duplicate" in r.lower():
                    all_reasons.append("Possible duplicate")
                elif "No matching UPI" in r:
                    all_reasons.append("No matching UPI transaction")
                elif "ceiling" in r:
                    all_reasons.append("Above auto-approve ceiling")
                else:
                    all_reasons.append(r)

        if all_reasons:
            reason_df = pd.Series(all_reasons).value_counts().reset_index()
            reason_df.columns = ["Reason", "Count"]
            fig_reasons = px.bar(
                reason_df, x="Count", y="Reason", orientation="h",
                title="Why invoices got flagged / routed for review",
                color="Reason",
            )
            fig_reasons.update_layout(showlegend=False)
            st.plotly_chart(fig_reasons, use_container_width=True)
        else:
            st.success("No exception reasons yet — every invoice so far has cleared cleanly.")
