import html

import streamlit as st


# HTML passed through st.markdown must not contain blank
# lines or indented blocks: the markdown parser turns those
# into code blocks and breaks the markup.


def _esc(value):
    return html.escape(str(value))


def _esc_multiline(value):
    return _esc(value).replace("\r\n", "\n").replace("\n", "<br>")


def _md(markup):
    st.markdown(markup, unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

def show_header(ai_online, category_count):

    if ai_online:

        status = (
            '<span class="dw-status-badge">'
            '<span class="dw-status-dot"></span>'
            'Local AI Assistant Ready'
            '</span>'
        )

    else:

        status = (
            '<span class="dw-status-badge offline">'
            '<span class="dw-status-dot"></span>'
            'Local AI Offline — start Ollama to enable AI analysis'
            '</span>'
        )

    _md(
        '<div class="dw-hero">'
        '<h1 class="dw-hero-title">DriveWise <span>AI</span></h1>'
        '<div class="dw-hero-subtitle">'
        'Smart vehicle diagnosis assistant — describe your '
        'symptoms and get trusted troubleshooting guidance.'
        '</div>'
        f'{status}'
        '<div class="dw-hero-stats">'
        '<div class="dw-stat">'
        '<div class="dw-stat-icon">🛡️</div>'
        '<div class="dw-stat-value">100% Local</div>'
        '<div class="dw-stat-label">Private, on-device analysis</div>'
        '</div>'
        '<div class="dw-stat">'
        '<div class="dw-stat-icon">📋</div>'
        f'<div class="dw-stat-value">{category_count} Categories</div>'
        '<div class="dw-stat-label">Symptom knowledge base</div>'
        '</div>'
        '<div class="dw-stat">'
        '<div class="dw-stat-icon">⚡</div>'
        '<div class="dw-stat-value">Instant</div>'
        '<div class="dw-stat-label">AI-powered guidance</div>'
        '</div>'
        '</div>'
        '</div>'
    )


# ============================================================
# STEPS
# ============================================================

def show_steps():

    _md(
        '<div class="dw-steps">'
        '<span class="dw-step">'
        '<span class="dw-step-num">1</span>'
        'Select Vehicle'
        '</span>'
        '<span class="dw-step">'
        '<span class="dw-step-num">2</span>'
        'Describe Problem'
        '</span>'
        '<span class="dw-step">'
        '<span class="dw-step-num">3</span>'
        'Get Diagnosis'
        '</span>'
        '</div>'
    )


# ============================================================
# SECTION HELPERS
# ============================================================

def _show_section(title, hint):

    _md(
        f'<div class="dw-section-title">{_esc(title)}</div>'
        f'<div class="dw-section-hint">{_esc(hint)}</div>'
    )


# ============================================================
# VEHICLE SECTION
# ============================================================

def show_vehicle_section():

    _show_section(
        "🚘 Select Your Vehicle",
        "Select your vehicle so DriveWise AI can provide "
        "relevant troubleshooting guidance.",
    )


def show_vehicle_card(brand, model, year, engine):

    tiles = [
        ("Brand", brand),
        ("Model", model),
        ("Year", year),
        ("Engine", engine),
    ]

    tiles_html = "".join(
        '<div class="dw-vehicle-tile">'
        f'<div class="dw-vehicle-tile-label">{_esc(label)}</div>'
        f'<div class="dw-vehicle-tile-value">{_esc(value)}</div>'
        '</div>'
        for label, value in tiles
    )

    _md(
        '<div class="dw-card">'
        '<div class="dw-card-header">🚗 Your Vehicle</div>'
        f'<div class="dw-vehicle-grid">{tiles_html}</div>'
        '</div>'
    )


# ============================================================
# PROBLEM SECTION
# ============================================================

def show_problem_section():

    _show_section(
        "🔧 Describe Your Problem",
        "Tap a quick symptom below or describe the issue in "
        "your own words — unusual sounds, warning lights, when "
        "it happens, and how long it has been happening.",
    )


def show_symptom_chips(chips):
    """Render quick-symptom buttons. Returns the phrase of the
    clicked chip, or None."""

    clicked = None

    rows = [chips[i:i + 3] for i in range(0, len(chips), 3)]

    for row in rows:

        columns = st.columns(3)

        for column, chip in zip(columns, row):

            icon, label, phrase = chip

            if column.button(
                f"{icon} {label}",
                use_container_width=True,
            ):
                clicked = phrase

    return clicked


# ============================================================
# DIAGNOSIS SECTION
# ============================================================

def show_diagnosis_header():

    _show_section(
        "🔍 Diagnosis",
        "Analysis based on your vehicle and reported symptoms.",
    )


def show_problem_summary(brand, model, year, engine, problem):

    _md(
        '<div class="dw-card">'
        '<div class="dw-card-header">📋 Report Summary</div>'
        f'<div class="dw-summary-line">'
        f'{_esc(brand)} {_esc(model)} • '
        f'{_esc(year)} • {_esc(engine)}'
        '</div>'
        '<div class="dw-summary-divider"></div>'
        '<div class="dw-result-label">Reported Problem</div>'
        f'<div class="dw-summary-problem">'
        f'{_esc_multiline(problem)}'
        '</div>'
        '</div>'
    )


COST_ESTIMATES = {
    "Low coolant": "PKR 2,000 – 6,000",
    "Thermostat failure": "PKR 5,000 – 18,000",
    "Radiator problem": "PKR 12,000 – 45,000",
    "Cooling fan failure": "PKR 6,000 – 25,000",
    "Clogged radiator fins": "PKR 1,500 – 6,000",
    "Blocked or collapsed radiator hose": "PKR 2,500 – 10,000",
    "Loose or worn drive belt": "PKR 2,000 – 9,000",
    "Weak battery": "PKR 15,000 – 38,000",
    "Corroded battery terminals": "PKR 500 – 2,500",
    "Parasitic battery drain": "PKR 2,500 – 12,000",
    "Faulty alternator charging": "PKR 8,000 – 40,000",
    "Worn starter motor": "PKR 7,000 – 35,000",
    "Worn brake pads": "PKR 8,000 – 30,000",
    "Brake dust or debris": "PKR 500 – 3,000",
    "Warped brake discs": "PKR 10,000 – 40,000",
    "Worn rear brake shoes": "PKR 4,000 – 15,000",
    "Spark plug problem": "PKR 3,000 – 15,000",
    "Engine misfire": "PKR 6,000 – 35,000",
    "CNG system tuning issue": "PKR 2,000 – 10,000",
    "Worn engine mounts": "PKR 6,000 – 30,000",
    "Contaminated or low-grade fuel": "PKR 3,000 – 20,000",
    "Low refrigerant": "PKR 3,000 – 12,000",
    "AC compressor problem": "PKR 20,000 – 90,000",
    "Condenser fan failure": "PKR 5,000 – 20,000",
    "Clogged AC condenser": "PKR 1,500 – 5,000",
    "Clogged cabin air filter": "PKR 1,000 – 4,000",
    "Oil leak": "PKR 4,000 – 50,000",
    "Insufficient oil": "PKR 3,000 – 12,000",
    "Worn suspension bushes": "PKR 5,000 – 25,000",
    "Worn shock absorbers": "PKR 15,000 – 75,000",
    "Damaged strut mounts": "PKR 5,000 – 30,000",
    "Worn tie rod ends": "PKR 4,000 – 18,000",
    "Dirty air filter": "PKR 1,000 – 7,000",
    "Under-inflated tyres": "PKR 500 – 2,000",
    "Dirty fuel injectors": "PKR 5,000 – 30,000",
    "Dragging brakes": "PKR 5,000 – 25,000",
    "Overdue oil change interval": "PKR 4,000 – 15,000",
    "Engine oil burning": "PKR 30,000 – 200,000",
    "Rich fuel mixture": "PKR 6,000 – 35,000",
    "Coolant entering engine": "PKR 40,000 – 250,000",
}

SEVERITY_COST_FALLBACK = {
    "low": "PKR 1,000 – 8,000",
    "medium": "PKR 4,000 – 35,000",
    "high": "PKR 20,000 – 200,000",
}


def get_cost_estimate(issue):
    """Rough repair cost range for a matched issue."""

    cause = str(issue.get("possible_cause", "")).strip()

    if cause in COST_ESTIMATES:
        return COST_ESTIMATES[cause]

    return SEVERITY_COST_FALLBACK.get(
        str(issue.get("severity", "")).lower().strip(),
        "Varies",
    )


# ============================================================
# CONFIDENCE METER
# ============================================================

def show_confidence_meter(percent, has_matches):

    if not has_matches:

        _md(
            '<div class="dw-meter-wrap">'
            '<div class="dw-meter-head">'
            '<span>Symptom Match</span>'
            '<span class="dw-meter-value muted">No match</span>'
            '</div>'
            '<div class="dw-meter">'
            '<div class="dw-meter-fill none" style="width:0%"></div>'
            '</div>'
            '<div class="dw-meter-note">'
            'None of your description matched the knowledge '
            'base — the AI will analyze it directly.'
            '</div>'
            '</div>'
        )

        return

    if percent >= 70:
        level = "high"

    elif percent >= 40:
        level = "medium"

    else:
        level = "low"

    _md(
        '<div class="dw-meter-wrap">'
        '<div class="dw-meter-head">'
        '<span>Symptom Match</span>'
        f'<span class="dw-meter-value">{percent}%</span>'
        '</div>'
        '<div class="dw-meter">'
        f'<div class="dw-meter-fill {level}" '
        f'style="width:{percent}%"></div>'
        '</div>'
        '<div class="dw-meter-note">'
        'Share of your description recognized by the '
        'knowledge base.'
        '</div>'
        '</div>'
    )


def _severity_pill(severity):

    level = str(severity).lower()

    if level == "high":
        css_class = "high"
        label = "HIGH"

    elif level == "medium":
        css_class = "medium"
        label = "MEDIUM"

    else:
        css_class = "low"
        label = "LOW"

    return (
        f'<span class="dw-pill dw-pill-{css_class}">'
        f'<span class="dw-pill-dot"></span>{label}</span>'
    )


def show_knowledge_base_results(matches):

    _show_section(
        "🔧 Knowledge Base Matches",
        "Known issues that match your reported symptoms.",
    )

    if not matches:

        show_info_alert(
            "No matching issue was found in the current knowledge "
            "base. The local AI will still analyze your problem."
        )

        return

    for issue in matches:

        severity = issue["severity"]

        _md(
            '<div class="dw-card">'
            '<div class="dw-result-head">'
            f'<div class="dw-result-title">'
            f'{_esc(issue["possible_cause"])}'
            '</div>'
            f'<div class="dw-result-meta">'
            f'{_severity_pill(severity)}'
            f'<span class="dw-cost-chip">'
            f'💰 {_esc(get_cost_estimate(issue))}'
            '</span>'
            '</div>'
            '</div>'
            '<div class="dw-result-block">'
            '<div class="dw-result-label">Recommended Action</div>'
            f'<div class="dw-result-text">'
            f'{_esc_multiline(issue["recommended_action"])}'
            '</div>'
            '</div>'
            '</div>'
        )

    st.caption(
        "💡 PKR cost ranges are rough estimates — actual "
        "prices vary by city, workshop, and parts quality."
    )

    high_severity = any(
        str(issue["severity"]).lower() == "high"
        for issue in matches
    )

    if high_severity:

        _md(
            '<div class="dw-alert dw-alert-high">'
            '<span class="dw-alert-icon">⚠️</span>'
            '<span><b>Safety Warning:</b> This issue may require '
            'professional inspection. If the vehicle is '
            'overheating, smoking, leaking fluids, or showing '
            'warning lights, stop driving when it is safe '
            'to do so.</span>'
            '</div>'
        )


# ============================================================
# AI SECTION
# ============================================================

def show_ai_section_header():

    _show_section(
        "🤖 AI Analysis",
        "Generated locally from your vehicle, symptoms, and "
        "knowledge base matches.",
    )


def show_card_header(title):

    _md(
        f'<div class="dw-card-header">{_esc(title)}</div>'
    )


def show_ai_unavailable(message=None, detail=None):

    if message:

        show_warning_alert(message)

        if detail:

            st.caption(f"Details: {detail}")

        return

    show_info_alert(
        "Local AI is currently unavailable. Start Ollama and "
        "run the diagnosis again. The knowledge-base results "
        "above are still available."
    )


# ============================================================
# ALERTS
# ============================================================

def show_info_alert(message):

    _md(
        '<div class="dw-alert dw-alert-info">'
        '<span class="dw-alert-icon">ℹ️</span>'
        f'<span>{_esc(message)}</span>'
        '</div>'
    )


def show_warning_alert(message):

    _md(
        '<div class="dw-alert dw-alert-warning">'
        '<span class="dw-alert-icon">⚠️</span>'
        f'<span>{_esc(message)}</span>'
        '</div>'
    )


# ============================================================
# FOOTER
# ============================================================

def show_footer():

    _md(
        '<div class="dw-footer">'
        '<div class="dw-footer-brand">🚗 DriveWise AI</div>'
        '<div class="dw-footer-text">'
        'Local AI Vehicle Troubleshooting Assistant'
        '</div>'
        '<div class="dw-footer-text">'
        'Troubleshooting guidance only — not a definitive '
        'mechanical diagnosis.'
        '</div>'
        '</div>'
    )
