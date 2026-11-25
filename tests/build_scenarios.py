"""Writes the UCF Travel Manual scenario JSON files (authoring aid; the JSON files are the truth).

    python3 tests/build_scenarios.py

Every line number is a line of the frozen handbook (src/plugin/data/policy.txt). Not collected by pytest.
"""

import hashlib
import json
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[1]
POLICY = (PLUGIN / "src/plugin/data/policy.txt").read_text(encoding="utf-8").split("\n")
OUT = PLUGIN / "src/plugin/data/scenarios"


def norm(text):
    return " ".join(text.split())


def keep(a, b, why, quote=None):
    text = norm(" ".join(POLICY[a - 1:b]))
    quote = text if quote is None else quote
    assert norm(quote) in text, (a, b, quote, text)
    return {"lines": [a, b], "sha256": hashlib.sha256(text.encode()).hexdigest(), "quote": quote, "why": why}


def near(a, b, quote, why):
    text = norm(" ".join(POLICY[a - 1:b]))
    assert norm(quote) in text, (a, b, quote, text)
    return {"lines": [a, b], "quote": quote, "why": why}


# ----- the clauses the answers rest on -----
ECONOMICAL = keep(106, 106, "all travel by the most efficient and economical means",
                  "All facets of travel are to be by the most efficient and economical means.")
BUDGET = keep(112, 112, "all travel is contingent upon budget and cost center approval",
              "All travel is contingent upon available budget and cost center approval.")
KEYS_AIRFARE = keep(122, 122, "airfare: a non-refundable economy ticket only")
SA = keep(194, 198, "travel is authorized in advance by a fully approved Spend Authorization")
LEISURE = keep(322, 322, "no leisure booking on Southwest Business",
               "Leisure travel booking is not allowed on Southwest Business.")
NONREF = keep(422, 422, "tickets must be non-refundable economy or coach",
              "Airline tickets must be non-refundable economy or coach class.")
UPGRADE = keep(426, 429, "an upgrade is at the traveller's cost, against a non-refundable economy quote")
FIRST = keep(430, 430, "first class or higher is not allowed")
BUSINESS = keep(431, 433, "business class: a segment of nine hours or longer and full-time business within 24 hours")
APPROVERS = keep(434, 435, "business class is approved by the Cost Center Manager, worktag managers and the VP")
QUESTIONS = keep(437, 439, "upgrade questions go to the Finance Business Center or the Travel Center of Expertise",
                 "If a traveler has questions regarding allowable upgrades, they should contact their respective "
                 "Finance Business Center or Travel Center of Expertise at travelfa@ucf.edu prior to booking the "
                 "flight.")
BUSINESS_DAY = keep(491, 493, "business should begin the day of or the day following arrival",
                    "UCF business should begin the day of or the day following a traveler's arrival at their "
                    "destination.")
DEVIATION = keep(495, 497, "a deviation needs a comparable quote showing the airfare selected is more economical")
NEW_TICKET = keep(505, 508, "a new ticket after an airline cancellation, after reasonable efforts")
RSO = keep(594, 596, "RSO activity is not official university business",
           "RSO activity is not considered official university business.")
PERSONAL_EXP = keep(1004, 1006, "personal expenses are strictly not reimbursable")
SPOUSE = keep(1015, 1015, "spouse/family related charges are not reimbursable", "Spouse/family related charges.")
FLY_AMERICA = keep(1055, 1058, "federal award travel uses a U.S. flag carrier")
FA_UNAVAILABLE = keep(1081, 1082, "exceptions: no U.S. carrier available, or 24 hours or more added")
FA_DOD = keep(1092, 1095, "no Open Skies exception for DOD funding; cost and convenience are no exception")
FA_APPROVAL = keep(1130, 1132, "Fly America exceptions are approved before booking on the Spend Authorization review")
STAY = keep(1251, 1253, "over thirty days at one location needs the provost or a vice president")
SPONSOR = keep(1259, 1261, "apply the sponsor's travel terms")
PERSONAL = keep(1389, 1391, "no reimbursement beyond the time the business needs")
BUSINESS_ONLY_FARE = keep(1402, 1404, "only up to the business-day-only airfare")
EARLY = keep(1457, 1460, "arriving more than one day early needs a quote for arriving one day prior")
EXCEPTIONS = keep(1264, 1267, "exceptions need the Travel Center of Expertise's prior approval")

# ----- nearby clauses that must not change the answer -----
D_FEES = near(423, 424, "Reasonable costs include, but are not limited to, baggage fees, and seat selection fees.",
              "bag and seat fees are allowable, not a fare choice")
D_CHANGE = near(464, 464, "Any costs incurred by UCF for changes to an airline ticket should be justified.",
                "change costs, not the fare choice")
D_CREDIT = near(468, 471, "Credits for cancelled flights booked through Concur for business travel will be available "
                "in the traveler's profile.", "credits are available; nothing requires their use")
D_MILES = near(483, 485, "Airfare tickets that were purchased by frequent-flyer miles or credit card reward programs "
               "are not reimbursable.", "miles tickets, not this booking")
D_TIME = near(489, 491, "A traveler is allowed up to three hours before a flight and up to two hours after a flight "
              "returns", "travel time for meals and per diem, not the fare")
D_TRAIN = near(805, 805, "Train tickets must be non-refundable economy or lowest travel class.", "trains, not flights")
D_DRIVE = near(690, 691, "If a traveler chooses to drive rather than fly, the amount of the reimbursement is limited "
               "to the amount it would have cost to fly", "driving, not flying")
D_FLY_AMERICA = near(1055, 1058, "the Principal Investigator (PI) of the award funded by federal award/grant must "
                     "comply with the Fly America Act", "applies to federal awards only")
D_FOREIGN_TAP = near(1027, 1028, "you must secure approval through the Travel Approval Petition", "registration "
                     "abroad; the record has it")
D_BUSINESS_DEF = near(436, 437, "Business class is deemed to be the class between economy and first class.",
                      "the name of the cabin, not its terms")
D_LAUNDRY = near(954, 956, "When official business is more than seven days", "laundry, not airfare")
D_ADVANCE = near(1290, 1290, "The travel period must be for a duration of five or more days.", "cash advances")

UCF = "UCF main campus, Orlando, FL"
CCM = {"approver_name": "Dana Whitfield", "approver_title": "Cost Center Manager, College of Engineering and "
       "Computer Science", "role": "COST_CENTER_MANAGER"}
WTM = {"approver_name": "Luis Navarro", "approver_title": "Worktag manager, Dean's Engineering Excellence Fund",
       "role": "WORKTAG_MANAGER"}
VP = {"approver_name": "Dr. Renata Osei", "approver_title": "Vice President for Research and Innovation",
      "role": "VICE_PRESIDENT"}
PROVOST = {"approver_name": "Dr. Martin Keene", "approver_title": "Provost and Vice President for Academic Affairs",
           "role": "PROVOST"}
GM = {"approver_name": "Hannah Cole", "approver_title": "Grant Manager, Office of Research", "role": "GRANT_MANAGER"}
ADVISOR = {"approver_name": "Dr. Omar Haddad", "approver_title": "Faculty advisor, UCF Rocketry Club",
           "role": "FACULTY_ADVISOR"}
GLOBAL = {"approver_name": "Karen Liu", "approver_title": "Travel Approval Petition reviewer, UCF Global",
          "role": "UCF_GLOBAL"}
# Lines 1027-1036: every trip outside the United States has its Travel Approval Petition approved by UCF Global
# (submitted before the Spend Authorization), so no foreign booking turns on it.
TAP_OK = {**GLOBAL, "subject": "TRAVEL_APPROVAL_PETITION", "status": "APPROVED",
          "wording": "Approved: the Travel Approval Petition for this trip; the Travel Safety Registration is on file.",
          "given_on": "2026-11-09"}
FOREIGN = {"DEL", "DXB", "FCO", "DOH", "NRT", "HND", "ICN", "FRA", "HKG", "LHR", "BOG", "GRU"}
GRANT_TAG = "Gift: Dean's Engineering Excellence Fund (an unrestricted gift)"


def sign(who, subject, wording, on="2026-11-16", status="APPROVED"):
    return {**who, "subject": subject, "status": status, "wording": wording if status != "PENDING" else "",
            "given_on": on}


SA_OK = sign(CCM, "SPEND_AUTHORIZATION", "Approved: the Spend Authorization for this trip.")


def business_ok(vp_status="APPROVED"):
    return [sign(CCM, "BUSINESS_CLASS", "Approved: business class for this trip's flights."),
            sign(WTM, "BUSINESS_CLASS", "Approved: business class for this trip's flights, charged to the gift fund."),
            sign(VP, "BUSINESS_CLASS", "Approved: business class for this trip's flights.", status=vp_status,
                 on="2026-11-18" if vp_status == "APPROVED" else "2026-11-20")]


