# Validation notes: ucf-flight-policy (paid wave 3 validation, 2026-11-25)

Run: `efficient_corporate_travel_agent/pilot/ladder/runs/validation_w3_2026-11-25/ucf-flight-policy@w3/`, arm
`full`, DeepSeek V4 Flash (Nebius), temperature 0, max_steps 6, max_tokens 8192, one run per scenario, at plugin
head d6676f3. Line numbers are lines of `src/plugin/data/policy.txt`.

## Results

28/32 valid (87.5%), mean field score 0.938, **easy 6/6**. Flags 2/4, boundary twins 6/8. $0.00193 billed per run,
22,676 prompt tokens per call; 29 of 32 runs would exceed the hosted 65,536 cap.

## Every failure, classified

| scenario | category | submitted vs key | class | evidence |
|---|---|---|---|---|
| fennel-moor | boundary_twin | BOOK Qatar business, LONG_FLIGHT_APPROVED; key American economy | model slip (boundary arithmetic) | "full-time business begins within 24 hours of arrival (workshop starts Dec 1; arrival Nov 30)". It compared dates, not hours: Qatar lands November 30 at 09:30 and the workshop starts December 1 at 10:30, 25 hours later (lines 431-433). The twin juniper-wake (08:30, 23 hours) passed. |
| walnut-ferry | boundary_twin | BOOK Southwest Wednesday, PERSONAL_TRAVEL_NOT_COVERED; key Southwest Monday | model slip | "The Monday December 7 flight was declined because those days (Dec 7-9) are personal days". It never compared fares: Monday ($284) is below Wednesday ($289), and lines 491-497 allow a deviation from the travel time when a comparable quote shows it is more economical. The twin cypress-lark ($294 Monday) passed. |
| onyx-lagoon | flag | BOOK Emirates business, LONG_FLIGHT_APPROVED; key FLAG | model slip | "business class is acceptable when at least one flight segment is nine hours or longer and it is approved ...". It dropped the second condition of lines 431-433 (full-time business within 24 hours of arrival "and/or return to headquarters") and never weighed the flight home, after which work resumes four days later. |
| slate-orchard | flag | BOOK Qatar business, LONG_FLIGHT_APPROVED, VICE_PRESIDENT; key FLAG | model slip | It quoted "full-time business begins within 24 hours of arrival" and never asked whether the two-hour welcome reception, 9.5 hours after landing, is "full -time business activity"; the sessions start 27.5 hours after landing. |

## Fixes (this commit)

No failure of this run is a defect. One latent grader gap of the idi aspen-fjord class (a traveller who sets an
approved upgrade aside to save money gives `COST_SAVINGS`) is closed:

- **marlin-gate (easy) and alder-flats:** "The department approved business class, but I'd rather save the money" and
  "The department signed off on business class, but book whatever costs the university least". `COST_SAVINGS` is
  accepted beside `LOWEST_FARE` where the vice president's business-class approval is on file and the traveller asks
  for economy (`economy()` in `src/plugin/rules.py` and the byte-identical `verifier/rules.py`; both keys in
  `tests/build_scenarios.py`; README). Both passed this run. uk-dbt cobalt-weir and alder-pennant key the same pair.

Not loosened: fennel-moor, walnut-ferry, onyx-lagoon, slate-orchard.

## Q2

The always-cheapest agent answers `LOWEST_FARE`, already accepted: unchanged at **8/32 (25%)**.

## Re-score at the new head (stored answers)

28/32, easy 6/6. No record or request changed, so no re-run is required.

## Checks

`uv run pytest -q` (252 passed), `uv run ruff check .`, `uv lock --check`, `check_shared.py`, byte-identical
`rules.py`, `tools/stock_verify.py` (32 scenarios, 0 failures), stock `nanoagent plugin inspect .` (exit 0).
