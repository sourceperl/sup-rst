import ipaddress
import re


def is_valid_ipv4(address: str) -> bool:
    """Checks if a string is a valid IPv4 address."""
    try:
        ipaddress.IPv4Address(address)
        return True
    except ipaddress.AddressValueError:
        return False


def is_valid_ipv6(address: str) -> bool:
    """Checks if a string is a valid IPv6 address."""
    try:
        ipaddress.IPv6Address(address)
        return True
    except ipaddress.AddressValueError:
        return False


def is_valid_hostname(hostname: str) -> bool:
    """
    Checks if a string conforms to general hostname format rules (RFCs 952, 1123).
    This does not check against actual DNS resolution.

    - Must be between 1 and 255 characters long.
    - Each label (segment separated by dots) must be between 1 and 63 characters long.
    - Labels can contain ASCII letters (a-z, A-Z), digits (0-9), and hyphens (-).
    - Labels cannot start or end with a hyphen.
    - The top-level domain (TLD) should ideally not be all digits (though this is not strictly enforced by all systems).
    """
    if not hostname or len(hostname) > 255:
        return False

    # Regex for a single label
    # ^[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$
    # Starts with alphanumeric, followed by 0-61 alphanumeric or hyphen,
    # ends with alphanumeric. Max 63 characters.
    label_pattern = re.compile(r"^[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$")

    labels = hostname.split('.')
    for label in labels:
        if not label_pattern.match(label) or len(label) > 63:
            return False

    # Optional: Check if the last label (TLD) is all digits.
    # While technically allowed by some systems, it's often an indicator of an IP address.
    # We're allowing it here for flexibility since the main function
    # will check for IP addresses separately.
    # if labels and labels[-1].isdigit():
    #     return False

    return True
