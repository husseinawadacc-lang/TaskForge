from db.session import SessionLocal
from db.models.plan import PlanORM


def seed_plans():
    session = SessionLocal()

    existing = session.query(PlanORM).count()
    if existing > 0:
        print("Plans already exist")
        session.close()
        return

    plans = [
        PlanORM(id=1, name="FREE", price=0),
        PlanORM(id=2, name="PRO", price=10),
    ]

    session.add_all(plans)
    session.commit()
    session.close()

    print("Plans seeded successfully")


if __name__ == "__main__":
    seed_plans()