"""The answer key's rules for the University of Central Florida Travel Manual (revised October 2026), as exact
integer code. Byte-identical in src/plugin/rules.py and verifier/rules.py; it imports only modules a verifier
may use.

Every rule cites the frozen handbook text (src/plugin/data/policy.txt) by line. Where the text leaves an
answer open, the rule returns FLAG_FOR_APPROVAL with the unclear words, and a scenario may depend on each
unclear phrase at most once (tests/test_scenarios.py). Combinations no scenario needs raise ValueError, so a
new scenario cannot fall silently into untested logic.

The duration hook. The manual's one flight-length threshold is the business-class rule of 7.1 (lines
431-433): "at least one segment of the flight shown on the purchased tickets is nine hours or longer". It is
inclusive ("or longer") and per segment: one flight of the ticket must be scheduled for 540 minutes or more;
flights are never added up, and ground time never counts. The same sentence adds a second test, that
"full -time business activity begins within 24 hours of arrival at the destination and/or return to
headquarters": that one compares the landing with the trip's schedule and is coded in ``day_test`` (within:
inclusive, at most 1,440 minutes).

Approvers (template SYNC_NOTES 4'): a BOOK or REFUSE accepts NONE and the role of every sign-off on file
(those it relies on, 4'(a'), and those it does not use, 4(b)); a hold awaiting a sign-off accepts only the
awaited roles; a hold over unclear words accepts the offices the manual sends such questions to.
"""

from contract import (
    Approver,
    Cabin,
    Clause,
    Decision,
    Funding,
    Leg,
    Passenger,
    Purpose,
    ReasonCode,
    Role,
    Status,
    Subject,
)

from .world import clock_minutes, day_number, days_between

HANDBOOK = "University of Central Florida, Travel Manual, revised October 2026"

# Each closed-list section and the heading it names in the frozen text (tests check every heading is there).
CLAUSE_HEADINGS = {
    Clause.INTRODUCTION: "1.0 Introduction",
    Clause.SPEND_AUTHORIZATIONS: "4.0 Spend Authorizations",
    Clause.SPEND_AUTHORIZATION_TYPES: "4.1 Types of Travel Spend Authorizations",
    Clause.ONLINE_BOOKING: "5.1 Online Travel Booking",
    Clause.SOUTHWEST_BUSINESS: "B. Accessing Southwest Business Booking Tool",
    Clause.REIMBURSEMENT_GUIDELINES: "6.1 General Guidelines for Travel Reimbursement",
    Clause.AIRFARE: "7.0 Airfare/Common Carrier",
    Clause.UPGRADED_TICKETS: "7.1 Upgraded Airline Tickets",
    Clause.CHANGING_TICKETS: "7.2 Changing or Cancelling Airline Tickets",
    Clause.AIRLINE_RECEIPTS: "7.3 Airline Receipts",
    Clause.ALLOWABLE_TRAVEL_TIME: "7.4 Allowable Travel Time",
    Clause.AIRLINE_DELAY: "7.5 Flight Delay or Cancellation by Airline",
    Clause.ELIGIBLE_RENTER: "8.6 Eligible Vehicle Renter",
    Clause.PERSONAL_VEHICLE: "11.0 Use of Personal Vehicle",
    Clause.TRAIN: "12.0 Train",
    Clause.NON_REIMBURSABLE: "15.0 Non-reimbursable Expenses",
    Clause.FOREIGN_TRAVEL: "16.0 Foreign Travel",
    Clause.FLY_AMERICA: "16.3 Fly America Act",
    Clause.FLY_AMERICA_EXCEPTIONS: "B. Permitted Exceptions to the Fly America Act",
    Clause.DOCUMENTING_EXCEPTIONS: "C. Documenting Exceptions",
    Clause.SPECIAL_CIRCUMSTANCES: "17.0 Travel with Special Circumstances",
    Clause.EXTENDED_STAY: "17.2 Travel in Excess of 30 Calendar Days Rule",
    Clause.SPONSORED_AWARD: "17.3 Travel on a Sponsored Award (Research, Service or Other)",
    Clause.TRAVEL_EXCEPTIONS: "17.4 Travel Exceptions",
    Clause.PERSONAL_TRAVEL: "21.0 Personal Travel",
}

