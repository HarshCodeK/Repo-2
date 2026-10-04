# Threat Model

- **Prompt injection in documents:** retrieved text is treated as evidence, not as instructions. The model is explicitly told to answer from evidence.
- **Oversized images:** uploaded image bytes are capped at 8 MiB before conversion; the API also bounds the encoded request size.
- **Secret leakage:** API keys are environment variables and are never committed.
- **Unsupported answers:** empty evidence results in an explicit refusal.
- **Provider failure:** HTTP errors propagate to the service boundary rather than silently fabricating an answer.
- **Untrusted uploads:** image validation uses Pillow verification before conversion.
