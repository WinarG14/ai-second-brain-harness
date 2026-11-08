# Provenance convention

Each knowledge file says where its content came from, so that a later session can check it.

1. Frontmatter `source` is mandatory: a URL, a repository path, or `user statement YYYY-MM-DD`.
2. `valid_from` is the date when the content was true or was checked.
3. `review_by` is the date after which the digest lists the file for a check.
4. In an answer, cite the file path and its `source`. Give `status` and `valid_from` when the
   file is a draft, superseded, or older than its `review_by` date.
5. If no source exists, say so. Do not invent a source.
6. A memory or a log entry is recall, not proof. Confirm a fact against its source before
   the user acts on it.