# Lines 431-433: business class only if "at least one segment of the flight shown on the purchased tickets is
# nine hours or longer" (inclusive, per segment).
SEGMENT_MINUTES = 540
DURATION_RULES = (
    {"name": "business-segment", "minutes": SEGMENT_MINUTES, "operator": ">=", "lines": [431, 433],
     "quote": "at least one segment of the flight shown on the purchased tickets is nine hours or longer"},
)

# Handbook-specific conventions shown by booking_requirements, beyond the template's (none here).
CONVENTIONS = ()

# Lines 432-433: "full -time business activity begins within 24 hours of arrival" (within: inclusive).
DAY_MINUTES = 24 * 60
# An event this long or longer is a working session; a shorter one (a reception) leaves "full -time" open.
SESSION_MINUTES = 240
# Lines 1251-1253: "more than thirty (30) days to a single location" (strict) needs the provost or a VP.
STAY_DAYS = 30
# Lines 1055-1058: U.S. flag air carriers, among the world's airlines.
US_CARRIERS = {"American Airlines", "Delta Air Lines", "United Airlines", "Alaska Airlines", "JetBlue",
               "Southwest Airlines"}
DEFENSE = "Department of Defense"

FULL_TIME_PHRASE = "full -time business activity"
AND_OR_PHRASE = "and/or return to headquarters"
# Who resolves an unclear upgrade question: lines 438-439 (the Finance Business Center or the Travel Center of
# Expertise, before booking) and lines 1264-1266 (exceptions need the Travel Center of Expertise's prior
# approval); NOT_NAMED because no clause names a role for this gap itself.
GAP_APPROVERS = [Approver.NOT_NAMED, Approver.FINANCE_BUSINESS_CENTER, Approver.TRAVEL_EXPERTISE_CENTER]
UNCLEAR_REASONS = [ReasonCode.UNCLEAR_POLICY_TEXT, ReasonCode.APPROVAL_REQUIRED]
# Lines 434-435: business class "must be approved by the Cost Center Manager, applicable worktag managers, and
# the appropriate Vice President".
ROLE_APPROVER = {
    Role.COST_CENTER_MANAGER: Approver.COST_CENTER_MANAGER,
    Role.WORKTAG_MANAGER: Approver.WORKTAG_MANAGER,
    Role.VICE_PRESIDENT: Approver.VICE_PRESIDENT,
    Role.PROVOST: Approver.PROVOST,
    Role.GRANT_MANAGER: Approver.GRANT_MANAGER,
    # Lines 1027-1029: foreign travel is approved through UCF Global's Travel Approval Petition.
    Role.UCF_GLOBAL: Approver.UCF_GLOBAL,
}
ECONOMY_CLAUSES = [Clause.AIRFARE, Clause.INTRODUCTION]


def over(rule, offer):
    """The duration hook: whether any one flight of ``offer`` is scheduled for 540 minutes or more."""
    if rule != "business-segment":
        raise ValueError(f"this handbook has no duration rule {rule!r}")
    return any(segment.scheduled_minutes >= SEGMENT_MINUTES for segment in offer.segments)


def by_value(items):
    return sorted(set(items), key=lambda item: item.value)


def answer(decision, offers, reasons, approvers, clauses, why, phrase=""):
    return {
        "decision": decision,
        "offer_ids": sorted(offer.offer_id for offer in offers),
        "cabins": by_value(offer.cabin for offer in offers) or [Cabin.NONE],
        "reason_codes": by_value(reasons),
        "approvers": by_value(approvers),
        "clauses": by_value(clauses),
        "unclear_phrase": phrase,
        "explanation": why,
    }


def cheapest(offers):
    if not offers:
        return []
    low = min(offer.fare_cents for offer in offers)
    return [offer for offer in offers if offer.fare_cents == low]


def one(offers, what):
    if len(offers) != 1:
        raise ValueError(f"{len(offers)} offers tie for {what}; a scenario gives exactly one")
    return offers[0]


