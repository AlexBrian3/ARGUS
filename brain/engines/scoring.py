"""
-------------------------------------------------------------------------------
ENGINE 5: OPPORTUNITY SCORING (HACKSCORE)
-------------------------------------------------------------------------------
This engine calculates a smart score called HACKSCORE (out of 100).

The Golden Rule of Hackathons:
A $20,000 hackathon with 100 participants is often 10x better than
a $500,000 hackathon with 15,000 participants.

We calculate:
1. How many builders are ACTUALLY serious competitors
2. How many prize dollars exist per serious competitor
3. Your estimated probability of placing or winning a bounty
4. The final HackScore (out of 100)
"""

from typing import Dict, Any, Tuple
from brain.config import HACKSCORE_WEIGHTS


class OpportunityScorer:
    """Calculates HackScore and expected-value ratios for any developer competition."""

    def calculate_competition_attractiveness(
        self,
        prize_usd: float,
        total_expected_competitors: int
    ) -> Tuple[float, int, float, float, float]:
        """
        Step-by-step calculation of how attractive the competition is.
        Returns:
            (attractiveness_score, serious_competitors, prize_per_builder, prob_placing, prob_any_reward)
        """

        # ------------------------------------------------------------------- #
        # Step 1: Estimate how many builders are actually serious competitors #
        # ------------------------------------------------------------------- #
        # In developer hackathons, historical data shows that only about 28% of
        # people who click "Register" actually submit a working, complete project.
        # The rest drop out or submit empty repos.
        completion_rate = 0.28
        estimated_serious_competitors = int(total_expected_competitors * completion_rate)

        # Make sure we have at least 10 serious competitors for realistic math
        serious_competitors = max(estimated_serious_competitors, 10)

        # ------------------------------------------------------------------- #
        # Step 2: Calculate the prize money per serious builder ($/builder)   #
        # ------------------------------------------------------------------- #
        prize_per_builder = prize_usd / serious_competitors

        # ------------------------------------------------------------------- #
        # Step 3: Turn the prize-per-builder ratio into a score (out of 20)   #
        # ------------------------------------------------------------------- #
        if prize_per_builder >= 1000.0:
            # Huge prize per person! Top score!
            attractiveness_score = 20.0

        elif prize_per_builder >= 500.0:
            # Very attractive (between 17.0 and 20.0 points)
            bonus = (prize_per_builder - 500.0) / 500.0 * 3.0
            attractiveness_score = 17.0 + bonus

        elif prize_per_builder >= 200.0:
            # Good opportunity (between 13.0 and 17.0 points)
            bonus = (prize_per_builder - 200.0) / 300.0 * 4.0
            attractiveness_score = 13.0 + bonus

        elif prize_per_builder >= 50.0:
            # Average event (between 9.0 and 13.0 points)
            bonus = (prize_per_builder - 50.0) / 150.0 * 4.0
            attractiveness_score = 9.0 + bonus

        else:
            # Too crowded for the prize amount (low score)
            ratio_fraction = prize_per_builder / 50.0
            attractiveness_score = max(4.0, ratio_fraction * 8.0)

        # ------------------------------------------------------------------- #
        # Step 4: Estimate win probabilities (clearly labeled as estimates)   #
        # ------------------------------------------------------------------- #
        # Probability of placing in top 3: scales down as competitors grow
        baseline_win_chance = 18.0 / (serious_competitors ** 0.55)
        prob_placing = min(max(baseline_win_chance, 0.05), 0.45)

        # Probability of winning ANY prize (including sponsor bounties and side tracks)
        prob_any_reward = min(max(prob_placing * 1.85, 0.10), 0.75)

        return (
            round(attractiveness_score, 1),
            serious_competitors,
            round(prize_per_builder, 2),
            round(prob_placing, 3),
            round(prob_any_reward, 3)
        )

    def calculate_hack_score(
        self,
        prize_usd: float,
        expected_competitors: int,
        skill_fit_score: float,
        sponsor_predictability: float = 85.0,
        ecosystem_momentum: float = 85.0,
        num_tracks_and_bounties: int = 5,
        has_participation_rewards: bool = True,
        is_accelerator_or_vc_backed: bool = True,
        cutting_edge_learning_value: float = 90.0
    ) -> Dict[str, Any]:
        """
        Computes the complete HackScore out of 100 by adding all 9 criteria.
        """

        # ------------------------------------------------------------------- #
        # Factor 1: Reward Quality (Max: 20 points)                           #
        # ------------------------------------------------------------------- #
        if prize_usd >= 1_000_000:
            reward_quality = 20.0
        elif prize_usd >= 500_000:
            reward_quality = 18.5
        elif prize_usd >= 100_000:
            reward_quality = 16.5
        elif prize_usd >= 50_000:
            reward_quality = 14.5
        elif prize_usd >= 20_000:
            reward_quality = 12.5
        else:
            reward_quality = max(6.0, (prize_usd / 20_000.0) * 11.0)

        # ------------------------------------------------------------------- #
        # Factor 2: Competition Attractiveness (Max: 20 points)               #
        # ------------------------------------------------------------------- #
        (
            comp_score,
            serious_competitors,
            prize_per_builder,
            prob_placing,
            prob_any_reward
        ) = self.calculate_competition_attractiveness(prize_usd, expected_competitors)

        # ------------------------------------------------------------------- #
        # Factor 3: Skill Fit (Max: 15 points)                                #
        # ------------------------------------------------------------------- #
        skill_fit = (skill_fit_score / 100.0) * 15.0

        # ------------------------------------------------------------------- #
        # Factor 4: Sponsor Predictability (Max: 10 points)                   #
        # ------------------------------------------------------------------- #
        sponsor_score = (sponsor_predictability / 100.0) * 10.0

        # ------------------------------------------------------------------- #
        # Factor 5: Ecosystem Momentum (Max: 10 points)                       #
        # ------------------------------------------------------------------- #
        momentum_score = (ecosystem_momentum / 100.0) * 10.0

        # ------------------------------------------------------------------- #
        # Factor 6: Prize Breadth & Bounty Tracks (Max: 10 points)            #
        # ------------------------------------------------------------------- #
        # More tracks mean more chances to win side bounties!
        prize_breadth = min(max(num_tracks_and_bounties * 2.0, 4.0), 10.0)

        # ------------------------------------------------------------------- #
        # Factor 7: Participation Rewards (Max: 5 points)                     #
        # ------------------------------------------------------------------- #
        participation_score = 5.0 if has_participation_rewards else 1.5

        # ------------------------------------------------------------------- #
        # Factor 8: Startup & Accelerator Potential (Max: 5 points)           #
        # ------------------------------------------------------------------- #
        startup_score = 5.0 if is_accelerator_or_vc_backed else 2.5

        # ------------------------------------------------------------------- #
        # Factor 9: Resume & Portfolio Learning Value (Max: 5 points)         #
        # ------------------------------------------------------------------- #
        learning_score = (cutting_edge_learning_value / 100.0) * 5.0

        # ------------------------------------------------------------------- #
        # Scale every factor to match HACKSCORE_WEIGHTS from config.py        #
        # ------------------------------------------------------------------- #
        # Each factor above is calculated on its default max (shown in the
        # comments), so if someone edits HACKSCORE_WEIGHTS in config.py to
        # rebalance how much a factor matters, that change actually takes
        # effect here instead of being silently ignored.
        default_max_points = {
            "reward_quality": 20.0,
            "competition_attractiveness": 20.0,
            "skill_fit": 15.0,
            "sponsor_history": 10.0,
            "ecosystem_momentum": 10.0,
            "prize_breadth": 10.0,
            "participation_rewards": 5.0,
            "startup_potential": 5.0,
            "portfolio_value": 5.0
        }

        def scaled(factor_name: str, raw_points: float) -> float:
            configured_max = HACKSCORE_WEIGHTS.get(factor_name, default_max_points[factor_name])
            return raw_points * (configured_max / default_max_points[factor_name])

        reward_quality = scaled("reward_quality", reward_quality)
        comp_score = scaled("competition_attractiveness", comp_score)
        skill_fit = scaled("skill_fit", skill_fit)
        sponsor_score = scaled("sponsor_history", sponsor_score)
        momentum_score = scaled("ecosystem_momentum", momentum_score)
        prize_breadth = scaled("prize_breadth", prize_breadth)
        participation_score = scaled("participation_rewards", participation_score)
        startup_score = scaled("startup_potential", startup_score)
        learning_score = scaled("portfolio_value", learning_score)

        # ------------------------------------------------------------------- #
        # Final Total: Sum all 9 factors (Clamped between 0.0 and 100.0)      #
        # ------------------------------------------------------------------- #
        total_hack_score = (
            reward_quality +
            comp_score +
            skill_fit +
            sponsor_score +
            momentum_score +
            prize_breadth +
            participation_score +
            startup_score +
            learning_score
        )

        final_score = min(max(round(total_hack_score, 1), 0.0), 100.0)

        return {
            "hack_score": final_score,
            "serious_competitors_est": serious_competitors,
            "prize_to_competitor_ratio_est": prize_per_builder,
            "prob_placing_est": prob_placing,
            "prob_any_reward_est": prob_any_reward,
            "breakdown": {
                "reward_quality": round(reward_quality, 1),
                "competition_attractiveness": round(comp_score, 1),
                "skill_fit": round(skill_fit, 1),
                "sponsor_history": round(sponsor_score, 1),
                "ecosystem_momentum": round(momentum_score, 1),
                "prize_breadth": round(prize_breadth, 1),
                "participation_rewards": round(participation_score, 1),
                "startup_potential": round(startup_score, 1),
                "portfolio_value": round(learning_score, 1)
            }
        }
