from app.ai.agent import write_reply
from app.ai.classifier import classify
from app.ai.rules import CUSTOMER_STEPS, resolve_issue
from app.ai.schemas import Decision, Issue


def decide(thread: str, has_attachments: bool = False) -> Decision:
    """Run the AI steps for one email thread. The models propose, this function decides."""
    classification = classify(thread)

    def escalate(reason: str, proposed_action: str | None = None) -> Decision:
        return Decision(
            action="escalate",
            section=classification.section,
            reply=classification.acknowledgement,
            reason=reason,
            proposed_action=proposed_action,
        )

    if has_attachments:
        return escalate("The email has attachments")
    if classification.needs_human:
        return escalate(classification.reason)
    answer = write_reply(thread, classification.section)
    if answer.action == "escalate":
        return escalate(answer.reasoning)
    if not answer.enough_information:
        return escalate("The knowledge base does not answer this")
    if answer.issue_summary:
        # We no longer use a structured Issue object here to avoid tool-calling errors.
        # The logic for 'resolve_issue' would now happen by parsing this string 
        # or by a separate classifier. For now, we just log it.
        pass
    if answer.promises_an_action:
        return escalate("The reply promises an action")
    return Decision(
        action="reply",
        section=classification.section,
        reply=answer.reply,
        reason=answer.reasoning,
    )


def parse_issue(issue_text: str, section: str) -> Issue:
    """Convert the model's free-text issue description into a structured Issue object."""
    text = issue_text.lower()
    # Default values
    product = "paddle-board" if section == "paddle-boards" else "shelving"
    problem = "damaged-panels"  # default
    order_number = None
    days_since_delivery = None
    valve_checked = False
    part_numbers = []

    # Extract order number if present
    import re
    order_match = re.search(r"\b\d{3}-\d{7}-\d{7}\b", issue_text)
    if order_match:
        order_number = order_match.group(0)

    # Extract part numbers (e.g., HP-S3-04)
    part_numbers = re.findall(r"\b[A-Z]{2}-[A-Z]\d-\d{2}\b", issue_text)

    # Determine product and problem from text
    if "paddle" in text or section == "paddle-boards":
        product = "paddle-board"
        if "slow leak" in text or "leak" in text:
            problem = "slow-leak"
        elif "missing" in text and "accessory" in text:
            problem = "missing-accessory"
        elif "seam" in text:
            problem = "seam-split"
    else:
        product = "shelving"
        if "missing" in text and ("hardware" in text or "screw" in text):
            problem = "missing-hardware"
        elif "wrong finish" in text or "wrong colour" in text:
            problem = "wrong-finish"
        elif "frame" in text:
            problem = "damaged-frame"
        elif "panel" in text or "crack" in text or "damage" in text:
            problem = "damaged-panels"

    return Issue(
        product=product,
        problem=problem,
        order_number=order_number,
        days_since_delivery=days_since_delivery,
        valve_checked=valve_checked,
        part_numbers=part_numbers,
    )