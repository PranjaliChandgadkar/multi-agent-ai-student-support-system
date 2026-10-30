# Visa knowledge sources

Add UTF-8 JSON files here, one source per file, with string fields `id`, `title`, `url`, `reviewed` (ISO review date), and `text`. IDs must contain only letters, numbers, underscores and hyphens. URLs must use HTTP(S). Restart the backend after changes.

This directory now bundles two reviewed US State Department summaries for international students preparing F-1 applications. See `docs/USA_SOURCE_REGISTER.md` for coverage, review notes and gaps. Use current official guidance for additional topics. Include jurisdiction, eligibility conditions, exceptions and effective dates in source text. Do not store personal student information here. Tests use temporary synthetic sources that are never installed into this directory.

Retrieval is lexical, with character chunks and overlap. Citations identify retrieved excerpts, not independent verification that every generated statement is entailed. Source freshness and completeness require human review.