def ev(starts, ends, what):
    return {"starts_local": starts, "ends_local": ends, "what": what}


def trip(**fields):
    base = {
        "traveller_name": "", "traveller_title": "", "passenger": "UCF_EMPLOYEE", "accompanies": "",
        "department": "Department of Mechanical and Aerospace Engineering", "headquarters": UCF, "origin": "MCO",
        "destination": "", "leg": "OUTBOUND", "travel_date": "", "fallback_date": "", "trip_end_date": "",
        "days_away": 0, "booking_date": "2026-11-23", "purpose": "", "purpose_kind": "CONFERENCE", "schedule": [],
        "must_arrive_by": "", "funding": "DEPARTMENT_FUNDS", "sponsor": "", "worktags": [], "requested_cabin": "ECONOMY",
        "refundable_requested": False, "airline_disruption": "", "airline_credits": [], "approvals": [SA_OK],
        "notes": [],
    }
    unknown = set(fields) - set(base)
    assert not unknown, unknown
    base.update(fields)
    if {base["origin"], base["destination"]} & FOREIGN:
        base["approvals"] = [*base["approvals"], TAP_OK]
    assert base["days_away"] > 0 and base["trip_end_date"], base["traveller_name"]
    return base


def fl(carrier, depart, minutes, via=None, layovers=None):
    spec = {"carrier": carrier, "depart": depart, "minutes": minutes}
    if via:
        spec["via"] = via
    if layovers:
        spec["layovers"] = layovers
    return spec


def of(slot, flight, cabin, cents, seats=True, refundable=False):
    data = {"slot": slot, "flight": flight, "cabin": cabin, "fare_cents": cents}
    if not seats:
        data["seats"] = False
    if refundable:
        data["refundable"] = True
    return data


def search(name, origin, destination, date, flights, offers):
    return {"name": name, "origin": origin, "destination": destination, "date": date, "return_date": "",
            "background": 0, "flights": flights, "offers": offers}


def expected(decision, slots, cabins, reasons, approvers, clauses, phrase=""):
    return {"decision": decision, "offer_slots": sorted(slots), "cabins": sorted(cabins), "reason_codes": sorted(reasons),
            "approvers": sorted(approvers), "clauses": sorted(clauses), "unclear_phrase": phrase}


SA_ROLES = ["COST_CENTER_MANAGER", "NONE"]
BIZ_ROLES = ["COST_CENTER_MANAGER", "NONE", "VICE_PRESIDENT", "WORKTAG_MANAGER"]
GAP = ["FINANCE_BUSINESS_CENTER", "NOT_NAMED", "TRAVEL_EXPERTISE_CENTER"]
ECON = ["AIRFARE", "INTRODUCTION"]
NOT_MET = ["LONG_FLIGHT_CONDITION_NOT_MET", "TRAVELER_PAYS_UPGRADE", "UPGRADE_NOT_ELIGIBLE"]
S = []


def scenario(id, category, overlays, request, trip_, searches, exp, must_keep, notes, twin_of="", twin_fact="",
             flag_twins=(), ambiguity="none", distractors=(), hidden=None):
    data = {
        "id": id, "category": category, "overlays": overlays, "twin_of": twin_of, "twin_fact": twin_fact,
        "flag_twins": list(flag_twins), "ambiguity_note": ambiguity, "request": request, "trip": trip_,
        "world": {"searches": searches}, "expected": exp, "must_keep": must_keep, "distractors": list(distractors),
        "design_notes": notes,
    }
    if hidden:
        data["answer_key_inputs"] = hidden
    if TAP_OK in trip_["approvals"] and exp["decision"] == "BOOK":
        exp["approvers"] = sorted({*exp["approvers"], "UCF_GLOBAL"})
    S.append(data)


# ============================== easy (6) ==============================
scenario(
    "citrus-knoll", "easy", ["multi_leg", "dearer_option"],
    "Please book the cheapest flight the policy allows to Denver on December 8. The conference opens the next "
    "morning.",
    trip(traveller_name="Kendra Moss", traveller_title="Assistant Professor", destination="DEN",
         travel_date="2026-12-08", trip_end_date="2026-12-11", days_away=4,
         purpose="Paper presentation at the Rocky Mountain Combustion Conference, Denver",
         schedule=[ev("2026-12-09 08:30", "2026-12-09 17:30", "Conference sessions, day one")]),
    [search("out", "MCO", "DEN", "2026-12-08",
            {"wn": fl("WN", "07:05", [275]), "dl": fl("DL", "06:10", [95, 210], via=["ATL"], layovers=[70]),
             "ua": fl("UA", "11:40", [280])},
            [of("wn-economy", "wn", "ECONOMY", 16900, refundable=True), of("dl-economy", "dl", "ECONOMY", 17600),
             of("ua-economy", "ua", "ECONOMY", 19400)])],
    expected("BOOK", ["dl-economy"], ["ECONOMY"], ["LOWEST_FARE", "REFUNDABLE_FARE_NOT_ALLOWED"], SA_ROLES, ECON),
    [ECONOMICAL, KEYS_AIRFARE, NONREF],
    "Southwest's 16900 fare is refundable, and lines 122 and 422 allow only a non-refundable economy ticket; the "
    "lowest non-refundable economy fare is Delta's connection through Atlanta at 17600. The conference opens the "
    "next morning, so the landing time decides nothing.",
    distractors=[D_FEES])

scenario(
    "heron-bayou", "easy", ["upgrade_not_taken"],
    "It's a long flight to Seattle on December 8, so I'd like business class if the university allows it; "
    "otherwise economy is fine. I have to be at the site visit on the morning of the 9th.",
    trip(traveller_name="Gavin Reyes", traveller_title="Research Engineer", destination="SEA",
         travel_date="2026-12-08", trip_end_date="2026-12-10", days_away=3, purpose_kind="SITE_VISIT",
         purpose="Site visit at the Boeing composites test facility, Seattle", requested_cabin="BUSINESS",
         schedule=[ev("2026-12-09 08:00", "2026-12-09 16:30", "Site visit and test review")]),
    [search("out", "MCO", "SEA", "2026-12-08",
            {"dl": fl("DL", "08:00", [390]), "as": fl("AS", "10:15", [395]),
             "ua": fl("UA", "07:10", [255, 165], via=["DEN"], layovers=[65])},
            [of("dl-economy", "dl", "ECONOMY", 34800), of("dl-business", "dl", "BUSINESS", 89000),
             of("as-economy", "as", "ECONOMY", 33900), of("ua-economy", "ua", "ECONOMY", 35500)])],
    expected("BOOK", ["as-economy"], ["ECONOMY"], NOT_MET, SA_ROLES, ["AIRFARE", "UPGRADED_TICKETS"]),
    [BUSINESS, UPGRADE, NONREF, ECONOMICAL],
    "No flight is nine hours or longer (390 minutes nonstop), so business class is not acceptable (lines 431-433) "
    "and an upgrade would be at the traveller's cost (426-429). The traveller accepts economy: Alaska's 33900 is "
    "the lowest economy fare.",
    distractors=[D_BUSINESS_DEF])

scenario(
    "amber-dune", "easy", ["multi_leg", "dearer_option"],
    "Please book business class to Dubai on December 7 for the materials workshop; the business-class approvals "
    "are in. If business isn't allowed, economy is fine.",
    trip(traveller_name="Dr. Samir Haddad", traveller_title="Professor", destination="DXB", travel_date="2026-12-07",
         trip_end_date="2026-12-12", days_away=6, purpose_kind="WORKSHOP",
         purpose="Invited lectures at the advanced materials workshop, Dubai", requested_cabin="BUSINESS",
         worktags=[GRANT_TAG], approvals=[SA_OK, *business_ok()],
         schedule=[ev("2026-12-09 09:00", "2026-12-09 17:00", "Workshop, day one"),
                   ev("2026-12-10 09:00", "2026-12-10 17:00", "Workshop, day two")]),
    [search("out", "MCO", "DXB", "2026-12-07",
            {"ek": fl("EK", "20:30", [820]), "dl": fl("DL", "13:00", [95, 800], via=["ATL"], layovers=[90])},
            [of("ek-economy", "ek", "ECONOMY", 121000), of("ek-business", "ek", "BUSINESS", 452000),
             of("dl-economy", "dl", "ECONOMY", 112500), of("dl-business", "dl", "BUSINESS", 431000)])],
    expected("BOOK", ["dl-business"], ["BUSINESS"], ["LONG_FLIGHT_APPROVED"], BIZ_ROLES, ["UPGRADED_TICKETS"]),
    [BUSINESS, APPROVERS, ECONOMICAL],
    "Both tickets carry a flight of nine hours or longer (EK 820, DL's Atlanta-Dubai 800 minutes) and the workshop "
    "begins within 24 hours of either landing (EK 19:10, DL 14:25 on December 8; workshop December 9 09:00). The "
    "Cost Center Manager, the gift fund's worktag manager and the Vice President approved business class (434-435): "
    "the lowest qualifying business fare, Delta's 431000.")

