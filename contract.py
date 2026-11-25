"""Each tool's and task's typed input and output (see nanoagent.plugin.v0001.contract): declarations only.

The first part is the original-handbook template's shared contract and is the same in every plugin made from
it. The HANDBOOK-SPECIFIC part in the middle is filled per handbook: the scenario ids, the closed lists of
approvers and sections, and the trip record; the shared inputs and outputs after it refer to those names.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Annotated

from slimconfig import Output

# ---------------------------------------------------------------------------------------------------------
# SHARED (template): keep identical across plugins, except the agent task's id in Task.BOOK_FLIGHT.
# ---------------------------------------------------------------------------------------------------------


class Tool(Enum):
    BOOKING_REQUIREMENTS = "booking_requirements"
    GET_TRIP = "get_trip"
    SEARCH_FLIGHTS = "search_flights"
    SOLVE_BOOKING = "solve_booking"


class Task(Enum):
    BOOKING_REQUIREMENTS = "booking-requirements"
    SEARCH_FLIGHTS = "search-flights"
    BOOK_FLIGHT = "book-ucf-flight"


class Decision(Enum):
    BOOK = "BOOK"
    REFUSE = "REFUSE"
    FLAG_FOR_APPROVAL = "FLAG_FOR_APPROVAL"


class Cabin(Enum):
    ECONOMY = "ECONOMY"
    PREMIUM_ECONOMY = "PREMIUM_ECONOMY"
    BUSINESS = "BUSINESS"
    FIRST = "FIRST"
    NONE = "NONE"


class ReasonCode(Enum):
    """Why the decision was made. The list is shared by every handbook plugin, so it also holds reasons
    that a given handbook never uses."""

    LOWEST_FARE = "LOWEST_FARE"
    UPGRADE_NOT_ELIGIBLE = "UPGRADE_NOT_ELIGIBLE"
    CLIENT_REIMBURSABLE = "CLIENT_REIMBURSABLE"
    UPGRADE_WITHIN_FARE_MARGIN = "UPGRADE_WITHIN_FARE_MARGIN"
    MEDICAL_NEED = "MEDICAL_NEED"
    COST_SAVINGS = "COST_SAVINGS"
    NO_ECONOMY_SEATS_URGENT = "NO_ECONOMY_SEATS_URGENT"
    TRAVELER_PAYS_UPGRADE = "TRAVELER_PAYS_UPGRADE"
    LONG_FLIGHT_APPROVED = "LONG_FLIGHT_APPROVED"
    LONG_FLIGHT_CONDITION_NOT_MET = "LONG_FLIGHT_CONDITION_NOT_MET"
    PREMIUM_ECONOMY_ALLOWED = "PREMIUM_ECONOMY_ALLOWED"
    UPGRADE_COST_NOT_NOMINAL = "UPGRADE_COST_NOT_NOMINAL"
    ALTERNATE_ROUTE_WITHIN_MARGIN = "ALTERNATE_ROUTE_WITHIN_MARGIN"
    ALTERNATE_ROUTE_TOO_EXPENSIVE = "ALTERNATE_ROUTE_TOO_EXPENSIVE"
    LOYALTY_PROGRAM_PREFERENCE = "LOYALTY_PROGRAM_PREFERENCE"
    COMPANION_NOT_COVERED = "COMPANION_NOT_COVERED"
    PERSONAL_TRAVEL_NOT_COVERED = "PERSONAL_TRAVEL_NOT_COVERED"
    OUTSIDE_POLICY_SCOPE = "OUTSIDE_POLICY_SCOPE"
    NO_COMPLIANT_OFFER = "NO_COMPLIANT_OFFER"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    UNCLEAR_POLICY_TEXT = "UNCLEAR_POLICY_TEXT"
    ADVANCE_PURCHASE_TOO_LATE = "ADVANCE_PURCHASE_TOO_LATE"
    DISTANCE_BELOW_MINIMUM = "DISTANCE_BELOW_MINIMUM"
    DRIVING_EXPECTED = "DRIVING_EXPECTED"
    RAIL_PREFERRED = "RAIL_PREFERRED"
    REFUNDABLE_FARE_NOT_ALLOWED = "REFUNDABLE_FARE_NOT_ALLOWED"
    PREFERRED_CARRIER_REQUIRED = "PREFERRED_CARRIER_REQUIRED"
    CONNECTION_TOO_LONG = "CONNECTION_TOO_LONG"
    OVERNIGHT_STOP_REQUIRED = "OVERNIGHT_STOP_REQUIRED"
    NATIONAL_CARRIER_REQUIRED = "NATIONAL_CARRIER_REQUIRED"
    SENIOR_ROLE_ENTITLEMENT = "SENIOR_ROLE_ENTITLEMENT"
    INTERNATIONAL_LONG_FLIGHT = "INTERNATIONAL_LONG_FLIGHT"
    TRAVELLER_LIMIT_PER_FLIGHT = "TRAVELLER_LIMIT_PER_FLIGHT"
    # HANDBOOK-SPECIFIC reason codes go below this line; keep every shared one above.
    FIRST_CLASS_NOT_ALLOWED = "FIRST_CLASS_NOT_ALLOWED"
    TRAVEL_TIME_DEVIATION_CHEAPER = "TRAVEL_TIME_DEVIATION_CHEAPER"
    TRAVEL_TIME_DEVIATION_DEARER = "TRAVEL_TIME_DEVIATION_DEARER"
    EXTENDED_STAY_APPROVAL = "EXTENDED_STAY_APPROVAL"
    FLY_AMERICA_US_CARRIER_REQUIRED = "FLY_AMERICA_US_CARRIER_REQUIRED"
    FLY_AMERICA_EXCEPTION = "FLY_AMERICA_EXCEPTION"
    TRAVEL_NOT_AUTHORIZED = "TRAVEL_NOT_AUTHORIZED"
    NOT_UNIVERSITY_BUSINESS = "NOT_UNIVERSITY_BUSINESS"
    LEISURE_BOOKING_NOT_ALLOWED = "LEISURE_BOOKING_NOT_ALLOWED"
    NEW_TICKET_AFTER_AIRLINE_DISRUPTION = "NEW_TICKET_AFTER_AIRLINE_DISRUPTION"
    MILES_TICKET_NOT_REIMBURSABLE = "MILES_TICKET_NOT_REIMBURSABLE"
    # Decoys: codes for rules of other handbooks that this one lacks, so the list hints at none of its own rules.
    WEEKEND_TRAVEL_HOME = "WEEKEND_TRAVEL_HOME"
    WEEKEND_TRIP_NOT_EARNED = "WEEKEND_TRIP_NOT_EARNED"
    NEXT_OF_KIN_TRAVEL = "NEXT_OF_KIN_TRAVEL"
    CREATIVE_TICKETING = "CREATIVE_TICKETING"
    DENIED_BOARDING_NOT_ALLOWED = "DENIED_BOARDING_NOT_ALLOWED"
    CHANCELLOR_WRITTEN_AUTHORIZATION = "CHANCELLOR_WRITTEN_AUTHORIZATION"
    DOUBLE_BOOKING_PROHIBITED = "DOUBLE_BOOKING_PROHIBITED"
    PRIVATE_AIRCRAFT_NOT_APPROVED = "PRIVATE_AIRCRAFT_NOT_APPROVED"
    SAME_CLASS_AS_CUSTOMER = "SAME_CLASS_AS_CUSTOMER"
    TRAVEL_PACKAGE_NOT_ITEMIZED = "TRAVEL_PACKAGE_NOT_ITEMIZED"


class TripType(Enum):
    ONE_WAY = "ONE_WAY"
    ROUND_TRIP = "ROUND_TRIP"


class Topic(Enum):
    ALL = "ALL"
    FIELDS = "FIELDS"
    AIRPORTS = "AIRPORTS"


CODE = "An IATA airport code, e.g. JFK"


@dataclass
class Airport(Output):
    code: Annotated[str, CODE]
    name: Annotated[str, "The airport's name"]
    city: Annotated[str, "The city it serves"]
    country: Annotated[str, "Its country, as an ISO code"]


@dataclass
class Segment(Output):
    flight_number: Annotated[str, "The airline's flight number, e.g. BA 117"]
    origin: Annotated[str, CODE]
    destination: Annotated[str, CODE]
    depart_local: Annotated[str, "When it leaves: YYYY-MM-DD HH:MM, local time at that airport"]
    arrive_local: Annotated[str, "When it lands: YYYY-MM-DD HH:MM, local time at that airport"]
    depart_utc: Annotated[str, "When it leaves: YYYY-MM-DD HH:MM, UTC"]
    arrive_utc: Annotated[str, "When it lands: YYYY-MM-DD HH:MM, UTC"]
    scheduled_minutes: Annotated[int, "Its scheduled time from departure to arrival, in minutes"]


@dataclass
class Offer(Output):
    offer_id: Annotated[str, "The offer's id, to submit when booking or holding it"]
    carrier: Annotated[str, "The airline"]
    trip_type: Annotated[TripType, "ONE_WAY, or ROUND_TRIP when the fare covers the flights out and back"]
    cabin: Annotated[Cabin, "The cabin sold on every flight of the offer"]
    fare_cents: Annotated[int, "The whole fare for one passenger, in cents of the search's currency"]
    seats_available: Annotated[bool, "False when this cabin is sold out on these flights: it is listed but cannot be bought"]
    refundable: Annotated[bool, "Whether the fare can be refunded or changed without a fee"]
    stops: Annotated[int, "Connections on the way out; zero for a nonstop"]
    segments: Annotated[list[Segment], "The flights out, in order"]
    layover_minutes: Annotated[list[int], "Minutes on the ground between consecutive flights out"]
    stopover_nights: Annotated[list[bool], "Per connection out: true when it is a ticketed stopover with a hotel night booked"]
    flying_minutes: Annotated[int, "The flights' scheduled minutes out added together, ground time left out"]
    elapsed_minutes: Annotated[int, "Minutes from the first departure out to the last arrival, ground time included"]
    return_segments: Annotated[list[Segment], "For a round trip, the flights back, in order; empty otherwise"]
    return_layover_minutes: Annotated[list[int], "Minutes on the ground between consecutive flights back"]
    return_stopover_nights: Annotated[list[bool], "Per connection back: true for a ticketed stopover with a hotel night"]
    return_flying_minutes: Annotated[int, "The flights' scheduled minutes back added together; zero one way"]
    return_elapsed_minutes: Annotated[int, "Minutes from the first departure back to the last arrival; zero one way"]


# ---------------------------------------------------------------------------------------------------------
# HANDBOOK-SPECIFIC: University of Central Florida, Travel Manual (revised October 2026).
# ---------------------------------------------------------------------------------------------------------


class Scenario(Enum):
    ALDER_FLATS = "alder-flats"
    AMBER_DUNE = "amber-dune"
    BASALT_WHARF = "basalt-wharf"
    BRINDLE_HEATH = "brindle-heath"
    CITRUS_KNOLL = "citrus-knoll"
    CYPRESS_LARK = "cypress-lark"
    DAHLIA_SWALE = "dahlia-swale"
    EMBER_THICKET = "ember-thicket"
    FENNEL_MOOR = "fennel-moor"
    GARNET_SPIRE = "garnet-spire"
    HEATHER_DOCK = "heather-dock"
    HERON_BAYOU = "heron-bayou"
    IVORY_SEDGE = "ivory-sedge"
    JUNIPER_WAKE = "juniper-wake"
    KESTREL_SOUND = "kestrel-sound"
    LINDEN_QUAY = "linden-quay"
    LUPINE_BAR = "lupine-bar"
    MALLOW_PIKE = "mallow-pike"
    MARLIN_GATE = "marlin-gate"
    ONYX_LAGOON = "onyx-lagoon"
    OSPREY_WREN = "osprey-wren"
    PECAN_SHOAL = "pecan-shoal"
    PLOVER_GLEN = "plover-glen"
    RUSSET_PLUME = "russet-plume"
    SABLE_CAIRN = "sable-cairn"
    SAGUARO_BEND = "saguaro-bend"
    SLATE_ORCHARD = "slate-orchard"
    SORREL_MESA = "sorrel-mesa"
    TAMARIND_COVE = "tamarind-cove"
    TEASEL_POND = "teasel-pond"
    THISTLE_CRAG = "thistle-crag"
    WALNUT_FERRY = "walnut-ferry"


class Approver(Enum):
    """Roles that may sign off. NONE: the decision relies on no one's sign-off, given or awaited (one for
    something else may be on file). NOT_NAMED: one is needed, but the handbook names no role."""

    NONE = "NONE"
    NOT_NAMED = "NOT_NAMED"
    COST_CENTER_MANAGER = "COST_CENTER_MANAGER"
    WORKTAG_MANAGER = "WORKTAG_MANAGER"
    VICE_PRESIDENT = "VICE_PRESIDENT"
    PROVOST = "PROVOST"
    GRANT_MANAGER = "GRANT_MANAGER"
    FINANCE_BUSINESS_CENTER = "FINANCE_BUSINESS_CENTER"
    TRAVEL_EXPERTISE_CENTER = "TRAVEL_EXPERTISE_CENTER"
    UCF_GLOBAL = "UCF_GLOBAL"
    OFFICE_OF_RESEARCH = "OFFICE_OF_RESEARCH"
    DEAN = "DEAN"
    CHIEF_FINANCIAL_OFFICER = "CHIEF_FINANCIAL_OFFICER"
    BOARD_OF_TRUSTEES = "BOARD_OF_TRUSTEES"


class Clause(Enum):
    """The handbook's sections, by heading."""

    INTRODUCTION = "INTRODUCTION"
    SPEND_AUTHORIZATIONS = "SPEND_AUTHORIZATIONS"
    SPEND_AUTHORIZATION_TYPES = "SPEND_AUTHORIZATION_TYPES"
    ONLINE_BOOKING = "ONLINE_BOOKING"
    SOUTHWEST_BUSINESS = "SOUTHWEST_BUSINESS"
    REIMBURSEMENT_GUIDELINES = "REIMBURSEMENT_GUIDELINES"
    AIRFARE = "AIRFARE"
    UPGRADED_TICKETS = "UPGRADED_TICKETS"
    CHANGING_TICKETS = "CHANGING_TICKETS"
    AIRLINE_RECEIPTS = "AIRLINE_RECEIPTS"
    ALLOWABLE_TRAVEL_TIME = "ALLOWABLE_TRAVEL_TIME"
    AIRLINE_DELAY = "AIRLINE_DELAY"
    ELIGIBLE_RENTER = "ELIGIBLE_RENTER"
    PERSONAL_VEHICLE = "PERSONAL_VEHICLE"
    TRAIN = "TRAIN"
    NON_REIMBURSABLE = "NON_REIMBURSABLE"
    FOREIGN_TRAVEL = "FOREIGN_TRAVEL"
    FLY_AMERICA = "FLY_AMERICA"
    FLY_AMERICA_EXCEPTIONS = "FLY_AMERICA_EXCEPTIONS"
    DOCUMENTING_EXCEPTIONS = "DOCUMENTING_EXCEPTIONS"
    SPECIAL_CIRCUMSTANCES = "SPECIAL_CIRCUMSTANCES"
    EXTENDED_STAY = "EXTENDED_STAY"
    SPONSORED_AWARD = "SPONSORED_AWARD"
    TRAVEL_EXCEPTIONS = "TRAVEL_EXCEPTIONS"
    PERSONAL_TRAVEL = "PERSONAL_TRAVEL"


