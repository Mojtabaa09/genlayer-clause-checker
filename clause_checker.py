# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json


class ClauseChecker(gl.Contract):
    """Checks whether an agent-to-agent agreement is clear enough
    for a jury to settle a dispute later."""

    last_agreement: str
    has_measurable_criteria: bool
    has_deadline: bool
    has_evidence_rule: bool
    verdict: str

    def __init__(self):
        self.last_agreement = ""
        self.has_measurable_criteria = False
        self.has_deadline = False
        self.has_evidence_rule = False
        self.verdict = ""

    @gl.public.write
    def check(self, agreement: str) -> None:
        def run():
            result = gl.nondet.exec_prompt(
                "You review agreements between two AI agents. "
                "Answer three yes/no questions about the agreement below.\n"
                "1. measurable: does it define success with checkable criteria "
                "(not vague words like 'good quality' or 'fast')?\n"
                "2. deadline: does it state a clear deadline?\n"
                "3. evidence: does it say what evidence counts in a dispute?\n"
                f'Agreement: "{agreement}"\n'
                'Respond ONLY with valid JSON: '
                '{"measurable": true|false, "deadline": true|false, "evidence": true|false}',
                response_format="json",
            )
            clean = {
                "measurable": bool(result.get("measurable")),
                "deadline": bool(result.get("deadline")),
                "evidence": bool(result.get("evidence")),
            }
            return json.dumps(clean, sort_keys=True)

        raw = gl.eq_principle.strict_eq(run)
        data = json.loads(raw)

        self.last_agreement = agreement
        self.has_measurable_criteria = data["measurable"]
        self.has_deadline = data["deadline"]
        self.has_evidence_rule = data["evidence"]

        # The final verdict is computed by plain deterministic code.
        if data["measurable"] and data["deadline"] and data["evidence"]:
            self.verdict = "READY_FOR_JURY"
        else:
            self.verdict = "NEEDS_REVISION"

    @gl.public.view
    def get_report(self) -> str:
        return json.dumps(
            {
                "verdict": self.verdict,
                "measurable": self.has_measurable_criteria,
                "deadline": self.has_deadline,
                "evidence": self.has_evidence_rule,
            },
            sort_keys=True,
        )
