# Mahdi Local AI on a Budget — from Kuwait 🇰🇼

**Dual Intel Arc Pro B60 + a 2017 i7-7700K: real local LLM benchmarks**

I'm testing what this older desktop can do with local models. This archive contains successful, completed experiment configurations only. A successful benchmark run can still produce wrong model answers: those scores are kept. It is not a complete log of every experiment I attempted.

The current machine has two 24GB Arc Pro B60s, an i7-7700K and 64GB DDR4. Earlier tests used one B60, a GTX1080Ti and 16GB host RAM. Those results are labeled separately; they are not a controlled comparison of the current machine.

## Results at a glance

The 1K/32K/64K/120K columns refer to the later fixed512-output-token speed plan at 131072 context. A dash means not measured under that plan. Older short/capped/vision workloads stay in the separate column. Rates include generated thinking. Input values are prefill throughput, not decode.

| Model / quant / mode | Hardware era | Runtime / backend | 1K output t/s | 32K | 64K | 120K | Other decode workload (t/s) | Input t/s (same size order unless marked) | VRAM/card GiB | Quality / scope |
|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3.8-Flash-Next Huihui IQ2_XS + Q6_K projections | 2×B60 | Strata SYCL+MTP/lookup | 59.2 | 51.1 | 51.1 | 52.8 | — | 663.3 / 1009.3 / 988.0 / 971.1 | 21.38 / 21.69 | reason 30/30; tools 30/30; JSON 30/30; code 18/18 |
| Nemotron Bolt-U74B-A9B AD-IQ2_XS (uncensored) | 2×B60 | llama.cpp SYCL | 28.7 | 26.7 | 24.8 | 22.1 | — | 207.6 / 233.6 / 230.2 / 224.1 | 13.60 / 17.09 | reason 30/30; tools 28/30; JSON 26/30; code 17/18 |
| Nemotron Bolt-N74B-A9B official24GB | 2×B60 | llama.cpp SYCL | 17.0† | — | — | — | — | 166.4† | 11.09 / 13.02 | reason 10/10; tools 9/10; JSON 9/10; code 6/6 |
| Same Huihui Qwen, requested spec2 | 2×B60 | Strata SYCL+MTP/lookup | 59.1 | 51.1 | — | — | — | — | 21.37 / 21.68 | tools10/10; JSON10/10 |
| Same Huihui Qwen, requested spec3 | 2×B60 | Strata SYCL+MTP/lookup | 58.3 | 50.6 | — | — | — | — | 21.38 / 21.70 | not retested |
| Same Huihui Qwen, requested spec4 | 2×B60 | Strata SYCL+MTP/lookup | 56.9 | 48.7 | — | — | — | — | 21.40 / 21.71 | not retested |
| Bolt-U, no draft | 2×B60 | llama.cpp Vulkan | 8.78 | — | — | — | — | 222.5 | 13.10 / 16.58 | N6 qualification3/3; no broad N5 quality suite |
| Bolt-U, LiLiCorr N5 | 2×B60 | llama.cpp Vulkan | 12.04 | — | — | — | — | 206.7 | 14.29 / 17.83 | N6 qualification3/3; no broad N5 quality suite |
| Qwen Q2-64K (64K capacity) | 2×B60 | Strata SYCL+MTP | — | — | — | — | 64.3 at26K input, short output | 1034.5 at26K | 21.44 / 21.75 | quality8/8; strict tools8/10; retrieval3/3 |
| Qwen huihui-UD-Q3_K_XL (64K capacity) | 2×B60 | Strata SYCL+MTP | — | — | — | — | 47.8 at26K input, short output | 208.4 at26K | 22.76 / 21.60 | quality8/8; strict tools10/10; retrieval3/3 |
| Qwen huihui-UD-Q4_K_XL (64K capacity) | 2×B60 | Strata SYCL+MTP | — | — | — | — | 31.3 at26K input, short output | 105.5 at26K | 22.77 / 22.14 | quality8/8; strict tools10/10; retrieval3/3 |
| Qwen3.8-27B Q4_K_M + DFlash2 Q4 | 1×B60,16GiB host era | Bionic Vulkan b11908 | — | — | — | — | 47.13 complete coding | — | — | One completed syntax-checked coding answer; one wrong greedy math answer |
| Same27B target/draft, tuned FP32 | 1×B60,16GiB host era | llama.cpp c3df4b7 SYCL | — | — | — | — | 106.80 complete coding | 201.68 at10K marker input | — | Synthetic10K marker correct; narrow coding check |
| Ornith1.5-35B-A3B Q4_K_M | 1×B60,16GiB host era | llama.cpp c3df4b7 SYCL | — | — | — | — | 77.61 complete thinking coding | 517.07 at9,775-token prompt | 20.87 post-test, not peak | Binary search545/545 cases; one correct tool selection |
| Ornith Q4 / MedGemma1.5-4B Q8 | B60 + GTX1080Ti | SYCL / CUDA12.8 | — | — | — | — | 78.73 /57.73 concurrent means | — | — | Synthetic color/spatial smoke; short concurrency only |
| qwen3vl-8b-thinking-q5 | GTX1080Ti,16GiB host era | llama.cpp b11908 CUDA12.8 | — | — | — | — | 42.28 synthetic QA median | — | — | status24/39; numeric12/27; parseable35/39 |
| qwen35-9b-q4 | GTX1080Ti,16GiB host era | llama.cpp b11908 CUDA12.8 | — | — | — | — | 45.21 synthetic QA median | — | — | status24/39; numeric14/27; parseable31/39 |
| medgemma15-4b-q8 | GTX1080Ti,16GiB host era | llama.cpp b11908 CUDA12.8 | — | — | — | — | 55.23 synthetic QA median | — | — | status13/39; numeric9/27; parseable36/39 |
| internvl35-8b-q4 | GTX1080Ti,16GiB host era | llama.cpp b11908 CUDA12.8 | — | — | — | — | 51.02 synthetic QA median | — | — | status22/39; numeric1/27; parseable39/39 |
| ministral3-8b-instruct-q4 | GTX1080Ti,16GiB host era | llama.cpp b11908 CUDA12.8 | — | — | — | — | 46.36 synthetic QA median | — | — | status8/39; numeric14/27; parseable30/39 |
| medgemma-4b-it-sftctiqa-q8 | GTX1080Ti,16GiB host era | llama.cpp b11908 CUDA12.8 | — | — | — | — | 54.76 synthetic QA median | — | — | status9/39; numeric0/27; parseable39/39 |
| youtu-vl-4b-instruct-q8 | GTX1080Ti,16GiB host era | llama.cpp b11908 CUDA12.8 | — | — | — | — | 42.39 synthetic QA median | — | — | status13/39; numeric13/27; parseable39/39 |
| gemma4-e4b-it-q4 | GTX1080Ti,16GiB host era | llama.cpp b11908 CUDA12.8 | — | — | — | — | 58.45 synthetic QA median | — | — | status22/39; numeric10/27; parseable39/39 |

