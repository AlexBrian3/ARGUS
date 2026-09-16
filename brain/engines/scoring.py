"""
Engine 5 — OPPORTUNITY SCORING
Calculates the proprietary HACKSCORE /100 and mathematical expected-value ratios:
- Reward quality: 20
- Competition attractiveness: 20 (penalizes massive 15k meat-grinders, rewards high prize-to-competitor ratio)
- Skill fit: 15
- Sponsor history: 10
- Ecosystem momentum: 10
- Prize breadth: 10
- Participation rewards: 5
- Startup potential: 5
- Portfolio/learning value: 5

Outputs transparent estimates (clearly labeled as estimates):
- Expected serious competitors
- Prize-to-competitor ratio ($ / serious competitor)
- Expected probability of placing (%)
- Expected probability of receiving any reward (%)
"""
from typing import Dict, Any, Tuple
from brain.config import HACKSCORE_WEIGHTS


class OpportunityScorer:
    def calculate_competition_attractiveness(self, prize_usd: float, total_expected_competitors: int) -> Tuple[float, int, float, float, float]:
        """
        Calculates competition attractiveness score (0-20) and EV metrics.
        A $20,000 event with 100 participants is often far superior to a $500,000 event with 15,000 participants.

        Returns:
            (attractiveness_score, serious_competitors, prize_to_comp_ratio, prob_placing, prob_any_reward)
        """
        # Historical heuristic: In developer hackathons, only 20-35% of registered signups submit a complete, functional project
        serious_competitors = max(int(total_expected_competitors * 0.28), 10)

        # Prize-to-competitor ratio ($ / serious competitor)
        prize_ratio = prize_usd / serious_competitors

        # Score curve:
        # > $1,000 per serious builder = 20.0
        # $500 - $1,000 = 17 - 19
        # $200 - $500 = 14 - 16
        # $50 - $200 = 10 - 13
        # < $50 = 5 - 9
        if prize_ratio >= 1000.0:
            attractiveness_score = 20.0
        elif prize_ratio >= 500.0:
            attractiveness_score = 17.0 + (prize_ratio - 500.0) / 500.0 * 3.0
        elif prize_ratio >= 200.0:
            attractiveness_score = 13.0 + (prize_ratio - 200.0) / 300.0 * 4.0
        elif prize_ratio >= 50.0:
            attractiveness_score = 9.0 + (prize_ratio - 50.0) / 150.0 * 4.0
        else:
            attractiveness_score = max(4.0, (prize_ratio / 50.0) * 8.0)

        # Expected placement probability for a top-tier prepared engineer
        # Baseline probability scales inversely with serious competitors and directly with prize breadth
        prob_placing = min(max(round(18.0 / (serious_competitors ** 0.55), 3), 0.05), 0.45)

        # Probability of winning *any* bounty / pool / track reward
        prob_any_reward = min(max(round(prob_placing * 1.85, 3), 0.10), 0.75)

        return (
            round(attractiveness_score, 1),
            serious_competitors,
            round(prize_ratio, 2),
            prob_placing,
            prob_any_reward
        )

    def calculate_hack_score(
        self,
        prize_usd: float,
        expected_competitors: int,
        skill_fit_score: float, # 0 - 100
        sponsor_predictability: float = 85.0, # 0 - 100
        ecosystem_momentum: float = 85.0, # 0 - 100
        num_tracks_and_bounties: int = 5,
        has_participation_rewards: bool = True,
        is_accelerator_or_vc_backed: bool = True,
        cutting_edge_learning_value: float = 90.0 # 0 - 100
    ) -> Dict[str, Any]:
        """
        Computes the complete HackScore /100 and breakdown.
        """
        # 1. Reward Quality (max 20)
        # Scale: $1M+ = 20, $500k = 18, $100k = 16, $50k = 14, $20k = 12
        if prize_usd >= 1000000:
            reward_quality = 20.0
        elif prize_usd >= 500000:
            reward_quality = 18.5
        elif prize_usd >= 100000:
            reward_quality = 16.5
        elif prize_usd >= 50000:
            reward_quality = 14.5
        elif prize_usd >= 20000:
            reward_quality = 12.5
        else:
            reward_quality = max(6.0, (prize_usd / 20000.0) * 11.0)

        # 2. Competition Attractiveness (max 20)
        (
            comp_attractiveness,
            serious_competitors,
            prize_ratio,
            prob_placing,
            prob_any_reward
        ) = self.calculate_competition_attractiveness(prize_usd, expected_competitors)

        # 3. Skill Fit (max 15)
        skill_fit = round((skill_fit_score / 100.0) * 15.0, 1)

        # 4. Sponsor History (max 10)
        sponsor_history = round((sponsor_predictability / 100.0) * 10.0, 1)

        # 5. Ecosystem Momentum (max 10)
        eco_momentum = round((ecosystem_momentum / 100.0) * 10.0, 1)

        # 6. Prize Breadth (max 10)
        # More tracks/bounties = higher chance of bagging multiple prizes
        prize_breadth = min(max(num_tracks_and_bounties * 2.0, 4.0), 10.0)

        # 7. Participation Rewards (max 5)
        part_rewards = 5.0 if has_participation_rewards else 1.5

        # 8. Startup Potential (max 5)
        startup_pot = 5.0 if is_accelerator_or_vc_backed else 2.5

        # 9. Portfolio/Learning Value (max 5)
        portfolio_val = round((cutting_edge_learning_value / 100.0) * 5.0, 1)

        total_score = (
            reward_quality +
            comp_attractiveness +
            skill_fit +
            sponsor_history +
            eco_momentum +
            prize_breadth +
            part_rewards +
            startup_pot +
            portfolio_val
        )

        total_score = min(max(round(total_score, 1), 0.0), 100.0)

        return {
            "hack_score": total_score,
            "serious_competitors_est": serious_competitors,
            "prize_to_competitor_ratio_est": prize_ratio,
            "prob_placing_est": prob_placing,
            "prob_any_reward_est": prob_any_reward,
            "breakdown": {
                "reward_quality": round(reward_quality, 1),
                "competition_attractiveness": round(comp_attractiveness, 1),
                "skill_fit": round(skill_fit, 1),
                "sponsor_history": round(sponsor_history, 1),
                "ecosystem_momentum": round(eco_momentum, 1),
                "prize_breadth": round(prize_breadth, 1),
                "participation_rewards": round(part_rewards, 1),
                "startup_potential": round(startup_pot, 1),
                "portfolio_value": round(portfolio_val, 1)
            }
        }
