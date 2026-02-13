"""
Contact Information Detector

Detects presence of contact information in text:
- Email addresses
- Phone numbers (various formats)
- Social media handles/URLs
"""

import re
from typing import NamedTuple


class DetectionResult(NamedTuple):
    """Result of contact detection."""
    has_contact_info: bool
    details: dict  # Optional: what was found (for debugging)


# Email pattern
EMAIL_PATTERN = re.compile(
    r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    re.IGNORECASE
)

# Phone patterns (Philippine formats)
PHONE_PATTERNS = [
    # PH Mobile with country code: +63 917 123 4567, +639171234567
    re.compile(r'\+63[-.\s]?9\d{2}[-.\s]?\d{3}[-.\s]?\d{4}'),
    # PH Mobile: 0917-123-4567, 09171234567, 0917 123 4567
    re.compile(r'\b09\d{2}[-.\s]?\d{3}[-.\s]?\d{4}\b'),
    # PH Landline with country code: +63 2 8123 4567 (Metro Manila)
    re.compile(r'\+63[-.\s]?2[-.\s]?\d{4}[-.\s]?\d{4}'),
    # PH Landline with country code: +63 XX XXX XXXX (Provincial)
    re.compile(r'\+63[-.\s]?\d{2}[-.\s]?\d{3}[-.\s]?\d{4}'),
    # PH Landline: (02) 8123-4567, 02-8123-4567 (Metro Manila 8-digit)
    re.compile(r'\(?\b02\)?[-.\s]?\d{4}[-.\s]?\d{4}\b'),
    # PH Landline: (044) 123-4567 (Provincial 7-digit)
    re.compile(r'\(?\b0\d{2}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'),
    # Raw 11-digit starting with 09 (mobile)
    re.compile(r'\b09\d{9}\b'),
    # Raw 10-12 digit sequences (fallback)
    re.compile(r'\b\d{10,12}\b'),
]

# Social media patterns
SOCIAL_PATTERNS = [
    # Twitter/X handle
    re.compile(r'(?:^|[\s(])@[a-zA-Z_][a-zA-Z0-9_]{0,14}\b'),
    # LinkedIn URL
    re.compile(r'linkedin\.com/in/[a-zA-Z0-9_-]+', re.IGNORECASE),
    # GitHub URL
    re.compile(r'github\.com/[a-zA-Z0-9_-]+', re.IGNORECASE),
    # Twitter/X URL
    re.compile(r'(?:twitter|x)\.com/[a-zA-Z0-9_]+', re.IGNORECASE),
    # Instagram URL or handle
    re.compile(r'instagram\.com/[a-zA-Z0-9_.]+', re.IGNORECASE),
    # Facebook URL
    re.compile(r'facebook\.com/[a-zA-Z0-9.]+', re.IGNORECASE),
    # Generic social URL patterns
    re.compile(r'(?:t\.me|telegram\.me)/[a-zA-Z0-9_]+', re.IGNORECASE),
    # WhatsApp
    re.compile(r'wa\.me/\d+', re.IGNORECASE),
]


def contains_contact_info(text: str) -> bool:
    """
    Check if text contains any contact information.
    
    Args:
        text: The text to analyze (can be description, work experience, etc.)
        
    Returns:
        True if contact info detected, False otherwise.
    """
    if not text:
        return False
    
    # Check email
    if EMAIL_PATTERN.search(text):
        return True
    
    # Check phone numbers
    for pattern in PHONE_PATTERNS:
        if pattern.search(text):
            return True
    
    # Check social media
    for pattern in SOCIAL_PATTERNS:
        if pattern.search(text):
            return True
    
    return False


def detect_contact_info(text: str) -> DetectionResult:
    """
    Detect contact information with details about what was found.
    
    Args:
        text: The text to analyze.
        
    Returns:
        DetectionResult with boolean and details dict.
    """
    if not text:
        return DetectionResult(has_contact_info=False, details={})
    
    found = {
        'emails': [],
        'phones': [],
        'social': [],
    }
    
    # Find emails
    found['emails'] = EMAIL_PATTERN.findall(text)
    
    # Find phones
    for pattern in PHONE_PATTERNS:
        matches = pattern.findall(text)
        found['phones'].extend(matches)
    found['phones'] = list(set(found['phones']))  # dedupe
    
    # Find social
    for pattern in SOCIAL_PATTERNS:
        matches = pattern.findall(text)
        found['social'].extend(matches)
    found['social'] = list(set(found['social']))  # dedupe
    
    has_contact = bool(found['emails'] or found['phones'] or found['social'])
    
    return DetectionResult(has_contact_info=has_contact, details=found)


# Simple API
def check(text: str) -> bool:
    """Simple boolean check for contact info."""
    return contains_contact_info(text)


def check_file(file_path: str) -> bool:
    """
    Check if a text file contains contact information.
    
    Args:
        file_path: Path to .txt file
        
    Returns:
        True if contact info detected, False otherwise.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return contains_contact_info(text)


def detect_from_file(file_path: str) -> DetectionResult:
    """
    Detect contact info from a text file with details.
    
    Args:
        file_path: Path to .txt file
        
    Returns:
        DetectionResult with boolean and details dict.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return detect_contact_info(text)


if __name__ == '__main__':
    # Test cases
    test_cases = [
        "I worked at Google for 5 years as a software engineer.",
        "Contact me at john.doe@email.com for more details.",
        "Call me at 0917-123-4567 to discuss.",
        "Find me on LinkedIn: linkedin.com/in/johndoe",
        "Follow @johndoe on Twitter for updates.",
        "My number is +63 917 123 4567",
        "Reach out via telegram: t.me/johndoe",
        "10 years experience in Python, JavaScript, and cloud infrastructure.",
        "Landline: (02) 8123-4567",
        "Text me at 09171234567",
        "Office: +63 2 8888 1234",
    ]
    
    print("Contact Info Detection Test\n" + "=" * 40)
    for text in test_cases:
        result = detect_contact_info(text)
        status = "✓ FOUND" if result.has_contact_info else "✗ clean"
        print(f"\n{status}: {text[:50]}...")
        if result.has_contact_info:
            print(f"  Details: {result.details}")
