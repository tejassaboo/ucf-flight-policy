# UCF Travel Manual Flight Policy

**No affiliation with the University of Central Florida.** The handbook is the university's public *Travel
Manual* (revised October 2026), bundled verbatim for research. It is a published public-university manual, but
treat it like the other original handbooks: do not publish this plugin before the course staff confirm that a
verbatim handbook may be redistributed (MASTER_PLAN section 4).

A `nanoagent.plugin/v0001` plugin. An agent handles one traveller's flight request under the university's real
travel manual: it reads the trip record, searches a simulated flight world and submits **BOOK**, **REFUSE** or
**FLAG_FOR_APPROVAL** with the offer, cabin, reason, approver and manual section. A deterministic Python verifier,
with no LLM, rebuilds the offers and the manual's answer itself and checks every field. Built from the
original-handbook template (`handbook_plugins/_template`); `tests/build_scenarios.py` writes the scenario files
(the JSON files are the truth).

## The handbook and the harness flag

The frozen text (`src/plugin/data/policy.txt`, 13,008 words, 1,513 lines, sha256 `041613bf...0ab4`, equal to
`pilot_work/originals/ucf-manual/frozen/SHA256SUMS`) is never paraphrased, and the task text restates no rule.
Under stock NanoAgent the agent does not see it: the plugin then runs as the `off` baseline. The `harness.policy`
switch of the NanoAgent fork (github.com/tejassaboo/nanoagent, branch `policy-switch`) adds it to the system
prompt: `harness.policy: full` adds all of it, and the selection methods add parts of it. These plugins are meant
to run with `query: instructions+input`, so a selector sees the traveller's request.

**The duration rule.** Business class is acceptable only if "at least one segment of the flight shown on the
purchased tickets is nine hours or longer and full -time business activity begins within 24 hours of arrival at
the destination and/or return to headquarters" (lines 431-433), approved by "the Cost Center Manager, applicable
worktag managers, and the appropriate Vice President" (434-435). `rules.over("business-segment", offer)` is per
flight and inclusive (540 scheduled minutes or more); flights never add up. The 24-hour test compares the
offer's landing with the trip record's schedule (within: inclusive).

**Size.** At 1.33 tokens a word the manual alone is about 17,300 tokens (88,581 characters, about 22,100 at 4
characters a token). Under `full` the first call carries about 19,500 input tokens (manual, task instructions
about 300, tool and submit schemas about 1,800, the request), and later calls about 20,500-21,500 as tool results
accumulate. A run makes 3 calls (`get_trip`, `search_flights`, `submit`): about 61,000 input tokens, under the
hosted cap of 65,536 with little margin; at 4 characters a token it is about 75,000 and over. The two early-departure
cases (`walnut-ferry`, `cypress-lark`) search two dates, so 4 calls and about 83,000 input tokens: over the cap. Run
`full` locally with a raised cap.

## Task

- **Input:** `TaskInput`: `scenario` (one of 32 case ids) and `request`, the traveller's own words.
- **Steps:** `get_trip`, then `search_flights` on the trip's route and date (and on the other day the record names,
  in the two early-departure cases), then `submit`.
- **Output:** `BookingOutput`: `decision`, `offer_id` (empty when refusing), `cabin` (`NONE` when refusing;
  otherwise the chosen offer's own cabin), `reason_code`, `approver` and `clause`, each from a closed list. The
  reason list is the template's shared list plus 11 UCF codes (`MILES_TICKET_NOT_REIMBURSABLE` stands for a rule
  no case tests) and 10 decoy codes from other handbooks' rules. Fares are in cents of US dollars.