scenario(
    "pecan-shoal", "easy", [],
    "My meeting date in Boston might still move, so I'd like a refundable ticket for December 9 if possible; if "
    "not, book what the policy allows.",
    trip(traveller_name="Lauren Pike", traveller_title="Program Coordinator", department="Office of Research",
         destination="BOS", travel_date="2026-12-09", trip_end_date="2026-12-11", days_away=3, purpose_kind="MEETING",
         purpose="Consortium planning meeting at Northeastern University, Boston", refundable_requested=True,
         schedule=[ev("2026-12-10 09:00", "2026-12-10 16:00", "Consortium planning meeting")]),
    [search("out", "MCO", "BOS", "2026-12-09",
            {"b6": fl("B6", "07:45", [165]), "dl": fl("DL", "06:30", [95, 135], via=["ATL"], layovers=[60])},
            [of("b6-economy", "b6", "ECONOMY", 21800), of("b6-refundable", "b6", "ECONOMY", 38900, refundable=True),
             of("dl-economy", "dl", "ECONOMY", 24300)])],
    expected("BOOK", ["b6-economy"], ["ECONOMY"], ["REFUNDABLE_FARE_NOT_ALLOWED"], SA_ROLES, ECON),
    [KEYS_AIRFARE, NONREF],
    "Lines 122 and 422: airline tickets must be non-refundable economy; the refundable fare is declined and the "
    "lowest non-refundable economy fare is JetBlue's 21800.",
    distractors=[D_CHANGE])

scenario(
    "osprey-wren", "easy", [],
    "Please book me first class to Los Angeles on December 8 for the advisory board meeting on the 9th. If the "
    "policy doesn't allow it, book what it allows; I have to be at the meeting.",
    trip(traveller_name="Dr. Celeste Arnaud", traveller_title="Dean's Fellow and Professor", destination="LAX",
         travel_date="2026-12-08", trip_end_date="2026-12-10", days_away=3, purpose_kind="MEETING",
         purpose="Industry advisory board meeting, Los Angeles", requested_cabin="FIRST",
         schedule=[ev("2026-12-09 09:00", "2026-12-09 15:00", "Advisory board meeting")]),
    [search("out", "MCO", "LAX", "2026-12-08",
            {"aa": fl("AA", "08:15", [330]), "dl": fl("DL", "07:00", [95, 270], via=["ATL"], layovers=[75]),
             "wn": fl("WN", "10:30", [335])},
            [of("aa-economy", "aa", "ECONOMY", 31800), of("aa-first", "aa", "FIRST", 98000),
             of("dl-economy", "dl", "ECONOMY", 29900), of("wn-economy", "wn", "ECONOMY", 30500)])],
    expected("BOOK", ["dl-economy"], ["ECONOMY"],
             ["FIRST_CLASS_NOT_ALLOWED", "LONG_FLIGHT_CONDITION_NOT_MET", "UPGRADE_NOT_ELIGIBLE"], SA_ROLES,
             ["AIRFARE", "UPGRADED_TICKETS"]),
    [FIRST, NONREF, ECONOMICAL],
    "Line 430: first class transportation, or higher, is NOT allowed; no business fare qualifies either. The "
    "traveller asks for what the policy allows: the lowest economy fare, Delta's 29900.")

scenario(
    "marlin-gate", "easy", ["multi_leg", "upgrade_not_taken"],
    "Please book me economy to Hong Kong on December 8 for the research collaboration meetings. The department "
    "approved business class, but I'd rather save the money.",
    trip(traveller_name="Dr. Wen Li", traveller_title="Associate Professor", destination="HKG",
         travel_date="2026-12-08", trip_end_date="2026-12-15", days_away=8, purpose_kind="RESEARCH",
         purpose="Research collaboration meetings at the Hong Kong University of Science and Technology",
         worktags=[GRANT_TAG], approvals=[SA_OK, *business_ok()],
         schedule=[ev("2026-12-10 09:00", "2026-12-10 17:00", "Collaboration meetings")]),
    [search("out", "MCO", "HKG", "2026-12-08",
            {"cx": fl("CX", "12:40", [960]), "aa": fl("AA", "07:00", [330, 900], via=["LAX"], layovers=[100])},
            [of("cx-economy", "cx", "ECONOMY", 132000), of("cx-business", "cx", "BUSINESS", 545000),
             of("aa-economy", "aa", "ECONOMY", 127500), of("aa-business", "aa", "BUSINESS", 521000)])],
    expected("BOOK", ["aa-economy"], ["ECONOMY"], ["LOWEST_FARE"], BIZ_ROLES, [*ECON, "UPGRADED_TICKETS"]),
    [NONREF, ECONOMICAL, BUSINESS],
    "Business class would qualify (long flights, approvals on file), but the traveller asks for economy: "
    "permission is not obligation. The lowest economy fare is American's connection through Los Angeles, 127500. "
    "The business approvals on file go unused (4(b)).")

# ============================== boundary twins (8) ==============================


def gru(minutes):
    return [search("out", "MCO", "GRU", "2026-12-08",
                   {"la": fl("LA", "21:30", [minutes]),
                    "aa": fl("AA", "19:10", [70, 505], via=["MIA"], layovers=[85])},
                   [of("la-economy", "la", "ECONOMY", 101500), of("la-business", "la", "BUSINESS", 312000),
                    of("aa-economy", "aa", "ECONOMY", 96500), of("aa-business", "aa", "BUSINESS", 287000)])]


def gru_trip(name):
    return trip(traveller_name=name, traveller_title="Associate Professor", destination="GRU",
                travel_date="2026-12-08", trip_end_date="2026-12-12", days_away=5, purpose_kind="WORKSHOP",
                purpose="Biofuels research workshop at the University of Sao Paulo", requested_cabin="BUSINESS",
                worktags=[GRANT_TAG], approvals=[SA_OK, *business_ok()],
                schedule=[ev("2026-12-09 13:00", "2026-12-09 18:00", "Workshop opening sessions"),
                          ev("2026-12-10 08:30", "2026-12-10 17:30", "Workshop sessions")])


GRU_REQUEST = ("Please book business class to Sao Paulo on December 8 for the biofuels workshop; the approvals are "
               "in. If business isn't allowed, economy is fine.")
scenario(
    "tamarind-cove", "boundary_twin", ["multi_leg", "dearer_option"], GRU_REQUEST, gru_trip("Dr. Ines Carvalho"),
    gru(540),
    expected("BOOK", ["la-business"], ["BUSINESS"], ["LONG_FLIGHT_APPROVED"], BIZ_ROLES, ["UPGRADED_TICKETS"]),
    [BUSINESS, APPROVERS],
    "LATAM's nonstop is scheduled for exactly 540 minutes: 'nine hours or longer' is inclusive, so its business "
    "fare qualifies; the workshop opens the afternoon it lands (08:30). American's business fare is cheaper but its "
    "flights are 70 and 505 minutes, none nine hours, so it does not qualify. Approvals are on file: LATAM business "
    "312000.",
    twin_of="saguaro-bend", twin_fact="LATAM nonstop scheduled 540 or 539 minutes")

scenario(
    "saguaro-bend", "boundary_twin", ["multi_leg"], GRU_REQUEST, gru_trip("Dr. Paulo Mendes"), gru(539),
    expected("BOOK", ["aa-economy"], ["ECONOMY"], NOT_MET, BIZ_ROLES, ["AIRFARE", "UPGRADED_TICKETS"]),
    [BUSINESS, NONREF, ECONOMICAL],
    "At 539 minutes no flight is nine hours or longer, so no business fare qualifies (lines 431-433) whatever the "
    "approvals; the traveller accepts economy: American's connection via Miami at 96500.",
    twin_of="tamarind-cove", twin_fact="LATAM nonstop scheduled 540 or 539 minutes")


def doh(start, name):
    return trip(traveller_name=name, traveller_title="Assistant Professor", destination="DOH",
                travel_date="2026-11-29", trip_end_date="2026-12-04", days_away=6, purpose_kind="WORKSHOP",
                purpose="Desalination research workshop at Qatar University, Doha", requested_cabin="BUSINESS",
                worktags=[GRANT_TAG], approvals=[SA_OK, *business_ok()],
                schedule=[ev(f"2026-12-01 {start}", "2026-12-01 17:00", "Workshop, day one"),
                          ev("2026-12-02 08:30", "2026-12-02 17:00", "Workshop, day two")])


def doh_search(day="2026-11-29"):
    return [search("out", "MCO", "DOH", day,
                   {"qr": fl("QR", "13:00", [750]), "aa": fl("AA", "16:20", [150, 700], via=["PHL"], layovers=[95])},
                   [of("qr-economy", "qr", "ECONOMY", 109000), of("qr-business", "qr", "BUSINESS", 398000),
                    of("aa-economy", "aa", "ECONOMY", 103500)])]


