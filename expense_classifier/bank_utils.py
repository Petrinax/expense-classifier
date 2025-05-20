import re
from typing import List, Optional


class Bank:
    def __init__(self, code, name, upi_regex_pattern, old_patterns=None):
        self.code: str = code
        self.name: str = name
        self.upi_regex_pattern: re.Pattern = upi_regex_pattern
        self.old_patterns: Optional[List[str]] = old_patterns if old_patterns else []

bank_codes: dict[str: Bank] = {
    "BOB": Bank(
        code="BOB",
        name="Bank Of Baroda",
        # V2 now extracts upi ref no as well.
        upi_regex_pattern=re.compile(r"^(?P<mode>\w+)(?:/(?P<upi_ref_no>\d{12}))?(?:/(?P<created_at>\d{2}:\d{2}:\d{2}))?(?:/(?P<sub_mode>\w+))?(?:/(?P<upi_id>[\w.-]+@[a-zA-Z]+))?(?:/(?P<payee>[\w\s\S]*))?$", re.IGNORECASE),
        old_patterns=[
            r"^upi/(?P<upi_ref_no>\d{12})/(?P<created_at>\d{2}:\d{2}:\d{2})/upi/(?P<upi_id>[\w.-]+@[a-zA-Z]+)(?:/(?P<payee>[\w\s\S]*))?$",
            r"^(?P<fixed>.{1,30})(?:/(?P<upi_id>[\w.-]+(?:@[\w.-]+)?))?(?:/(?P<payee>[\w\s\S]*))?$"
        ]
    ),
    "PNB": Bank(
        code="PNB",
        name="Punjab National Bank",
        upi_regex_pattern=re.compile(r"^(?P<mode>\w+)(?:/(?P<upi_ref_no>\d{12}))?(?:/(?P<sub_mode>\w+))?(?:/(?P<upi_id>[\w.-]+(?:@[\w.-]+)?))?(?:/(?P<payee>[\w\s\S]*))?$", re.IGNORECASE),
        old_patterns=[
            r"^(?P<fixed>.{1,21})(?:/(?:\w+\s+)?(?P<upi_id>[\w.-]+(?:@[\w.-]+)?))?(?:/(?P<payee>[\w\s\S]*))?$"
        ]
    ),
    "SBI": Bank(
            code="SBI",
            name="State Bank Of India",
            upi_regex_pattern=re.compile(r"^[\s\w]*-(?P<mode>UPI)/(?P<sub_mode>CR|DR)/(?P<upi_ref_no>\d{12})(?:/(?P<payee>[\w\s\S]+))?(?:/(?P<bank_code>\w+))?(?:/(?P<upi_id>[\w@.-]+))?(?:/(?P<reference>.*))?--[\s]*$", re.IGNORECASE),
        )
}
