"""Small direct-API speed harness derived from the archived streaming client.

Requires an already running user-selected server. Does not start/stop models or
change any server configuration. Prompts must be supplied by the person running it.
Generated prose is not saved. Authentication, if needed, comes from BENCH_AUTH.
"""
import argparse,json,os,pathlib,statistics,time,urllib.request

def request(base,model,prompt,seed):
    body={'model':model,'messages':[{'role':'user','content':prompt}],
          'temperature':0.2,'top_p':0.95,'top_k':40,'min_p':0,
          'reasoning_effort':'high','seed':seed,'max_tokens':512,
          'cache_prompt':False,'stream':True,'stream_options':{'include_usage':True}}
    headers={'Content-Type':'application/json'}
    auth=os.environ.get('BENCH_AUTH')
    if auth:headers['Authorization']='Bearer '+auth
    req=urllib.request.Request(base.rstrip('/')+'/v1/chat/completions',data=json.dumps(body).encode(),headers=headers)
    start=time.monotonic();first=None;timing={};usage={};complete=False;finish=None
    with urllib.request.urlopen(req,timeout=600) as stream:
        for line in stream:
            if not line.startswith(b'data: '):continue
            payload=line[6:].strip()
            if payload==b'[DONE]':complete=True;break
            obj=json.loads(payload)
            if obj.get('error'):raise RuntimeError('Server reported an error')
            timing=obj.get('timings',timing);usage=obj.get('usage',usage)
            for c in obj.get('choices',[]):
                d=c.get('delta',{})
                if first is None and any(d.get(k) for k in ['content','reasoning_content','tool_calls']):first=time.monotonic()-start
                finish=c.get('finish_reason') or finish
    result={'seed':seed,'complete':complete,'finish_reason':finish,'TTFT_s':first,'wall_s':time.monotonic()-start,'timings':timing,'usage':usage,'generated_prose':'[omitted]'}
    if not complete:raise RuntimeError('Stream ended without DONE')
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--base-url',required=True);p.add_argument('--model',required=True)
    p.add_argument('--prompt-file',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True)
    args=p.parse_args();prompt=args.prompt_file.read_text();rows=[]
    for seed in [31415,31416,31417]:
        row=request(args.base_url,args.model,prompt,seed)
        if row['timings'].get('cache_n',0)!=0:raise RuntimeError('Cold request reused KV')
        rows.append(row);args.output.write_text(json.dumps(rows,indent=2)+'\n')
    values=[r['timings']['predicted_per_second'] for r in rows]
    print(json.dumps({'output_tps_median':statistics.median(values),'range':[min(values),max(values)],'repetitions':len(rows)}))
if __name__=='__main__':main()
