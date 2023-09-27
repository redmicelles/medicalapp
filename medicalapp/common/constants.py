NAME_PATTERN: str = r"^[a-zA-z-]\S+$"
PASSWORD_PATTERN: str = (
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*]).{10,30}$"
)
DOCTOR_PATTERN: str = r"^[a-zA-z-\s]+$"