class Passenger(Enum):
    UCF_EMPLOYEE = "UCF_EMPLOYEE"
    UCF_STUDENT = "UCF_STUDENT"
    FAMILY_MEMBER = "FAMILY_MEMBER"


class Purpose(Enum):
    CONFERENCE = "CONFERENCE"
    MEETING = "MEETING"
    RESEARCH = "RESEARCH"
    TEACHING = "TEACHING"
    WORKSHOP = "WORKSHOP"
    SITE_VISIT = "SITE_VISIT"
    STUDENT_ORGANIZATION_EVENT = "STUDENT_ORGANIZATION_EVENT"
    VACATION = "VACATION"


class Leg(Enum):
    """Which flight of the trip the request is for."""

    OUTBOUND = "OUTBOUND"
    RETURN = "RETURN"


class Funding(Enum):
    DEPARTMENT_FUNDS = "DEPARTMENT_FUNDS"
    FEDERAL_AWARD = "FEDERAL_AWARD"
    PRIVATE_AWARD = "PRIVATE_AWARD"
    CLUB_FUNDS = "CLUB_FUNDS"
    PERSONAL_FUNDS = "PERSONAL_FUNDS"


class Role(Enum):
    """The signer's role, as the university's records give it."""

    COST_CENTER_MANAGER = "COST_CENTER_MANAGER"
    WORKTAG_MANAGER = "WORKTAG_MANAGER"
    VICE_PRESIDENT = "VICE_PRESIDENT"
    PROVOST = "PROVOST"
    GRANT_MANAGER = "GRANT_MANAGER"
    FACULTY_ADVISOR = "FACULTY_ADVISOR"
    UCF_GLOBAL = "UCF_GLOBAL"


