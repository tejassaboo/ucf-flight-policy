# Independent audit: ucf-flight-policy (2026-11-25)

I audited the builder's commit 846671d against `pilot_work/tier_plan/build/WAVE3_AUDIT_BRIEF.md`, the wave 3 build
brief's 12 lessons, MASTER_PLAN section 4, EDGE_CASES 1-3 and 5, and the worked audits (fedex-office,
goodman-networks, hillrom, georgia-sao). No money spent, nothing pushed. Line numbers are lines of the frozen
handbook (`src/plugin/data/policy.txt`).

## Method

- I read the manual's flight-relevant sections myself: 1.0, 4.0-4.2, 5.1, 7.0-7.5, 8.6, 15.0, 16.1-16.3, 17.1-17.4
  and 21.1. I skimmed lodging, mileage, per diem and advances for anything that touches a ticket.
- I printed every `get_trip` record and every pinned `search_flights` result through the plugin's own tools.
- I answered each case from the text and those outputs before I looked at `rules.py`.
- Then I compared my answers with every accept set (decision, offer, cabin, reason, approver, clause).
- I diffed each twin pair field by field.

## Verdict

**Pass after fixes.** My decision and offer agree with the key in all 28 non-flag cases. The four flags are sound:

- `slate-orchard` and `onyx-lagoon` turn on unclear words, and both offers are accepted in each.
- `ivory-sedge` and `russet-plume` are clear holds.

The twin pairs each differ in one fact:

| Pair | The one fact |
|---|---|
| `basalt-wharf` / `linden-quay` | Delta's Atlanta-Rome flight, 535 or 545 minutes |
| `fennel-moor` / `juniper-wake` | the workshop starts 10:30 or 08:30 |
| `saguaro-bend` / `tamarind-cove` | LATAM's flight, 539 or 540 minutes |
| `cypress-lark` / `walnut-ferry` | the Monday fare, 29400 or 28400 |
| `heather-dock` / `onyx-lagoon` | work resumes Friday or Monday (plus the annual-leave note that explains it) |

The other checks also pass:

- No request leaks rule wording.
- Every request that names a cabin or fare the policy may decline has a fallback.
- Every case states when the business starts.
- The decline sentence is in the task instructions.

The defects were one missing record fact that affected 19 foreign trips, and reason and clause sets that were too
narrow on the three refusals.

## Defects found and fixed

1. **The Travel Approval Petition was missing from every foreign trip** (19 cases: `alder-flats`, `amber-dune`,
   `basalt-wharf`, `fennel-moor`, `garnet-spire`, `heather-dock`, `ivory-sedge`, `juniper-wake`, `linden-quay`,
   `lupine-bar`, `marlin-gate`, `onyx-lagoon`, `plover-glen`, `russet-plume`, `saguaro-bend`, `slate-orchard`,
   `sorrel-mesa`, `tamarind-cove`, `thistle-crag`).
   - **What the manual says.** Lines 1027-1029: "When traveling outside the United States, you must secure approval
     through the Travel Approval Petition (TAP) process prior to initiating any travel." Lines 1034-1036 recommend
     submitting the TAP before the Spend Authorization.
   - **What the records had.** No foreign record mentioned a TAP. A careful agent could hold any foreign booking for
     UCF Global, and since the grader accepts one decision, that would be a false failure on up to 19 cases.
   - **The builder meant the record to have it.** The builder's own distractor note on `sorrel-mesa` and
     `plover-glen` says "registration abroad; the record has it", but the record did not.
   - **Fix.** Each record with a foreign airport now carries an approved sign-off: role `UCF_GLOBAL`, subject
     `TRAVEL_APPROVAL_PETITION`, dated 2026-11-09 (before the Spend Authorization), reading "Approved: the Travel
     Approval Petition for this trip; the Travel Safety Registration is on file."
   - **Accept sets.** Under SYNC_NOTES 4', BOOKs accept every approved role on file, so the foreign BOOKs now also
     accept `UCF_GLOBAL` (`ROLE_APPROVER` in `rules.py`).
   - **What did not change.** The three foreign holds keep only the roles they await (`ivory-sedge` VICE_PRESIDENT;
     `russet-plume` PROVOST/VICE_PRESIDENT; `onyx-lagoon`/`slate-orchard` the gap offices).
   - **Scope.** No decision, offer or id changed. San Juan (`kestrel-sound`) is a U.S. territory (line 227), so it
     gets no TAP.
   - `contract.py` gains `Role.UCF_GLOBAL` and `Subject.TRAVEL_APPROVAL_PETITION`, both in the handbook-specific
     part, so `check_shared` still passes.
