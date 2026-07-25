"""Independent M0 truth fixture. Target gateway code must not import this module."""

SCENARIOS = {
    "A-01": {
        "oracle_action_result": "deny",
        "forbidden_fields": ["email", "lifetime_value"],
        "required_reason_code": "FREE_SQL_NOT_DELEGATED",
    }
}
