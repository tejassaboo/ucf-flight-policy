"""The handbook-specific settings the template's acceptance tests read. Every other file in tests/ is the
template's and stays identical across plugins (see TEMPLATE_GUIDE.md)."""

from pathlib import Path

import contract

ROOT = Path(__file__).resolve().parents[1]

# Ids that are published or taken: a new plugin never reuses one (MASTER_PLAN section 4, "id check").
PUBLISHED_IDS = {
    "aiib-delegation-entitlement", "ec-mission-cabin-allowance", "ftr-city-pair-fare-selection",
    "gates-vendor-flight-ranking", "njc-cabin-meal-allowance", "sfc-travel-preapproval", "uc-g28-expense-audit",
    "un-staff-air-travel-audit", "vt-airfare-policy-booking", "wa-saam-travel-versioned-audit",
    "energy-corporate-flight-booking", "pharma-distributor-flight-booking", "shipping-company-flight-booking",
    "telecommunications-flight-booking", "preference-aware-flight-booking", "llm-context-compress",
    "weather-alert", "word-check", "arxiv-source",
}

# The frozen original's SHA256SUMS, when this checkout sits beside pilot_work/ (skipped elsewhere).
FROZEN_SHA256SUMS = ROOT.parents[1] / "pilot_work" / "originals" / "ucf-manual" / "frozen" / "SHA256SUMS"

# Scenario mix by primary category (EDGE_CASES.md section 5.2; the 32-scenario row).
MIX = {"easy": 6, "boundary_twin": 8, "multi_rule": 5, "hidden_clause": 3, "distractor": 3, "refusal": 3, "flag": 4}

# Overlay minimums (EDGE_CASES.md section 5.3) for the rules this handbook has. It has no overnight-stop rule.
OVERLAY_MINIMUMS = {
    "multi_leg": 3, "date_arithmetic": 2, "month_end": 1, "personal_travel": 1, "multi_traveller": 1,
    "dearer_option": 2, "upgrade_not_taken": 2, "outside_air_section": 2,
}

# Words a scenario id may not contain beyond the template's universal list: this handbook's rule and role
# terms.
ID_FORBIDDEN_TERMS = {
    "first", "business", "economy", "coach", "premium", "segment", "nine", "arrival", "headquarters", "return",
    "home", "refundable", "refund", "credit", "miles", "points", "spouse", "husband", "wife", "companion", "family",
    "personal", "vacation", "holiday", "leisure", "southwest", "student", "club", "rso", "rocketry", "federal",
    "grant", "award", "defense", "navy", "naval", "carrier", "america", "lufthansa", "skies", "stay", "extended",
    "provost", "vice", "president", "manager", "worktag", "authorization", "spend", "denied", "budget", "cancel",
    "cancelled", "delay", "disruption", "reception", "early", "deviation", "quote", "time", "day", "week",
    "foundation", "private", "public", "domestic", "foreign", "international",
}

# The handbook-specific enums whose member words a scenario id may not contain either.
ID_CATEGORY_ENUMS = [contract.Passenger, contract.Purpose, contract.Leg, contract.Funding, contract.Role,
                     contract.Subject, contract.Status]

# How many scenarios a degenerate agent may pass: one that always holds the right offer for approval, and
# one that always books the cheapest seat (with the right section). Set to what each actually passes (README).
MAX_PASS_ALWAYS_FLAG = 2
MAX_PASS_ALWAYS_LOWEST = 8

# Hand-built duration cases beyond the automatic both-sides tests: (rule, outbound scheduled minutes per
# flight, layovers, expected True / False / None for unclear). The rule is per segment: flights never add up.
DURATION_CASES = [
    ("business-segment", [540], [], True),
    ("business-segment", [539], [], False),
    ("business-segment", [300, 300], [60], False),  # 600 minutes in the air, no one flight nine hours
    ("business-segment", [95, 545], [75], True),  # a short hop beside a qualifying flight
    ("business-segment", [95, 535], [75], False),
    ("business-segment", [545, 95], [75], True),
]
