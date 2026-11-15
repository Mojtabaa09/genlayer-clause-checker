# Clause Checker (GenLayer Intelligent Contract)

A small Intelligent Contract that checks whether an agreement between two AI agents is clear enough for a jury to settle a dispute later.

Most agent disputes start with a vague agreement ("deliver good quality work fast"). This contract flags that before the deal starts.

## How it works

1. You send the agreement text to `check`.
2. Each GenLayer validator runs an LLM and answers three yes/no questions:
   - **measurable**: does the agreement define success with checkable criteria?
   - **deadline**: does it state a clear deadline?
   - **evidence**: does it say what evidence counts in a dispute?
3. Validators must agree on the answers (`strict_eq` consensus).
4. The final verdict is computed by plain deterministic code:
   - all three true -> `READY_FOR_JURY`
   - otherwise -> `NEEDS_REVISION`
5. Read the result with `get_report`.

GenLayer is not decorative here: the judgment itself is made by validators running LLMs and reaching consensus.

## Run it in GenLayer Studio (no install)

1. Open https://studio.genlayer.com
2. Open the Contracts tab, upload `clause_checker.py`.
3. Open Run and Deploy, select the file, click Deploy (no constructor inputs).
4. Under Write Methods, call `check` with an agreement text and click Send Transaction.
5. Wait until the transaction shows FINALIZED.
6. Under Read Methods, click Call Contract on `get_report`.

## Example 1: vague agreement

Input:

```
Agent A will deliver good quality work fast.
```

Result (from my Studio run):

```
{"deadline": false, "evidence": false, "measurable": false, "verdict": "NEEDS_REVISION"}
```

## Example 2: clear agreement

Input:

```
Agent A will deliver 50 product descriptions of at least 80 words each by Friday 18:00 UTC. A delivery counts as accepted if all 50 are original and match the product list in the shared spreadsheet. Evidence is the delivered file and the spreadsheet.
```

Result (from my Studio run):

```
{"deadline": true, "evidence": true, "measurable": true, "verdict": "READY_FOR_JURY"}
```

## Limitations

- It only checks how clear an agreement is. It does not settle the dispute itself.
- Tested only in GenLayer Studio. Results come from LLMs, so borderline agreements may vary between runs.
- The first line of the contract pins the GenVM runner version. If Studio uses a newer one, copy the header line from a built-in Studio example.

## Partner

(Add the Internet Court partner and how it is used here, once decided.)

## License

MIT
