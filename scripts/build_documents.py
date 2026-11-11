"""Render the public write-up from the sanitized, completed-run exports."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text())
repo='https://github.com/MahdiMOH618/mahdi-local-ai-on-a-budget'
rows=[]
def row(model,hardware,backend,speeds=None,other='—',inp='—',vram='—',quality='—'):
    speeds=speeds or {};rows.append([model,hardware,backend]+[str(speeds.get(k,'—')) for k in ['1K','32K','64K','120K']]+[other,inp,vram,quality])
for model in ['Qwen','Bolt-U','Bolt-N']:
    topic='qwen-huihui-128k' if model=='Qwen' else 'bolt';m=read(f'results/{topic}/{model}-summary.json')
    speed={str(int(k)//1000)+'K':f"{v['cold']['output_tps']:.1f}" for k,v in m['speed'].items() if v.get('cold')}
    if model=='Bolt-N':speed['1K']='17.0†'
    c=m['categories'];q='; '.join(f"{name} {c[k]['passed']}/{c[k]['total']}" for k,name in [('T4','reason'),('T5','tools'),('JSON','JSON'),('T3','code')])
    vr=m['resource_peaks']['VRAM_GiB'];inp=' / '.join(f"{m['speed'][str(n)]['cold']['input_tps']:.1f}" for n in [1000,32000,64000,120000] if m['speed'].get(str(n),{}).get('cold'))
    label={'Qwen':'Qwen3.8-Flash-Next Huihui IQ2_XS + Q6_K projections','Bolt-U':'Nemotron Bolt-U74B-A9B AD-IQ2_XS (uncensored)','Bolt-N':'Nemotron Bolt-N74B-A9B official24GB'}[model]
    row(label,'2×B60','Strata SYCL+MTP/lookup' if model=='Qwen' else 'llama.cpp SYCL',speed,inp=inp or '166.4†',vram=f"{vr['0']:.2f} / {vr['1']:.2f}",quality=q)
mtp=read('results/qwen-mtp-windows/summary.json')
for label,m in mtp['modes'].items():
    speeds=mtp['controller']['speeds'][label];vr=m['peak_VRAM_GiB']
    row('Same Huihui Qwen, requested '+label,'2×B60','Strata SYCL+MTP/lookup',{'1K':f"{speeds['1K_output_tps_median']:.1f}",'32K':f"{speeds['32K_output_tps_median']:.1f}"},vram=f"{vr['0']:.2f} / {vr['1']:.2f}",quality='tools10/10; JSON10/10' if label=='spec2' else 'not retested')
li=read('results/lilicorr-vulkan/final-review.json')['data']
for tag,m in li.items():
    vr={str(i):v for i,v in enumerate(m['VRAM_GiB'])};row('Bolt-U, '+('no draft' if 'none' in tag else 'LiLiCorr N5'),'2×B60','llama.cpp Vulkan',{'1K':f"{m['output_tps']:.2f}"},inp=f"{m['input_tps']:.1f}",vram=f"{vr['0']:.2f} / {vr['1']:.2f}",quality='N6 qualification3/3; no broad N5 quality suite')
quant=read('results/qwen-q2-q3-q4/completed-64k-arms.json')
for label,m in quant['models'].items():
    s=m['summary'];sc=m['scores'];vr=s['resources']['peak_sampled_gpu_mib']
    row('Qwen '+label+' (64K capacity)','2×B60','Strata SYCL+MTP',other=f"{s['cold']['output_tps']:.1f} at26K input, short output",inp=f"{s['cold']['input_tps']:.1f} at26K",vram=f"{vr['0']/1024:.2f} / {vr['1']/1024:.2f}",quality=f"quality{sc['quality_passes']}/{sc['quality_cases']}; strict tools{sc['tools']['passed']}/10; retrieval3/3")
row('Qwen3.8-27B Q4_K_M + DFlash2 Q4','1×B60,16GiB host era','Bionic Vulkan b11908',other='47.13 complete coding',quality='One completed syntax-checked coding answer; one wrong greedy math answer')
# The 545-case count belongs to the Ornith comparison, not this older short run.
rows[-1][-1]='One completed syntax-checked coding answer; one wrong greedy math answer'
row('Same27B target/draft, tuned FP32','1×B60,16GiB host era','llama.cpp c3df4b7 SYCL',other='106.80 complete coding',inp='201.68 at10K marker input',quality='Synthetic10K marker correct; narrow coding check')
row('Ornith1.5-35B-A3B Q4_K_M','1×B60,16GiB host era','llama.cpp c3df4b7 SYCL',other='77.61 complete thinking coding',inp='517.07 at9,775-token prompt',vram='20.87 post-test, not peak',quality='Binary search545/545 cases; one correct tool selection')
row('Ornith Q4 / MedGemma1.5-4B Q8','B60 + GTX1080Ti','SYCL / CUDA12.8',other='78.73 /57.73 concurrent means',quality='Synthetic color/spatial smoke; short concurrency only')
vision=read('results/synthetic-vision-qa/eight-model-summary.json')['models']
for model,m in vision.items():
    row(model,'GTX1080Ti,16GiB host era','llama.cpp b11908 CUDA12.8',other=f"{m['median_decode_tps']:.2f} synthetic QA median",quality=f"status{m['primary_status_matches']}/39; numeric{m['quant_correct']}/27; parseable{m['parseable']}/39")
header=['Model / quant / mode','Hardware era','Runtime / backend','1K output t/s','32K','64K','120K','Other decode workload (t/s)','Input t/s (same size order unless marked)','VRAM/card GiB','Quality / scope']
lines=['# Mahdi Local AI on a Budget — from Kuwait 🇰🇼','', '**Dual Intel Arc Pro B60 + a 2017 i7-7700K: real local LLM benchmarks**','',
"I'm testing what this older desktop can do with local models. This archive contains successful, completed experiment configurations only. A successful benchmark run can still produce wrong model answers: those scores are kept. It is not a complete log of every experiment I attempted.",'',
'The current machine has two24GB Arc Pro B60s, an i7-7700K and64GB DDR4. Earlier tests used one B60, a GTX1080Ti and16GB host RAM. Those results are labeled separately; they are not a controlled comparison of the current machine.','',
'## Results at a glance','',
'The1K/32K/64K/120K columns refer to the later fixed512-output-token speed plan at131072 context. A dash means not measured under that plan. Older short/capped/vision workloads stay in the separate column. Rates include generated thinking. Input values are prefill throughput, not decode.','',
'| '+' | '.join(header)+' |','|'+'|'.join(['---']*len(header))+'|']
for r in rows:lines.append('| '+' | '.join(r)+' |')
lines += ['',
'† Bolt-N1K was one qualification timing, not a three-run speed median; it did not receive the full speed suite. Bolt-U1K/32K have3 repetitions;64K/120K one each. Qwen historical speeds have3 at every size.','',
'The one strict Bolt-U coding exception was a frozen-sandbox rejection of `heapq`, not proof of an incorrect algorithm. JSON scores share the strict-tool cases; they are not another independent dataset. Three-run MTP speed ranges overlap. Complete per-request timings and scores are in [results](results/) and [the source manifest](source-manifest.json).','',
'## What I found','',
'- My Huihui-adapted Qwen3.8-Flash-Next IQ2_XS configuration produced about51–59 decode t/s over the1K–120K plan on the two B60s. Strata reported its routed experts resident across the GPUs. PLE remained SSD-backed and token embeddings host-mapped: this does **not** mean every file byte fits in VRAM.','- Requested MTP `--spec 2` was best observed:59.1/51.1 t/s at1K/32K versus58.3/50.6 for3 and56.9/48.7 for4. The geometric-mean lead was only1.2% over3 and4.4% over4; three repeats and overlapping ranges do not prove a universal optimum. Lookup drafting remained enabled, and requested/effective windows differ.','- Bolt-U on SYCL produced28.7/26.7/24.8/22.1 t/s at1K/32K/64K/120K. Qwen was1.9–2.4× faster in these working configurations. Reasoning and normalized retrieval tied; Qwen followed the final JSON contract more consistently. Engines, cache formats and drafting differ.','- LiLiCorr N5 on Vulkan raised Bolt-U1K decode from8.78 to12.04 t/s, a37% median improvement with62.7% draft acceptance. The three N5 runs ranged8.80–12.95. This is only20% of the historical Qwen1K speed; no32K or broad quality inference follows.','- The earlier Qwen27B single-B60 tests showed a large backend/configuration effect. The same completed coding workload reached47.13 t/s on the tuned Vulkan configuration and106.80 on a later SYCL configuration; this was not the later1K fixed-output test.','- The controlled64K Q2/Q3/Q4 comparison favored Q2 speed. The three median short-output cold rates at about26K input were64.3,47.8 and31.3 t/s. Q3/Q4 also changed abliteration and used pinned host expert data read by the GPUs, so this is not a precision-only comparison.','- Qwen context-capacity runs completed at8K–192K without stage trimming and256K/264K with stage trimming. Near-full decode varied48.0–59.6 t/s.264K exceeds the GGUF-declared256K context: that checks capacity/speed, not reliable long-context reasoning.','- A synthetic sequential API cache test confirmed reuse after enabling bounded prompt checkpoints. Reuse in the client application was not established.','- On the older B60+1080Ti setup, simultaneous Ornith and MedGemma short workloads averaged78.73 and57.73 decode t/s. These are separate user workloads, not one user receiving their sum.','- The eight-model vision comparison exposed confident errors on controlled synthetic alignment and numeric tasks. Higher decode speed, successful image ingestion and larger quantization are not evidence of medical accuracy. No patient data is published.','',
'## Timeline of included work','']
inv=read('inventory.json')
for g in sorted(inv['groups'],key=lambda x:x['date']):lines.append('- **'+g['date']+' — '+g['topic']+':** '+g['tested']+'.')
lines += ['',
'## Limitations','',
'These are small, local tests rather than a standard leaderboard. Some results have one repetition; some intentionally hit the output budget. Historical sampling varies by study, and the small vision tests used a different top-k and output allowance. Some older runs paged on a16GB host, so their latency is not directly comparable with the later64GB setup.','',
'Qwen and Bolt-U both passed12/12 of the small injection cases. Those cases did not separate them and do not certify prompt-injection resistance. The reasoning suite also saturates. Benign completion scores are not correctness or helpfulness scores. Uncensored/abliterated variants were used; raw generated prose and image/message payloads are omitted from this public metrics-first release.','',
'Only completed configurations are included at the owner’s request; do not read the omission of other experiments as evidence that every tested configuration worked. Reused baselines and cumulative vision reports are counted once. [Inventory](inventory.md), [methodology](methodology.md), [hardware](hardware.md), [model files and SHA256](results/model-files/). One older MedGemma1.5 Q8 hash was not recoverable from the retained final records; that reproducibility gap is explicit.','',
'## Files and reuse','',
'`results/` contains scrubbed scores, request metrics, identities and narrow summaries. `scripts/` contains a direct API client, offline summary tool and original synthetic fixture generators with adaptation notes. No model weights, private chats, browser data, authentication material, service configuration or automatic deployment scripts are included.','',
'Scripts are MIT licensed; the results/data and write-ups are [CC BY4.0](https://creativecommons.org/licenses/by/4.0/), attributed to **Mahdi Local AI on a Budget**. Model weights and upstream software retain their own licenses and are not redistributed.','',
'This is a personal archive from Kuwait, not a hardware/vendor endorsement. Questions and corrections are welcome through this repository’s issues.','']
(R/'README.md').write_text('\n'.join(lines))
(R/'summary-data.json').write_text(json.dumps({'repository':repo,'columns':header,'rows':rows,'scope':'Completed successful run configurations, unfiltered task scores'},indent=2)+'\n')
hardware='''# Hardware and runtime eras

Current workstation: two Intel Arc Pro B60 24GB cards; Intel Core i7-7700K (4 cores/8 threads,2017);64GB DDR4-2400 (4×16GB); ASUS PRIME Z270-A; Ubuntu24.04.5 LTS. The B60s use the xe driver and SYCL/Level Zero. Each card has a32GiB ReBAR window; each CPU PEG link was observed at PCIe3.0 x8. No serials, disk identifiers, hostnames or network addresses are distributed.

The28–31 October studies are a separate hardware era: generally16GiB system RAM and one B60 plus a GTX1080Ti11GB for the second service/vision work. CUDA used the1080Ti; these are not dual-B60 CUDA measurements. Some older tests paged, and their wall times must retain that limitation.

Runtime records: Bionic1.1.9 build6 with Vulkan runtime2.65.1 / llama.cpp b11908; official SYCL b11908 FP32/FP16 and later c3df4b7 source build; CUDA b11908/a4699400e with CUDA12.8; Strata native SYCL0.1.56 at ffa80d73133ea5c548aefe57889a16e8085a938f (Terminal product/version labels differ); Bolt SYCL459ab1cdd3c566168c814b6f50cb1a7e6eb79914; LiLiCorr Vulkan7592b61d3b53ca5b39a25a03508fa1246b78c579. Paired LiLiCorr speed arms use the exact same Vulkan executable.

The short successful hardware check exercised32GiB RAM with16 patterns, simultaneous checked FP16 GEMM on both cards, and previously44GiB of VRAM. It does not certify every byte of64GB system RAM or48GB VRAM,24/7 stability, PSU margins or theoretical peak GPU throughput.
'''
(R/'hardware.md').write_text(hardware)
method='''# Methodology and interpretation

## Later128K Qwen/Bolt and drafter studies

Context capacity is131072, not a promise of131072 input tokens. Templates, tokenizers and output headroom change actual input counts. Frozen public/synthetic text is identical across relevant models; rendered token counts differ. The full external corpus and all raw outputs are not redistributed. Exact frozen source-file hashes identify retained local fixtures.

Temperature0.2, top-p0.95, top-k40, min-p0, high thinking; frozen seeds31415/31416/31417 for repeated speed cases. Speed outputs allow512 tokens including thinking. Qwen has3 repetitions at each of1K/32K/64K/120K. Bolt-U has3 at1K/32K and1 at64K/120K. Bolt-N gets one1K qualification timing and one quality repetition, not a complete speed sweep. Nondeterminism and first-use kernel costs remain possible.

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
'''
(R/'methodology.md').write_text(method)
for p in [R/'README.md',R/'hardware.md',R/'methodology.md']:
    t=p.read_text()
    for a,b in [('two24GB','two 24GB'),('and64GB','and 64GB'),('and16GB','and 16GB'),('The1K','The 1K'),('at131072','at 131072'),('at1K','at 1K'),('at8K','at 8K'),('and256K','and 256K'),('264K exceeds','264K exceeds'),('Only20%','Only 20%'),('about51','about 51'),('produced28','produced 28'),('was1.9','was 1.9'),('from8.78','from 8.78'),('to12.04','to 12.04'),('a37%','a 37%'),('with62.7','with 62.7'),('ranged8.80','ranged 8.80'),('only20%','only 20%'),('at8K','at 8K'),('varied48','varied 48'),('at about26K','at about 26K'),('were64.3','were 64.3'),('at1K','at 1K'),('has3','has 3'),('has one1K','has one 1K'),('Bolt-N1K','Bolt-N 1K'),('CC BY4.0','CC BY 4.0')]:t=t.replace(a,b)
    p.write_text(t)
from copyedit_markdown import format_repository
format_repository(R)
print('Rendered README, methodology, hardware and summary-data.')
if __name__=='__main__':pass