- **Approver** (template SYNC_NOTES 4'): a BOOK or REFUSE accepts `NONE` and the role of every sign-off on file
  (those it relies on and those it leaves unused); a hold awaiting a sign-off accepts only the awaited role(s); a
  hold over unclear words accepts `NOT_NAMED`, `FINANCE_BUSINESS_CENTER` or `TRAVEL_EXPERTISE_CENTER` (lines 437-439
  and 1264-1266 send such questions there). Every trip outside the United States carries UCF Global's approved
  Travel Approval Petition (lines 1027-1029), so its BOOK also accepts `UCF_GLOBAL`.
- **Success:** every field is one the answer key accepts. Score = fields right / 6.
- **Hidden facts:** `heather-dock` and `onyx-lagoon` (flights home) carry `answer_key_inputs.outbound_hours` (13),
  the hours from the outbound landing to the first business, which the trip record states in its notes.

| Scenario | Category | Expected decision (offer; cabin) | Reason | Approver | Clause (frozen lines) |
|---|---|---|---|---|---|
| `amber-dune` | easy | BOOK (dl-business; BUSINESS) | LONG_FLIGHT_APPROVED | COST_CENTER_MANAGER or NONE or UCF_GLOBAL or VICE_PRESIDENT or WORKTAG_MANAGER | UPGRADED_TICKETS (431-433, 434-435, 106) |
| `citrus-knoll` | easy | BOOK (dl-economy; ECONOMY) | LOWEST_FARE or REFUNDABLE_FARE_NOT_ALLOWED | COST_CENTER_MANAGER or NONE | AIRFARE or INTRODUCTION (106, 122, 422) |
| `heron-bayou` | easy | BOOK (as-economy; ECONOMY) | LONG_FLIGHT_CONDITION_NOT_MET or TRAVELER_PAYS_UPGRADE or UPGRADE_NOT_ELIGIBLE | COST_CENTER_MANAGER or NONE | AIRFARE or UPGRADED_TICKETS (431-433, 426-429, 422, 106) |
| `marlin-gate` | easy | BOOK (aa-economy; ECONOMY) | COST_SAVINGS or LOWEST_FARE | COST_CENTER_MANAGER or NONE or UCF_GLOBAL or VICE_PRESIDENT or WORKTAG_MANAGER | AIRFARE or INTRODUCTION or UPGRADED_TICKETS (422, 106, 431-433) |
| `osprey-wren` | easy | BOOK (dl-economy; ECONOMY) | FIRST_CLASS_NOT_ALLOWED or LONG_FLIGHT_CONDITION_NOT_MET or UPGRADE_NOT_ELIGIBLE | COST_CENTER_MANAGER or NONE | AIRFARE or UPGRADED_TICKETS (430, 422, 106) |
| `pecan-shoal` | easy | BOOK (b6-economy; ECONOMY) | REFUNDABLE_FARE_NOT_ALLOWED | COST_CENTER_MANAGER or NONE | AIRFARE or INTRODUCTION (122, 422) |
| `basalt-wharf` | boundary_twin | BOOK (aa-economy; ECONOMY) | LONG_FLIGHT_CONDITION_NOT_MET or TRAVELER_PAYS_UPGRADE or UPGRADE_NOT_ELIGIBLE | COST_CENTER_MANAGER or NONE or UCF_GLOBAL or VICE_PRESIDENT or WORKTAG_MANAGER | AIRFARE or UPGRADED_TICKETS (431-433, 422, 106) |
| `cypress-lark` | boundary_twin | BOOK (wn-wednesday; ECONOMY) | LOWEST_FARE or PERSONAL_TRAVEL_NOT_COVERED or TRAVEL_TIME_DEVIATION_DEARER | COST_CENTER_MANAGER or NONE | ALLOWABLE_TRAVEL_TIME or PERSONAL_TRAVEL (491-493, 495-497, 1457-1460, 1402-1404) |
| `fennel-moor` | boundary_twin | BOOK (aa-economy; ECONOMY) | LONG_FLIGHT_CONDITION_NOT_MET or TRAVELER_PAYS_UPGRADE or UPGRADE_NOT_ELIGIBLE | COST_CENTER_MANAGER or NONE or UCF_GLOBAL or VICE_PRESIDENT or WORKTAG_MANAGER | AIRFARE or UPGRADED_TICKETS (431-433, 422, 106) |
| `juniper-wake` | boundary_twin | BOOK (qr-business; BUSINESS) | LONG_FLIGHT_APPROVED | COST_CENTER_MANAGER or NONE or UCF_GLOBAL or VICE_PRESIDENT or WORKTAG_MANAGER | UPGRADED_TICKETS (431-433, 434-435) |
| `linden-quay` | boundary_twin | BOOK (dl-business; BUSINESS) | LONG_FLIGHT_APPROVED | COST_CENTER_MANAGER or NONE or UCF_GLOBAL or VICE_PRESIDENT or WORKTAG_MANAGER | UPGRADED_TICKETS (431-433, 434-435) |
| `saguaro-bend` | boundary_twin | BOOK (aa-economy; ECONOMY) | LONG_FLIGHT_CONDITION_NOT_MET or TRAVELER_PAYS_UPGRADE or UPGRADE_NOT_ELIGIBLE | COST_CENTER_MANAGER or NONE or UCF_GLOBAL or VICE_PRESIDENT or WORKTAG_MANAGER | AIRFARE or UPGRADED_TICKETS (431-433, 422, 106) |
| `tamarind-cove` | boundary_twin | BOOK (la-business; BUSINESS) | LONG_FLIGHT_APPROVED | COST_CENTER_MANAGER or NONE or UCF_GLOBAL or VICE_PRESIDENT or WORKTAG_MANAGER | UPGRADED_TICKETS (431-433, 434-435) |
| `walnut-ferry` | boundary_twin | BOOK (wn-monday; ECONOMY) | COST_SAVINGS or LOWEST_FARE or TRAVEL_TIME_DEVIATION_CHEAPER | COST_CENTER_MANAGER or NONE | ALLOWABLE_TRAVEL_TIME or PERSONAL_TRAVEL (491-493, 495-497, 1457-1460, 1402-1404) |
| `garnet-spire` | multi_rule | BOOK (nh-business; BUSINESS) | FIRST_CLASS_NOT_ALLOWED or UPGRADE_NOT_ELIGIBLE | COST_CENTER_MANAGER or NONE or UCF_GLOBAL or VICE_PRESIDENT or WORKTAG_MANAGER | UPGRADED_TICKETS (430, 431-433, 434-435) |
| `heather-dock` | multi_rule | BOOK (dl-business; BUSINESS) | LONG_FLIGHT_APPROVED | COST_CENTER_MANAGER or NONE or UCF_GLOBAL or VICE_PRESIDENT or WORKTAG_MANAGER | UPGRADED_TICKETS (431-433, 434-435) |
| `mallow-pike` | multi_rule | BOOK (aa-economy; ECONOMY) | LOWEST_FARE or NEW_TICKET_AFTER_AIRLINE_DISRUPTION | COST_CENTER_MANAGER or NONE | AIRFARE or AIRLINE_DELAY or CHANGING_TICKETS or INTRODUCTION (505-508, 106, 422) |
| `sorrel-mesa` | multi_rule | BOOK (ua-economy; ECONOMY) | FLY_AMERICA_US_CARRIER_REQUIRED or NATIONAL_CARRIER_REQUIRED | COST_CENTER_MANAGER or GRANT_MANAGER or NONE or UCF_GLOBAL | FLY_AMERICA or FLY_AMERICA_EXCEPTIONS or SPONSORED_AWARD (1055-1058, 1092-1095, 1259-1261) |
| `thistle-crag` | multi_rule | BOOK (jl-business; BUSINESS) | EXTENDED_STAY_APPROVAL or LONG_FLIGHT_APPROVED | COST_CENTER_MANAGER or NONE or UCF_GLOBAL or VICE_PRESIDENT or WORKTAG_MANAGER | EXTENDED_STAY or UPGRADED_TICKETS (1251-1253, 431-433, 434-435) |
| `ember-thicket` | hidden_clause | REFUSE (none; NONE) | NOT_UNIVERSITY_BUSINESS or OUTSIDE_POLICY_SCOPE or TRAVEL_NOT_AUTHORIZED | NONE | ELIGIBLE_RENTER or INTRODUCTION or SPEND_AUTHORIZATIONS (594-596, 194-198) |
| `kestrel-sound` | hidden_clause | BOOK (wn-economy; ECONOMY) | EXTENDED_STAY_APPROVAL or LOWEST_FARE | COST_CENTER_MANAGER or NONE or PROVOST | AIRFARE or EXTENDED_STAY or INTRODUCTION (1251-1253, 422, 106) |
| `lupine-bar` | hidden_clause | BOOK (lh-economy; ECONOMY) | FLY_AMERICA_EXCEPTION or LOWEST_FARE | COST_CENTER_MANAGER or GRANT_MANAGER or NONE or UCF_GLOBAL | DOCUMENTING_EXCEPTIONS or FLY_AMERICA or FLY_AMERICA_EXCEPTIONS or SPONSORED_AWARD (1055-1058, 1081-1082, 1130-1132) |
| `alder-flats` | distractor | BOOK (ua-economy; ECONOMY) | COST_SAVINGS or LOWEST_FARE | COST_CENTER_MANAGER or NONE or UCF_GLOBAL or VICE_PRESIDENT or WORKTAG_MANAGER | AIRFARE or INTRODUCTION or UPGRADED_TICKETS (422, 106) |
| `plover-glen` | distractor | BOOK (ba-economy; ECONOMY) | LOWEST_FARE | COST_CENTER_MANAGER or NONE or UCF_GLOBAL | AIRFARE or FLY_AMERICA or INTRODUCTION or SPONSORED_AWARD (422, 106, 1259-1261) |
| `teasel-pond` | distractor | BOOK (dl-economy; ECONOMY) | COST_SAVINGS or LOWEST_FARE | COST_CENTER_MANAGER or NONE | AIRFARE or CHANGING_TICKETS or INTRODUCTION (106, 422) |
| `brindle-heath` | refusal | REFUSE (none; NONE) | TRAVEL_NOT_AUTHORIZED | COST_CENTER_MANAGER or NONE | INTRODUCTION or SPEND_AUTHORIZATIONS (194-198, 112) |
| `dahlia-swale` | refusal | REFUSE (none; NONE) | COMPANION_NOT_COVERED or LEISURE_BOOKING_NOT_ALLOWED or NOT_UNIVERSITY_BUSINESS or OUTSIDE_POLICY_SCOPE or PERSONAL_TRAVEL_NOT_COVERED or TRAVEL_NOT_AUTHORIZED | COST_CENTER_MANAGER or NONE | NON_REIMBURSABLE or ONLINE_BOOKING or PERSONAL_TRAVEL or SOUTHWEST_BUSINESS or SPEND_AUTHORIZATIONS (322, 1015, 1004-1006) |
| `sable-cairn` | refusal | REFUSE (none; NONE) | NOT_UNIVERSITY_BUSINESS or OUTSIDE_POLICY_SCOPE or PERSONAL_TRAVEL_NOT_COVERED or TRAVEL_NOT_AUTHORIZED | NONE | INTRODUCTION or NON_REIMBURSABLE or PERSONAL_TRAVEL or SPEND_AUTHORIZATIONS (1389-1391, 1004-1006, 194-198) |
| `ivory-sedge` | flag | FLAG_FOR_APPROVAL (dl-business; BUSINESS) | APPROVAL_REQUIRED | VICE_PRESIDENT | UPGRADED_TICKETS (431-433, 434-435) |
| `onyx-lagoon` | flag | FLAG_FOR_APPROVAL (dl-business or dl-economy; BUSINESS or ECONOMY) | APPROVAL_REQUIRED or UNCLEAR_POLICY_TEXT | FINANCE_BUSINESS_CENTER or NOT_NAMED or TRAVEL_EXPERTISE_CENTER | TRAVEL_EXCEPTIONS or UPGRADED_TICKETS (431-433, 434-435, 437-439, 1264-1267) |
| `russet-plume` | flag | FLAG_FOR_APPROVAL (aa-economy; ECONOMY) | APPROVAL_REQUIRED or EXTENDED_STAY_APPROVAL | PROVOST or VICE_PRESIDENT | EXTENDED_STAY or SPEND_AUTHORIZATIONS (1251-1253, 194-198) |
| `slate-orchard` | flag | FLAG_FOR_APPROVAL (aa-economy or qr-business; BUSINESS or ECONOMY) | APPROVAL_REQUIRED or UNCLEAR_POLICY_TEXT | FINANCE_BUSINESS_CENTER or NOT_NAMED or TRAVEL_EXPERTISE_CENTER | TRAVEL_EXCEPTIONS or UPGRADED_TICKETS (431-433, 434-435, 437-439, 1264-1267) |

Mix (EDGE_CASES.md 5.2, 32-scenario row): 6 easy, 8 boundary twins, 5 multi-rule, 3 hidden clause, 3 distractor,
3 refusal, 4 flags (12.5%). Boundary twins: a nonstop of 540 against 539 scheduled minutes (`tamarind-cove`,
`saguaro-bend`); the first workshop session 23 against 25 hours after landing (`juniper-wake`, `fennel-moor`); an
early personal-days flight 500 cents cheaper or dearer than the allowable day's (`walnut-ferry`, `cypress-lark`); a
connection whose long flight is 545 against 535 minutes, both adding to more than nine hours (`linden-quay`,
`basalt-wharf`). Unclear-text flags: "full -time business activity" (`slate-orchard`; twins `juniper-wake`,
`fennel-moor`) and "and/or return to headquarters" (`onyx-lagoon`; twins `heather-dock`, `fennel-moor`). Approval
holds: business class with the Vice President's sign-off pending (`ivory-sedge`; twins `amber-dune`,
`saguaro-bend`) and a 42-day stay without the provost's or a vice president's approval (`russet-plume`; twins
`kestrel-sound`, `citrus-knoll`).