DOH_REQUEST = ("Please book business class to Doha on November 29 for the desalination workshop; the approvals are "
               "in. If business isn't allowed, economy is fine.")
scenario(
    "juniper-wake", "boundary_twin", ["date_arithmetic", "month_end", "dearer_option"], DOH_REQUEST,
    doh("08:30", "Dr. Amira Saleh"), doh_search(),
    expected("BOOK", ["qr-business"], ["BUSINESS"], ["LONG_FLIGHT_APPROVED"], BIZ_ROLES, ["UPGRADED_TICKETS"]),
    [BUSINESS, APPROVERS],
    "Qatar's 750-minute nonstop lands November 30 at 09:30; the workshop begins December 1 at 08:30, 23 hours later, "
    "within 24 hours (lines 431-433). Approvals on file: Qatar business 398000 (American sells economy only).",
    twin_of="fennel-moor", twin_fact="workshop starts 08:30 or 10:30 on December 1 (23 or 25 hours after landing)")

scenario(
    "fennel-moor", "boundary_twin", ["date_arithmetic", "month_end"], DOH_REQUEST, doh("10:30", "Dr. Yusuf Karim"),
    doh_search(),
    expected("BOOK", ["aa-economy"], ["ECONOMY"], NOT_MET, BIZ_ROLES, ["AIRFARE", "UPGRADED_TICKETS"]),
    [BUSINESS, NONREF, ECONOMICAL],
    "The workshop begins December 1 at 10:30, 25 hours after the Qatar flight lands (November 30 09:30): not within "
    "24 hours, so business is not acceptable even with approvals. Economy: American's connection at 103500.",
    twin_of="juniper-wake", twin_fact="workshop starts 08:30 or 10:30 on December 1 (23 or 25 hours after landing)")


def san(monday):
    return [search("monday", "MCO", "SAN", "2026-12-07",
                   {"wn": fl("WN", "09:00", [345]), "aa": fl("AA", "07:30", [165, 185], via=["DFW"], layovers=[70])},
                   [of("wn-monday", "wn", "ECONOMY", monday), of("aa-monday", "aa", "ECONOMY", 33100)]),
            search("wednesday", "MCO", "SAN", "2026-12-09",
                   {"wn": fl("WN", "09:00", [345]), "dl": fl("DL", "07:15", [95, 270], via=["ATL"], layovers=[80])},
                   [of("wn-wednesday", "wn", "ECONOMY", 28900), of("dl-wednesday", "dl", "ECONOMY", 31200)])]


def san_trip(name):
    return trip(traveller_name=name, traveller_title="Lecturer", department="Department of Civil, Environmental and "
                "Construction Engineering", destination="SAN", travel_date="2026-12-07", fallback_date="2026-12-09",
                trip_end_date="2026-12-12", days_away=6,
                purpose="Coastal engineering conference, San Diego, December 10-11",
                schedule=[ev("2026-12-10 08:30", "2026-12-10 17:00", "Conference, day one"),
                          ev("2026-12-11 08:30", "2026-12-11 15:00", "Conference, day two")],
                notes=["Monday December 7 to Wednesday December 9 are personal days with family in San Diego.",
                       ("No flight leaving Orlando on Thursday December 10 lands in San Diego before the conference "
                       "opens.")])


SAN_REQUEST = ("I'd like to fly to San Diego on Monday the 7th to spend a few days with my sister before the "
               "conference on Thursday the 10th. If the university won't pay for the Monday flight, book me on "
               "Wednesday the 9th instead.")
scenario(
    "walnut-ferry", "boundary_twin", ["personal_travel", "date_arithmetic", "outside_air_section"], SAN_REQUEST,
    san_trip("Marisol Vega"), san(28400),
    expected("BOOK", ["wn-monday"], ["ECONOMY"], ["COST_SAVINGS", "LOWEST_FARE", "TRAVEL_TIME_DEVIATION_CHEAPER"],
             SA_ROLES, ["ALLOWABLE_TRAVEL_TIME", "PERSONAL_TRAVEL"]),
    [BUSINESS_DAY, DEVIATION, EARLY, BUSINESS_ONLY_FARE],
    "Business begins Thursday, so Monday is three days early: a deviation from the allowable travel time (491-493), "
    "which a comparable quote must show is more economical (495-497). The Monday fare (28400) is below the lowest "
    "Wednesday fare (28900): book Monday.",
    twin_of="cypress-lark", twin_fact="Southwest's Monday fare 28400 or 29400 (Wednesday 28900)")

scenario(
    "cypress-lark", "boundary_twin", ["personal_travel", "date_arithmetic", "outside_air_section"], SAN_REQUEST,
    san_trip("Derek Olsen"), san(29400),
    expected("BOOK", ["wn-wednesday"], ["ECONOMY"],
             ["LOWEST_FARE", "PERSONAL_TRAVEL_NOT_COVERED", "TRAVEL_TIME_DEVIATION_DEARER"], SA_ROLES,
             ["ALLOWABLE_TRAVEL_TIME", "PERSONAL_TRAVEL"]),
    [BUSINESS_DAY, DEVIATION, EARLY, BUSINESS_ONLY_FARE],
    "Monday's lowest fare (29400) is dearer than Wednesday's (28900), so the deviation is not more economical "
    "(495-497) and UCF pays only up to the business-day-only airfare (1402-1404). The traveller asked for Wednesday "
    "in that case: Southwest Wednesday 28900.",
    twin_of="walnut-ferry", twin_fact="Southwest's Monday fare 28400 or 29400 (Wednesday 28900)")


def fco(minutes):
    return [search("out", "MCO", "FCO", "2026-12-08",
                   {"dl": fl("DL", "16:30", [95, minutes], via=["ATL"], layovers=[75]),
                    "aa": fl("AA", "17:45", [150, 515], via=["PHL"], layovers=[80])},
                   [of("dl-economy", "dl", "ECONOMY", 91500), of("dl-business", "dl", "BUSINESS", 268000),
                    of("aa-economy", "aa", "ECONOMY", 88500), of("aa-business", "aa", "BUSINESS", 259000)])]


def fco_trip(name):
    return trip(traveller_name=name, traveller_title="Research Professor", destination="FCO",
                travel_date="2026-12-08", trip_end_date="2026-12-13", days_away=6, purpose_kind="MEETING",
                purpose="Project review with the Italian Space Agency partners, Rome", requested_cabin="BUSINESS",
                worktags=[GRANT_TAG], approvals=[SA_OK, *business_ok()],
                schedule=[ev("2026-12-10 09:00", "2026-12-10 17:00", "Project review, day one"),
                          ev("2026-12-11 09:00", "2026-12-11 13:00", "Project review, day two")])


FCO_REQUEST = ("Please book business class to Rome on December 8 for the project review; the approvals are in. If "
               "business isn't allowed, economy is fine.")
scenario(
    "linden-quay", "boundary_twin", ["multi_leg", "dearer_option"], FCO_REQUEST, fco_trip("Dr. Hugo Brandt"), fco(545),
    expected("BOOK", ["dl-business"], ["BUSINESS"], ["LONG_FLIGHT_APPROVED"], BIZ_ROLES, ["UPGRADED_TICKETS"]),
    [BUSINESS, APPROVERS],
    "Delta's Atlanta-Rome flight is 545 minutes, one segment nine hours or longer, so Delta's business fare "
    "qualifies; the review begins 22 hours after it lands. American's flights (150 and 515 minutes) add to more than "
    "nine hours but no one segment is, so its cheaper business fare does not qualify. Delta business 268000.",
    twin_of="basalt-wharf", twin_fact="Delta's Atlanta-Rome flight 545 or 535 minutes")

scenario(
    "basalt-wharf", "boundary_twin", ["multi_leg"], FCO_REQUEST, fco_trip("Dr. Nadia Petrov"), fco(535),
    expected("BOOK", ["aa-economy"], ["ECONOMY"], NOT_MET, BIZ_ROLES, ["AIRFARE", "UPGRADED_TICKETS"]),
    [BUSINESS, NONREF, ECONOMICAL],
    "At 535 minutes no single segment of either ticket is nine hours or longer, though both itineraries add to more; "
    "'at least one segment' (431-432) rules business out. Economy: American via Philadelphia, 88500.",
    twin_of="linden-quay", twin_fact="Delta's Atlanta-Rome flight 545 or 535 minutes")