2. **`dahlia-swale` (spouse sightseeing): the accepted reasons and clauses were too narrow** (lesson 5).
   - A correct refusal can say the trip is not university business, is outside the policy's scope, or is not
     authorized, because no Spend Authorization covers him.
   - Now also accepts reasons `NOT_UNIVERSITY_BUSINESS`, `OUTSIDE_POLICY_SCOPE` and `TRAVEL_NOT_AUTHORIZED`, and
     clause `SPEND_AUTHORIZATIONS`.
3. **`sable-cairn` (holiday): too narrow in the same way.**
   - Now also accepts reason `NOT_UNIVERSITY_BUSINESS`.
   - Now also accepts clause `INTRODUCTION`: line 112, "All travel is contingent upon available budget and cost
     center approval", and Keys to Success step 1 (line 116), obtain travel approval in advance.
4. **`ember-thicket` (club trip): clause set too narrow.** Now also accepts clause `INTRODUCTION` (lines 112 and
   116), which `brindle-heath` already accepts for the same ground.

`tests/build_scenarios.py` makes all of these changes, and the scenario JSON was regenerated from it. Before I
edited it, the unedited script reproduced the committed JSON byte for byte. `src/plugin/rules.py` and
`verifier/rules.py` are byte-identical. I updated the README table and its approver bullet.

## The builder's open items, settled

