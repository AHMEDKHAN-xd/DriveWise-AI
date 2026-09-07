from datetime import datetime

import streamlit as st
import pandas as pd

from ai.diagnosis import check_ollama, stream_ai_diagnosis

from ui.styles import load_styles

from ui.maintenance import show_maintenance_section

from ui.components import (
    show_header,
    show_steps,
    show_vehicle_section,
    show_vehicle_card,
    show_problem_section,
    show_symptom_chips,
    show_diagnosis_header,
    show_problem_summary,
    show_knowledge_base_results,
    show_ai_section_header,
    show_card_header,
    show_ai_unavailable,
    show_info_alert,
    show_warning_alert,
    show_footer,
    get_cost_estimate,
    show_confidence_meter,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="DriveWise AI",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="auto",
)


# ============================================================
# LOAD UI STYLES
# ============================================================

load_styles()


# ============================================================
# LOCAL AI STATUS (checked once per session)
# ============================================================

if "ai_online" not in st.session_state:
    st.session_state["ai_online"] = check_ollama()


# ============================================================
# LOAD KNOWLEDGE BASE
# ============================================================

try:
    cars = pd.read_csv("data/cars.csv")
    issues = pd.read_csv("data/issues.csv")

except Exception as e:

    st.error(
        "Could not load the DriveWise knowledge base."
    )

    st.code(str(e))

    st.stop()


# ============================================================
# HEADER
# ============================================================

show_header(
    st.session_state["ai_online"],
    issues["symptom"].nunique(),
)

show_steps()


# ============================================================
# SYMPTOM ALIASES
# ============================================================

symptom_aliases = {

    "engine overheating": [
        "overheating",
        "overheat",
        "getting overheated",
        "engine is hot",
        "engine gets hot",
        "engine getting hot",
        "engine is getting hot",
        "running hot",
        "car is running hot",
        "temperature is high",
        "temperature keeps rising",
        "temperature gauge is high",
        "car is overheating",
        "car gets too hot",
        "car is getting too hot",
        "engine temperature",
    ],

    "battery not starting": [
        "battery dead",
        "dead battery",
        "car won't start",
        "car will not start",
        "engine won't start",
        "engine will not start",
        "not starting",
        "doesn't start",
        "does not start",
        "starting problem",
        "clicking when starting",
    ],

    "brake noise": [
        "brake noise",
        "brakes making noise",
        "brakes make noise",
        "brakes are making noise",
        "brakes squeaking",
        "brakes are squeaking",
        "brakes squeal",
        "brakes squealing",
        "brakes are squealing",
        "squeaky brakes",
        "squealing brakes",
        "brakes grinding",
        "brakes are grinding",
        "grinding noise when braking",
        "noise when braking",
        "noise from brakes",
        "braking noise",
    ],

    "engine shaking": [
        "engine shaking",
        "car shaking",
        "engine vibrating",
        "car vibrating",
        "vehicle shaking",
        "vehicle vibrating",
        "shaking while driving",
        "shaking when idling",
        "rough idle",
        "engine running rough",
    ],

    "car ac not cooling": [
        "ac not cooling",
        "ac isn't cooling",
        "ac is not cooling",
        "air conditioner not cooling",
        "air conditioning not cooling",
        "ac blowing warm air",
        "ac is blowing warm air",
        "ac blowing hot air",
        "ac is blowing hot air",
        "air conditioner blowing warm air",
        "air conditioner blowing hot air",
        "ac is warm",
        "ac feels warm",
        "car ac not cold",
        "car ac is not cold",
        "air conditioning is warm",
        "air conditioning blowing warm air",
    ],

    "low engine oil": [
        "low oil",
        "engine oil low",
        "oil level low",
        "oil is low",
        "not enough oil",
        "engine needs oil",
        "oil warning light",
        "oil light is on",
        "low oil warning",
    ],

    "suspension noise": [
        "suspension noise",
        "suspension knocking",
        "suspension knock",
        "khat khat noise",
        "clunking noise",
        "noise over bumps",
        "noise on speed breakers",
        "shock absorber noise",
    ],

    "poor fuel average": [
        "poor fuel average",
        "fuel average is low",
        "fuel average low",
        "average kam ho gaya",
        "mileage dropped",
        "low mileage",
        "using too much fuel",
        "fuel consumption is high",
    ],

    "exhaust smoke": [
        "exhaust smoke",
        "smoke from exhaust",
        "smoke from silencer",
        "smoke from tailpipe",
        "blue smoke",
        "black smoke",
        "white smoke",
        "car is smoking",
    ],
}


