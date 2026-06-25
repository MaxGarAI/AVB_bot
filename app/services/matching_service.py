from __future__ import annotations


class MatchingService:
    CATEGORY_RULES: dict[str, list[str]] = {
        "собака|собак": ["pet_services", "pet_food"],
        "pet|животное|кошк|питом": ["pet_services", "pet_food", "veterinary"],
        "авто|машин|bmw|mercedes": ["insurance", "automotive", "car_loans"],
        "владелец дом|homeowner": ["insurance", "home_services", "solar", "mortgage"],
        "страхов": ["insurance"],
        "ремонт|сервис|обслуживан": ["automotive", "home_services"],
        "семь|дети|родител": ["education", "insurance", "family_finance"],
        "бизнес|предпринимател": ["loans", "saas", "legal_services", "crm"],
        "здоров|фитнес|спорт": ["health", "fitness"],
        "космет|салон|груминг|барбер": ["grooming", "cosmetics", "beauty"],
        "стомат|зуб": ["insurance", "health", "cosmetics"],
        "финанс|кредит|займ": ["loans", "finance"],
        "юрист|адвокат": ["legal_services"],
        "бухгалтер": ["loans", "saas", "crm"],
    }

    def match(self, segments: list[dict], needs: list[str]) -> list[dict]:
        opportunities: list[dict] = []
        seen_categories: set[str] = set()
        combined_text = " ".join(
            [seg.get("name", "") for seg in segments]
            + [seg.get("pain_points_json", "") for seg in segments]
            + needs
        ).lower()

        for keyword_chain, categories in self.CATEGORY_RULES.items():
            keywords = keyword_chain.split("|")
            if any(kw in combined_text for kw in keywords):
                for category in categories:
                    if category not in seen_categories:
                        seen_categories.add(category)
                        opportunities.append({
                            "category": category,
                            "confidence_score": 80,
                            "weight": 0.8,
                        })

        return opportunities