† Bolt-N 1K was one qualification timing, not a three-run speed median; it did not receive the full speed suite. Bolt-U1K/32K have3 repetitions;64K/120K one each. Qwen historical speeds have3 at every size.

The one strict Bolt-U coding exception was a frozen-sandbox rejection of `heapq`, not proof of an incorrect algorithm. JSON scores share the strict-tool cases; they are not another independent dataset. Three-run MTP speed ranges overlap. Complete per-request timings and scores are in [results](results/) and [the source manifest](source-manifest.json).

## What I found

- My Huihui-adapted Qwen3.8-Flash-Next IQ2_XS configuration produced about 51–59 decode t/s over the1K–120K plan on the two B60s. Strata reported its routed experts resident across the GPUs. PLE remained SSD-backed and token embeddings host-mapped: this does **not** mean every file byte fits in VRAM.
- Requested MTP `--spec 2` was best observed:59.1/51.1 t/s at 1K/32K versus58.3/50.6 for3 and56.9/48.7 for4. The geometric-mean lead was only1.2% over3 and4.4% over4; three repeats and overlapping ranges do not prove a universal optimum. Lookup drafting remained enabled, and requested/effective windows differ.
- Bolt-U on SYCL produced 28.7/26.7/24.8/22.1 t/s at 1K/32K/64K/120K. Qwen was 1.9–2.4× faster in these working configurations. Reasoning and normalized retrieval tied; Qwen followed the final JSON contract more consistently. Engines, cache formats and drafting differ.
- LiLiCorr N5 on Vulkan raised Bolt-U1K decode from 8.78 to 12.04 t/s, a 37% median improvement with 62.7% draft acceptance. The three N5 runs ranged 8.80–12.95. This is only 20% of the historical Qwen1K speed; no32K or broad quality inference follows.
- The earlier Qwen27B single-B60 tests showed a large backend/configuration effect. The same completed coding workload reached47.13 t/s on the tuned Vulkan configuration and106.80 on a later SYCL configuration; this was not the later1K fixed-output test.
- The controlled64K Q2/Q3/Q4 comparison favored Q2 speed. The three median short-output cold rates at about 26K input were 64.3,47.8 and31.3 t/s. Q3/Q4 also changed abliteration and used pinned host expert data read by the GPUs, so this is not a precision-only comparison.
- Qwen context-capacity runs completed at 8K–192K without stage trimming and 256K/264K with stage trimming. Near-full decode varied 48.0–59.6 t/s.264K exceeds the GGUF-declared256K context: that checks capacity/speed, not reliable long-context reasoning.
- A synthetic sequential API cache test confirmed reuse after enabling bounded prompt checkpoints. Reuse in the client application was not established.
- On the older B60+1080Ti setup, simultaneous Ornith and MedGemma short workloads averaged78.73 and57.73 decode t/s. These are separate user workloads, not one user receiving their sum.
- The eight-model vision comparison exposed confident errors on controlled synthetic alignment and numeric tasks. Higher decode speed, successful image ingestion and larger quantization are not evidence of medical accuracy. No patient data is published.