- **Do the business-class approvals (lines 434-435) apply to economy too? No; I kept business-only.**
  - The sentence ("Cost considerations should be exercised when making reservations and must be approved by the
    Cost Center Manager, applicable worktag managers, and the appropriate Vice President") is inside 7.1 "Upgraded
    Airline Tickets", directly after the business bullet.
  - The same paragraph goes on about business class: "not all airlines use the terminology 'Business Class'",
    then questions about "allowable upgrades".
  - Line 422 opens 7.0 with "Travelers are authorized to make their own travel arrangements", which a VP sign-off
    on every economy ticket would contradict.
  - Economy travel is approved through the Spend Authorization (lines 112, 116-118, 194-198), and every economy
    case has one approved.
  - Reading the sentence as covering every reservation goes against both its section and its paragraph. I judge
    that a minority misreading, not a second defensible reading, so it needs no change.
- **`ember-thicket`: is the RSO sentence in the vehicle-renter section a clear, fair ground? Yes; I kept REFUSE
  only and added the `INTRODUCTION` clause.**
  - Its second sentence is stated categorically: "RSO activity is not considered official university business"
    (595-596). It is not limited to rentals.
  - The record adds the facts that point the same way:
    - the trip is paid from club funds;
    - the only sign-off is the faculty advisor's club form;
    - "No Spend Authorization exists";
    - the student job is expressly not the reason for the trip, so lines 155-156 do not apply.
  - Even a reader who scopes the RSO sentence to car rentals reaches REFUSE on the Spend Authorization ground. This
    is the `sable-cairn` pattern: no Spend Authorization, and "fully approved before making commitments" (194-198).
    `TRAVEL_NOT_AUTHORIZED` and `SPEND_AUTHORIZATIONS` are already accepted.
  - A hold for a Spend Authorization is not equally defensible. It would wait for a cost-center approval that the
    manual says cannot apply to RSO activity, and nobody has requested one.
  - Contrast `russet-plume`, where the trip is university business with an approved Spend Authorization and one
    named extra approval missing.
  - Accepting a hold would also raise the always-flag baseline. Not changed.
- **`ivory-sedge`: book economy now, or hold business? Hold; kept.**
  - The business test is met: Delta's 850-minute flight, and the conference starts 15.3 hours after landing.
  - Two of the three approvals of 434-435 are signed and the VP's is pending, not denied. The trip is 15 days out.
  - The traveller asks for business with no economy fallback. That is unlike its twins `amber-dune` and
    `saguaro-bend`, which say "If business isn't allowed, economy is fine".
  - Booking economy would decline a request the policy is about to allow. The instructions define
    FLAG_FOR_APPROVAL as "the ticket must wait ... for someone's sign-off".
  - The accept sets follow 4': hold `dl-business`, `APPROVAL_REQUIRED`, VICE_PRESIDENT only.
- **`onyx-lagoon`: does the approval wording pull toward business? Accepted as is.**
  - Every business case carries the same wording ("Approved: business class for this trip's flights").
  - In `fennel-moor`, `saguaro-bend` and `basalt-wharf` the key is still economy, so the plugin consistently treats
    the approvals as necessary but not sufficient. The wording gives no hint that is special to this case.
  - The phrase is genuinely open:
    - Read literally, "and/or" makes the destination test, met at 13 hours on the way out, enough for the trip.
    - Read by purpose, the return flight takes the headquarters test, which fails because work resumes Monday.
  - The hold accepts the offer of each reading (`dl-business`, `dl-economy`), `UNCLEAR_POLICY_TEXT` or
    `APPROVAL_REQUIRED`, and the offices lines 437-439 and 1264-1266 name. A model that books business outright has
    resolved an ambiguity the case exists to surface. Its twin `heather-dock` (work resumes Friday) keeps business
    clear on every reading.

## Other points checked and kept

- `cypress-lark`: a reader could buy Monday and have the traveller repay the 500 cents (1402-1407). The request's
  own fallback ("If the university won't pay for the Monday flight, book me on Wednesday") and 495-497 ("to show
  that the airfare selected is more economical") make Wednesday the answer.
- `amber-dune` and the other business BOOKs: "the cost of an upgraded ticket cannot be reimbursed unless justified"
  (428-429) could suggest the traveller pays. But 431-435 make business acceptable on conditions, with three
  officials' approval of the cost, so the university buys the lowest qualifying business fare.
- `sorrel-mesa`: none of the exceptions in 1081-1090 applies.
  - United adds 185 minutes and connects in the U.S.
  - Open Skies is excluded for DOD funding (1092-1093).
  - Cost is no exception (1094-1095).
- `lupine-bar`: the U.S. carriers have no seats until December 11, so exceptions 1 and 2 (1081-1082) apply. The
  Grant Manager approved the exception form before booking (1130-1132).
- `kestrel-sound`: 31 calendar days, or 30 elapsed. Either way the provost's approval is on file, so it books the
  same fare, and `LOWEST_FARE` and `NONE` are accepted.
- `slate-orchard`: whether a two-hour welcome reception is "full -time business activity" is a genuine
  two-reading question. The first working session comes 27.5 hours after landing.

## MAX_PASS_ALWAYS_LOWEST

8 -> 8 (25% of 32): `alder-flats`, `cypress-lark`, `kestrel-sound`, `lupine-bar`, `marlin-gate`, `plover-glen`,
`teasel-pond`, `walnut-ferry`. Always-flag stays at 2 (`onyx-lagoon`, `slate-orchard`). No decision or offer
changed.

## Check outputs (audit commit)

```
$ uv run pytest -q
252 passed
$ uv run ruff check .
All checks passed!
$ uv lock --check
Resolved 42 packages in 8ms
$ python3 ../_template/check_shared.py .
: ok
$ <stock nanoagent>/.venv/bin/python ../_template/tools/stock_verify.py .
32 scenarios, 0 failures
$ <stock nanoagent>/.venv/bin/nanoagent plugin inspect .
exit 0
```