class Subject(Enum):
    """What a sign-off covers."""

    SPEND_AUTHORIZATION = "SPEND_AUTHORIZATION"
    BUSINESS_CLASS = "BUSINESS_CLASS"
    EXTENDED_STAY = "EXTENDED_STAY"
    FLY_AMERICA_EXCEPTION = "FLY_AMERICA_EXCEPTION"
    CLUB_TRAVEL_FORM = "CLUB_TRAVEL_FORM"
    TRAVEL_APPROVAL_PETITION = "TRAVEL_APPROVAL_PETITION"


class Status(Enum):
    APPROVED = "APPROVED"
    PENDING = "PENDING"
    DENIED = "DENIED"


@dataclass
class Approval(Output):
    approver_name: Annotated[str, "Who signs"]
    approver_title: Annotated[str, "Their job title"]
    role: Annotated[Role, "Their role for this sign-off"]
    subject: Annotated[Subject, "What it covers"]
    status: Annotated[Status, "APPROVED, PENDING (sent, not yet signed) or DENIED"]
    wording: Annotated[str, "What it says, word for word; empty while pending"]
    given_on: Annotated[str, "The day it was signed or sent, YYYY-MM-DD"]


@dataclass
class Event(Output):
    starts_local: Annotated[str, "When it starts: YYYY-MM-DD HH:MM, local time where the flight lands"]
    ends_local: Annotated[str, "When it ends: YYYY-MM-DD HH:MM, local time there"]
    what: Annotated[str, "What it is, in plain words"]


