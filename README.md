# Documentation claim audit

This offline tool compares documentation statements about payment-number well-formedness with static Python evidence. It never executes inspected code or accesses the network.

## Usage

```sh
credit-card-validation-claim-audit audit . --verbose
credit-card-validation-claim-audit audit . --json --ignore vendor --fail-on medium
python3 -m credit_card_validation_claim_audit --version
```

The default threshold is high; medium includes evidence found only in tests. Exit status is 0 for a pass, 2 when a finding meets the threshold, and 1 for an input or usage error. Root README and Markdown under docs are inspected; fenced blocks are skipped, but inline code counts. Source under fixtures, examples, and docs is excluded. Test files are reported separately. Symlinks are skipped.

## Differentiation

This family concerns well-formed payment numbers and recognised brands. It does not cover generic input checks, payment processing, extraction of payment details, account authentication, password verification, password hashing, password generation, PDF encryption, email sending, SMS sending, document extraction, barcode decoding, email address checks, phone number checks, password strength, JSON Schema, date checks, JSON decoding, regular expressions, URL parsing or fetching, domain checks, URL checks, or IP address checks.

Other separate families cover spreadsheet reading and generation, word-document reading and generation, presentation reading and generation, PDF extraction, generation, merging, splitting, rotation, form-filling, watermarking, redaction, compression and annotation, table extraction, OCR, e-signatures, screen recording, video generation, QR and barcode generation and scanning, audio mixing, generation and editing, source separation, speech recognition, text-to-speech, noise suppression, and music generation and transcription.

## Limitations

Matching is static and exact, not semantic. Paraphrases are missed. A denial outside the listed forms may be mistaken for a positive statement. Dead code counts. Unresolved alias chains are missed. Each route must be in one module. Only Python source is read. Runtime-only imports and plugins are invisible. A claim outside the root README and docs is invisible.

A construction alone does not count. A network-name property read alone does not count. A regex match alone does not count. A prefix test alone does not count. An import alone does not count. A subprocess invocation does not count. Generic input checks alone do not count. Email checks alone do not count. Phone checks alone do not count. Payment processing alone does not count. Extraction alone does not count. A locally defined route name is shadowed. A locally defined generic name is shadowed. Generic aliases beyond one import are missed.

The paired construction and property read count even in code that never runs. Generating or appending a checksum digit counts even though it does not judge a complete number. A brand-specific call counts regardless of its input. A module alias held in a variable may be missed. A roadmap statement is still treated as a claim. A changelog statement is still treated as a claim. A TODO statement is still treated as a claim.

```text
validate card
```

A remote policy lookup can mean this instead of local code. This may be a false positive; review it manually.

```text
check card
```

A manual runbook step can mean this. This may be a false positive; review it manually.

```text
card validation
```

A roadmap entry can mean this. This may be a false positive; review it manually.

```text
card validator
```

A hosted page can mean this. This may be a false positive; review it manually.

```text
valid card
```

Reader advice can mean this. This may be a false positive; review it manually.

```text
card is valid
```

A successful lookup can mean this. This may be a false positive; review it manually.

```text
card check
```

An expiry lookup can mean this. This may be a false positive; review it manually.

```text
card checker
```

A network identification service can mean this. This may be a false positive; review it manually.

```text
card number check
```

A documented pattern without code can mean this. This may be a false positive; review it manually.

```text
verify card
```

Ownership verification can mean this. This may be a false positive; review it manually.

```text
detect invalid card
```

A length-only rule can mean this. This may be a false positive; review it manually.

```text
card well formed
```

A theoretical discussion can mean this. This may be a false positive; review it manually.

```text
is valid card
```

A statement about generated data can mean this. This may be a false positive; review it manually.

```text
card validity
```

A specification section can mean this. This may be a false positive; review it manually.

```text
luhn check
```

An algorithm design discussion can mean this. This may be a false positive; review it manually.
