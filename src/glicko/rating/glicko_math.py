from dataclasses import dataclass
import math
from typing import List, Tuple


@dataclass(frozen=True)
class GlickoConstants:
    TAU: float = 0.2  # System constant, controls rating volatility update
    EPSILON: float = 1e-6  # Convergence tolerance
    MAX_ITERATIONS: int = 100  # Prevent infinite loops


class GlickoMath:
    """Static utility class for Glicko-2 mathematical functions."""

    @staticmethod
    def calculate_g(phi: float) -> float:
        """Calculate the g(phi) function.

        Args:
            phi (float): average rating deviation of the team

        Returns:
            float: g(phi) value
        """
        return 1 / math.sqrt(1 + 3 * phi**2 / math.pi**2)

    @staticmethod
    def calculate_E(g_phi: float, mu: float, mu_j: float) -> float:
        """Calculate the expected outcome between 2 teams by
        using the g(phi) function and the rating of the teams.
        We use team 1 as the reference team here. mu refers to the
        average rating of team 1 and mu_j refers to the average rating of team 2.

        Args:
            g_phi (float): g(phi) value
            mu (float): average team rating of team 1
            mu_j (float): average team rating of team 2

        Returns:
            float: Expected outcome between the two teams. The
            scale is between 0 and 1.
        """
        return 1 / (1 + math.exp(-g_phi * (mu - mu_j)))

    @staticmethod
    def calculate_v(g: float, E: float) -> float:
        """Calculate the ancillary variance annotation v.

        Args:
            g (float): g(phi) value
            E (float): Expected outcome

        Returns:
            float: ancillary variance
        """
        return 1 / (g**2 * E * (1 - E))

    @staticmethod
    def calculate_delta(v: float, g: float, outcome: int, E: float) -> float:
        """Calculate the delta which is a measure of the
        difference between the expected outcome and the actual
        outcome of the match scaled by the ancillary variance and g(phi).

        Args:
            v (float): ancillary variance
            g (float): g(phi) value
            outcome (int): simulated outcome of the match. 1 if team 1 wins, 0 if team 2 wins
            E (float): Expected outcome

        Returns:
            float: delta value
        """
        outcome_minus_expected = outcome - E

        delta = v * g * outcome_minus_expected

        return delta

    @staticmethod
    def calculate_new_volatility(
        sigma: float,
        phi: float,
        delta: float,
        v: float,
        tau: float = GlickoConstants.TAU,
    ) -> float:
        """Calculate new volatility using iteration method.

        Args:
            sigma: Current volatility
            phi: Rating deviation
            delta: Rating change factor
            v: Estimated variance
            tau: System constant (default: 0.2)

        Returns:
            float: New volatility value
        """
        if any(x < 0 for x in [sigma, phi, v, tau]):
            raise ValueError("Input parameters must be non-negative")

        def optimization_function(x: float) -> float:
            """Helper function for iteration."""
            exp_x = math.exp(x)
            denominator = 2 * (phi**2 + v + exp_x) ** 2

            return (exp_x * (delta**2 - phi**2 - v - exp_x)) / denominator - (
                x - math.log(sigma**2)
            ) / tau**2

        def find_bounds() -> tuple[float, float]:
            """Determine iteration bounds."""
            a = math.log(sigma**2)

            if delta**2 > phi**2 + v:
                b = math.log(delta**2 - phi**2 - v)
            else:
                k = 1
                while optimization_function(a - k * tau) < 0:
                    k += 1
                    if k > GlickoConstants.MAX_ITERATIONS:
                        raise RuntimeError("Failed to converge on bounds")
                b = a - k * tau

            return a, b

        # Illinois algorithm implementation
        a, b = find_bounds()
        iterations = 0

        while abs(b - a) > GlickoConstants.EPSILON:
            c = a + (a - b) * optimization_function(a) / (
                optimization_function(b) - optimization_function(a)
            )

            if optimization_function(c) * optimization_function(b) < 0:
                a = b
            else:
                a = a - (b - a) * optimization_function(a) / (
                    optimization_function(b) - optimization_function(a)
                )
            b = c

            iterations += 1
            if iterations > GlickoConstants.MAX_ITERATIONS:
                raise RuntimeError("Failed to converge on solution")

        return math.exp(a / 2)

    @staticmethod
    def calculate_phi_star(phi: float, sigma: float) -> float:
        """Calculate the value phi star, which is an intermediate
        value used in the calculation of the new rating deviation.

        Args:
            phi (float): average rating deviation of the team
            sigma (float): volatility of the team

        Returns:
            float: phi star value
        """
        return math.sqrt(phi**2 + sigma**2)

    @staticmethod
    def calculate_new_phi(phi_star: float, v: float) -> float:
        """Calculate the new rating deviation based on the
        intermediate value phi star and the ancillary variance v

        Args:
            phi_star (float): intermediate value
            v (float): ancillary variance

        Returns:
            float: new rating deviation
        """
        new_phi = 1 / math.sqrt(1 / phi_star**2 + 1 / v)
        return new_phi

    @staticmethod
    def calculate_new_mu(
        mu: float, new_sigma: float, g_phi: float, outcome: int, expected_outcome: float
    ) -> float:
        """Calculate the new average rating of the team based on the
        current average rating, the new volatility, g(phi) value, the
        outcome of the match, and the expected outcome.

        Args:
            mu (float): current average rating of the team
            new_sigma (float): new volatility
            g_phi (float): g(phi) value
            outcome (int): simulated outcome of the match. 1 if team 1 wins, 0 if team 2 wins
            expected_outcome (float): Expected outcome

        Returns:
            float: new average rating
        """
        mu = mu + new_sigma**2 * g_phi * (outcome - expected_outcome)
        return mu
