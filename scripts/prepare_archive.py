"""Build a successful-runs-only, metrics-first archive from read-only originals.

No model is loaded, server contacted, service changed, credential read, or post sent.
Generated responses and input messages are intentionally omitted from exports.
"""
from pathlib import Path
import datetime,hashlib,json,os,re,statistics

ROOT=Path(__file__).resolve().parents[1]
HOME=Path.home()
DOC=HOME/'Documents/ChatGPT/Local AI & Models'
MANIFEST=[]
PRIVATE_EXACT={'service','started_service','finished_service','verification','host','hostname','ip','ip_address','mac','mac_address','port','email','username','serial','serial_number','uuid','request_id','api_response_id','engine_request_id','idempotency_key'}
OMIT_TEXT={'messages','message','response','responses','prompt','prompt_text','content','raw_final','raw_reasoning','reasoning_content','reasoning','answer','parsed_answer','final','raw_response','raw_output','output_text','reason','text','explanation','tool_result','error_detail','manual_failure_examples','parsed','parsed_output','prediction','output','completion','result_text','assistant_text','visible_answer','final_answer','answer_text','thinking_text','raw_text'}
def scrub(text):
    text=str(text).replace(str(HOME),'~').replace(HOME.name,'<user>')
    host=os.uname().nodename
    if host:text=text.replace(host,'<host>')
    text=re.sub(re.escape('/'+'home'+'/')+r'[^/\s"\x27<>]+','~',text)
    text=re.sub(r'[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s"<>]+','<user-profile>',text)
    text=re.sub(r'https?://(?:\d{1,3}\.){3}\d{1,3}(?::\d+)?(?:/[^\s"<>]*)?','<local-endpoint>',text)
    text=re.sub(r'\b\d{1,3}(?:\.\d{1,3}){3}\b','<address>',text)
    text=re.sub(r'\b(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}\b','<device>',text)
    text=re.sub(r'\b[0-9a-fA-F]{8}-(?:[0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}\b','<identifier>',text)
    text=re.sub(r'\b[0-9a-fA-F]{4}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}\.[0-7]\b','<pci-device>',text)
    text=re.sub(r'[A-Za-z0-9.!#$%&\x27*+/=?^_`{|}~-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}','<contact>',text)
    text=re.sub(r'\bgh[pousr]_[A-Za-z0-9_]{20,}\b','[omitted]',text)
    text=re.sub(r'\bgithub_pat_[A-Za-z0-9_]+\b','[omitted]',text)
    text=re.sub(r'\b(?:port|localhost)\s*:?\s*\d{2,5}\b','local endpoint',text,flags=re.I)
    text=re.sub(r'(--port[\s=]+)\d+','\\1<port>',text)
    return text
def clean(value,key=''):
    low=key.lower()
    if low in PRIVATE_EXACT or any(t in low for t in ['password','passwd','credential','api_key','private_key','access_token','auth_token','authorization','serial_number']):return '[omitted]'
    if low in OMIT_TEXT:return '[omitted]'
    if low in ['temperature_sensors_max_c','engine_log_evidence','notes','restoration','final_restoration','rollback','deployment_state','original_q2_configuration','final_verification','supervisor_incident','traffic_interference']:return '[omitted]'
    if isinstance(value,dict):return {scrub(k):clean(v,k) for k,v in value.items()}
    if isinstance(value,list):return [clean(v) for v in value]
    if isinstance(value,str):
        if value.startswith('data:') or len(value)>24000:return '[omitted]'
        return scrub(value)
    return value
