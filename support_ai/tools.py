import json

DATABASE = {
    "ORD-101": {
        "customer_name": "Sarah",
        "item": "Mechanical Keyboard",
        "price": 2000.0,
        "charged": 4000.0,  # Double-charge scenario
        "status": "Delivered",
        "delivery_date": "2026-09-18"
    },
    "ORD-202": {
        "customer_name": "Marcus",
        "item": "UltraWide Gaming Monitor",
        "price": 250000.0,
        "charged": 250000.0,
        "status": "In Transit",
        "delivery_date": "2026-09-25"
    }
}

ESCALATION_QUEUE = []
EXECUTION_LOGS = []

def lookup_order(order_id: str) -> str:
    """Fetch order details, payment, and status by Order ID."""
    clean_id = order_id.strip().upper()
    order = DATABASE.get(clean_id)
    if not order:
        res = json.dumps({"error": f"Order {order_id} not found."})
    else:
        res = json.dumps(order)
    
    EXECUTION_LOGS.append({
        "name": "lookup_order",
        "args": {"order_id": clean_id},
        "result": res
    })
    return res

def issue_refund(order_id: str, amount: float, reason: str) -> str:
    """Process refund with strict RS 3500 safety guardrail."""
    clean_id = order_id.strip().upper()
    if clean_id not in DATABASE:
        res = json.dumps({"error": "Order ID not found."})
    elif amount > 3500.0:
        res = json.dumps({
            "status": "BLOCKED",
            "reason": f"Amount ${amount} exceeds automated safety limit of RS 3500."
        })
    else:
        DATABASE[clean_id]["charged"] -= amount
        res = json.dumps({
            "status": "SUCCESS",
            "transaction_id": f"TXN-REF-{clean_id[-3:]}77",
            "refunded_amount": amount,
            "new_balance": DATABASE[clean_id]["charged"]
        })

    EXECUTION_LOGS.append({
        "name": "issue_refund",
        "args": {"order_id": clean_id, "amount": amount, "reason": reason},
        "result": res
    })
    return res

def escalate_to_human(order_id: str, issue_summary: str, sentiment: str, suggested_action: str) -> str:
    """Escalate to a human manager when policies are exceeded."""
    ticket = {
        "ticket_id": f"TICK-{len(ESCALATION_QUEUE) + 101}",
        "order_id": order_id,
        "summary": issue_summary,
        "sentiment": sentiment,
        "suggested_action": suggested_action
    }
    ESCALATION_QUEUE.append(ticket)
    res = json.dumps({"status": "ESCALATED", "ticket": ticket})

    EXECUTION_LOGS.append({
        "name": "escalate_to_human",
        "args": {"order_id": order_id, "issue_summary": issue_summary},
        "result": res
    })
    return res