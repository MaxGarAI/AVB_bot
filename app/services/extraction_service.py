from __future__ import annotations

import json
import re


class ExtractionService:
    def extract(self, transcript: str, general_context: str = "") -> dict:
        return {
            "business_profile": self._extract_business(transcript),
            "audience_profile": self._extract_audience(transcript),
            "segments": self._extract_segments(transcript),
            "channels": self._extract_channels(transcript),
        }

    @staticmethod
    def _extract_business(transcript: str) -> dict:
        result: dict[str, str | int | None] = {
            "business_name": None,
            "industry": None,
            "website": None,
            "city": None,
            "state": None,
            "years_in_business": None,
            "employees": None,
        }

        website_match = re.search(r"(?:сайт[е\s]|https?://)?([a-zA-Z0-9][a-zA-Z0-9.-]*\.[a-zA-Z]{2,})", transcript)
        if website_match:
            result["website"] = website_match.group(1).rstrip(".")

        city_match = re.search(r"(?:в\s)([А-Я][а-яё]+)(?:,|\.|\s|$)", transcript)
        if city_match:
            result["city"] = city_match.group(1)

        name_match = re.search(r"(?:называ[ею]мся|это)\s+([A-ZА-Я][A-Za-zА-Яа-яёЁ0-9\s]+?)(?:\.|,|\s+работаем|\s+в\s|$)", transcript)
        if name_match:
            result["business_name"] = name_match.group(1).strip()

        # Fallback: find capitalized name
        if not result["business_name"]:
            name_match2 = re.search(r"\b([A-ZА-Я][a-zа-яё]{2,}(?:Pro|Plus|Max)?)\b", transcript)
            if name_match2 and name_match2.group(1).lower() not in ("у", "нас", "в", "на", "с", "по", "от"):
                result["business_name"] = name_match2.group(1)

        years_match = re.search(r"(\d+)\s+(?:год|лет)", transcript)
        if years_match:
            result["years_in_business"] = int(years_match.group(1))

        employees_match = re.search(r"(\d+)\s+(?:сотрудник|человек)", transcript)
        if employees_match:
            result["employees"] = int(employees_match.group(1))

        return result

    @staticmethod
    def _extract_audience(transcript: str) -> dict:
        result: dict[str, int | float | None] = {
            "monthly_customers": None,
            "repeat_rate": None,
        }

        monthly_match = re.search(r"(\d+)\s+(?:клиент[ао]в)?\s*(?:в\s)?месяц", transcript)
        if monthly_match:
            result["monthly_customers"] = int(monthly_match.group(1))

        rate_match = re.search(r"(\d+)\s*(?:%|процент[ао]?в?)", transcript)
        if rate_match:
            result["repeat_rate"] = int(rate_match.group(1))

        return result

    @staticmethod
    def _extract_segments(transcript: str) -> list[dict]:
        segments: list[dict] = []

        owner_patterns = [
            (r"владельц[ыа]\s+([^.]*)", "владельцы"),
            (r"(?:покупател[ияей]|клиенты)\s+([^.]*)", "клиенты"),
        ]

        for pattern, default_name in owner_patterns:
            match = re.search(pattern, transcript, re.IGNORECASE)
            if match:
                description = match.group(1).strip()[:80]
                segments.append({
                    "name": default_name,
                    "description": description,
                    "pain_points": [],
                })

        # If nothing found but transcript talks about audience
        if not segments and re.search(r"(?:клиент|аудитори|покупател|владельц)", transcript, re.IGNORECASE):
            segments.append({
                "name": "Основные клиенты",
                "description": transcript[:100],
                "pain_points": [],
            })

        return segments

    @staticmethod
    def _extract_channels(transcript: str) -> list[dict]:
        channels: list[dict] = []
        channel_keywords = {
            "email": "email",
            "почт": "email",
            "sms": "sms",
            "ватсап": "whatsapp",
            "whatsapp": "whatsapp",
            "instagram": "instagram",
            "инстаграм": "instagram",
            "facebook": "facebook",
            "telegram": "telegram",
            r"соц[и\s]": "social",
            "социальн": "social",
        }

        for keyword, channel_type in channel_keywords.items():
            if re.search(keyword, transcript, re.IGNORECASE):
                if not any(c["channel_type"] == channel_type for c in channels):
                    channels.append({"channel_type": channel_type})

        return channels