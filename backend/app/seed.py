from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.cost_of_living import CostOfLiving
from app.models.country import Country
from app.models.job_market import JobMarket
from app.models.salary import Salary
from app.models.tax import Tax
from app.models.user import User
from app.models.visa_program import VisaProgram

COUNTRIES = [
    ("Germany", "DE", 8.3, 6.5, 4.0, 8.8, 8.9, 78000, 32, 1500, 1100, 120, ["Java", "Spring Boot", "SAP"]),
    ("Canada", "CA", 8.0, 5.5, 5.0, 8.5, 8.4, 86000, 30, 1700, 1250, 130, ["Cloud", "DevOps", "Azure"]),
    ("Australia", "AU", 8.2, 5.0, 5.5, 8.6, 8.5, 91000, 31, 1800, 1300, 140, ["Data", "Platform", "Cybersecurity"]),
    ("Netherlands", "NL", 8.6, 6.0, 4.5, 9.0, 9.0, 84000, 34, 1650, 1200, 110, ["Java", "Frontend", "Cloud"]),
    ("Singapore", "SG", 7.4, 4.5, 7.0, 8.2, 9.1, 98000, 22, 2100, 1500, 120, ["Data Engineering", "AI", "FinTech"]),
    ("UAE", "AE", 7.0, 3.0, 8.5, 7.8, 8.0, 94000, 10, 2000, 1400, 180, ["Backend", "FinTech", "Cloud"]),
    ("United Kingdom", "UK", 7.8, 5.8, 5.8, 8.3, 8.3, 82000, 33, 1850, 1250, 150, ["JavaScript", "AI", "Data"]),
    ("Ireland", "IE", 8.1, 5.6, 5.0, 8.4, 8.6, 88000, 30, 1750, 1200, 130, ["Cloud", "SRE", "Python"]),
    ("Sweden", "SE", 8.8, 6.2, 4.8, 9.2, 9.2, 76000, 36, 1400, 1100, 100, ["Backend", "Data", "Mobile"]),
    ("Norway", "NO", 8.7, 6.4, 5.2, 9.3, 9.3, 93000, 35, 1900, 1350, 115, ["Energy Tech", "Java", "Cloud"]),
]


def seed() -> None:
    db = SessionLocal()
    try:
        if db.query(Country).first():
            return

        user = User(email="demo@wayfarer.ai", full_name="Demo User", hashed_password=get_password_hash("demo12345"))
        db.add(user)
        db.flush()

        for name, code, wlb, visa_diff, pr_diff, healthcare, safety, salary, tax, rent, living, transport, skills in COUNTRIES:
            country = Country(
                name=name,
                code=code,
                work_life_balance_score=wlb,
                visa_difficulty_score=visa_diff,
                pr_difficulty_score=pr_diff,
                healthcare_score=healthcare,
                safety_score=safety,
            )
            db.add(country)
            db.flush()

            db.add(Salary(country_id=country.id, role="Software Engineer", average_annual_salary_usd=salary))
            db.add(Tax(country_id=country.id, effective_tax_percent=tax))
            db.add(
                CostOfLiving(
                    country_id=country.id,
                    rent_usd=rent,
                    living_expenses_usd=living,
                    transport_usd=transport,
                )
            )
            db.add(
                VisaProgram(
                    country_id=country.id,
                    visa_name=f"{name} Skilled Worker Visa",
                    pathway_summary=f"Employer sponsorship route with PR progression in {name}.",
                    processing_time_months=4,
                )
            )
            for idx, skill in enumerate(skills):
                db.add(JobMarket(country_id=country.id, skill=skill, demand_score=9 - idx))

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