def read(path):return json.loads(path.read_text())
def write(topic,name,obj,source=None):
    dest=ROOT/'results'/topic/name;dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(clean(obj),indent=2,ensure_ascii=False)+'\n')
    if source:MANIFEST.append({'public_file':str(dest.relative_to(ROOT)),'source':scrub(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'public_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'transformation':'Identifiers scrubbed; raw generated prose/messages/images omitted; numerical scores retained'})
def export(topic,source,name=None):
    if source.is_file():write(topic,name or source.name,read(source),source)
def metrics(topic,source,name):
    if source.is_file():
        a=read(source)
        write(topic,name,a,source)

# A completed run can include wrong answers and budget truncations; do not remove
# failed quality cases. Only incomplete experimental arms are outside this archive.
P=DOC/'Bionic optimization/2026-10-28'
for name in ['baseline-benchmark.json','tuned-benchmark.json','dflash-benchmark.json','dflash-mmvq-benchmark.json','dflash-mesa26-benchmark.json','suite-results.json','complete-results.json','no-draft-results.json']:
    export('qwen27b-vulkan',P/name)
S=P/'Intel SYCL test'
for name in ['fp16-results.json','fp32-dflash12-results.json','sycl-suite-results.json','sycl-repeat-results.json','sycl-complete-results.json','latest-fp32-results.json','latest-fp32-repeat-results.json','latest-fp32-pmin02-results.json','latest-fp32-pmin02-ub512-results.json','latest-fp32-pmin02-ub1024-results.json','latest-fp32-pmin02-long-results.json','latest-fp32-pmin02-ub512-long-results.json','latest-fp32-pmin02-ub1024-long-results.json','context-sweep-results.json']:
    export('qwen27b-sycl',S/name)
P=DOC/'Ornith benchmark'
for name in ['results.json','qwen-baseline.json'] :export('ornith-single-b60',P/name)
for name in ['dual-gpu-results.json','dual-gpu-sustained.json']:export('ornith-medgemma-concurrent',P/name)
for name in ['results.json','gap-results.json','input-control-results.json','tool-assisted-result.json']:
    export('qwen9b-q4-controls',DOC/'Qwen 3.5 9B replacement'/name)

latest=DOC/'Gemma 4 E4B benchmark/comparison-summary.json'
v=read(latest)
vision={}
for model,m in v['models'].items():
    vision[model]={k:x for k,x in m.items() if isinstance(x,(int,float,bool)) or k in ['decode_range','repeatability']}
write('synthetic-vision-qa','eight-model-summary.json',{'date':'2026-10-30','hardware':'GTX1080Ti CUDA, historical16GiB host RAM era','scope':'41 synthetic cases/model:39QA plus capacity/tool; not clinical validation','primary_vs_rescue':'Primary4096 total-token budget; budget-rescue scores separate','models':vision},latest)
for folder,label,file in [('Qwen3 VL 8B Thinking test','four-model-primary','full-results-normalized.json'),('Ministral 3 8B review benchmark','ministral','results.json'),('MedGemma SFTCTIQA benchmark','medgemma-sftctiqa','results.json'),('Youtu VL 4B benchmark','youtu','results.json'),('Gemma 4 E4B benchmark','gemma4','results.json')]:
    export('synthetic-vision-qa',DOC/folder/file,label+'.json')

P=HOME/'strata-trial'
report=(P/'context-sweep-20261107/COMPLETE-REPORT.txt').read_text()
contexts=[]
for line in report.splitlines():
    cells=[s.strip() for s in line.split('|')]
    if len(cells)==10 and cells[-1]=='passed':contexts.append(dict(zip(['context','variant','short_output_tps','near_full_input','near_full_output_tps','input_seconds','sampled_VRAM_GiB','cgroup_peak_RAM_GiB_including_cache','swap_GiB','status'],cells)))
write('qwen-context-sweep','passed-contexts.json',{'date':'2026-11-07','model':'Qwen3.8-Flash-Next IQ2_XS','runtime':'Strata0.1.56 SYCL, MTPspec2, INT8KV','rows':contexts,'limitations':'512 output tokens; near-full workload one sample/context;264K beyond declared256K; capacity/speed only, not accuracy; short rates2 samples'},P/'context-sweep-20261107/COMPLETE-REPORT.txt')
export('qwen-cache-reuse',P/'cache-reuse-20261108/summary.json')
write('strata-runtime-validation','summary.json',{'date':'2026-11-07','model':'Qwen3.8-Flash-Next IQ2_XS','runtime':'Strata0.1.56 SYCL','successful_requests':23,'fresh_starts':4,'correct_tool_roundtrips':3,'gcd_assertions_passed':3,'output_tps':{'gcd':56.7,'capped_prose':47.3,'streaming_explanation':52.1,'completed_high_thinking':63.6},'prefill_examples_tps':[1124.1,802.2],'experts':'100% resident across2B60s; PLE SSD-backed and token embeddings host-mapped','scope':'Short runtime validation, not broad quality/stability'},P/'dual-runtime-fix-20261107/REPORT.txt')
write('hardware-checks','passed-stress.json',{'date':'2026-11-07','CPU':'4AVX2/FMA plus4memory workers; no arithmetic mismatch','RAM':'32GiB checked with16 patterns in about94seconds; zero mismatches; not all64GiB certified','GPU_workload':'Both checked2048-square FP16GEMM/FP32output for90seconds','GPU_effective_TFLOPS':[28.52,26.89],'CPU_peak_C':78,'GPU_peak_C':[52,51],'BAR_per_card_GiB':32,'VRAM_prior_checked':'44GiB total,22per card; not every physical byte tested','limitation':'Custom matrix workload; not theoretical peak or model tokens/s'},P/'system-check-20261107/REPORT.txt')

qsource=P/'uncensored-q3-q4-20261108/final-benchmark-data.json';q=read(qsource)
qmodels={k:v for k,v in q['models'].items() if k!='Q2'}
write('qwen-q2-q3-q4','completed-64k-arms.json',{'date':'2026-11-08–09','context':65536,'models':qmodels,'method':'Same64K protocol; short outputs and approximately26K cold prefix, not the later512-token1K32K protocol','confounds':'Original Q2 vs patched Q3/Q4 changes both quantization and abliteration; Q3/Q4 GPU-read pinned host expert mirrors, not CPU expert computation','interference_note':'Q2 clean warm subset has2 pairs; all original3 pairs retained in metrics; one interleaved non-benchmark request invalidates the third cache comparison'},qsource)
write('qwen-q2-q3-q4','model-identities.json',{'prepared_models':q['prepared_models'],'baseline_weight_verification':q['baseline_weight_verification'],'backend':q['backend'],'weight_sizes':q['weight_sizes']},qsource)

B=HOME/'bench-bolt';aggregate=read(B/'comparison-data.json')
for name,folder in [('Qwen','Qwen-historical'),('Bolt-U','Bolt-U'),('Bolt-N','Bolt-N')]:
    topic='qwen-huihui-128k' if name=='Qwen' else 'bolt'
    export(topic,B/'results'/folder/'requests.json',name+'-requests.json')
    export(topic,B/'results'/folder/'scores.json',name+'-scores.json')
    write(topic,name+'-summary.json',{k:v for k,v in aggregate['models'][name].items() if k!='failures'},B/'comparison-data.json')
for label in ['Bolt-U','Bolt-N']:
    export('bolt',B/'provenance'/('download-verified-'+label+'.json'),label+'-identity.json')
export('bolt',B/'provenance/llama-commit.json')
P=HOME/'strata-trial/mtp-spec-comparison-20261111'
export('qwen-mtp-windows',P/'summary.json')
for spec in ['spec2','spec3','spec4']:
    for stage in ['speed','json']:
        d=P/'results'/spec/stage
        for name in ['requests.json','scores.json','summary.json']:export('qwen-mtp-windows',d/name,spec+'-'+stage+'-'+name)
V=B/'lilicorr/vulkan'
for tag in ['Bolt-U-Nnone','Bolt-U-N5']:
    for name in ['requests.json','scores.json']:export('lilicorr-vulkan',V/'results'/tag/name,tag+'-'+name)
export('lilicorr-vulkan',V/'provenance/final-review.json')
export('lilicorr-vulkan',V/'provenance/original-build.json')
export('lilicorr-vulkan',V/'provenance/download-verified.json','drafter-identity.json')
write('lilicorr-vulkan','successful-smoke.json',{'passed':True,'questions':3,'all_correct_clean_thinking_separated':True,'full_target_GPU_layers':'89/89','full_draft_GPU_layers':'6/6','step0_N':6,'block_size':8,'attention':'enabled','heavy_CPU_graph_operations':0,'scope':'No broader quality or32K suite'},V/'provenance/step0-proof.json')

(ROOT/'source-manifest.json').write_text(json.dumps(MANIFEST,indent=2,ensure_ascii=False)+'\n')
print('Exported',len(MANIFEST),'provenance-linked sanitized files; no original modified.')