@dataclass
class AirlineCredit(Output):
    airline: Annotated[str, "The airline that holds it"]
    amount_cents: Annotated[int, "Its value, in cents of the search's currency"]
    source: Annotated[str, "The cancelled ticket it comes from"]


@dataclass
class Trip(Output):
    traveller_name: Annotated[str, "Who flies"]
    traveller_title: Annotated[str, "Their job title, or their relation to the employee they go with"]
    passenger: Annotated[Passenger, "What the person flying is to the university"]
    accompanies: Annotated[str, "For a family member, the employee they go with, by name and title; empty otherwise"]
    department: Annotated[str, "The university department or office the trip is for; for a student club, the club"]
    headquarters: Annotated[str, "The traveller's official headquarters: campus, city and state"]
    origin: Annotated[Airport, "Where the flight leaves from"]
    destination: Annotated[Airport, "Where the flight goes"]
    leg: Annotated[Leg, "OUTBOUND for the flight to the business, RETURN for the flight back to headquarters"]
    travel_date: Annotated[str, "The day the traveller asks to leave, YYYY-MM-DD: the local date at the origin airport"]
    fallback_date: Annotated[
        str, "Another day the traveller names to leave on, YYYY-MM-DD, if the day asked for is not one the university pays for; empty when none"
    ]
    trip_end_date: Annotated[str, "The last day of the whole trip, YYYY-MM-DD"]
    days_away: Annotated[int, "How long the whole trip lasts, in days, counting the day it starts and the day it ends"]
    booking_date: Annotated[str, "Today in this world, the day the ticket is bought, YYYY-MM-DD"]
    purpose: Annotated[str, "Why the trip is made, in plain words"]
    purpose_kind: Annotated[Purpose, "The kind of trip"]
    schedule: Annotated[
        list[Event], "The traveller's business where this flight lands, in order: at the destination, or for a flight back, at headquarters"
    ]
    must_arrive_by: Annotated[
        str, "The latest local date and time, YYYY-MM-DD HH:MM, at which the traveller can land and still do the business; empty when there is no such limit"
    ]
    funding: Annotated[Funding, "Who pays for the trip"]
    sponsor: Annotated[str, "For an award, who funds it (the agency or foundation) and its terms on travel; empty otherwise"]
    worktags: Annotated[list[str], "The funding worktags charged besides the cost center (grants, projects, gifts)"]
    requested_cabin: Annotated[Cabin, "The cabin the traveller asks for"]
    refundable_requested: Annotated[bool, "True when the traveller asks for a fare that can be refunded"]
    airline_disruption: Annotated[
        str, "What the airline did to the traveller's original flight for this trip, and what the traveller has done about it; empty when nothing"
    ]
    airline_credits: Annotated[list[AirlineCredit], "Credits from cancelled tickets in the traveller's booking profile"]
    approvals: Annotated[list[Approval], "Sign-offs on file or sent for this trip"]
    notes: Annotated[list[str], "Other facts on file for this trip"]


