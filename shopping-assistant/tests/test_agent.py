import pytest
from app.agent import redeem_discount_code, discount_codes_store

def setup_function():
    """Reset the mock database before each test."""
    discount_codes_store["WELCOME50"]["redeemed_by"] = []
    discount_codes_store["SUMMER20"]["redeemed_by"] = []

def test_successful_redemption():
    """Test that a valid code can be redeemed successfully."""
    response = redeem_discount_code("WELCOME50", "user_123")
    assert "Successfully redeemed" in response
    assert "user_123" in discount_codes_store["WELCOME50"]["redeemed_by"]

def test_invalid_code():
    """Security Boundary: Test that an invalid code is rejected."""
    response = redeem_discount_code("FAKECODE", "user_123")
    assert "Invalid discount code" in response

def test_double_redemption_prevention():
    """Security Boundary (Tampering/Replay): Prevent users from redeeming the same code twice."""
    # First redemption
    redeem_discount_code("WELCOME50", "user_123")

    # Second redemption attempt
    response = redeem_discount_code("WELCOME50", "user_123")
    assert "has already redeemed" in response
    # Ensure it's only in the list once
    assert discount_codes_store["WELCOME50"]["redeemed_by"].count("user_123") == 1

def test_case_insensitivity():
    """Business Logic: Ensure codes are case insensitive."""
    response = redeem_discount_code("welcome50", "user_456")
    assert "Successfully redeemed" in response
    assert "user_456" in discount_codes_store["WELCOME50"]["redeemed_by"]

def test_different_users_same_code():
    """Business Logic: Ensure different users can redeem the same global code."""
    redeem_discount_code("WELCOME50", "user_111")
    response = redeem_discount_code("WELCOME50", "user_222")
    assert "Successfully redeemed" in response
    assert "user_111" in discount_codes_store["WELCOME50"]["redeemed_by"]
    assert "user_222" in discount_codes_store["WELCOME50"]["redeemed_by"]
