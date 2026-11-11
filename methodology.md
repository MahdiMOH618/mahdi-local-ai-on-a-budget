# Methodology and interpretation

## Later128K Qwen/Bolt and drafter studies

Context capacity is131072, not a promise of131072 input tokens. Templates, tokenizers and output headroom change actual input counts. Frozen public/synthetic text is identical across relevant models; rendered token counts differ. The full external corpus and all raw outputs are not redistributed. Exact frozen source-file hashes identify retained local fixtures.

Temperature0.2, top-p0.95, top-k40, min-p0, high thinking; frozen seeds31415/31416/31417 for repeated speed cases. Speed outputs allow512 tokens including thinking. Qwen has 3 repetitions at each of1K/32K/64K/120K. Bolt-U has 3 at 1K/32K and1 at64K/120K. Bolt-N gets one1K qualification timing and one quality repetition, not a complete speed sweep. Nondeterminism and first-use kernel costs remain possible.

Cold requests reuse zero KV tokens; OS file/driver/shader caches are not flushed. Cached follow-ups are a separate measurement and actual reused counts are retained. Decode t/s excludes prefill; input t/s measures new prompt work. Local first streamed token can be reasoning, not visible final text, and is not remote desktop/UI latency.512-token speed samples may end before a final answer.

The historical Qwen baseline already used MTP requested spec2 plus lookup; it is not a no-drafter control. Effective verifier windows can differ. MTP2/3/4 keeps pipeline/lookup behavior and reports accepted/offered guesses including lookup. Bolt uses llama.cpp/F16 KV without MTP, while Qwen uses Strata/INT8 KV. Configuration comparisons must not be recast as architecture-only causal experiments.

Reasoning has10 cases×3, coding6×3, tools10×3 and injection4×3 for the full candidate. Final JSON checks are on those same tool cases, not10 additional prompts. Bolt-N has one repetition of reasoning/coding/retrieval/tools+JSON. For the matching single retrieval haystack, Qwen raw facts10/15 become15/15 after removing only trailing punctuation/whitespace; Bolt-U15/15 and Bolt-N5/5 are unchanged. Across all three original Qwen haystacks, raw40/45 becomes45/45. Original scores remain preserved. Retrieval multi-hop counts are separate.

The coding sandbox permits only its frozen import allowlist. Bolt-U17/18 includes a rejected heapq import: an execution-contract exception, not demonstrated faulty priority-queue logic. Benign16/16 or46/48 completion does not imply factual correctness or safety. A whole completed benchmark retains wrong answers and truncations; those are not filtered away to make the archive look better.

## Older studies

The27B Vulkan/SYCL short tests commonly used greedy temperature0 and seed42, disabled thinking only for those requests and mixed capped timing with separate completed-answer checks. Their performance rows are not the later1K fixed512-token protocol.

The eight-model vision cohort used41 controlled synthetic phantom/report cases (39QA plus capacity/tool),16K context,4096 total output tokens, temperature0.2/top-p0.95/top-k20/min-p0/seed42. Native thinking policy is primary. A single budget-rescue retry is reported separately for unfinished/unparseable outputs; complete wrong answers were not resampled. These are not clinical images or clinical validation. Reused cumulative summaries are not independent repeated trials.

The controlled64K Q2/Q3/Q4 study used approximately25990-token cold prefixes with short outputs and small8-case quality checks, not the later1K/32K512-output plan. Quantization and abliteration both change. A documented interleaved unrelated engine request invalidates the third Q2 cache-pair comparison: all raw benchmark metrics are retained, but only two clean warm pairs are used for that comparison. No unrelated prompt content is published.

Context sweeps vary the configured capacity and have one near-full sample per context. Above-declared-context operation is only capacity/speed evidence. Resource peaks are sampled, not instrumented allocation maxima; cgroup RAM can include file cache. GPU-resident experts do not mean that SSD-backed PLE or mapped embeddings reside on the GPUs.

## Public release policy

Only successful, completed experimental configurations are released in this edition. Incomplete/owner-cancelled experiments are not evidence of success. All task-score failures inside included complete runs remain counted. Raw generated prose, messages, reasoning and image payloads are conservatively replaced with [omitted]; this also prevents distributing harmful/offensive generations. Only numerical evidence, controlled case labels and selected short factual summaries are included. Source artifacts are read-only; each transformed export has original/public SHA256 in source-manifest.json.