def minute_of(text):
    """Minutes since 1970 of a YYYY-MM-DD HH:MM time (both sides read in the same local time)."""
    return day_number(text[:10]) * 1440 + clock_minutes(text[11:])


def on_file(trip, status=Status.APPROVED):
    return [record for record in trip.approvals if record.status == status]


def roles_on_file(trip):
    """Approver roles of every approved sign-off on file (a club advisor's form stands for none)."""
    return [ROLE_APPROVER[record.role] for record in on_file(trip) if record.role in ROLE_APPROVER]


def signed(trip, subject, role, status=Status.APPROVED):
    return [record for record in trip.approvals
            if record.subject == subject and record.role == role and record.status == status
            and days_between(record.given_on, trip.booking_date) >= 0]


def book(trip, offers, reasons, clauses, why):
    """A BOOK accepts NONE and every approved sign-off's role (SYNC_NOTES 4'(a') and 4(b)). A BOOK that declines
    what the traveller asked for carries only the codes for the ground of declining (brief lesson 12)."""
    return answer(Decision.BOOK, offers, reasons, [Approver.NONE, *roles_on_file(trip)], clauses, why)


def refuse(trip, reasons, clauses, why, extra=()):
    return answer(Decision.REFUSE, [], reasons, [Approver.NONE, *roles_on_file(trip), *extra], clauses, why)


def plain_economy(offers):
    """Seated economy fares that are not refundable (lines 122 and 422)."""
    return [offer for offer in offers if offer.seats_available and offer.cabin == Cabin.ECONOMY and not offer.refundable]


def leaves_on(offers, day):
    return [offer for offer in offers if offer.segments[0].depart_local[:10] == day]