## Timeline of included work

- **2026-10-28 — bionic-vulkan:** Memory/context, Mesa/MMVQ and drafting; short coding/prose/math.
- **2026-10-28–29 — qwen27b-sycl:** Runtime, draft length/p-min, ubatch, marker/context tests.
- **2026-10-29 — ornith-single:** Coding, tools, short speed and10K input.
- **2026-10-29 — ornith-medgemma-concurrent:** Alone/concurrent text and synthetic-image generation.
- **2026-10-30 — qwen9b-q4-controls:** Batch/FA, synthetic alignment controls and tool-assisted checks.
- **2026-10-30 — synthetic-vision-qa:** Frozen41 synthetic phantom QA/capacity/tool cases per model.
- **2026-11-07 — hardware-stress-startup:** Successful CPU/RAM/GPU stress only.
- **2026-11-07 — dual-runtime-fix:** Dense-slab device-detection fix, restart/tools/SSE validation.
- **2026-11-07 — qwen-context-sweep:** 8K–264K capacity, near-full prefill/decode; trimmed stage weights.
- **2026-11-08 — qwen-cache-reuse:** Prompt-cache0 vs3, sequential synthetic prefix reuse.
- **2026-11-08–09 — qwen-q2-q3-q4:** 64K speed/quality/coding/retrieval; host expert pinning.
- **2026-11-10 — qwen-huihui-128k:** 1K32K64K120K512-output speed and frozen quality3reps.
- **2026-11-11 — qwen-mtp-window:** Requested spec2/3/4;1K32K3 cold reps;fastest JSON/tools.
- **2026-11-11 — bolt:** 128K context, speed and quality.
- **2026-11-11 — lilicorr-vulkan:** Step0N6;1K none vsN5,3 cold reps512output.

## Limitations

These are small, local tests rather than a standard leaderboard. Some results have one repetition; some intentionally hit the output budget. Historical sampling varies by study, and the small vision tests used a different top-k and output allowance. Some older runs paged on a16GB host, so their latency is not directly comparable with the later64GB setup.

Qwen and Bolt-U both passed12/12 of the small injection cases. Those cases did not separate them and do not certify prompt-injection resistance. The reasoning suite also saturates. Benign completion scores are not correctness or helpfulness scores. Uncensored/abliterated variants were used; raw generated prose and image/message payloads are omitted from this public metrics-first release.

Only completed configurations are included at the owner’s request; do not read the omission of other experiments as evidence that every tested configuration worked. Reused baselines and cumulative vision reports are counted once. [Inventory](inventory.md), [methodology](methodology.md), [hardware](hardware.md), [model files and SHA256](results/model-files/). One older MedGemma1.5 Q8 hash was not recoverable from the retained final records; that reproducibility gap is explicit.

## Files and reuse

`results/` contains scrubbed scores, request metrics, identities and narrow summaries. `scripts/` contains a direct API client, offline summary tool and original synthetic fixture generators with adaptation notes. No model weights, private chats, browser data, authentication material, service configuration or automatic deployment scripts are included.

Scripts are MIT licensed; the results/data and write-ups are [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), attributed to **Mahdi Local AI on a Budget**. Model weights and upstream software retain their own licenses and are not redistributed.

This is a personal archive from Kuwait, not a hardware/vendor endorsement. Questions and corrections are welcome through this repository’s issues.