Degenerate agents: one that always holds the right offer as unclear passes the 2 unclear holds; one that always
books the cheapest seat with `LOWEST_FARE` and approver `NONE` passes 8 (25%): `alder-flats`, `cypress-lark`,
`kestrel-sound`, `lupine-bar`, `marlin-gate`, `plover-glen`, `teasel-pond` and `walnut-ferry`, whose answer is the
lowest seated fare and whose request, if declined at all, is declined on a cost comparison. A BOOK that declines
what the traveller asked for (cabin, fare type, airline or day) accepts only the reason codes for the manual's
ground of declining, as the task instructions say. Decisions: 24 BOOK (7 in business), 4 REFUSE, 4 FLAG.

## Tools

| Tool | Does | Code |
|---|---|---|
| `booking_requirements` | The trip record's fields, the world's conventions (local times, dates, fares, sold-out seats) and its airports | `src/plugin/guide.py` |
| `get_trip` | A case's request and trip record: traveller, department, route, dates, schedule where the flight lands, funding, requested cabin, sign-offs, notes | `src/plugin/tools.py` |
| `search_flights` | Every offer on a route and local date: the pinned scenario offers only (background offers are off); a search the case does not pin lists nothing and says so | `src/plugin/world.py` |
| `solve_booking` | The answer key (`rules.solve`), the agent task's `reference`, never shown to the agent | `src/plugin/rules.py` |