def solve(trip, offers, hidden):
    """The answer key for one trip and the offers of its pinned searches: the decision, and every accepted
    offer id, cabin, reason, approver and section. ``hidden`` (answer_key_inputs) gives, for a flight back to
    headquarters only, ``outbound_hours``: the whole hours from the outbound landing to the first business at
    the destination, which the trip record states in words."""
    if set(hidden) - {"outbound_hours"} or (hidden and trip.leg != Leg.RETURN):
        raise ValueError("only a flight back to headquarters carries answer_key_inputs (outbound_hours)")
    if trip.passenger == Passenger.FAMILY_MEMBER:
        return refuse(trip, [ReasonCode.COMPANION_NOT_COVERED, ReasonCode.PERSONAL_TRAVEL_NOT_COVERED,
                             ReasonCode.LEISURE_BOOKING_NOT_ALLOWED, ReasonCode.NOT_UNIVERSITY_BUSINESS,
                             ReasonCode.OUTSIDE_POLICY_SCOPE, ReasonCode.TRAVEL_NOT_AUTHORIZED],
                      [Clause.SOUTHWEST_BUSINESS, Clause.ONLINE_BOOKING, Clause.NON_REIMBURSABLE, Clause.PERSONAL_TRAVEL,
                       Clause.SPEND_AUTHORIZATIONS],
                      "Line 322: leisure travel booking is not allowed on Southwest Business; line 1015: spouse/family "
                      "related charges are strictly not reimbursable (lines 997, 1004-1006: personal expenses). The "
                      "university buys no ticket for the employee's spouse.")
    if trip.purpose_kind == Purpose.STUDENT_ORGANIZATION_EVENT:
        return refuse(trip, [ReasonCode.NOT_UNIVERSITY_BUSINESS, ReasonCode.OUTSIDE_POLICY_SCOPE,
                             ReasonCode.TRAVEL_NOT_AUTHORIZED],
                      [Clause.ELIGIBLE_RENTER, Clause.SPEND_AUTHORIZATIONS, Clause.INTRODUCTION],
                      "Lines 594-596: RSO activity is not considered official university business; lines 194-198: "
                      "travel on UCF business is authorized in advance by a Spend Authorization, and none exists. "
                      "The university buys no ticket for the club's trip.")
    if trip.purpose_kind == Purpose.VACATION:
        return refuse(trip, [ReasonCode.PERSONAL_TRAVEL_NOT_COVERED, ReasonCode.OUTSIDE_POLICY_SCOPE,
                             ReasonCode.TRAVEL_NOT_AUTHORIZED, ReasonCode.NOT_UNIVERSITY_BUSINESS],
                      [Clause.PERSONAL_TRAVEL, Clause.NON_REIMBURSABLE, Clause.SPEND_AUTHORIZATIONS, Clause.INTRODUCTION],
                      "Lines 1389-1391: travelers are not reimbursed for expenses beyond the official business of the "
                      "university; lines 1004-1006: personal expenses are strictly not reimbursable; lines 194-198: "
                      "only travel on UCF business is authorized. A holiday trip gets no university ticket.")
    if trip.passenger not in (Passenger.UCF_EMPLOYEE,):
        raise ValueError(f"a {trip.passenger.value} on university business is not modelled")
    sa = [record for record in trip.approvals if record.subject == Subject.SPEND_AUTHORIZATION]
    if any(record.status == Status.DENIED for record in sa):
        return refuse(trip, [ReasonCode.TRAVEL_NOT_AUTHORIZED], [Clause.SPEND_AUTHORIZATIONS, Clause.INTRODUCTION],
                      "Lines 194-198: travel on UCF business must be authorized in advance, and the Spend Authorization "
                      "must be fully approved before making commitments to travel; line 112: all travel is contingent "
                      "upon cost center approval. The Spend Authorization was denied, so nothing is bought.",
                      extra=[Approver.COST_CENTER_MANAGER])
    if not any(record.status == Status.APPROVED for record in sa):
        raise ValueError("a trip without an approved Spend Authorization is not modelled")
    stay = extended_stay(trip)
    if trip.must_arrive_by:
        late = [offer for offer in offers if offer.segments[-1].arrive_local > trip.must_arrive_by]
        if not late:
            raise ValueError("an arrival limit that rules out nothing is not modelled")
        offers = [offer for offer in offers if offer not in late]
    if trip.fallback_date:
        return deviation(trip, offers, stay)
    if trip.airline_disruption:
        return disruption(trip, offers, stay)
    if trip.funding == Funding.FEDERAL_AWARD:
        return fly_america(trip, offers, stay)
    if trip.requested_cabin in (Cabin.BUSINESS, Cabin.FIRST):
        return premium(trip, offers, stay, hidden)
    if trip.requested_cabin != Cabin.ECONOMY:
        raise ValueError(f"a {trip.requested_cabin.value} request is not modelled")
    return economy(trip, offers, stay)


def extended_stay(trip):
    """Lines 1251-1253: travel for more than thirty days to a single location needs the provost's or the
    appropriate vice president's approval. Returns None for a stay of 30 days or less, True when that approval
    is on file, False when it is not."""
    if trip.days_away <= STAY_DAYS:
        if any(record.subject == Subject.EXTENDED_STAY for record in trip.approvals):
            raise ValueError("a long-stay approval on a short trip is not modelled")
        return None
    return bool(signed(trip, Subject.EXTENDED_STAY, Role.PROVOST) or signed(trip, Subject.EXTENDED_STAY,
                                                                              Role.VICE_PRESIDENT))


def hold_for_stay(trip, held, why):
    return answer(Decision.FLAG_FOR_APPROVAL, [held], [ReasonCode.APPROVAL_REQUIRED, ReasonCode.EXTENDED_STAY_APPROVAL],
                  [Approver.PROVOST, Approver.VICE_PRESIDENT], [Clause.EXTENDED_STAY, Clause.SPEND_AUTHORIZATIONS],
                  "Lines 1251-1253: employee travel for more than thirty days to a single location requires approval "
                  f"from the provost or appropriate vice president; the trip lasts {trip.days_away} days and no such "
                  f"approval is on file (the Spend Authorization alone does not give it). {why}")


def stay_reasons(stay):
    return [ReasonCode.EXTENDED_STAY_APPROVAL] if stay else []


def stay_clauses(stay):
    return [Clause.EXTENDED_STAY] if stay else []


