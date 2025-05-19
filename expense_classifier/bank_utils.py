
class Bank:
    def __init__(self, code, name, upi_regex_pattern=None):
        self.code = code
        self.name = name
        self.upi_regex_pattern = upi_regex_pattern


bank_codes: dict[str: Bank] = {
    "BOB": Bank(
        code="BOB",
        name="Bank Of Baroda",
        upi_regex_pattern=r"^(?P<fixed>.{1,30})(?:/(?P<upi_id>[\w.-]+(?:@[\w.-]+)?))?(?:/(?P<payee>[\w\s\S]*))?$"
    ),
    "PNB": Bank(
        code="PNB",
        name="Punjab National Bank",
        upi_regex_pattern=
        r"^(?P<fixed>.{1,21})(?:/(?:\w+\s+)?(?P<upi_id>[\w.-]+(?:@[\w.-]+)?))?(?:/(?P<payee>[\w\s\S]*))?$"
    )
}