| Task | Does | Runner |
|---|---|---|
| `book-ucf-flight` | Handles one booking request | `agent`, with `get_trip` and `search_flights`; reference `solve_booking` |
| `booking-requirements` | Shows `booking_requirements` | `tool` |
| `search-flights` | Shows `search_flights` | `tool` |

## Layout

- `contract.py`: the template's shared contract plus this handbook's scenario ids, approvers, sections and trip record.
- `src/plugin/`: `world.py` (the simulated world: real airports and airline hubs, distance-based times
  and fares, opaque offer ids), `scenarios.py`, `guide.py`, `answer.py`, `tools.py`, `rules.py` (this
  handbook's rules, citing frozen lines), `__main__.py`.
- `src/plugin/data/`: `policy.txt` (frozen), `handbook.json`, `scenarios/*.json`.
- `verifier/`: byte-identical copies of `world.py`, `scenarios.py`, `guide.py`, `answer.py` and
  `rules.py`, plus `booking.py` (`verify_task`) and `tools.py` (`verify_input`, `verify_output`).
- `tests/`: the template's acceptance suite; `tests/plugin_spec.py` holds this handbook's settings;
  `tests/build_scenarios.py` writes the scenario files.
- `tests/BUILD_NOTES.md`: build decisions, check outputs and the blind read.

## Develop and run

```bash
uv sync --extra dev
uv run pytest
uv run ruff check .
uv lock --check
python3 tests/build_scenarios.py   # rewrites src/plugin/data/scenarios/*.json
# from a NanoAgent checkout (stock NanoAgent runs this plugin as the `off` baseline;
# the fork's `harness.policy: full` flag adds the handbook):
nanoagent plugin inspect <this folder>
nanoagent plugin pack <this folder> /tmp/ucf-flight-policy.tar.gz
<nanoagent>/.venv/bin/python ../_template/tools/stock_verify.py .
```

Offline: `hosts: []`, an empty `.env`, `write: []`, no clock (each case fixes its `booking_date`).
