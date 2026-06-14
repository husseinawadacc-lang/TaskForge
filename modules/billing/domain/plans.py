from modules.billing.domain.models import Plan


PLANS = {
    1: Plan(id=1, name="FREE", price=0, max_projects=1),
    2: Plan(id=2, name="PRO", price=1000, max_projects=100),
}


def get_plan(plan_id: int) -> Plan:
    return PLANS[plan_id]