def economy(trip, offers, stay):
    """Lines 106, 122 and 422: the most economical means, a non-refundable economy ticket only."""
    plain = plain_economy(offers)
    low = one(cheapest(plain), "the lowest non-refundable economy fare")
    if stay is False:
        return hold_for_stay(trip, low, "Hold the lowest non-refundable economy fare for it.")
    seated = [offer for offer in offers if offer.seats_available and offer.cabin == Cabin.ECONOMY]
    if trip.refundable_requested:
        if not any(offer.refundable for offer in seated):
            raise ValueError("a refundable request with no refundable fare listed is not modelled")
        return book(trip, [low], [ReasonCode.REFUNDABLE_FARE_NOT_ALLOWED, *stay_reasons(stay)],
                    [*ECONOMY_CLAUSES, *stay_clauses(stay)],
                    "Lines 122 and 422: airline tickets must be non-refundable economy or coach class, so the "
                    "refundable fare the traveller asked for cannot be bought; the lowest non-refundable economy fare.")
    if trip.airline_credits:
        credit = one(trip.airline_credits, "the credit")
        theirs = cheapest([offer for offer in plain if offer.carrier == credit.airline])
        if not theirs or theirs[0] is low or theirs[0].fare_cents - credit.amount_cents <= low.fare_cents:
            raise ValueError("a credit that makes its airline cost the university least is not modelled")
        return book(trip, [low], [ReasonCode.LOWEST_FARE, ReasonCode.COST_SAVINGS],
                    [*ECONOMY_CLAUSES, Clause.CHANGING_TICKETS],
                    f"Lines 469-471: credits for cancelled flights stay in the traveller's profile; nothing requires "
                    f"their use, and with the {credit.amount_cents}-cent credit applied {credit.airline}'s lowest fare "
                    f"still costs {theirs[0].fare_cents - credit.amount_cents} cents against {low.fare_cents}: line 106 "
                    "(the most economical means) gives the lowest non-refundable economy fare.")
    cheaper_refundable = [offer for offer in seated if offer.refundable and offer.fare_cents < low.fare_cents]
    reasons = [ReasonCode.LOWEST_FARE, *stay_reasons(stay)]
    why = "Lines 106 and 422: the most economical means, a non-refundable economy ticket: the lowest such fare"
    if cheaper_refundable:
        reasons.append(ReasonCode.REFUNDABLE_FARE_NOT_ALLOWED)
        why += "; the cheaper refundable fare is not a non-refundable ticket (lines 122 and 422)"
    if stay:
        why += "; lines 1251-1253: the stay of over thirty days is approved by the provost or a vice president"
    if trip.sponsor and trip.funding == Funding.PRIVATE_AWARD:
        why += "; the award is not federal, so the Fly America Act (lines 1055-1058) does not apply"
        return book(trip, [low], reasons, [*ECONOMY_CLAUSES, Clause.SPONSORED_AWARD, Clause.FLY_AMERICA], why + ".")
    clauses = [*ECONOMY_CLAUSES, *stay_clauses(stay)]
    if signed(trip, Subject.BUSINESS_CLASS, Role.VICE_PRESIDENT):
        clauses.append(Clause.UPGRADED_TICKETS)
        # Setting an approved upgrade aside to save money names the cost saving (validation w3: idi aspen-fjord;
        # uk-dbt cobalt-weir and alder-pennant key the same pair).
        reasons.append(ReasonCode.COST_SAVINGS)
        why += "; business class is approved, but the traveller asks for economy and permission is not obligation"
    return book(trip, [low], reasons, clauses, why + ".")


