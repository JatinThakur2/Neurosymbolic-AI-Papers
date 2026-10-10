You are checking whether the AUTHORS of published research papers have publicly released code, models or data for the paper. This is for a systematic review's reproducibility indicator.

INPUT: {BATCH} (JSON lines with rid, title, venue, year, url, github, stratum). There are {N} records.

For EACH record:
1. Use WebSearch (and WebFetch when needed) to find an author-released artifact: a public code repository (GitHub, GitLab, Hugging Face, Bitbucket), a released model or dataset, or a project page linking to code. Good queries: "<title> github", "<title> code", the arXiv page of the paper (arXiv abstract pages often link code), the OpenReview or ACL Anthology page, Papers with Code.
2. Count it as RELEASED only if the artifact is by the paper's authors (or their lab/organisation) and is clearly for this paper. A link already in the `github` field counts if it is the authors' repo for this paper — verify it quickly.
3. NOT released: no artifact found after a reasonable search (about 2–4 searches); only a "coming soon" / empty repository; only third-party reimplementations; only an artifact for a different paper.
4. Do not spend more than about 4 tool calls on one record.

OUTPUT: write {OUT} with Python's csv module, header exactly:
rid,released,artifact_type,url,note
- released: yes | no | unclear
- artifact_type: code | data | model | code+data | none (semicolon-combine if needed)
- url: the artifact URL (empty if none)
- note: at most 15 words (e.g. "repo empty", "linked from arXiv abstract", "found via Papers with Code").
One row per record, all {N}, in input order.

FINAL REPLY: counts of yes/no/unclear and any record you are unsure about (rid + one line). Do not paste the table.
