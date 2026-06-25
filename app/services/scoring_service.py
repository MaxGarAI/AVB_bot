from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ScoringResult:
    audience_size_score: float = 0.0
    audience_trust_score: float = 2.0
    reachability_score: float = 0.0
    cross_sell_score: float = 0.0
    data_quality_score: float = 0.0
    partner_score_total: float = 0.0
    reasoning: str = ""
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)


class ScoringService:
    MAX_PER_FACTOR = 2.0
    TOTAL_MAX = 10.0

    def calculate(self, profile: dict) -> ScoringResult:
        audience = profile.get("audience_profile") or {}
        segments = profile.get("segments") or []
        channels = profile.get("channels") or []
        opportunities = profile.get("opportunities") or []
        distribution = profile.get("distribution_capabilities") or {}
        business = profile.get("business_profile") or {}

        monthly = audience.get("monthly_customers", 0) or 0
        audience_size = self._score_audience_size(monthly, segments)

        reachability = self._score_reachability(channels, distribution)

        cross_sell = self._score_cross_sell(opportunities, segments)

        data_quality = self._score_data_quality(profile)

        trust = 1.0
        if audience.get("repeat_rate", 0):
            trust = min(2.0, (audience.get("repeat_rate", 0) or 0) / 50.0)

        total = round((audience_size + reachability + cross_sell + data_quality + trust) * 2.0 / 2.0, 1)
        total = min(float(self.TOTAL_MAX), max(0.0, total))

        strengths = []
        weaknesses = []
        if monthly >= 300:
            strengths.append("Большая аудитория")
        else:
            weaknesses.append("Небольшая аудитория")
        if len(segments) >= 2:
            strengths.append("Хорошая сегментация")
        if len(channels) >= 2:
            strengths.append("Много каналов коммуникации")

        return ScoringResult(
            audience_size_score=audience_size,
            audience_trust_score=trust,
            reachability_score=reachability,
            cross_sell_score=cross_sell,
            data_quality_score=data_quality,
            partner_score_total=total,
            strengths=strengths,
            weaknesses=weaknesses,
        )

    @staticmethod
    def _score_audience_size(monthly: int, segments: list) -> float:
        score = 0.0
        if monthly >= 500:
            score = 2.0
        elif monthly >= 100:
            score = 1.0
        score += min(0.5, len(segments) * 0.2)
        return score

    @staticmethod
    def _score_reachability(channels: list, distribution: dict) -> float:
        score = min(2.0, len(channels) * 0.4)
        if distribution.get("can_send_email"):
            score += 0.3
        if distribution.get("can_send_sms"):
            score += 0.3
        if distribution.get("can_do_personal_recommendations"):
            score += 0.5
        return min(2.0, score)

    @staticmethod
    def _score_cross_sell(opportunities: list, segments: list) -> float:
        score = min(2.0, len(opportunities) * 0.5)
        return score

    @staticmethod
    def _score_data_quality(profile: dict) -> float:
        filled = 0
        total = 6
        if profile.get("business_profile"):
            filled += 1
        if profile.get("audience_profile"):
            filled += 1
        if profile.get("segments"):
            filled += 1
        if profile.get("channels"):
            filled += 1
        if profile.get("distribution_capabilities"):
            filled += 1
        if profile.get("opportunities"):
            filled += 1
        return round((filled / total) * 2.0, 1)