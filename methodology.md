# Methodology and interpretation

## Later 128K Qwen/Bolt and drafter studies

Context capacity is 131072, not a promise of 131072 input tokens. Templates, tokenizers and output headroom change actual input counts. Frozen public/synthetic text is identical across relevant models; rendered token counts differ. The full external corpus and all raw outputs are not redistributed. Exact frozen source-file hashes identify retained local fixtures.

Temperature 0.2, top-p 0.95, top-k 40, min-p 0, high thinking; frozen seeds 31415/31416/31417 for repeated speed cases. Speed outputs allow 512 tokens including thinking. Qwen has 3 repetitions at each of 1K/32K/64K/120K. Bolt-U has 3 at 1K/32K and 1 at 64K/120K. Bolt-N gets one 1K qualification timing and one quality repetition, not a complete speed sweep. Nondeterminism and first-use kernel costs remain possible.

Cold requests reuse zero KV tokens; OS file/driver/shader caches are not flushed. Cached follow-ups are a separate measurement and actual reused counts are retained. Decode t/s excludes prefill; input t/s measures new prompt work. Local first streamed token can be reasoning, not visible final text, and is not remote desktop/UI latency. 512-token speed samples may end before a final answer.

The historical Qwen baseline already used MTP requested spec 2 plus lookup; it is not a no-drafter control. Effective verifier windows can differ. MTP 2/3/4 keeps pipeline/lookup behavior and reports accepted/offered guesses including lookup. Bolt uses llama.cpp / F16 KV without MTP, while Qwen uses Strata / INT8 KV. Configuration comparisons must not be recast as architecture-only causal experiments.

Reasoning has 10 cases×3, coding 6×3, tools 10×3 and injection 4×3 for the full candidate. Final JSON checks are on those same tool cases, not 10 additional prompts. Bolt-N has one repetition of reasoning/coding/retrieval/tools+JSON. For the matching single retrieval haystack, Qwen raw facts 10/15 become 15/15 after removing only trailing punctuation/whitespace; Bolt-U 15/15 and Bolt-N 5/5 are unchanged. Across all three original Qwen haystacks, raw 40/45 becomes 45/45. Original scores remain preserved. Retrieval multi-hop counts are separate.

The coding sandbox permits only its frozen import allowlist. Bolt-U 17/18 includes a rejected heapq import: an execution-contract exception, not demonstrated faulty priority-queue logic. Benign 16/16 or 46/48 completion does not imply factual correctness or safety. A whole completed benchmark retains wrong answers and truncations; those are not filtered away to make the archive look better.

## Older studies

The 27B Vulkan/SYCL short tests commonly used greedy temperature 0 and seed 42, disabled thinking only for those requests and mixed capped timing with separate completed-answer checks. Their performance rows are not the later 1K fixed 512-token protocol.

The eight-model vision cohort used 41 controlled synthetic phantom/report cases (39 QA plus capacity/tool), 16K context, 4096 total output tokens, temperature 0.2/top-p 0.95/top-k 20/min-p 0/seed 42. Native thinking policy is primary. A single budget-rescue retry is reported separately for unfinished/unparseable outputs; complete wrong answers were not resampled. These are not clinical images or clinical validation. Reused cumulative summaries are not independent repeated trials.

The controlled 64K Q2/Q3/Q4 study used approximately 25990-token cold prefixes with short outputs and small 8-case quality checks, not the later 1K/32K inputs, 512-token output plan. Quantization and abliteration both change. A documented interleaved unrelated engine request invalidates the third Q2 cache-pair comparison: all raw benchmark metrics are retained, but only two clean warm pairs are used for that comparison. No unrelated prompt content is published.

Context sweeps vary the configured capacity and have one near-full sample per context. Above-declared-context operation is only capacity/speed evidence. Resource peaks are sampled, not instrumented allocation maxima; cgroup RAM can include file cache. GPU-resident experts do not mean that SSD-backed PLE or mapped embeddings reside on the GPUs.

## Public release policy

Only successful, completed experimental configurations are released in this edition. Incomplete/owner-cancelled experiments are not evidence of success. All task-score failures inside included complete runs remain counted. Raw generated prose, messages, reasoning and image payloads are conservatively replaced with [omitted]; this also prevents distributing harmful/offensive generations. Only numerical evidence, controlled case labels and selected short factual summaries are included. Source artifacts are read-only; each transformed export has original/public SHA256 in source-manifest.json.