# ---------------------------------------------------------------------------------------------------------
# SHARED (template), continued: the tools' and tasks' inputs and outputs.
# ---------------------------------------------------------------------------------------------------------


@dataclass
class TaskInput(Output):
    scenario: Annotated[Scenario, "The booking request's case id"]
    request: Annotated[str, "The traveller's request, in their own words"]


@dataclass
class TripInput(Output):
    scenario: Annotated[Scenario, "The booking request's case id, as the task input gives it"]


@dataclass
class TripOutput(Output):
    scenario: Annotated[Scenario, "The case id"]
    request: Annotated[str, "The traveller's request, in their own words"]
    trip: Annotated[Trip, "The trip record behind the request"]


@dataclass
class SearchInput(Output):
    scenario: Annotated[Scenario, "The booking request's case id"]
    origin: Annotated[str, "The airport to leave from: An IATA airport code, e.g. JFK"]
    destination: Annotated[str, "The airport to fly to: An IATA airport code, e.g. JFK"]
    date: Annotated[str, "The day to leave, YYYY-MM-DD: the local date at the origin airport, on or after the booking date"]
    return_date: Annotated[str, "For round-trip fares, the day to fly back, YYYY-MM-DD, local at the destination; empty for one way"]


@dataclass
class SearchOutput(Output):
    note: Annotated[str, "Where the offers come from, and a word when this case lists none for the search"]
    currency: Annotated[str, "The currency of every fare, as an ISO code"]
    offers: Annotated[list[Offer], "Every offer leaving on that local date, in departure order"]


