# algo.py
import math
from datetime import datetime, timedelta
from typing import List

from .types import Breakdown, CommitData, Result


class ELO:
    def __init__(self) -> None:
        self.DECAY_PER_DAY = 0.99
        self.MAX_AGE_DAYS = 90
        self.TZ_OFFSET_MIN = 0

        self.WEIGHTS = {
            "loc": 0.25,
            "time": 0.10,
            "day": 0.05,
            "message": 0.20,
            "consistency": 0.15,
            "frequency": 0.25,
        }

    def calculate(self, commits: List[CommitData]) -> Result:
        now = datetime.now()

        # Filter and sort commits
        recent: List[CommitData] = []
        for c in commits:
            age_days = (now - c["timestamp"]).days
            if age_days <= self.MAX_AGE_DAYS:
                recent.append(c)

        recent.sort(key=lambda c: c["timestamp"])

        if not recent:
            return {
                "eloDelta": 0,
                "breakdown": {
                    "lateNightContribution": 0,
                    "burstContribution": 0,
                    "messageQualityDeduction": 0,
                    "frequencyContribution": 0,
                    "consistencyContribution": 0,
                },
            }

        # Calculate once, outside loop
        burstiness = self._simple_burstiness(recent)

        total = 0.0
        weight_sum = 0.0
        avg_time_score = 0.0
        total_msg_score = 0.0
        total_frequency = 0.0
        total_combined_consistency = 0.0

        for c in recent:
            age_days = (now - c["timestamp"]).total_seconds() / 86400
            w = pow(self.DECAY_PER_DAY, age_days)

            loc_score = self._loc_score(c)
            time_score = self._time_score(c)
            day_score = self._day_score(c)

            # ML signals from each commit
            msg_score = c.get("commit_score", 0.5)
            frequency = c.get("commit_frequency", 0.0)
            ml_consistency = c.get("commit_consistency", 0.5)

            # Track for averages
            avg_time_score += time_score
            total_msg_score += msg_score
            total_frequency += frequency

            # Combine consistency signals
            combined_consistency = (ml_consistency + (1.0 - burstiness)) / 2
            total_combined_consistency += combined_consistency

            # Weighted combination
            combined = (
                self.WEIGHTS["loc"] * loc_score
                + self.WEIGHTS["time"] * time_score
                + self.WEIGHTS["day"] * day_score
                + self.WEIGHTS["message"] * msg_score
                + self.WEIGHTS["consistency"] * combined_consistency
                + self.WEIGHTS["frequency"] * frequency
            )

            spike = combined * 30
            total += spike * w
            weight_sum += w

        # Calculate averages
        commit_count = len(recent)
        avg_time_score /= commit_count
        avg_msg_score = total_msg_score / commit_count
        avg_frequency = total_frequency / commit_count
        avg_combined_consistency = total_combined_consistency / commit_count

        level = int(round(total))

        breakdown: Breakdown = {
            "lateNightContribution": round((1 - avg_time_score) * 100),
            "burstContribution": round(burstiness * 100),
            "messageQualityDeduction": round((1 - avg_msg_score) * 100),
            "frequencyContribution": round(avg_frequency * 100),
            "consistencyContribution": round(avg_combined_consistency * 100),
        }

        result: Result = {
            "eloDelta": level,
            "breakdown": breakdown,
        }

        return result

    def _loc_score(self, c: CommitData) -> float:
        """Score based on lines changed (0-1 scale)"""
        changes = c["additions"] + c["deletions"]
        return min(1.0, math.log10(changes + 1) / 4)

    def _time_score(self, c: CommitData) -> float:
        """Score based on time of day (peak during work hours)"""
        hour = self._hour_local(c)

        if 9 <= hour <= 17:
            return 1.0
        elif 6 <= hour <= 8 or 18 <= hour <= 22:
            return 0.5
        else:
            return 0.0

    def _day_score(self, c: CommitData) -> float:
        """Score based on day of week"""
        day = self._day_local(c)
        return 1.0 if day not in (0, 6) else 0.3

    def _simple_burstiness(self, commits: List[CommitData]) -> float:
        if len(commits) < 3:
            return 0.0

        hours: List[float] = []
        for i in range(1, len(commits)):
            diff_h = (
                commits[i]["timestamp"] - commits[i - 1]["timestamp"]
            ).total_seconds() / 3600
            hours.append(max(0.0, min(48.0, diff_h)))

        avg = sum(hours) / len(hours)
        variance = sum((h - avg) ** 2 for h in hours) / len(hours)
        sd = math.sqrt(variance)
        cv = sd / avg if avg > 0 else 0

        return min(1.0, cv / 2)

    def _hour_local(self, c: CommitData) -> int:
        adjusted = c["timestamp"] + timedelta(minutes=self.TZ_OFFSET_MIN)
        return adjusted.hour

    def _day_local(self, c: CommitData) -> int:
        adjusted = c["timestamp"] + timedelta(minutes=self.TZ_OFFSET_MIN)
        weekday = adjusted.weekday()
        return (weekday + 1) % 7
