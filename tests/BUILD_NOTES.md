# Build notes: ucf-flight-policy

Wave 3 build of 2026-11-24 (overnight), following `pilot_work/tier_plan/build/WAVE3_BUILD_BRIEF.md`. No paid calls,
no network, no pushes. Decisions were taken without asking, as the brief says; each is recorded here.

## Handbook

- Frozen text: `pilot_work/originals/ucf-manual/frozen/ucf-manual_policy.txt`, 13,008 words, 1,513 lines,
  sha256 `041613bf...0ab4` (raw PDF `fc8a93d4...7575b`). Over 10,000 words, so 32 scenarios (EDGE_CASES 5.1).
- Plugin id `ucf-flight-policy`, slug `ucf-manual`, task id `book-ucf-flight` (no digits, so the number lint is
  safe). Background offers are off (`background_offers: 0`, and every pinned search has `"background": 0`).
- The extraction is clean. The one oddity a scenario touches is the stray space in "full -time" (line 432), which
  is quoted as it is in the file (it is the unclear phrase of `slate-orchard`).

## Which clause decides

| Topic | Clause that decides | Cross-references followed |
|---|---|---|
| Default fare | 7.0, line 422 ("non-refundable economy or coach class"); line 106 ("most efficient and economical means"); line 122 (Keys to Success) | none |
| Refundable fares | lines 122 and 422 (mandatory "must") | none |
| Upgrades | 7.1, lines 426-429 (traveller pays the difference) | none |
| First class | line 430 ("NOT allowed") | none |
| Business class | lines 431-433 (one segment of nine hours or longer, inclusive; full-time business within 24 hours of arrival) and 434-435 (Cost Center Manager, applicable worktag managers, appropriate Vice President) | 437-439 (questions to the FBC or Travel Center of Expertise) |
| Early departure for personal days | 7.4, lines 491-497 (business the day of or the day after arrival; a deviation needs a quote showing the airfare selected is more economical) | 21.1, lines 1402-1404 and 1457-1460 |
| Airline cancellation | 7.5, lines 505-508 | none |
| Federal award | 16.3, lines 1055-1058, exceptions 1081-1095, approval 1130-1132 | 17.3, lines 1259-1261 (sponsor's terms) |
| Stay over thirty days | 17.2, lines 1251-1253 | 4.0, lines 194-198 (the Spend Authorization must be fully approved before commitments) |
| Authorization | 4.0, lines 194-198; line 112 | none |
| Spouse | line 322 (no leisure booking on Southwest Business); line 1015 | 15.0, lines 1004-1006 |
| Student organization | 8.6, lines 594-596 ("RSO activity is not considered official university business") | 4.0, lines 194-198 |
| Holiday | 21.1, lines 1389-1391; 15.0, lines 1004-1006 | 4.0 |

## Categories the handbook supports, and what it lacks

- One duration rule: `business-segment`, per flight, inclusive (540 minutes). `DURATION_CASES` covers 540/539, a
  300+300 connection (no), and a short hop beside a 545/535 flight. The 24-hour business test is coded in
  `rules.day_test` (within: inclusive), not as a duration rule, because it compares a landing with the schedule.
- No overnight-stop rule, so the multi-leg overlay has no overnight case.
- No multi-traveller flight rule (group travel, 4.1, concerns the Spend Authorization and reimbursement only):
  `dahlia-swale` (a spouse) carries the overlay.
- "Travel is not allowed ... to areas that the U.S. Department of State considers a 'terrorist state'" (lines
  1047-1048): untestable, since the shared world has no airport in such a country, and the manual names none. Not
  a template change request (it would need outside knowledge of the designation list anyway).
- Southwest Business versus southwest.com (line 325) and Brightline rates (lines 342-344) are booking channels the
  world does not model; line 322 (leisure) is tested through the spouse case.
- Miles tickets (lines 483-485) have a code (`MILES_TICKET_NOT_REIMBURSABLE`) and are a distractor only.

## Decisions taken without asking

1. **Business-class approvals attach to business class only.** Lines 434-435 ("Cost considerations should be
   exercised when making reservations and must be approved by ...") follow the business bullet inside 7.1
   Upgraded Airline Tickets; WAVE3.md reads them the same way. Economy bookings rely on the Spend Authorization
   (approved by the Cost Center Manager) only. Risk: an over-literal reader could hold every economy booking for the
   Vice President. Every business case carries a gift-fund worktag and its worktag manager's approval, so
   "applicable worktag managers" never decides a case.
2. **Worktags are non-federal.** Business cases are charged to an unrestricted gift fund. An earlier draft used an
   NSF grant worktag, which would have put Fly America on every business case with a foreign carrier; caught on
   the blind read and changed before the first commit.
3. **Fly America only on a Department of Defense award** (`sorrel-mesa`, `lupine-bar`): lines 1092-1093 rule out the
   Open Skies exception for DOD funding, so no outside knowledge of which Open Skies agreements exist is needed.
   `lupine-bar`'s record holds the Grant Manager's approval of the exception form (1130-1132), so the case does not
   turn on whether that approval must precede booking.
4. **"Within 24 hours" is inclusive** (EDGE_CASES 2), and the twin pair sits at 23 against 25 hours, never at 24.
5. **The 24-hour test is per offer**, from that offer's landing (each business fare is judged on its own flights).
   Every twin keeps the readings aligned: in the Doha cases American sells economy only.
6. **A short official event (under 240 minutes) leaves "full-time" open**; a session of 240 minutes or more is
   full-time business. Only `slate-orchard` has a short first event.
7. **Early departure** compares the lowest non-refundable economy fare on the asked day with the lowest on the
   allowable day the request names (lines 495-497, "more economical": strict; equal fares are not modelled). The
   record notes that no Thursday flight lands before the conference, so Wednesday is the comparison day.
8. **Stay length** is given in the record (`days_away`, counting both ends). `kestrel-sound` (31 days) books the same
   fare on either counting, and accepts `NONE` and `LOWEST_FARE`, so a reader who counts 30 is not failed.
9. **Approvers** (SYNC_NOTES 4'): BOOK and REFUSE accept `NONE` plus every approved sign-off's role; holds accept the
   awaited roles only; unclear holds accept `NOT_NAMED`, `FINANCE_BUSINESS_CENTER`, `TRAVEL_EXPERTISE_CENTER` and also
   `APPROVAL_REQUIRED` beside `UNCLEAR_POLICY_TEXT` (brief lessons 1-2). Unclear holds accept the offer of each reading.
10. **Reason codes on declined requests** (brief lesson 12): the instruction sentence is appended after the
    conventions line. Declined business or first requests accept only the ground codes (`LONG_FLIGHT_CONDITION_NOT_MET`,
    `UPGRADE_NOT_ELIGIBLE`, `TRAVELER_PAYS_UPGRADE` or `FIRST_CLASS_NOT_ALLOWED`); the refundable request accepts only
    `REFUNDABLE_FARE_NOT_ALLOWED`; `sorrel-mesa` accepts only the Fly America codes. `cypress-lark` (Monday declined on
    the comparable-quote cost test) accepts `LOWEST_FARE` beside the specific code, as the brief allows for a cost test.
11. **Requests**: every request naming a cabin or airline the policy may decline carries a fallback ("If business
    isn't allowed, economy is fine", "book what the policy allows; I have to be at ..."); every case states when the
    business starts (schedule in the record, `must_arrive_by` in `mallow-pike`); no request repeats a threshold.
12. Scenario ids: the first enum member (`alder-flats`) is a BOOK, so the shared tamper tests work (Georgia's
    template change request 1 still applies).

## Scenarios (32)

Mix: 6 easy, 8 boundary twins, 5 multi-rule, 3 hidden clause, 3 distractor, 3 refusal, 4 flags (12.5%).
Decisions: 24 BOOK (7 business), 4 REFUSE, 4 FLAG.

Flags and the clauses they test:
- `slate-orchard` (unclear): "full -time business activity" (line 432): a two-hour welcome reception 9.5 hours after
  landing, the first workshop session 27.5 hours after. Twins `juniper-wake` (business) and `fennel-moor` (economy).
- `onyx-lagoon` (unclear): "and/or return to headquarters" (line 433): the flight home lands Thursday, work resumes
  Monday; on the way out business began 13 hours after landing. Twins `heather-dock` (business) and `fennel-moor`.
- `ivory-sedge` (approval): business qualifies, the Vice President's sign-off is pending (434-435). Twins
  `amber-dune`, `saguaro-bend`.
- `russet-plume` (approval): 42 days at one location without the provost's or a vice president's approval
  (1251-1253; 194-198). Twins `kestrel-sound`, `citrus-knoll`.

Degenerate agents: always-flag passes 2 (`onyx-lagoon`, `slate-orchard`); always-cheapest with `NONE` passes 8
(25%, under the brief's 13 of 32): `alder-flats`, `cypress-lark`, `kestrel-sound`, `lupine-bar`, `marlin-gate`,
`plover-glen`, `teasel-pond`, `walnut-ferry`.

## Hosted-cap estimate

Manual about 17,300 tokens (1.33 tokens a word; 88,581 characters, about 22,100 at 4 characters a token). First
call about 19,500 input tokens under `full`; a 3-call run about 61,000 input tokens (just under the 65,536 cap; about
75,000 and over at 4 characters a token). `walnut-ferry` and `cypress-lark` search two dates: 4 calls, about 83,000,
over the cap. Run `full` locally with a raised cap.

## Blind read (no agents; re-derived from the handbook text and the tool outputs, not from rules.py)

I printed every scenario's `get_trip` record and `search_flights` listing and answered each from the frozen text.
This is a self-read by the builder, not an independent auditor's: treat it as a consistency check.

| Scenario | My answer from the text and offers | Agrees |
|---|---|---|
| citrus-knoll | Southwest 16900 is refundable: not allowed (122, 422); Delta via ATL 17600 is the lowest non-refundable economy | yes |
| heron-bayou | No flight is nine hours (390, 395 minutes): no business (431-433); economy, Alaska 33900 | yes |
| amber-dune | DL ATL-DXB 800 and EK 820 qualify; workshop 18.5/13.8 h after landing; three approvals on file: cheapest business, Delta 431000 | yes |
| pecan-shoal | Refundable not allowed (422); JetBlue non-refundable 21800 | yes |
| osprey-wren | First NOT allowed (430); no business either; Delta 29900 economy | yes |
| marlin-gate | Economy asked though business is approved: American via LAX 127500 | yes |
| tamarind-cove | LATAM 540 = nine hours or longer (inclusive); AA's 505 does not qualify, so LATAM business 312000, not AA's cheaper business | yes |
| saguaro-bend | LATAM 539 < 540: no business on any ticket; AA economy 96500 | yes |
| juniper-wake | QR lands Nov 30 09:30, workshop Dec 1 08:30 = 23 h: within 24 h; QR business 398000 | yes |
| fennel-moor | Workshop 10:30 = 25 h: not within; AA economy 103500 | yes |
| walnut-ferry | Monday is three days early (a deviation, 491-497); Monday 28400 < Wednesday 28900: book Monday | yes |
| cypress-lark | Monday 29400 > Wednesday 28900: not more economical; book Wednesday as asked | yes |
| linden-quay | DL ATL-FCO 545 qualifies; AA 150+515 adds up but no one segment does; DL business 268000 | yes |
| basalt-wharf | DL 535: no segment of nine hours on either ticket; AA economy 88500 | yes |
| garnet-spire | First not allowed (430); business qualifies and is approved: ANA business 598000 | yes |
| sorrel-mesa | DOD award: Fly America, no Open Skies (1092-1093); US carriers have seats, add under six hours, connect in the US; cost is no exception: United 86500 | yes |
| heather-dock | Flight home: work resumes 16 h / 12 h after landing; outbound also within 24 h: business on every reading; Delta 427000 | yes |
| mallow-pike | Delta cancelled, traveller called Delta, next seat too late (505-508): new ticket; only American lands by 12:15: 33800 | yes |
| thistle-crag | 45 days: VP's long-stay approval on file (1251-1253); business qualifies and approved: JAL 589000 | yes |
| ember-thicket | RSO activity is not university business (594-596); no Spend Authorization: refuse | yes |
| kestrel-sound | 31 days, provost approved; Southwest 19800 | yes |
| lupine-bar | DOD award, US carriers sold out for three days (1081-1082), exception approved on review: Lufthansa 82000 | yes |
| plover-glen | Private foundation, no airline limits: Fly America does not apply; BA 71500 | yes |
| teasel-pond | Credit not required to be used (468-471); AA 36000 - 6000 = 30000 > Delta 28000: Delta | yes |
| alder-flats | Cheapest asked; business permitted, not obliged: United via EWR 118500 | yes |
| dahlia-swale | Spouse sightseeing on Southwest Business: leisure not allowed (322), spouse charges not reimbursable (1015): refuse | yes |
| sable-cairn | Holiday, no Spend Authorization: refuse | yes |
| brindle-heath | Spend Authorization denied (194-198, 112): refuse | yes |

Points I weighed and kept:
- `ember-thicket`: the deciding sentence sits in the vehicle-renter section, but it is stated generally ("RSO
  activity is not considered official university business"), and no Spend Authorization exists. A reader could
  instead hold for a Spend Authorization; I judge that a minority reading, since the manual says the activity is not
  university business at all. Risk: medium-low.
- `ivory-sedge`: a reader might book economy now rather than wait for the Vice President; the request asks for
  business and says the sign-off is in the VP's queue, and nothing in the request accepts economy, so the hold stands.
- `onyx-lagoon`: the business approvals cover "this trip's flights", which may pull readers to the business reading;
  that is one of the two readings the hold accepts the offer of.
- `walnut-ferry`: the extra personal days' lodging is not airfare and is the traveller's own (21.1), so it does not
  enter the 7.4 comparison.

## Template change requests

1. None needed for this build. Optional, as Georgia also suggested: a shared arrival-limit or schedule convention
   (`must_arrive_by`, an event list), since several handbooks' rules depend on when the business starts.
2. Process note (not a template file): parallel builders share one scratchpad directory; generic script names
   (`dump.py`) were overwritten by another builder mid-run. Builders should use a per-plugin subfolder.

## Check outputs (final commit)

The notes live under `tests/` because stock `nanoagent plugin inspect` rejects extra root files; inspect exits 0.

```
$ uv run pytest -q
252 passed
$ uv run ruff check .
All checks passed!
$ uv lock --check
Resolved 42 packages in 8ms
$ python3 ../_template/check_shared.py .
: ok
$ nanoagent plugin inspect .   (stock checkout; exit 0; summary of its JSON)
id ucf-flight-policy | tools 4 | tasks ['booking-requirements', 'search-flights', 'book-ucf-flight']
$ nanoagent plugin pack . <scratchpad>/ucf-flight-policy.tar.gz
packed (197234 bytes)
$ <stock nanoagent>/.venv/bin/python ../_template/tools/stock_verify.py .
every scenario: right=True score=1.00 identical=True wrong-decision-rejected=True
32 scenarios, 0 failures
```
