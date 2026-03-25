"""Tests for the Indicator entity."""

from domain.entities.indicator import Indicator


class TestIndicator:
    """Tests T-D-16, T-D-17 from test plan"""

    def test_value_in_range_returns_true(self):
        """T-D-16: Valid value within indicator range"""
        indicator = Indicator(
            id="ind-1",
            name="mood",
            unit="/10",
            min_value=1.0,
            max_value=10.0,
        )
        assert indicator.is_value_in_range(5.0) is True

    def test_value_above_range_returns_false(self):
        """T-D-17: Value above max is rejected"""
        indicator = Indicator(
            id="ind-1",
            name="mood",
            unit="/10",
            min_value=1.0,
            max_value=10.0,
        )
        assert indicator.is_value_in_range(15.0) is False

    def test_value_below_range_returns_false(self):
        """Value below min is rejected"""
        indicator = Indicator(
            id="ind-1",
            name="mood",
            unit="/10",
            min_value=1.0,
            max_value=10.0,
        )
        assert indicator.is_value_in_range(0.0) is False

    def test_value_at_min_boundary(self):
        """Edge case: value exactly at min is valid"""
        indicator = Indicator(
            id="ind-1",
            name="mood",
            unit="/10",
            min_value=1.0,
            max_value=10.0,
        )
        assert indicator.is_value_in_range(1.0) is True

    def test_value_at_max_boundary(self):
        """Edge case: value exactly at max is valid"""
        indicator = Indicator(
            id="ind-1",
            name="mood",
            unit="/10",
            min_value=1.0,
            max_value=10.0,
        )
        assert indicator.is_value_in_range(10.0) is True
