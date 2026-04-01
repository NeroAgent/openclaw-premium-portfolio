# Verification Code Patterns

The `extract_codes` and `wait-for-code` commands detect codes using these heuristics:

## Code Formats

| Pattern | Example | Typical Use |
|---------|---------|-------------|
| 4-8 digits | `123456` | 2FA, PINs |
| Alphanumeric (6-8) | `ABC1234` | Some services |
| With prefix "code is" | "Your code is: 123456" | Email verifications |
| With "enter" | "Enter 123456" | OTP instructions |
| With "OTP" | "OTP: 123456" | One-time passwords |

## Link Patterns

Looks for URLs containing:
- `verify`
- `confirm`
- `activation`
- `token=`
- `auth`
- `signup`
- `validate`

## Limitations

- May produce false positives (e.g., random 6-digit numbers in invoices)
- May miss codes that are images (OCR not used)
- May miss codes embedded in HTML buttons (we scan body text only)

## Improving Accuracy

If you find missed codes, we can refine regex patterns. Provide examples of the email format.

## Privacy

Code extraction occurs locally; no external API calls. Email content is not stored permanently.

---

For advanced pattern customization, you can modify the regex in `extract_codes.py`.