def deviation(trip, offers, stay):
    """Lines 491-497: business should begin the day of or the day following arrival; a deviation from the
    allowable travel time must be supported by a comparable quote showing the airfare selected is more economical.
    Lines 1402-1404 and 1457-1460: UCF reimburses only up to the business-day-only airfare."""
    if stay is not None or trip.requested_cabin != Cabin.ECONOMY or not trip.schedule:
        raise ValueError("a travel-time deviation with a long stay or a premium cabin is not modelled")
    starts = trip.schedule[0].starts_local[:10]
    if days_between(trip.travel_date, starts) <= 1 or not 0 <= days_between(trip.fallback_date, starts) <= 1:
        raise ValueError("a deviation needs an early day asked and a fallback inside the allowable travel time")
    asked = one(cheapest(plain_economy(leaves_on(offers, trip.travel_date))), "the asked day's lowest fare")
    allowed = one(cheapest(plain_economy(leaves_on(offers, trip.fallback_date))), "the allowable day's lowest fare")
    clauses = [Clause.ALLOWABLE_TRAVEL_TIME, Clause.PERSONAL_TRAVEL]
    if asked.fare_cents == allowed.fare_cents:
        raise ValueError("an early fare equal to the allowable one is not modelled")
    if asked.fare_cents < allowed.fare_cents:
        return book(trip, [asked], [ReasonCode.TRAVEL_TIME_DEVIATION_CHEAPER, ReasonCode.LOWEST_FARE,
                                    ReasonCode.COST_SAVINGS], clauses,
                    f"Lines 495-497: leaving {days_between(trip.travel_date, starts)} days before the business is a "
                    f"deviation from the allowable travel time; its fare ({asked.fare_cents} cents) is more economical "
                    f"than the allowable day's ({allowed.fare_cents}), so the early flight is bought.")
    return book(trip, [allowed], [ReasonCode.TRAVEL_TIME_DEVIATION_DEARER, ReasonCode.LOWEST_FARE,
                                  ReasonCode.PERSONAL_TRAVEL_NOT_COVERED], clauses,
                f"Lines 495-497: the early flight ({asked.fare_cents} cents) is not more economical than the allowable "
                f"day's ({allowed.fare_cents}), and lines 1402-1404 pay only the business-day-only airfare; the "
                "traveller asked for the allowable day in that case.")


def disruption(trip, offers, stay):
    """Lines 505-508: after an airline cancels, a traveler may purchase a new ticket when they have made all
    reasonable efforts with the airline and waiting for its next flight would inconvenience them."""
    if stay is not None or not trip.must_arrive_by or trip.requested_cabin != Cabin.ECONOMY:
        raise ValueError("an airline disruption without an arrival limit is not modelled")
    low = one(cheapest(plain_economy(offers)), "the lowest fare that lands in time")
    return book(trip, [low], [ReasonCode.NEW_TICKET_AFTER_AIRLINE_DISRUPTION, ReasonCode.LOWEST_FARE],
                [Clause.AIRLINE_DELAY, Clause.CHANGING_TICKETS, *ECONOMY_CLAUSES],
                "Lines 505-508: the airline cancelled the flight, the traveller has tried to resolve it with the "
                "airline, and its next seat lands after the business: a new ticket may be bought. The lowest "
                "non-refundable economy fare that lands in time (line 106).")


def fly_america(trip, offers, stay):
    """Lines 1055-1058: travel on a federal award flies a U.S. flag carrier, except in the situations of lines
    1081-1093; lines 1092-1093: Open Skies exceptions do not apply to Department of Defense funding; lines
    1094-1095: ticket cost and convenience are not exceptions."""
    if DEFENSE not in trip.sponsor or stay is not None or trip.requested_cabin != Cabin.ECONOMY:
        raise ValueError("a federal award other than the Department of Defense's, or with a long stay, is not modelled")
    plain = plain_economy(offers)
    us = [offer for offer in plain if offer.carrier in US_CARRIERS]
    clauses = [Clause.FLY_AMERICA, Clause.FLY_AMERICA_EXCEPTIONS, Clause.SPONSORED_AWARD]
    if us:
        low_us = one(cheapest(us), "the lowest U.S. carrier fare")
        if one(cheapest(plain), "the lowest fare") is low_us:
            raise ValueError("a federal trip whose lowest fare is already a U.S. carrier's is not modelled")
        return book(trip, [low_us], [ReasonCode.FLY_AMERICA_US_CARRIER_REQUIRED, ReasonCode.NATIONAL_CARRIER_REQUIRED],
                    clauses,
                    "Lines 1055-1058: the federal award's travel must use a U.S. flag carrier; the U.S. carriers have "
                    "seats, so no exception of lines 1081-1090 applies, the Department of Defense funding rules out "
                    "the Open Skies exception (lines 1092-1093), and the cheaper foreign fare is no exception (lines "
                    "1094-1095). The lowest U.S. carrier fare.")
    listed = [offer for offer in offers if offer.carrier in US_CARRIERS and offer.cabin == Cabin.ECONOMY]
    if not listed:
        raise ValueError("a federal trip with no U.S. carrier on the route is not modelled")
    return book(trip, [one(cheapest(plain), "the lowest fare")], [ReasonCode.FLY_AMERICA_EXCEPTION,
                                                                  ReasonCode.LOWEST_FARE],
                [*clauses, Clause.DOCUMENTING_EXCEPTIONS],
                "Lines 1081-1082: the U.S. carriers' seats are sold out on the day and the record says they have none "
                "for days, so a U.S. carrier is not available and would extend the travel time by 24 hours or more; "
                "the exception is approved on review (lines 1130-1132). The lowest fare with seats.")


