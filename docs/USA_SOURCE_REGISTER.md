# USA visa source register

Reviewed for this project: 30 October 2026. These are manually curated summaries, not live web retrieval or government endorsement.

| Local source ID | Publisher and official page | Coverage |
| --- | --- | --- |
| us-student-application | [Department of State: Student Visa](https://travel.state.gov/content/travel/en/us-visas/study/student-visa.html) | Application sequence and interview preparation |
| us-ds160 | [Department of State: DS-160 FAQ](https://travel.state.gov/content/travel/en/us-visas/visa-information-resources/forms/ds-160-online-nonimmigrant-visa-application/ds-160-faqs.html) | Form preparation and accuracy |

## Pending review — not loaded into RAG

- [DHS: Maintaining Status](https://studyinthestates.dhs.gov/maintaining-status)
- [DHS: Training Opportunities](https://studyinthestates.dhs.gov/training-opportunities-in-the-united-states)
- [USCIS: Students and Employment](https://www.uscis.gov/working-in-the-united-states/students-and-exchange-visitors/students-and-employment)

Direct page retrieval for these sources failed during this implementation. Search snippets and third-party mirrors were not accepted as sufficient for ingestion. No employment or status rules from these pages are bundled.

## Update procedure

1. Open the exact official URL and record the review date separately from any effective date.
2. Read the relevant section, including exceptions and links to current notices. Distinguish proposals from rules in force.
3. Update the JSON summary, preserving its stable ID and URL. Keep each topic self-contained; avoid splitting conditions from their exceptions.
4. Update this register and run tests. Restart FastAPI to reload the files.
5. Check representative questions for accurate retrieval, valid citations and appropriate abstention.

Review before a student-facing release and whenever a source changes. This prototype does not automatically detect changes or enforce expiry of sources.
