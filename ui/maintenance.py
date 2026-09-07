import streamlit as st

from ui.components import _show_section


MAINTENANCE_SCHEDULE = [
    ("Engine oil & filter", 10_000),
    ("Tire rotation & pressure check", 10_000),
    ("Air filter", 20_000),
    ("Cabin (AC) filter", 20_000),
    ("Brake pads & discs inspection", 20_000),
    ("Battery health check", 20_000),
    ("Brake fluid replacement", 40_000),
    ("Spark plugs", 60_000),
    ("Engine coolant replacement", 60_000),
    ("Transmission fluid", 60_000),
    ("Timing belt", 100_000),
]


def _service_row(name, interval_km, current_km):

    next_due = (current_km // interval_km + 1) * interval_km

    due_in = next_due - current_km

    soon_threshold = max(1_000, int(interval_km * 0.1))

    if due_in <= soon_threshold:
        pill = (
            '<span class="dw-pill dw-pill-medium">'
            '<span class="dw-pill-dot"></span>DUE SOON</span>'
        )

    else:
        pill = (
            '<span class="dw-pill dw-pill-low">'
            '<span class="dw-pill-dot"></span>OK</span>'
        )

    return (
        '<div class="dw-maint-row">'
        f'<div class="dw-maint-name">{name}</div>'
        f'<div class="dw-maint-info">{pill}'
        f'<span class="dw-maint-due">'
        f'next at {next_due:,} km '
        f'(in {due_in:,} km)'
        '</span></div>'
        '</div>'
    )


def show_maintenance_section(vehicle_label):

    _show_section(
        "🛠️ Maintenance Schedule",
        f"Standard service intervals for your "
        f"{vehicle_label}. Enter your current mileage "
        f"to see what is coming up next.",
    )

    current_km = st.number_input(
        "Current mileage (km)",
        min_value=0,
        max_value=1_000_000,
        step=1_000,
        key="mileage_km",
    )

    if current_km <= 0:

        st.caption(
            "Enter your odometer reading above to see "
            "upcoming services."
        )

        return

    rows = "".join(
        _service_row(name, interval, int(current_km))
        for name, interval in MAINTENANCE_SCHEDULE
    )

    st.markdown(
        '<div class="dw-card">'
        f'<div class="dw-card-header">🗓️ Upcoming Services — '
        f'{int(current_km):,} km</div>'
        f'{rows}'
        '</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "💡 Generic intervals assuming each service was "
        "last done on schedule — always follow your "
        "manufacturer's service manual."
    )