def day_test(trip, offer, hidden):
    """Lines 432-433: whether full-time business activity begins within 24 hours of the offer's landing, at the
    destination "and/or" on return to headquarters. True, False, or the unclear phrase."""
    land = minute_of(offer.segments[-1].arrive_local)
    events = trip.schedule
    if not events:
        raise ValueError("a business-class question without a schedule is not modelled")
    gap = minute_of(events[0].starts_local) - land
    if gap < 0:
        raise ValueError("business before the landing is not modelled")
    sessions = [event for event in events
                if minute_of(event.ends_local) - minute_of(event.starts_local) >= SESSION_MINUTES]
    if gap > DAY_MINUTES:
        here = False
    elif minute_of(events[0].ends_local) - minute_of(events[0].starts_local) >= SESSION_MINUTES:
        here = True
    elif sessions and minute_of(sessions[0].starts_local) - land > DAY_MINUTES:
        here = FULL_TIME_PHRASE
    else:
        raise ValueError("a short first event followed by a session within the day is not modelled")
    if trip.leg == Leg.OUTBOUND:
        return here
    if here is True:
        return True
    if here is not False or "outbound_hours" not in hidden:
        raise ValueError("a flight back needs a clear test at headquarters and the outbound hours")
    if hidden["outbound_hours"] * 60 <= DAY_MINUTES:
        return AND_OR_PHRASE
    raise ValueError("a flight back whose outbound test also failed is not modelled")