# ============================== multi-rule (5) ==============================
scenario(
    "garnet-spire", "multi_rule", ["dearer_option"],
    "Please book me first class to Tokyo on December 8 for the robotics symposium. If first isn't allowed, book the "
    "best the policy allows; the business-class approvals are in, and I have to be at the symposium on the 10th.",
    trip(traveller_name="Dr. Kenji Mori", traveller_title="Professor and Department Chair", destination="NRT",
         travel_date="2026-12-08", trip_end_date="2026-12-14", days_away=7,
         purpose="Keynote at the international robotics symposium, Tokyo", requested_cabin="FIRST",
         worktags=[GRANT_TAG], approvals=[SA_OK, *business_ok()],
         schedule=[ev("2026-12-10 09:00", "2026-12-10 17:30", "Symposium, day one")]),
    [search("out", "MCO", "NRT", "2026-12-08",
            {"jl": fl("JL", "11:00", [840]), "nh": fl("NH", "13:30", [830])},
            [of("jl-economy", "jl", "ECONOMY", 138000), of("jl-business", "jl", "BUSINESS", 612000),
             of("jl-first", "jl", "FIRST", 1180000), of("nh-economy", "nh", "ECONOMY", 131000),
             of("nh-business", "nh", "BUSINESS", 598000)])],
    expected("BOOK", ["nh-business"], ["BUSINESS"], ["FIRST_CLASS_NOT_ALLOWED", "UPGRADE_NOT_ELIGIBLE"], BIZ_ROLES,
             ["UPGRADED_TICKETS"]),
    [FIRST, BUSINESS, APPROVERS],
    "Line 430: first class is NOT allowed, even with approvals. Business class qualifies (830- and 840-minute "
    "nonstops; the symposium begins within 24 hours of either landing) and is approved by all three (434-435): the "
    "best the policy allows is the lowest business fare, ANA's 598000.")

scenario(
    "sorrel-mesa", "multi_rule", ["multi_leg", "dearer_option", "outside_air_section"],
    "Lufthansa's nonstop to Frankfurt on December 8 is the cheapest; please book it, or if that isn't allowed, book "
    "what the policy allows. I have to be at the program review on the 10th.",
    trip(traveller_name="Dr. Ethan Brooks", traveller_title="Associate Professor", destination="FRA",
         travel_date="2026-12-08", trip_end_date="2026-12-12", days_away=5, purpose_kind="MEETING",
         purpose="Program review for the Office of Naval Research award, Frankfurt", funding="FEDERAL_AWARD",
         sponsor="U.S. Department of Defense, Office of Naval Research; the award follows federal travel rules",
         worktags=["Grant: ONR award N0014 (naval materials)"],
         approvals=[SA_OK, sign(GM, "SPEND_AUTHORIZATION", "Approved: the Spend Authorization, charged to the ONR "
                                "award.")],
         schedule=[ev("2026-12-10 09:00", "2026-12-10 17:00", "Program review")]),
    [search("out", "MCO", "FRA", "2026-12-08",
            {"lh": fl("LH", "18:00", [535]), "ua": fl("UA", "17:05", [160, 470], via=["EWR"], layovers=[90]),
             "dl": fl("DL", "16:20", [95, 530], via=["ATL"], layovers=[80])},
            [of("lh-economy", "lh", "ECONOMY", 78000), of("ua-economy", "ua", "ECONOMY", 86500),
             of("dl-economy", "dl", "ECONOMY", 91000)])],
    expected("BOOK", ["ua-economy"], ["ECONOMY"], ["FLY_AMERICA_US_CARRIER_REQUIRED", "NATIONAL_CARRIER_REQUIRED"],
             ["COST_CENTER_MANAGER", "GRANT_MANAGER", "NONE"], ["FLY_AMERICA", "FLY_AMERICA_EXCEPTIONS",
                                                                 "SPONSORED_AWARD"]),
    [FLY_AMERICA, FA_DOD, SPONSOR],
    "The trip is on a Department of Defense award: the Fly America Act applies (1055-1058) and the Open Skies "
    "exception does not (1092-1093); United and Delta have seats, add 185 and 170 minutes to the trip, and connect in "
    "the United States, so no exception of 1081-1090 applies, and ticket cost is no exception (1094-1095). The lowest U.S. "
    "carrier fare: United via Newark, 86500.",
    distractors=[D_FOREIGN_TAP])


def dxb_home(resume, name):
    return trip(traveller_name=name, traveller_title="Professor", origin="DXB", destination="MCO", leg="RETURN",
                travel_date="2026-12-10", trip_end_date="2026-12-10", days_away=6, purpose_kind="WORKSHOP",
                purpose="Flight home from the water-reuse workshop in Dubai (December 7-9)", requested_cabin="BUSINESS",
                worktags=[GRANT_TAG], approvals=[SA_OK, *business_ok()],
                schedule=[ev(f"{resume} 08:00", f"{resume} 17:00", "Work at the main campus")],
                notes=[("Outbound: flew Orlando to Dubai on December 5 and landed December 6 at 19:10; the workshop "
                       "began December 7 at 08:30, 13 hours later.")] + (
                    ["Friday December 11 is a day of annual leave; work at the main campus resumes Monday December 14."]
                    if resume == "2026-12-14" else []))


def dxb_search():
    return [search("home", "DXB", "MCO", "2026-12-10",
                   {"ek": fl("EK", "08:30", [990]), "dl": fl("DL", "09:45", [960, 90], via=["ATL"], layovers=[110])},
                   [of("ek-economy", "ek", "ECONOMY", 118000), of("ek-business", "ek", "BUSINESS", 449000),
                    of("dl-economy", "dl", "ECONOMY", 109500), of("dl-business", "dl", "BUSINESS", 427000)])]


DXB_REQUEST = ("Please book my flight home from Dubai on December 10. I'd like business class for the long flight if "
               "the university allows it; otherwise economy.")
scenario(
    "heather-dock", "multi_rule", ["multi_leg", "dearer_option"], DXB_REQUEST, dxb_home("2026-12-11", "Dr. Farah Nasser"),
    dxb_search(),
    expected("BOOK", ["dl-business"], ["BUSINESS"], ["LONG_FLIGHT_APPROVED"], BIZ_ROLES, ["UPGRADED_TICKETS"]),
    [BUSINESS, APPROVERS],
    "Flight home: both tickets carry a flight over nine hours, and work at headquarters resumes December 11 08:00, "
    "16 hours after Emirates lands (16:00) and 12 hours after Delta lands (20:05); the outbound test was met too, so "
    "every reading of 'arrival at the destination and/or return to headquarters' allows business. Approvals on "
    "file: Delta business 427000.",
    hidden={"outbound_hours": 13})

scenario(
    "mallow-pike", "multi_rule", ["dearer_option"],
    "Delta cancelled my 6 a.m. flight to Washington this morning and can't get me there until tonight. I have to "
    "be on the review panel at 1 p.m. today; please buy me a new ticket that gets me there in time.",
    trip(traveller_name="Dr. Priyanka Shah", traveller_title="Associate Professor", destination="DCA",
         travel_date="2026-12-08", trip_end_date="2026-12-09", days_away=2, booking_date="2026-12-08",
         purpose_kind="MEETING", purpose="Proposal review panel at the National Science Foundation, Alexandria, VA",
         must_arrive_by="2026-12-08 12:15",
         schedule=[ev("2026-12-08 13:00", "2026-12-08 17:00", "Review panel")],
         airline_disruption="Delta cancelled DL 1187, Orlando 06:00 to Washington National, on December 8. The "
         "traveller called Delta at 05:10: Delta's first open seat lands at 18:40, after the panel.",
         notes=["The panel venue is 30 minutes from Washington National."]),
    [search("out", "MCO", "DCA", "2026-12-08",
            {"aa": fl("AA", "09:05", [130]), "wn": fl("WN", "13:40", [130]),
             "dl": fl("DL", "12:20", [95, 105], via=["ATL"], layovers=[70])},
            [of("aa-economy", "aa", "ECONOMY", 33800), of("wn-economy", "wn", "ECONOMY", 26900),
             of("dl-economy", "dl", "ECONOMY", 29900)])],
    expected("BOOK", ["aa-economy"], ["ECONOMY"], ["LOWEST_FARE", "NEW_TICKET_AFTER_AIRLINE_DISRUPTION"], SA_ROLES,
             ["AIRFARE", "AIRLINE_DELAY", "CHANGING_TICKETS", "INTRODUCTION"]),
    [NEW_TICKET, ECONOMICAL, NONREF],
    "Lines 505-508: the airline cancelled, the traveller tried Delta first, and Delta's next seat lands after the "
    "panel, so a new ticket may be bought. Only American's 09:05 (lands 11:15) arrives by 12:15; Southwest and "
    "Delta are cheaper but land at 15:50 and 16:50.",
    distractors=[D_CHANGE])

