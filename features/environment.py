"""Behave environment configuration."""


def before_all(context):
    """Run before all tests."""
    pass


def before_scenario(context, scenario):
    """Run before each scenario."""
    context.order_service = None
    context.order = None
    context.promotions = {}


def after_scenario(context, scenario):
    """Run after each scenario."""
    pass
