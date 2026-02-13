# Contact Info Checker

Detect contact information (email, phone, social media) in text.

## Installation

```bash
pip install -e .
```

Or just copy `contact_detector.py` into your project.

## Usage

```python
from contact_detector import check, detect_contact_info

# Simple boolean check
has_contact = check("Email me at test@example.com")  # True
has_contact = check("10 years Python experience")    # False

# Detailed detection
result = detect_contact_info("Call 0917-123-4567 or email test@email.com")
result.has_contact_info  # True
result.details           # {'emails': ['test@email.com'], 'phones': ['0917-123-4567'], 'social': []}
```

## What It Detects

- **Emails**: Standard email format
- **Phone Numbers**: Philippine formats (mobile, landline, +63)
- **Social Media**: @handles, LinkedIn, GitHub, Twitter/X, Instagram, Facebook, Telegram, WhatsApp

## API

### `check(text: str) -> bool`
Simple boolean check for any contact info.

### `detect_contact_info(text: str) -> DetectionResult`
Returns `DetectionResult` with:
- `has_contact_info`: bool
- `details`: dict with `emails`, `phones`, `social` lists

### `contains_contact_info(text: str) -> bool`
Alias for `check()`.

## License

MIT