scenario(
    "thistle-crag", "multi_rule", ["date_arithmetic", "dearer_option", "outside_air_section"],
    "Please book business class to Tokyo on January 6 for my visiting research appointment at the University of "
    "Tokyo; I'll be there until February 19. The business-class and long-stay approvals are in. If business isn't "
    "allowed, economy is fine.",
    trip(traveller_name="Dr. Grace Tanaka", traveller_title="Professor", destination="HND", travel_date="2027-01-06",
         trip_end_date="2027-02-19", days_away=45, purpose_kind="RESEARCH",
         purpose="Visiting research appointment at the University of Tokyo, January 6 - February 19",
         requested_cabin="BUSINESS", worktags=[GRANT_TAG],
         approvals=[SA_OK, *business_ok(), sign(VP, "EXTENDED_STAY", "Approved: the research stay in Tokyo, January "
                                                "6 - February 19, 2027.")],
         schedule=[ev("2027-01-08 09:00", "2027-01-08 17:00", "Laboratory work begins")]),
    [search("out", "MCO", "HND", "2027-01-06",
            {"jl": fl("JL", "11:30", [835]), "nh": fl("NH", "13:00", [830])},
            [of("jl-economy", "jl", "ECONOMY", 136000), of("jl-business", "jl", "BUSINESS", 589000),
             of("nh-economy", "nh", "ECONOMY", 129500), of("nh-business", "nh", "BUSINESS", 604000)])],
    expected("BOOK", ["jl-business"], ["BUSINESS"], ["EXTENDED_STAY_APPROVAL", "LONG_FLIGHT_APPROVED"], BIZ_ROLES,
             ["EXTENDED_STAY", "UPGRADED_TICKETS"]),
    [STAY, BUSINESS, APPROVERS],
    "A 45-day stay at one location needs the provost's or the appropriate vice president's approval (1251-1253): "
    "the Vice President for Research approved it. Business class qualifies (835/830-minute nonstops, laboratory "
    "work within 24 hours of either landing) and is approved (434-435): the lowest business fare, JAL's 589000.")

# ============================== hidden clause (3) ==============================
scenario(
    "ember-thicket", "hidden_clause", ["outside_air_section"],
    "Our rocketry club, a registered student organization, is going to the launch competition in Houston on "
    "December 10. Can you book my flight on the university's account?",
    trip(traveller_name="Priya Raman", traveller_title="Undergraduate student; president of the UCF Rocketry Club",
         passenger="UCF_STUDENT", department="UCF Rocketry Club (a Registered Student Organization)",
         headquarters="UCF main campus, Orlando, FL", destination="IAH", travel_date="2026-12-10",
         trip_end_date="2026-12-13", days_away=4, purpose_kind="STUDENT_ORGANIZATION_EVENT",
         purpose="The club's entry in the intercollegiate launch competition, Houston", funding="CLUB_FUNDS",
         approvals=[sign(ADVISOR, "CLUB_TRAVEL_FORM", "Approved: the club's travel form for the competition.")],
         schedule=[ev("2026-12-11 08:00", "2026-12-11 18:00", "Launch competition")],
         notes=[("Priya also works ten hours a week as a student assistant in the College of Engineering; this trip "
                "is not part of that job."), "No Spend Authorization exists for this trip."]),
    [search("out", "MCO", "IAH", "2026-12-10",
            {"ua": fl("UA", "08:10", [160]), "wn": fl("WN", "11:00", [165])},
            [of("ua-economy", "ua", "ECONOMY", 19800), of("wn-economy", "wn", "ECONOMY", 18400)])],
    expected("REFUSE", [], ["NONE"], ["NOT_UNIVERSITY_BUSINESS", "OUTSIDE_POLICY_SCOPE", "TRAVEL_NOT_AUTHORIZED"],
             ["NONE"], ["ELIGIBLE_RENTER", "INTRODUCTION", "SPEND_AUTHORIZATIONS"]),
    [RSO, SA],
    "Lines 594-596 (in the vehicle-renter section): RSO activity is not considered official university business; "
    "lines 194-198: travel on UCF business is authorized in advance, and no Spend Authorization exists. Her "
    "student job does not make the club's trip university business (lines 155-156 cover travel related to the "
    "employment role). The university buys no ticket.")

scenario(
    "kestrel-sound", "hidden_clause", ["date_arithmetic", "month_end", "outside_air_section"],
    "I'm teaching the winter intensive course at the University of Puerto Rico. Please book my flight to San Juan on "
    "November 30; I'll be there until December 30.",
    trip(traveller_name="Dr. Lucia Ramos", traveller_title="Associate Professor", department="Department of "
         "Modern Languages and Literatures", destination="SJU", travel_date="2026-11-30", trip_end_date="2026-12-30",
         days_away=31, purpose_kind="TEACHING",
         purpose="Teaching the winter intensive course at the University of Puerto Rico, San Juan",
         approvals=[SA_OK, sign(PROVOST, "EXTENDED_STAY", "Approved: the teaching assignment in San Juan, November 30 "
                                "- December 30, 2026.")],
         schedule=[ev("2026-12-01 08:00", "2026-12-01 16:00", "First day of classes")]),
    [search("out", "MCO", "SJU", "2026-11-30",
            {"wn": fl("WN", "07:30", [170]), "b6": fl("B6", "09:10", [165]),
             "aa": fl("AA", "06:40", [70, 160], via=["MIA"], layovers=[75])},
            [of("wn-economy", "wn", "ECONOMY", 19800), of("b6-economy", "b6", "ECONOMY", 21500),
             of("aa-economy", "aa", "ECONOMY", 24600)])],
    expected("BOOK", ["wn-economy"], ["ECONOMY"], ["EXTENDED_STAY_APPROVAL", "LOWEST_FARE"],
             ["COST_CENTER_MANAGER", "NONE", "PROVOST"], ["AIRFARE", "EXTENDED_STAY", "INTRODUCTION"]),
    [STAY, NONREF, ECONOMICAL],
    "The stay is 31 days (November 30 to December 30, counting both): more than thirty days at one location, which "
    "needs the provost's or a vice president's approval (1251-1253, a section outside the airfare rules). The "
    "provost approved it, so book the lowest non-refundable economy fare, Southwest's 19800.",
    distractors=[D_LAUNDRY, D_ADVANCE])

scenario(
    "lupine-bar", "hidden_clause", ["multi_leg", "outside_air_section"],
    "Please book my flight to Frankfurt on December 8 for the program review on the 10th; it's charged to my Office "
    "of Naval Research award.",
    trip(traveller_name="Dr. Marcus Hale", traveller_title="Research Professor", destination="FRA",
         travel_date="2026-12-08", trip_end_date="2026-12-12", days_away=5, purpose_kind="MEETING",
         purpose="Program review for the Office of Naval Research award, Frankfurt", funding="FEDERAL_AWARD",
         sponsor="U.S. Department of Defense, Office of Naval Research; the award follows federal travel rules",
         worktags=["Grant: ONR award N0014 (naval materials)"],
         approvals=[SA_OK, sign(GM, "FLY_AMERICA_EXCEPTION", "Approved on review: the Fly America Act exception form "
                                "for this trip.", on="2026-11-20")],
         schedule=[ev("2026-12-10 09:00", "2026-12-10 17:00", "Program review")],
         notes=["Delta and United show no open economy seats to Frankfurt until December 11."]),
    [search("out", "MCO", "FRA", "2026-12-08",
            {"lh": fl("LH", "18:00", [535]), "ua": fl("UA", "17:05", [160, 470], via=["EWR"], layovers=[90]),
             "dl": fl("DL", "16:20", [95, 530], via=["ATL"], layovers=[80])},
            [of("lh-economy", "lh", "ECONOMY", 82000), of("ua-economy", "ua", "ECONOMY", 80500, seats=False),
             of("dl-economy", "dl", "ECONOMY", 79000, seats=False)])],
    expected("BOOK", ["lh-economy"], ["ECONOMY"], ["FLY_AMERICA_EXCEPTION", "LOWEST_FARE"],
             ["COST_CENTER_MANAGER", "GRANT_MANAGER", "NONE"],
             ["DOCUMENTING_EXCEPTIONS", "FLY_AMERICA", "FLY_AMERICA_EXCEPTIONS", "SPONSORED_AWARD"]),
    [FLY_AMERICA, FA_UNAVAILABLE, FA_APPROVAL],
    "The Fly America Act applies (1055-1058), but the U.S. carriers' fares are sold out and they have no seats for "
    "three days: a U.S. carrier is not available and would extend the travel time by 24 hours or more (1081-1082). "
    "The exception form is approved on review (1130-1132). Lufthansa 82000 is the only fare with seats.")

