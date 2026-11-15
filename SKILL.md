---
name: clause-check-before-escrow
description: Use before creating a natural-language escrow (for example with Arkhai's `nla escrow:create --demand ...`). Checks that the demand text is clear enough for a jury to settle later, using a GenLayer Intelligent Contract. Trigger when an agent is about to lock funds against a natural-language agreement.
---

# Clause Check Before Escrow

## Why

A natural-language escrow is only as good as its demand text. If the demand says "good quality work, fast", both sides can claim they are right and the dispute starts on day one. This skill adds one step before funds are locked: check the demand with the Clause Checker contract on GenLayer.

## When to use

Use this right before any step that locks funds against a natural-language agreement, for example:

```
nla escrow:create --demand "<natural language demand>" --amount <token-amount>
```

(Command and options as documented in the Arkhai `natural-language-agreements` README.)

## Steps

1. Draft the demand text you plan to pass to `--demand`.
2. Open GenLayer Studio (https://studio.genlayer.com), deploy `clause_checker.py` from this repo (see README), and call `check` with the demand text. Wait until the transaction is FINALIZED.
3. Call `get_report`. It returns JSON with `measurable`, `deadline`, `evidence` and `verdict`.
4. Decide:
   - `READY_FOR_JURY`: continue and create the escrow.
   - `NEEDS_REVISION`: rewrite the demand to fix the missing parts, then check again. Do not create the escrow yet.

## How to fix a demand

- `measurable` is false: replace vague words ("good", "fast", "professional") with checkable criteria (counts, formats, thresholds).
- `deadline` is false: add an exact date and time with a timezone.
- `evidence` is false: say what evidence counts in a dispute (files, links, logs).

## Example

Vague demand, verdict `NEEDS_REVISION`:

```
Agent A will deliver good quality work fast.
```

Clear demand, verdict `READY_FOR_JURY`:

```
Agent A will deliver 50 product descriptions of at least 80 words each by Friday 18:00 UTC. A delivery counts as accepted if all 50 are original and match the product list in the shared spreadsheet. Evidence is the delivered file and the spreadsheet.
```

## Limits

- This skill checks clarity only. It does not create the escrow and it does not settle the dispute.
- Results come from validators running LLMs, so borderline demands may vary between runs.
- Tested in GenLayer Studio only.
