import base64
from functools import lru_cache
from pathlib import Path

import streamlit as st


@lru_cache(maxsize=1)
def _hero_image_data_uri():

    image_path = (
        Path(__file__).resolve().parent.parent
        / "assets"
        / "car-hero.jpg"
    )

    encoded = base64.b64encode(
        image_path.read_bytes()
    ).decode("utf-8")

    return f"data:image/jpeg;base64,{encoded}"


def load_styles():

    st.markdown(
        """
        <style>
        :root {

            --dw-bg: #0A0E13;
            --dw-surface: #111823;
            --dw-surface-2: #16202D;
            --dw-border: #243244;

            --dw-ink: #F0F6FC;
            --dw-body: #C5D1DE;
            --dw-muted: #8B9BAB;

            --dw-brand: #22C55E;
            --dw-brand-strong: #16A34A;
            --dw-brand-glow: rgba(34, 197, 94, 0.32);
            --dw-brand-tint: rgba(34, 197, 94, 0.09);
            --dw-brand-border: rgba(34, 197, 94, 0.38);
            --dw-brand-text: #6EE7A0;
            --dw-brand-dark: #0E5C33;

            --dw-low-bg: rgba(34, 197, 94, 0.12);
            --dw-low-text: #6EE7A0;
            --dw-low-border: rgba(34, 197, 94, 0.42);

            --dw-medium-bg: rgba(245, 158, 11, 0.12);
            --dw-medium-text: #FBBF24;
            --dw-medium-border: rgba(245, 158, 11, 0.42);

            --dw-high-bg: rgba(239, 68, 68, 0.12);
            --dw-high-text: #F87171;
            --dw-high-border: rgba(239, 68, 68, 0.48);

            --dw-info-bg: rgba(59, 130, 246, 0.10);
            --dw-info-text: #93C5FD;
            --dw-info-border: rgba(59, 130, 246, 0.38);
        }


        /* ================================
           MAIN PAGE
        ================================= */

        html, body, .stApp, .stApp [class] {
            font-family: -apple-system, BlinkMacSystemFont,
                "Segoe UI", Inter, Roboto, "Helvetica Neue",
                Arial, sans-serif;
        }

        .stApp {
            background:
                radial-gradient(
                    1100px 500px at 85% -10%,
                    rgba(34, 197, 94, 0.07),
                    transparent 60%
                ),
                var(--dw-bg);
        }

        .main .block-container,
        div[data-testid="stMainBlockContainer"] {
            max-width: 1060px;
            padding-top: 2.2rem;
            padding-bottom: 4rem;
        }

        #MainMenu, footer {
            visibility: hidden;
        }

        hr {
            border-color: var(--dw-border) !important;
        }

        div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stMarkdownContainer"] li {
            color: var(--dw-body);
        }

        div[data-testid="stMarkdownContainer"] strong {
            color: var(--dw-ink);
        }


        /* ================================
           HERO
        ================================= */

        .dw-hero {
            position: relative;
            border-radius: 24px;
            overflow: hidden;
            min-height: 400px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 60px 40px;
            text-align: center;
            color: #FFFFFF;
            background-color: var(--dw-bg);
            background-image:
                linear-gradient(
                    180deg,
                    rgba(10, 14, 19, 0.62) 0%,
                    rgba(10, 14, 19, 0.55) 40%,
                    rgba(10, 14, 19, 0.88) 78%,
                    #0A0E13 100%
                ),
                url("__HERO_URI__");
            background-size: cover;
            background-position: center 30%;
            box-shadow:
                0 24px 60px rgba(0, 0, 0, 0.55),
                0 0 0 1px rgba(34, 197, 94, 0.14);
        }

        .dw-hero-title {
            font-size: 46px;
            font-weight: 800;
            letter-spacing: -1.3px;
            color: #FFFFFF;
            margin: 0;
            text-shadow: 0 2px 18px rgba(0, 0, 0, 0.65);
        }

        .dw-hero-title span {
            color: var(--dw-brand-text);
        }

        .dw-hero-subtitle {
            font-size: 16.5px;
            color: rgba(240, 246, 252, 0.88);
            margin-top: 10px;
            line-height: 1.55;
            max-width: 560px;
            margin-left: auto;
            margin-right: auto;
            text-shadow: 0 1px 10px rgba(0, 0, 0, 0.7);
        }

        .dw-status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-top: 20px;
            padding: 7px 16px;
            border-radius: 50px;
            background: rgba(10, 14, 19, 0.55);
            border: 1px solid rgba(34, 197, 94, 0.45);
            backdrop-filter: blur(6px);
            font-size: 13px;
            font-weight: 700;
            color: #FFFFFF;
        }

        .dw-status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #4ADE80;
            box-shadow: 0 0 0 4px rgba(74, 222, 128, 0.25);
        }

        .dw-status-badge.offline {
            border-color: rgba(248, 113, 113, 0.5);
        }

        .dw-status-badge.offline .dw-status-dot {
            background: #F87171;
            box-shadow: 0 0 0 4px rgba(248, 113, 113, 0.22);
        }

        .dw-hero-stats {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 34px;
            padding-top: 24px;
            border-top: 1px solid rgba(255, 255, 255, 0.16);
        }

        .dw-stat {
            flex: 1;
            min-width: 170px;
            padding: 2px 14px;
        }

        .dw-stat + .dw-stat {
            border-left: 1px solid rgba(255, 255, 255, 0.16);
        }

        .dw-stat-icon {
            font-size: 21px;
        }

        .dw-stat-value {
            font-size: 19px;
            font-weight: 800;
            color: #FFFFFF;
            margin-top: 5px;
        }

        .dw-stat-label {
            font-size: 12.5px;
            color: rgba(240, 246, 252, 0.72);
            margin-top: 2px;
        }


        /* ================================
           STEPS
        ================================= */

        .dw-steps {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 24px 0 4px;
        }

        .dw-step {
            display: inline-flex;
            align-items: center;
            gap: 9px;
            padding: 7px 15px;
            border-radius: 50px;
            background: var(--dw-surface);
            border: 1px solid var(--dw-border);
            font-size: 13px;
            font-weight: 600;
            color: var(--dw-body);
        }

        .dw-step-num {
            width: 22px;
            height: 22px;
            border-radius: 50%;
            background: var(--dw-brand-tint);
            color: var(--dw-brand-text);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: 800;
        }


        /* ================================
           SECTION HEADINGS
        ================================= */

        .dw-section-title {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 25px;
            font-weight: 800;
            color: var(--dw-ink);
            letter-spacing: -0.4px;
            margin-top: 36px;
        }

        .dw-section-title::before {
            content: "";
            width: 5px;
            height: 26px;
            border-radius: 3px;
            background: linear-gradient(
                180deg, var(--dw-brand), var(--dw-brand-dark)
            );
            flex-shrink: 0;
            box-shadow: 0 0 12px var(--dw-brand-glow);
        }

        .dw-section-hint {
            font-size: 14px;
            color: var(--dw-muted);
            line-height: 1.55;
            margin: 8px 0 18px;
        }


        /* ================================
           BUTTONS
        ================================= */

        div[data-testid="stButton"] > button[kind="primary"],
        div[data-testid="stButton"] > button[data-testid="baseButton-primary"] {
            background: linear-gradient(
                180deg, #26A85C 0%, #16A34A 100%
            ) !important;
            border: 1px solid rgba(34, 197, 94, 0.55) !important;
            color: #FFFFFF !important;
            width: 100%;
            min-height: 56px;
            border-radius: 14px !important;
            font-size: 17px !important;
            font-weight: 750 !important;
            box-shadow:
                0 12px 28px var(--dw-brand-glow),
                inset 0 1px 0 rgba(255, 255, 255, 0.18);
            transition: filter 0.15s ease;
        }

        div[data-testid="stButton"] > button[kind="primary"]:hover,
        div[data-testid="stButton"] > button[data-testid="baseButton-primary"]:hover {
            filter: brightness(1.12);
        }

        div[data-testid="stButton"] > button[kind="secondary"],
        div[data-testid="stButton"] > button[data-testid="baseButton-secondary"] {
            background: var(--dw-surface) !important;
            border: 1.5px solid var(--dw-brand-border) !important;
            color: var(--dw-brand-text) !important;
            border-radius: 50px !important;
            font-size: 13.5px !important;
            font-weight: 650 !important;
            min-height: 38px;
            padding: 4px 16px !important;
            transition: background 0.15s ease, border-color 0.15s ease;
        }

        div[data-testid="stButton"] > button[kind="secondary"]:hover,
        div[data-testid="stButton"] > button[data-testid="baseButton-secondary"]:hover {
            background: var(--dw-brand-tint) !important;
            border-color: var(--dw-brand) !important;
        }

        div[data-testid="stDownloadButton"] > button {
            background: var(--dw-surface) !important;
            border: 1.5px solid var(--dw-brand-border) !important;
            color: var(--dw-brand-text) !important;
            border-radius: 50px !important;
            font-size: 13.5px !important;
            font-weight: 650 !important;
            min-height: 38px;
            padding: 4px 12px !important;
            transition: background 0.15s ease, border-color 0.15s ease;
        }

        div[data-testid="stDownloadButton"] > button:hover {
            background: var(--dw-brand-tint) !important;
            border-color: var(--dw-brand) !important;
        }


        /* ================================
           INPUTS
        ================================= */

        div[data-testid="stSelectbox"] label,
        div[data-testid="stTextArea"] label {
            font-size: 13px !important;
            font-weight: 650 !important;
            color: #C5D1DE !important;
            margin-bottom: 4px !important;
        }

        div[data-baseweb="select"] > div {
            border-radius: 12px;
            min-height: 46px;
            border-color: var(--dw-border) !important;
            background: var(--dw-surface);
        }

        div[data-baseweb="select"]:focus-within > div {
            border-color: var(--dw-brand) !important;
            box-shadow: 0 0 0 3px var(--dw-brand-tint) !important;
        }

        div[data-testid="stTextArea"] textarea {
            border-radius: 14px;
            border-color: var(--dw-border);
            font-size: 15px;
            line-height: 1.55;
            background: var(--dw-surface);
            color: var(--dw-ink);
        }

        div[data-testid="stTextArea"] textarea::placeholder {
            color: var(--dw-muted);
        }

        div[data-testid="stTextArea"] textarea:focus {
            border-color: var(--dw-brand) !important;
            box-shadow: 0 0 0 3px var(--dw-brand-tint) !important;
        }

        div[data-testid="stCaptionContainer"] {
            color: var(--dw-muted) !important;
        }


        /* ================================
           CARDS
        ================================= */

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 18px;
            border: 1px solid var(--dw-border);
            background: var(--dw-surface);
            box-shadow: 0 10px 34px rgba(0, 0, 0, 0.35);
        }

        .dw-card {
            background: var(--dw-surface);
            border: 1px solid var(--dw-border);
            border-radius: 18px;
            padding: 22px 24px;
            box-shadow: 0 10px 34px rgba(0, 0, 0, 0.35);
            margin-bottom: 14px;
        }

        .dw-card-header {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 16px;
            font-weight: 750;
            color: var(--dw-brand-text);
            margin-bottom: 16px;
        }

        .dw-vehicle-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
        }

        .dw-vehicle-tile {
            flex: 1;
            min-width: 150px;
            background: var(--dw-brand-tint);
            border: 1px solid var(--dw-brand-border);
            border-radius: 14px;
            padding: 13px 16px;
        }

        .dw-vehicle-tile-label {
            font-size: 11px;
            font-weight: 750;
            letter-spacing: 0.07em;
            text-transform: uppercase;
            color: var(--dw-brand-text);
            opacity: 0.75;
        }

        .dw-vehicle-tile-value {
            font-size: 17px;
            font-weight: 750;
            color: var(--dw-ink);
            margin-top: 4px;
        }


        /* ================================
           CONFIDENCE METER
        ================================= */

        .dw-meter-wrap {
            margin: 4px 0 18px;
        }

        .dw-meter-head {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            font-size: 13.5px;
            font-weight: 700;
            color: var(--dw-body);
            margin-bottom: 7px;
        }

        .dw-meter-value {
            font-size: 15px;
            font-weight: 800;
            color: var(--dw-ink);
        }

        .dw-meter-value.muted {
            color: var(--dw-muted);
            font-size: 13px;
            font-weight: 700;
        }

        .dw-meter {
            height: 10px;
            border-radius: 50px;
            background: var(--dw-surface-2);
            border: 1px solid var(--dw-border);
            overflow: hidden;
        }

        .dw-meter-fill {
            height: 100%;
            border-radius: 50px;
            transition: width 0.4s ease;
        }

        .dw-meter-fill.high {
            background: linear-gradient(90deg, #16A34A, #4ADE80);
            box-shadow: 0 0 10px var(--dw-brand-glow);
        }

        .dw-meter-fill.medium {
            background: linear-gradient(90deg, #D97706, #FBBF24);
        }

        .dw-meter-fill.low {
            background: linear-gradient(90deg, #DC2626, #F87171);
        }

        .dw-meter-fill.none {
            background: transparent;
        }

        .dw-meter-note {
            font-size: 12px;
            color: var(--dw-muted);
            margin-top: 6px;
        }


        /* ================================
           SEVERITY PILLS
        ================================= */

        .dw-pill {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            padding: 4px 13px;
            border-radius: 50px;
            font-size: 12px;
            font-weight: 750;
            letter-spacing: 0.05em;
            white-space: nowrap;
        }

        .dw-pill-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: currentColor;
            box-shadow: 0 0 8px currentColor;
        }

        .dw-pill-low {
            background: var(--dw-low-bg);
            color: var(--dw-low-text);
            border: 1px solid var(--dw-low-border);
        }

        .dw-pill-medium {
            background: var(--dw-medium-bg);
            color: var(--dw-medium-text);
            border: 1px solid var(--dw-medium-border);
        }

        .dw-pill-high {
            background: var(--dw-high-bg);
            color: var(--dw-high-text);
            border: 1px solid var(--dw-high-border);
        }


        /* ================================
           RESULT CARDS
        ================================= */

        .dw-result-head {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 14px;
        }

        .dw-result-meta {
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 7px;
            flex-shrink: 0;
        }

        .dw-cost-chip {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            font-size: 12.5px;
            font-weight: 650;
            color: var(--dw-brand-text);
            background: var(--dw-brand-tint);
            border: 1px solid var(--dw-brand-border);
            border-radius: 50px;
            padding: 4px 12px;
            white-space: nowrap;
        }

        .dw-result-title {
            font-size: 17px;
            font-weight: 750;
            color: var(--dw-ink);
            line-height: 1.35;
        }

        .dw-result-block {
            margin-top: 14px;
        }

        .dw-result-label {
            font-size: 11px;
            font-weight: 750;
            letter-spacing: 0.07em;
            text-transform: uppercase;
            color: var(--dw-muted);
        }

        .dw-result-text {
            font-size: 14.5px;
            color: var(--dw-body);
            line-height: 1.6;
            margin-top: 4px;
        }

        .dw-summary-line {
            font-size: 15.5px;
            font-weight: 650;
            color: var(--dw-ink);
        }

        .dw-summary-problem {
            font-size: 14.5px;
            color: var(--dw-body);
            line-height: 1.6;
            white-space: pre-wrap;
        }

        .dw-summary-divider {
            border-top: 1px solid var(--dw-border);
            margin: 16px 0;
        }


        /* ================================
           ALERTS
        ================================= */

        .dw-alert {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            border-radius: 14px;
            padding: 14px 18px;
            font-size: 14px;
            line-height: 1.55;
            margin: 12px 0;
        }

        .dw-alert-icon {
            font-size: 17px;
            line-height: 1.3;
        }

        .dw-alert-info {
            background: var(--dw-info-bg);
            border: 1px solid var(--dw-info-border);
            color: var(--dw-info-text);
        }

        .dw-alert-warning {
            background: var(--dw-medium-bg);
            border: 1px solid var(--dw-medium-border);
            color: var(--dw-medium-text);
        }

        .dw-alert-high {
            background: var(--dw-high-bg);
            border: 1px solid var(--dw-high-border);
            color: var(--dw-high-text);
        }


        /* ================================
           AI REPORT
        ================================= */

        div[data-testid="stMarkdownContainer"] h3 {
            color: var(--dw-brand-text);
            font-weight: 800;
            font-size: 18px;
            letter-spacing: -0.2px;
            border-bottom: 2px solid var(--dw-brand-tint);
            padding-bottom: 6px;
            margin-top: 22px;
        }


        /* ================================
           MAINTENANCE SCHEDULE
        ================================= */

        .dw-maint-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 14px;
            padding: 11px 0;
            border-bottom: 1px solid var(--dw-border);
            flex-wrap: wrap;
        }

        .dw-maint-row:last-child {
            border-bottom: none;
        }

        .dw-maint-name {
            font-size: 14.5px;
            font-weight: 650;
            color: var(--dw-ink);
        }

        .dw-maint-info {
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }

        .dw-maint-due {
            font-size: 12.5px;
            color: var(--dw-muted);
            white-space: nowrap;
        }


        /* ================================
           SIDEBAR
        ================================= */

        .dw-sidebar-title {
            font-size: 18px;
            font-weight: 800;
            color: var(--dw-ink);
            letter-spacing: -0.3px;
            margin-bottom: 4px;
        }

        section[data-testid="stSidebar"] {
            background: var(--dw-surface);
            border-right: 1px solid var(--dw-border);
        }

        section[data-testid="stSidebar"] .stButton > button {
            text-align: left !important;
            white-space: normal !important;
            line-height: 1.35 !important;
            min-height: 44px !important;
        }


        /* ================================
           FOOTER
        ================================= */

        .dw-footer {
            text-align: center;
            margin-top: 54px;
            padding-top: 26px;
            border-top: 1px solid var(--dw-border);
        }

        .dw-footer-brand {
            font-size: 15px;
            font-weight: 800;
            color: var(--dw-brand-text);
        }

        .dw-footer-text {
            font-size: 13px;
            color: var(--dw-muted);
            line-height: 1.65;
            margin-top: 5px;
        }


        /* ================================
           MOBILE
        ================================= */

        @media (max-width: 700px) {

            .dw-hero {
                min-height: 340px;
                padding: 40px 20px;
                background-position: center 20%;
            }

            .dw-hero-title {
                font-size: 34px;
            }

            .dw-hero-subtitle {
                font-size: 15px;
            }

            .dw-stat {
                min-width: 100%;
                padding: 8px 0;
            }

            .dw-stat + .dw-stat {
                border-left: none;
                border-top: 1px solid rgba(255, 255, 255, 0.16);
            }

            .dw-section-title {
                font-size: 21px;
                margin-top: 30px;
            }

            .dw-card {
                padding: 18px 16px;
            }

            .dw-vehicle-tile {
                min-width: 130px;
            }
        }
        </style>
        """.replace("__HERO_URI__", _hero_image_data_uri()),
        unsafe_allow_html=True
    )