# ============================== distractor (3) ==============================
scenario(
    "plover-glen", "distractor", [],
    "Please book my flight to London on December 7 for the archive visit that starts on the 9th; it's paid from my "
    "Halvorsen Foundation award.",
    trip(traveller_name="Dr. Eleanor Price", traveller_title="Associate Professor", department="Department of History",
         destination="LHR", travel_date="2026-12-07", trip_end_date="2026-12-15", days_away=9, purpose_kind="RESEARCH",
         purpose="Archive research at the British Library, London", funding="PRIVATE_AWARD",
         sponsor="The Halvorsen Foundation, a private foundation; the award's terms set no airline or travel limits",
         worktags=["Gift: Halvorsen Foundation research award"],
         schedule=[ev("2026-12-09 09:30", "2026-12-09 17:00", "Archive research")]),
    [search("out", "MCO", "LHR", "2026-12-07",
            {"ba": fl("BA", "18:40", [515]), "dl": fl("DL", "16:05", [95, 545], via=["ATL"], layovers=[70]),
             "aa": fl("AA", "17:00", [70, 520], via=["MIA"], layovers=[90])},
            [of("ba-economy", "ba", "ECONOMY", 71500), of("dl-economy", "dl", "ECONOMY", 78000),
             of("aa-economy", "aa", "ECONOMY", 76200)])],
    expected("BOOK", ["ba-economy"], ["ECONOMY"], ["LOWEST_FARE"], SA_ROLES,
             ["AIRFARE", "FLY_AMERICA", "INTRODUCTION", "SPONSORED_AWARD"]),
    [NONREF, ECONOMICAL, SPONSOR],
    "The award is a private foundation's, not federal, so the Fly America Act (1055-1058) does not apply, and its "
    "terms set no airline limits (1259-1261). The lowest non-refundable economy fare is British Airways' 71500.",
    distractors=[D_FLY_AMERICA, D_FOREIGN_TAP])

scenario(
    "teasel-pond", "distractor", [],
    "Please book me to Detroit on December 9 for the site visit the next morning. I have an American credit in my "
    "Concur profile from a trip I cancelled in October; use it if it saves the university money.",
    trip(traveller_name="Tomas Varga", traveller_title="Research Associate", destination="DTW",
         travel_date="2026-12-09", trip_end_date="2026-12-11", days_away=3, purpose_kind="SITE_VISIT",
         purpose="Site visit at the automotive battery test lab, Detroit",
         airline_credits=[{"airline": "American Airlines", "amount_cents": 6000,
                           "source": "Cancelled October trip, Orlando to Chicago (booked through Concur)"}],
         schedule=[ev("2026-12-10 08:30", "2026-12-10 16:00", "Site visit")]),
    [search("out", "MCO", "DTW", "2026-12-09",
            {"dl": fl("DL", "07:10", [160]), "wn": fl("WN", "11:25", [165]),
             "aa": fl("AA", "06:45", [95, 105], via=["CLT"], layovers=[60])},
            [of("dl-economy", "dl", "ECONOMY", 28000), of("wn-economy", "wn", "ECONOMY", 31500),
             of("aa-economy", "aa", "ECONOMY", 36000)])],
    expected("BOOK", ["dl-economy"], ["ECONOMY"], ["COST_SAVINGS", "LOWEST_FARE"], SA_ROLES,
             ["AIRFARE", "CHANGING_TICKETS", "INTRODUCTION"]),
    [ECONOMICAL, NONREF],
    "Lines 469-471 keep the credit in the profile but do not require its use. With the 6000-cent credit, American "
    "costs 30000, still more than Delta's 28000: the most economical means (106) is Delta.",
    distractors=[D_CREDIT, D_MILES])

scenario(
    "alder-flats", "distractor", ["multi_leg", "upgrade_not_taken"],
    "Please book my flight to Delhi on December 8 for the research partner meetings on the 10th. The department "
    "signed off on business class, but book whatever costs the university least; I'll manage in economy.",
    trip(traveller_name="Dr. Arjun Mehta", traveller_title="Professor", destination="DEL", travel_date="2026-12-08",
         trip_end_date="2026-12-14", days_away=7, purpose_kind="MEETING",
         purpose="Research partner meetings at the Indian Institute of Technology Delhi", worktags=[GRANT_TAG],
         approvals=[SA_OK, *business_ok()],
         schedule=[ev("2026-12-10 09:00", "2026-12-10 17:00", "Partner meetings")]),
    [search("out", "MCO", "DEL", "2026-12-08",
            {"ai": fl("AI", "21:00", [900]), "ua": fl("UA", "15:00", [160, 830], via=["EWR"], layovers=[120])},
            [of("ai-economy", "ai", "ECONOMY", 124000), of("ai-business", "ai", "BUSINESS", 468000),
             of("ua-economy", "ua", "ECONOMY", 118500), of("ua-business", "ua", "BUSINESS", 455000)])],
    expected("BOOK", ["ua-economy"], ["ECONOMY"], ["LOWEST_FARE"], BIZ_ROLES, [*ECON, "UPGRADED_TICKETS"]),
    [NONREF, ECONOMICAL],
    "Business class would qualify and is approved, but the traveller asks for the cheapest: the business rule "
    "(431-435) permits, it does not oblige. The lowest economy fare is United via Newark, 118500.",
    distractors=[near(431, 433, "Business class travel is only acceptable if at least one segment", "permission only")])

# ============================== refusal (3) ==============================
scenario(
    "dahlia-swale", "refusal", ["multi_traveller", "personal_travel", "outside_air_section"],
    "Please book my husband, Marcus, on the same Southwest flight to Austin on December 8 through the university's "
    "Southwest Business account; he's coming along to sightsee while I'm at the conference.",
    trip(traveller_name="Marcus Ortega", traveller_title="Spouse of Dr. Elena Ortega", passenger="FAMILY_MEMBER",
         accompanies="Dr. Elena Ortega, Associate Professor, Department of Physics", department="Department of Physics",
         destination="AUS", travel_date="2026-12-08", trip_end_date="2026-12-11", days_away=4, purpose_kind="VACATION",
         purpose="Accompanying his wife on her conference trip, to sightsee in Austin",
         notes=["Dr. Ortega's own ticket on the same flight is already booked under her approved Spend Authorization."]),
    [search("out", "MCO", "AUS", "2026-12-08",
            {"wn": fl("WN", "09:20", [170]), "aa": fl("AA", "07:00", [150, 75], via=["DFW"], layovers=[60])},
            [of("wn-economy", "wn", "ECONOMY", 22900), of("aa-economy", "aa", "ECONOMY", 25400)])],
    expected("REFUSE", [], ["NONE"], ["COMPANION_NOT_COVERED", "LEISURE_BOOKING_NOT_ALLOWED", "NOT_UNIVERSITY_BUSINESS",
                                      "OUTSIDE_POLICY_SCOPE", "PERSONAL_TRAVEL_NOT_COVERED", "TRAVEL_NOT_AUTHORIZED"],
             SA_ROLES, ["NON_REIMBURSABLE", "ONLINE_BOOKING", "PERSONAL_TRAVEL", "SOUTHWEST_BUSINESS",
                        "SPEND_AUTHORIZATIONS"]),
    [LEISURE, SPOUSE, PERSONAL_EXP],
    "Line 322: leisure travel booking is not allowed on Southwest Business; line 1015: spouse/family related charges "
    "are strictly not reimbursable. The university buys no ticket for him. The Spend Authorization on file is his "
    "wife's and goes unused (4(b)).")

scenario(
    "sable-cairn", "refusal", ["personal_travel", "outside_air_section"],
    "Can you book my flight to Las Vegas on December 19 through the university's travel account? It's a holiday "
    "trip with friends.",
    trip(traveller_name="Bryce Holloway", traveller_title="Laboratory Manager", destination="LAS",
         travel_date="2026-12-19", trip_end_date="2026-12-23", days_away=5, purpose_kind="VACATION",
         purpose="Holiday trip with friends", approvals=[],
         notes=["No Spend Authorization exists for this trip."]),
    [search("out", "MCO", "LAS", "2026-12-19",
            {"wn": fl("WN", "08:30", [310]), "dl": fl("DL", "07:15", [95, 250], via=["ATL"], layovers=[65])},
            [of("wn-economy", "wn", "ECONOMY", 21900), of("dl-economy", "dl", "ECONOMY", 26400)])],
    expected("REFUSE", [], ["NONE"], ["NOT_UNIVERSITY_BUSINESS", "OUTSIDE_POLICY_SCOPE", "PERSONAL_TRAVEL_NOT_COVERED",
                                      "TRAVEL_NOT_AUTHORIZED"],
             ["NONE"], ["INTRODUCTION", "NON_REIMBURSABLE", "PERSONAL_TRAVEL", "SPEND_AUTHORIZATIONS"]),
    [PERSONAL, PERSONAL_EXP, SA],
    "A holiday has no university business: expenses beyond the official business are not reimbursed (1389-1391), "
    "personal expenses are strictly not reimbursable (1004-1006), and no Spend Authorization exists (194-198).")

