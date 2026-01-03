import re
import ipaddress
from urllib.parse import urlparse

# Common URL shorteners
URL_SHORTENERS = [
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly"
]

# Common scam keywords
SCAM_KEYWORDS = [
    "free", "urgent", "verify", "claim", "reward",
    "win", "prize", "limited", "offer"
]

def is_ip_address(url):
    try:
        ipaddress.ip_address(url)
        return True
    except:
        return False


def analyze_qr_data(data: str):
    risk_score = 0
    reasons = []

    # Check if data is a URL
    parsed = urlparse(data)
    is_url = parsed.scheme in ["http", "https"]

    if is_url:
        domain = parsed.netloc.lower()

        # URL shortener check
        for short in URL_SHORTENERS:
            if short in domain:
                risk_score += 3
                reasons.append("Uses URL shortener")
                break

        # IP address URL check
        if is_ip_address(domain.split(":")[0]):
            risk_score += 3
            reasons.append("Uses IP address instead of domain")

        # HTTPS check
        if parsed.scheme != "https":
            risk_score += 1
            reasons.append("Not using HTTPS")

    # Scam keyword check
    lower_data = data.lower()
    for word in SCAM_KEYWORDS:
        if word in lower_data:
            risk_score += 1
            reasons.append(f"Contains keyword: {word}")

    # Final verdict
    if risk_score >= 4:
        verdict = "SCAM"
    elif risk_score >= 2:
        verdict = "SUSPICIOUS"
    else:
        verdict = "SAFE"

    return verdict, reasons