@dataclass
class BookingOutput(Output):
    decision: Annotated[
        Decision,
        "BOOK: buy offer_id now. REFUSE: buy nothing, because the organisation buys no ticket at all for this request. "
        "FLAG_FOR_APPROVAL: hold offer_id and buy nothing yet, because someone must approve it first or "
        "the handbook's words leave the answer open",
    ]
    offer_id: Annotated[str, "The offer bought or held, exactly as search_flights listed it; empty when refusing"]
    cabin: Annotated[Cabin, "That offer's cabin; NONE when refusing"]
    reason_code: Annotated[ReasonCode, "Why, from the closed list"]
    approver: Annotated[
        Approver,
        "The role whose sign-off this decision relies on, whether already on file or still awaited; NONE when "
        "this decision relies on no one's sign-off, even if a sign-off for something else is on file; NOT_NAMED "
        "when a sign-off is needed but the handbook names no role",
    ]
    clause: Annotated[Clause, "The handbook section the decision rests on"]


@dataclass
class SolveOutput(Output):
    trip: Annotated[Trip, "The trip record"]
    offers: Annotated[list[Offer], "Every offer on the trip's route and date"]
    decision: Annotated[Decision, "The correct decision"]
    offer_ids: Annotated[list[str], "Every offer id that is a correct choice; empty when refusing"]
    cabins: Annotated[list[Cabin], "Every correct cabin"]
    reason_codes: Annotated[list[ReasonCode], "Every accepted reason"]
    approvers: Annotated[list[Approver], "Every accepted approver"]
    clauses: Annotated[list[Clause], "Every accepted section"]
    unclear_phrase: Annotated[str, "For a hold over unclear words, those words; empty otherwise"]
    explanation: Annotated[str, "How the answer key reached the answer"]


@dataclass
class FieldHelp(Output):
    name: Annotated[str, "The trip record field's name"]
    kind: Annotated[str, "Its type"]
    description: Annotated[str, "What it means"]


@dataclass
class RequirementsInput(Output):
    topic: Annotated[Topic, "ALL for everything, FIELDS for the trip record's fields, AIRPORTS for the airport list"]


@dataclass
class RequirementsOutput(Output):
    fields: Annotated[list[FieldHelp], "The trip record's fields; empty for AIRPORTS"]
    conventions: Annotated[list[str], "How times, dates, fares and seats work in this world; empty for AIRPORTS"]
    airports: Annotated[list[Airport], "The airports the simulated world knows; empty for FIELDS"]


TOOLS = {
    Tool.BOOKING_REQUIREMENTS: (RequirementsInput, RequirementsOutput),
    Tool.GET_TRIP: (TripInput, TripOutput),
    Tool.SEARCH_FLIGHTS: (SearchInput, SearchOutput),
    Tool.SOLVE_BOOKING: (TaskInput, SolveOutput),
}
TASKS = {
    Task.BOOKING_REQUIREMENTS: (RequirementsInput, RequirementsOutput),
    Task.SEARCH_FLIGHTS: (SearchInput, SearchOutput),
    Task.BOOK_FLIGHT: (TaskInput, BookingOutput),
}