scenario(
    "brindle-heath", "refusal", ["outside_air_section"],
    "My Spend Authorization for the Boston conference came back denied, but I'd still like to go. Please book the "
    "December 9 flight.",
    trip(traveller_name="Nora Feld", traveller_title="Graduate Research Assistant", destination="BOS",
         travel_date="2026-12-09", trip_end_date="2026-12-12", days_away=4,
         purpose="Poster presentation at the New England Fluids Conference, Boston",
         approvals=[sign(CCM, "SPEND_AUTHORIZATION", "Denied: the cost center has no travel budget left this fiscal "
                         "year.", status="DENIED")],
         schedule=[ev("2026-12-10 08:30", "2026-12-10 17:00", "Conference, day one")]),
    [search("out", "MCO", "BOS", "2026-12-09",
            {"b6": fl("B6", "07:45", [165]), "dl": fl("DL", "06:30", [95, 135], via=["ATL"], layovers=[60])},
            [of("b6-economy", "b6", "ECONOMY", 24500), of("dl-economy", "dl", "ECONOMY", 26800)])],
    expected("REFUSE", [], ["NONE"], ["TRAVEL_NOT_AUTHORIZED"], ["COST_CENTER_MANAGER", "NONE"],
             ["INTRODUCTION", "SPEND_AUTHORIZATIONS"]),
    [SA, BUDGET],
    "Lines 194-198: travel must be authorized in advance and the Spend Authorization fully approved before any "
    "commitment; line 112: travel is contingent upon cost center approval. It was denied: buy nothing.")

# ============================== flag (4) ==============================
scenario(
    "onyx-lagoon", "flag", ["multi_leg", "unclear_phrase"], DXB_REQUEST, dxb_home("2026-12-14", "Dr. Omar Siddiqui"),
    dxb_search(),
    expected("FLAG_FOR_APPROVAL", ["dl-business", "dl-economy"], ["BUSINESS", "ECONOMY"],
             ["APPROVAL_REQUIRED", "UNCLEAR_POLICY_TEXT"], GAP, ["TRAVEL_EXCEPTIONS", "UPGRADED_TICKETS"],
             phrase="and/or return to headquarters"),
    [BUSINESS, APPROVERS, QUESTIONS, EXCEPTIONS],
    "The flight home lands Thursday 16:00 (Emirates) or 20:05 (Delta), and work at headquarters resumes Monday "
    "08:00, more than 24 hours later; on the way out, the workshop began 13 hours after landing. 'arrival at the "
    "destination and/or return to headquarters' (432-433) either lets the met destination test carry the trip "
    "(business) or applies the headquarters test to the flight home (economy).",
    flag_twins=["heather-dock", "fennel-moor"],
    ambiguity={"phrase": "and/or return to headquarters",
               "readings": [("'and/or': business beginning within 24 hours of arrival at the destination is enough, "
                            "so the business approved for the trip covers the flight home too"),
                            ("for the flight home the test is the return to headquarters, where work resumes more than "
                            "24 hours after landing, so the flight home is economy")]},
    hidden={"outbound_hours": 13})

scenario(
    "slate-orchard", "flag", ["date_arithmetic", "unclear_phrase"],
    "Please book business class to Doha on December 8 for the desalination workshop; the approvals are in. If "
    "business isn't allowed, economy is fine.",
    trip(traveller_name="Dr. Layla Haddad", traveller_title="Assistant Professor", destination="DOH",
         travel_date="2026-12-08", trip_end_date="2026-12-13", days_away=6, purpose_kind="WORKSHOP",
         purpose="Desalination research workshop at Qatar University, Doha", requested_cabin="BUSINESS",
         worktags=[GRANT_TAG], approvals=[SA_OK, *business_ok()],
         schedule=[ev("2026-12-09 19:00", "2026-12-09 21:00", "Welcome reception for workshop participants"),
                   ev("2026-12-10 13:00", "2026-12-10 18:00", "Workshop sessions"),
                   ev("2026-12-11 08:30", "2026-12-11 17:00", "Workshop sessions")]),
    doh_search("2026-12-08"),
    expected("FLAG_FOR_APPROVAL", ["aa-economy", "qr-business"], ["BUSINESS", "ECONOMY"],
             ["APPROVAL_REQUIRED", "UNCLEAR_POLICY_TEXT"], GAP, ["TRAVEL_EXCEPTIONS", "UPGRADED_TICKETS"],
             phrase="full -time business activity"),
    [BUSINESS, APPROVERS, QUESTIONS, EXCEPTIONS],
    "Qatar lands December 9 09:30; the welcome reception (two hours) starts 9.5 hours later, the first workshop "
    "session 27.5 hours later. Whether a reception is 'full -time business activity' (432) decides business against "
    "economy.",
    flag_twins=["juniper-wake", "fennel-moor"],
    ambiguity={"phrase": "full -time business activity",
               "readings": [("the official reception is business activity of the trip and begins within 24 hours, so "
                            "business class is acceptable"),
                            ("full-time activity means the working sessions, which begin more than 24 hours after "
                            "landing, so the flight is economy")]})

scenario(
    "ivory-sedge", "flag", ["multi_leg", "approval_required"],
    "Business class to Seoul on December 8, please, for the conference on the 10th. My cost center manager and the "
    "gift fund's worktag manager have signed off; the VP's sign-off is still in her queue.",
    trip(traveller_name="Dr. Min-jun Park", traveller_title="Associate Professor", destination="ICN",
         travel_date="2026-12-08", trip_end_date="2026-12-13", days_away=6,
         purpose="Plenary talk at the international photonics conference, Seoul", requested_cabin="BUSINESS",
         worktags=[GRANT_TAG], approvals=[SA_OK, *business_ok("PENDING")],
         schedule=[ev("2026-12-10 09:00", "2026-12-10 17:00", "Conference, day one")]),
    [search("out", "MCO", "ICN", "2026-12-08",
            {"ke": fl("KE", "12:00", [860]), "dl": fl("DL", "10:30", [95, 850], via=["ATL"], layovers=[85])},
            [of("ke-economy", "ke", "ECONOMY", 126000), of("ke-business", "ke", "BUSINESS", 512000),
             of("dl-economy", "dl", "ECONOMY", 119000), of("dl-business", "dl", "BUSINESS", 489000)])],
    expected("FLAG_FOR_APPROVAL", ["dl-business"], ["BUSINESS"], ["APPROVAL_REQUIRED"], ["VICE_PRESIDENT"],
             ["UPGRADED_TICKETS"]),
    [BUSINESS, APPROVERS],
    "Business qualifies (850/860-minute flights, conference within 24 hours of either landing), but lines 434-435 "
    "need the Vice President's approval besides the Cost Center Manager's and the worktag manager's; it is "
    "pending. Hold the lowest qualifying business fare, Delta's 489000, for the VP.",
    flag_twins=["amber-dune", "saguaro-bend"],
    ambiguity="none: the Vice President's sign-off is pending; the text is clear")

scenario(
    "russet-plume", "flag", ["multi_leg", "date_arithmetic", "outside_air_section", "approval_required"],
    "Please book my flight to Bogota on January 4 for my six-week field study; I'll be there until February 14.",
    trip(traveller_name="Dr. Camila Rojas", traveller_title="Assistant Professor", department="Department of "
         "Anthropology", destination="BOG", travel_date="2027-01-04", trip_end_date="2027-02-14", days_away=42,
         purpose_kind="RESEARCH", purpose="Ethnographic field study in Bogota, January 4 - February 14",
         schedule=[ev("2027-01-05 09:00", "2027-01-05 17:00", "Field work begins")],
         notes=["The Spend Authorization was filed under the standard individual-trip travel type."]),
    [search("out", "MCO", "BOG", "2027-01-04",
            {"av": fl("AV", "10:20", [235]), "aa": fl("AA", "07:10", [70, 195], via=["MIA"], layovers=[80])},
            [of("av-economy", "av", "ECONOMY", 38500), of("aa-economy", "aa", "ECONOMY", 36200)])],
    expected("FLAG_FOR_APPROVAL", ["aa-economy"], ["ECONOMY"], ["APPROVAL_REQUIRED", "EXTENDED_STAY_APPROVAL"],
             ["PROVOST", "VICE_PRESIDENT"], ["EXTENDED_STAY", "SPEND_AUTHORIZATIONS"]),
    [STAY, SA],
    "The trip lasts 42 days at one location: more than thirty days needs the provost's or the appropriate vice "
    "president's approval (1251-1253), and the Spend Authorization on file (cost center manager, standard travel "
    "type) does not give it. Hold the lowest fare, American via Miami 36200, for that approval.",
    flag_twins=["kestrel-sound", "citrus-knoll"],
    ambiguity="none: the provost's or vice president's approval for a stay over thirty days is missing; the text is "
              "clear")


def main():
    assert len(S) == 32, len(S)
    OUT.mkdir(parents=True, exist_ok=True)
    for path in OUT.glob("*.json"):
        path.unlink()
    for data in S:
        (OUT / f"{data['id']}.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(S)} scenarios")


if __name__ == "__main__":
    main()
