# Scripts

- `analyze_results.py`: read-only offline archive inventory; no network/model calls.
- `benchmark_client.py`: compact streaming API speed client derived from the measured harness. Requires an already running server, a user-supplied base URL/model/prompt file and optional BENCH_AUTH environment value. It does not manage services or store generated prose. The archived study used its original frozen fixture files and system nonce; this compact client is not falsely presented as a byte-identical reproduction of every historical request.
- `generate_coding_fixtures.py`: original synthetic six-project/test generator, with source digest in `original-generator-provenance.json`.
- `freeze_prompt_inputs_reference.py`: historical prompt sizing/retrieval generator. Home references are scrubbed. It requires local tokenizer/corpus assets and the original fixture context, not redistributed here. Do not run it expecting a self-contained benchmark installation.
- `prepare_archive.py` / `build_documents.py`: deterministic export/write-up helpers for the owner’s retained artifacts; source files are read-only.
- `followups.py`: read-only GitHub collection and local reply drafts. It contains no posting path.
- `manage_followups.py`: manages only this publication’s marked user cron entry, preserving unrelated entries.

No server configuration, production service launcher, stored authentication material, model weights or browser/session data is distributed. Use the original source hashes and per-request metrics to understand historical measurements; generated fixtures must not be mislabeled as the original frozen inputs.