# ============================================================
# QUICK SYMPTOM CHIPS
# ============================================================

quick_symptoms = [
    ("🔥", "Overheating", "engine overheating"),
    ("🔋", "Won't Start", "battery not starting"),
    ("🛑", "Brake Noise", "brake noise"),
    ("🌀", "Shaking", "engine shaking"),
    ("❄️", "AC Not Cooling", "car AC not cooling"),
    ("🛢️", "Low Oil", "low engine oil"),
    ("🛞", "Suspension Noise", "suspension noise"),
    ("⛽", "Poor Fuel Average", "poor fuel average"),
    ("💨", "Exhaust Smoke", "exhaust smoke"),
]


# ============================================================
# VEHICLE SELECTION
# ============================================================

show_vehicle_section()


brands = (
    cars["brand"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

if not brands:
    st.error("No vehicle brands found in cars.csv.")
    st.stop()


brand = st.selectbox(
    "Select your car brand",
    brands,
)


brand_cars = cars[
    cars["brand"].astype(str) == str(brand)
]


models = (
    brand_cars["model"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

if not models:
    st.error("No models found for this brand.")
    st.stop()


model = st.selectbox(
    "Select your car model",
    models,
)


model_cars = brand_cars[
    brand_cars["model"].astype(str) == str(model)
]


years = (
    model_cars["year"]
    .dropna()
    .unique()
    .tolist()
)

if not years:
    st.error("No years found for this model.")
    st.stop()


year = st.selectbox(
    "Select your car year",
    years,
)


year_car = model_cars[
    model_cars["year"] == year
]

if year_car.empty:
    st.error("Vehicle information could not be found.")
    st.stop()


engine = year_car["engine"].iloc[0]


# ============================================================
# VEHICLE CARD
# ============================================================

show_vehicle_card(
    brand,
    model,
    year,
    engine,
)


# ============================================================
# PROBLEM DESCRIPTION
# ============================================================

show_problem_section()


if "problem_text" not in st.session_state:
    st.session_state["problem_text"] = ""


chip_phrase = show_symptom_chips(quick_symptoms)

if chip_phrase:

    current = st.session_state["problem_text"]

    if chip_phrase.lower() not in current.lower():

        st.session_state["problem_text"] = (
            f"{current}, {chip_phrase}"
            if current
            else chip_phrase
        )


problem = st.text_area(
    "Describe your symptoms",
    key="problem_text",
    placeholder=(
        "Example: My car starts shaking when I stop "
        "at a traffic light and the engine feels rough..."
    ),
    height=160,
    label_visibility="collapsed",
)


st.caption(
    "💡 Tip: Mention unusual sounds, warning lights, "
    "when the problem happens, and how long it has "
    "been happening."
)


# ============================================================
# DIAGNOSE BUTTON
# ============================================================

st.write("")

diagnose_clicked = st.button(
    "🔍 Diagnose Vehicle",
    type="primary",
    use_container_width=True,
)


# ============================================================
# KNOWLEDGE BASE SEARCH
# ============================================================

def find_matches(user_problem):
    """Return knowledge-base issues matching the problem text."""

    matches = []

    for _, issue in issues.iterrows():

        symptom = (
            str(issue["symptom"])
            .lower()
            .strip()
        )

        possible_phrases = symptom_aliases.get(
            symptom,
            [symptom],
        )

        matched = any(
            phrase in user_problem
            for phrase in possible_phrases
        )

        if matched:
            matches.append(issue.to_dict())

    return matches


def compute_match_confidence(user_problem, matches):
    """Percentage of the problem text covered by matched
    symptom phrases (longest phrase per category,
    overlapping matches not double-counted)."""

    if not matches or not user_problem:
        return 0

    covered_spans = []
    total = 0

    for issue in matches:

        symptom = (
            str(issue["symptom"])
            .lower()
            .strip()
        )

        phrases = symptom_aliases.get(symptom, [symptom])

        best = ""

        for phrase in phrases:

            if phrase in user_problem and len(phrase) > len(best):
                best = phrase

        if not best:
            continue

        start = user_problem.find(best)

        span = (start, start + len(best))

        overlaps = any(
            s < span[1] and span[0] < e
            for s, e in covered_spans
        )

        if not overlaps:
            covered_spans.append(span)
            total += len(best)

    if not covered_spans:
        return 0

    return min(
        100,
        round(100 * total / len(user_problem)),
    )


def build_knowledge_base_text(matches):

    if not matches:
        return (
            "No matching issue was found in the "
            "current knowledge base."
        )

    sections = []

    for issue in matches:

        sections.append(
            f"""
Possible Cause: {issue['possible_cause']}

Severity: {issue['severity']}

Recommended Action:
{issue['recommended_action']}

---
"""
        )

    return "".join(sections)


def build_ai_prompt(brand, model, year, engine, problem, kb_text):

    return f"""
You are DriveWise AI, an automotive troubleshooting assistant.

Vehicle:
Brand: {brand}
Model: {model}
Year: {year}
Engine: {engine}

Driver's reported problem:
{problem}

Relevant information from the DriveWise knowledge base:

{kb_text}

Based on the driver's problem and the knowledge base,
provide clear and practical troubleshooting guidance.

Use this structure:

### Most Likely Cause

Explain the most likely cause.

### Other Possible Causes

List other reasonable possibilities.

### What to Check

Give practical checks the driver can consider.

### Recommended Next Action

Explain what should happen next.

### Severity

State whether the issue appears Low, Medium, or High
and explain why.

### Safety Warning

Mention any important safety concern.

Important:

- This is troubleshooting guidance, not a definitive
  mechanical diagnosis.
- Do not claim certainty.
- Do not recommend unsafe repairs.
- Recommend professional inspection when appropriate.
- Use the knowledge base information as your primary source.
"""


def build_report_text(diagnosis):

    lines = [
        "=" * 52,
        "DRIVEWISE AI — VEHICLE DIAGNOSIS REPORT",
        "=" * 52,
        f"Generated: {datetime.now().strftime('%d %b %Y, %H:%M')}",
        "",
        "VEHICLE",
        "-" * 52,
        f"Brand:  {diagnosis['brand']}",
        f"Model:  {diagnosis['model']}",
        f"Year:   {diagnosis['year']}",
        f"Engine: {diagnosis['engine']}",
        "",
        "REPORTED PROBLEM",
        "-" * 52,
        diagnosis["problem"],
        "",
    ]

    matches = diagnosis["matches"]

    if matches:

        lines.append(
            f"KNOWLEDGE BASE MATCHES ({len(matches)})"
        )

        lines.append("-" * 52)

        for i, issue in enumerate(matches, 1):

            lines.append(
                f"{i}. {issue['possible_cause']} "
                f"[{str(issue['severity']).upper()}]"
            )

            lines.append(
                f"   Est. Repair Cost: "
                f"{get_cost_estimate(issue)}"
            )

            lines.append(
                f"   Recommended Action: "
                f"{issue['recommended_action']}"
            )

            lines.append("")

    else:

        lines.append("KNOWLEDGE BASE MATCHES")
        lines.append("-" * 52)
        lines.append(
            "No matching issue was found in the "
            "current knowledge base."
        )
        lines.append("")

    lines.append("AI ANALYSIS")
    lines.append("-" * 52)

    if diagnosis.get("ai_result"):
        lines.append(diagnosis["ai_result"])
    elif diagnosis.get("ai_status") == "error":
        lines.append(
            "AI analysis could not be completed for this "
            "report."
        )
    elif diagnosis.get("ai_status") == "empty":
        lines.append(
            "The local AI returned an empty response for this "
            "report."
        )
    elif diagnosis.get("ai_status") == "offline":
        lines.append(
            "AI analysis was unavailable because the local AI "
            "service was offline."
        )
    else:
        lines.append(
            "AI analysis was not available when this "
            "report was generated."
        )

    lines += [
        "",
        "=" * 52,
        "Troubleshooting guidance only — not a definitive",
        "mechanical diagnosis.",
        "Generated locally by DriveWise AI.",
    ]

    return "\n".join(lines)


# ============================================================
# RUN DIAGNOSIS
# ============================================================

if diagnose_clicked:

    if not problem.strip():

        show_warning_alert(
            "Please describe your car problem first."
        )

    else:

        matches = find_matches(
            problem.lower().strip()
        )

        st.session_state["diagnosis"] = {
            "brand": brand,
            "model": model,
            "year": year,
            "engine": engine,
            "problem": problem,
            "matches": matches,
            "confidence": compute_match_confidence(
                problem.lower().strip(),
                matches,
            ),
            "kb_text": build_knowledge_base_text(
                matches
            ),
            "ai_result": None,
            "ai_status": "pending",
            "ai_error": None,
        }

        # Record in session history (same object, so the
        # streamed AI result stays in the history entry)

        history = st.session_state.setdefault(
            "history", []
        )

        history[:] = [
            entry
            for entry in history
            if (
                entry["brand"],
                entry["model"],
                entry["year"],
                entry["problem"],
            )
            != (
                brand,
                model,
                year,
                problem,
            )
        ]

        history.append(
            st.session_state["diagnosis"]
        )

        if len(history) > 10:
            history[:] = history[-10:]


# ============================================================
# SHOW DIAGNOSIS (persists across widget changes)
# ============================================================

diagnosis = st.session_state.get("diagnosis")

if diagnosis is not None:

    st.divider()

    header_col, report_col, clear_col = st.columns([4, 1, 1])

    with header_col:
        show_diagnosis_header()

    with report_col:

        st.markdown(
            '<div style="height:30px;"></div>',
            unsafe_allow_html=True,
        )

        st.download_button(
            "⬇ Report",
            data=build_report_text(diagnosis),
            file_name=(
                f"drivewise_report_"
                f"{diagnosis['brand']}_"
                f"{diagnosis['model']}_"
                f"{diagnosis['year']}.txt"
            ).replace(" ", "_").lower(),
            mime="text/plain",
            use_container_width=True,
            key="download_report",
        )

    with clear_col:
        st.markdown(
            '<div style="height:30px;"></div>',
            unsafe_allow_html=True,
        )

        clear_clicked = st.button(
            "✕ Clear Results",
            key="clear_diagnosis",
        )

    if clear_clicked:
        st.session_state.pop("diagnosis", None)
        st.rerun()

    # ========================================================
    # CONFIDENCE METER
    # ========================================================

    show_confidence_meter(
        diagnosis.get("confidence", 0),
        bool(diagnosis["matches"]),
    )

    # ========================================================
    # VEHICLE + PROBLEM SUMMARY
    # ========================================================

    show_problem_summary(
        diagnosis["brand"],
        diagnosis["model"],
        diagnosis["year"],
        diagnosis["engine"],
        diagnosis["problem"],
    )

    # ========================================================
    # KNOWLEDGE BASE RESULTS
    # ========================================================

    show_knowledge_base_results(
        diagnosis["matches"]
    )

    # ========================================================
    # LOCAL AI
    # ========================================================

    st.divider()

    show_ai_section_header()

    ai_status = diagnosis.get("ai_status")

    if ai_status not in {
        "pending",
        "ok",
        "offline",
        "error",
        "empty",
    } or (
        ai_status == "ok" and not diagnosis.get("ai_result")
    ):
        ai_status = (
            "ok" if diagnosis.get("ai_result") else "pending"
        )
        diagnosis["ai_status"] = ai_status
        diagnosis.setdefault("ai_error", None)

    fresh_run = diagnose_clicked and problem.strip()
    retry_requested = st.session_state.pop(
        "retry_ai_requested", False
    )

    if ai_status == "pending" and (
        fresh_run or retry_requested
    ):
        st.session_state["ai_online"] = check_ollama()

        if not st.session_state["ai_online"]:
            diagnosis["ai_status"] = "offline"

        else:
            ai_prompt = build_ai_prompt(
                diagnosis["brand"],
                diagnosis["model"],
                diagnosis["year"],
                diagnosis["engine"],
                diagnosis["problem"],
                diagnosis["kb_text"],
            )

            try:
                with st.container(border=True):
                    show_card_header("🤖 AI Analysis")
                    with st.spinner("Analyzing with local AI…"):
                        ai_result = st.write_stream(
                            stream_ai_diagnosis(ai_prompt)
                        )

            except Exception as exc:
                diagnosis["ai_result"] = None
                diagnosis["ai_status"] = "error"
                diagnosis["ai_error"] = (
                    f"{type(exc).__name__}: {exc}"
                )[:200]

            else:
                ai_result = str(ai_result).strip()

                if ai_result:
                    diagnosis["ai_result"] = ai_result
                    diagnosis["ai_status"] = "ok"
                    diagnosis["ai_error"] = None
                    st.rerun()

                else:
                    diagnosis["ai_status"] = "empty"
                    diagnosis["ai_error"] = (
                        "The local model returned no text."
                    )

        ai_status = diagnosis["ai_status"]

    if ai_status == "ok":
        with st.container(border=True):
            show_card_header("🤖 AI Analysis")
            st.markdown(diagnosis["ai_result"])

    elif ai_status == "offline":
        show_ai_unavailable()

    elif ai_status == "error":
        show_ai_unavailable(
            "AI analysis could not be completed. The knowledge-"
            "base results above are still available.",
            diagnosis.get("ai_error"),
        )

    elif ai_status == "empty":
        show_ai_unavailable(
            "The local AI returned an empty response. The knowledge-"
            "base results above are still available.",
            diagnosis.get("ai_error"),
        )

    else:
        show_info_alert(
            "AI analysis has not been run for this diagnosis yet."
        )

    if ai_status != "ok" and st.button(
        "🔄 Retry AI Analysis",
        key="retry_ai_analysis",
    ):
        diagnosis["ai_result"] = None
        diagnosis["ai_status"] = "pending"
        diagnosis["ai_error"] = None
        st.session_state["retry_ai_requested"] = True
        st.rerun()


# ============================================================
# DIAGNOSIS HISTORY (SIDEBAR)
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="dw-sidebar-title">🕘 Diagnosis History</div>',
        unsafe_allow_html=True,
    )

    history = st.session_state.get("history", [])

    if not history:

        st.caption(
            "Your diagnoses this session will "
            "appear here."
        )

    else:

        for i, entry in enumerate(reversed(history)):

            snippet = entry["problem"][:38]

            if len(entry["problem"]) > 38:
                snippet += "…"

            if st.button(
                f"{entry['brand']} {entry['model']} — {snippet}",
                key=f"history_{i}",
                use_container_width=True,
            ):
                st.session_state["diagnosis"] = entry
                st.rerun()

        st.write("")

        if st.button(
            "🗑 Clear History",
            key="clear_history",
            use_container_width=True,
        ):
            st.session_state["history"] = []
            st.rerun()


# ============================================================
# MAINTENANCE SCHEDULE
# ============================================================

show_maintenance_section(
    f"{brand} {model} ({year})"
)


# ============================================================
# FOOTER
# ============================================================

show_footer()