def premium(trip, offers, stay, hidden):
    """Lines 426-439: first class or higher is not allowed (430); business class only if one flight of the
    ticket is nine hours or longer and full-time business activity begins within 24 hours of arrival (431-433),
    approved by the Cost Center Manager, the applicable worktag managers and the appropriate Vice President
    (434-435); otherwise the traveller pays any upgrade (426-429)."""
    if stay is False:
        raise ValueError("a premium request on an unapproved long stay is not modelled")
    plain = plain_economy(offers)
    low = one(cheapest(plain), "the lowest non-refundable economy fare")
    business = [offer for offer in offers if offer.seats_available and offer.cabin == Cabin.BUSINESS
                and not offer.refundable]
    verdicts = {offer.offer_id: day_test(trip, offer, hidden) for offer in business if over("business-segment", offer)}
    fits = [offer for offer in business if verdicts.get(offer.offer_id) is True]
    unclear = [offer for offer in business if isinstance(verdicts.get(offer.offer_id), str)]
    first = trip.requested_cabin == Cabin.FIRST
    clauses = [Clause.UPGRADED_TICKETS, *stay_clauses(stay)]
    if fits and unclear:
        raise ValueError("clear and unclear business fares together are not modelled")
    if unclear:
        if first or not approved_business(trip):
            raise ValueError("an unclear business test with a first request or missing approvals is not modelled")
        phrase = verdicts[unclear[0].offer_id]
        if any(verdicts[offer.offer_id] != phrase for offer in unclear):
            raise ValueError("two unclear phrases on one trip are not modelled")
        held = [one(cheapest(unclear), "the unclear business fare"), low]
        return answer(Decision.FLAG_FOR_APPROVAL, held, UNCLEAR_REASONS, GAP_APPROVERS, [*clauses, Clause.TRAVEL_EXCEPTIONS],
                      unclear_why(phrase), phrase=phrase)
    if not fits:
        reasons = [ReasonCode.LONG_FLIGHT_CONDITION_NOT_MET, ReasonCode.UPGRADE_NOT_ELIGIBLE]
        reasons += [ReasonCode.FIRST_CLASS_NOT_ALLOWED] if first else [ReasonCode.TRAVELER_PAYS_UPGRADE]
        return book(trip, [low], [*reasons, *stay_reasons(stay)], [*clauses, Clause.AIRFARE],
                    "Lines 431-433: no business fare here has a flight of nine hours or longer followed within 24 hours "
                    "by full-time business, so business class is not acceptable"
                    + ("; line 430: first class is NOT allowed" if first else
                       "; lines 426-429: an upgrade is the traveller's own cost")
                    + ". The lowest non-refundable economy fare (lines 106, 422).")
    chosen = one(cheapest(fits), "the lowest qualifying business fare")
    pending = awaited(trip)
    if pending:
        if first:
            raise ValueError("a first request with business approvals pending is not modelled")
        return answer(Decision.FLAG_FOR_APPROVAL, [chosen], [ReasonCode.APPROVAL_REQUIRED], pending, clauses,
                      "Lines 434-435: business class must be approved by the Cost Center Manager, applicable worktag "
                      "managers and the appropriate Vice President; the flight qualifies (lines 431-433) but "
                      f"{', '.join(role.value for role in pending)} has not signed yet. Hold the lowest qualifying "
                      "business fare.")
    if not approved_business(trip):
        raise ValueError("a qualifying business request without its approvals sent is not modelled")
    reasons = [ReasonCode.FIRST_CLASS_NOT_ALLOWED, ReasonCode.UPGRADE_NOT_ELIGIBLE] if first else [
        ReasonCode.LONG_FLIGHT_APPROVED]
    return book(trip, [chosen], [*reasons, *stay_reasons(stay)], clauses,
                ("Line 430: first class is NOT allowed. " if first else "")
                + "Lines 431-433: this ticket has a flight of nine hours or longer and full-time business begins "
                "within 24 hours of landing; lines 434-435: the Cost Center Manager, the worktag manager and the Vice "
                "President approved business class. The lowest qualifying business fare (cost considerations, line "
                "434)" + ("; lines 1251-1253: the long stay is approved" if stay else "") + ".")


def needed_roles(trip):
    roles = [Role.COST_CENTER_MANAGER, Role.VICE_PRESIDENT]
    return [*roles, Role.WORKTAG_MANAGER] if trip.worktags else roles


def approved_business(trip):
    return all(signed(trip, Subject.BUSINESS_CLASS, role) for role in needed_roles(trip))


def awaited(trip):
    """The business-class approvers still pending (none denied, none missing)."""
    waiting = []
    for role in needed_roles(trip):
        if signed(trip, Subject.BUSINESS_CLASS, role):
            continue
        if not signed(trip, Subject.BUSINESS_CLASS, role, Status.PENDING):
            raise ValueError(f"a business request with no {role.value} sign-off sent is not modelled")
        waiting.append(ROLE_APPROVER[role])
    return waiting


def unclear_why(phrase):
    if phrase == FULL_TIME_PHRASE:
        return ("Lines 431-433: business class needs 'full -time business activity' to begin within 24 hours of "
                "arrival. A short official event (a reception) begins within the day, but the first working session "
                "begins more than 24 hours after landing; the manual does not say whether the reception counts. One "
                "reading books business, the other economy; lines 438-439 send such upgrade questions to the Finance "
                "Business Center or the Travel Center of Expertise before booking.")
    return ("Lines 431-433: business class needs full-time business activity within 24 hours of 'arrival at the "
            "destination and/or return to headquarters'. On this flight home, work at headquarters resumes days "
            "after landing, while on the way out business began within the day. One reading lets the destination "
            "test carry the return ticket, the other applies the headquarters test to it; lines 438-439 send such "
            "questions to the Finance Business Center or the Travel Center of Expertise before booking.")
