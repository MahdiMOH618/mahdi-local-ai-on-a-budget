"""Read-only GitHub follow-ups. Never creates posts, replies or other mutations."""
from pathlib import Path
from datetime import datetime,timedelta,timezone
from zoneinfo import ZoneInfo
import argparse,fcntl,json,os,shutil,subprocess,urllib.parse
ROOT=Path(__file__).resolve().parents[1]
STATE=ROOT/'followup-state.json'
TZ=ZoneInfo('Asia/Kuwait')
def gh_get(endpoint,extra=None):
    gh=shutil.which('gh') or str(Path.home()/'.local/bin/gh')
    env=dict(os.environ);env['GH_PROMPT_DISABLED']='1'
    env.setdefault('XDG_RUNTIME_DIR',str(Path('/run/user')/str(os.getuid())))
    env.setdefault('DBUS_SESSION_BUS_ADDRESS','unix:path='+env['XDG_RUNTIME_DIR']+'/bus')
    # Explicit GET is an invariant: this program has no posting path.
    args=[gh,'api','--method','GET',endpoint,'--paginate','--slurp']
    if extra:args+=extra
    p=subprocess.run(args,capture_output=True,text=True,env=env,timeout=120)
    if p.returncode:raise RuntimeError('GitHub read failed; check gh auth status in a terminal')
    return json.loads(p.stdout)
def pages(values):
    for page in values:
        for value in page:yield value
def suggestion(item,repo_url):
    body=(item.get('title','')+' '+item.get('body','')).lower()
    if any(x in body for x in ['lilicorr','draft-dflash','vulkan']):
        return 'Thanks for the question. In my three cold 1K runs, Bolt-U on Vulkan went from 8.78 t/s without a drafter to 12.04 with LiLiCorr N5, with 62.7% acceptance. The N5 range was 8.80–12.95, so I would not generalize that 37% median gain to longer inputs or overall quality. The saved measurements are here: '+repo_url+'/tree/main/results/lilicorr-vulkan'
    if any(x in body for x in ['spec','mtp','drafter']):
        return 'My requested spec2 setting was best observed at 59.1/51.1 t/s for 1K/32K, versus 58.3/50.6 for spec3 and 56.9/48.7 for spec4. Each used three cold runs; the ranges overlap and lookup remained enabled, so this is a small configuration-specific finding rather than a universal optimum. Details: '+repo_url+'/tree/main/results/qwen-mtp-windows'
    if any(x in body for x in ['vram','memory','ram','fit','125b']):
        return 'The current machine has two 24GB B60s, an i7-7700K and 64GB RAM. The later Qwen baseline sampled about 21.38/21.69 GiB VRAM. Strata reported routed experts resident across both GPUs, but PLE stayed SSD-backed and token embeddings host-mapped; I am not claiming every model-file byte is in VRAM. Hardware and limits: '+repo_url+'/blob/main/hardware.md'
    if any(x in body for x in ['quality','json','score','accuracy','medical']):
        return 'These are small local tests, not a broad intelligence or clinical-accuracy claim. Wrong answers and budget truncations remain in the scores of completed runs, JSON checks overlap the tool cases, and some comparisons use a single repetition. The exact scope and grading are here: '+repo_url+'/blob/main/methodology.md'
    return 'Thanks for the question. I have not verified that specific point from the retained measurements, so I do not want to guess or turn this small test into a broader claim. The reproducible scope, versions and limitations are here: '+repo_url+'/blob/main/methodology.md'
def collect(state):
    repo=state['repository'];since=state['last_checked'];q=urllib.parse.urlencode({'state':'all','since':since,'per_page':100})
    items=[]
    for a in pages(gh_get('repos/'+repo+'/issues?'+q)):
        items.append({'kind':'pull request' if 'pull_request' in a else 'issue','id':a['id'],'number':a['number'],'updated':a['updated_at'],'title':a['title'],'body':a.get('body') or '', 'author':a['user']['login'],'url':a['html_url']})
    for a in pages(gh_get('repos/'+repo+'/issues/comments?'+urllib.parse.urlencode({'since':since,'per_page':100}))):
        items.append({'kind':'comment','id':a['id'],'updated':a['updated_at'],'title':'Repository discussion/comment','body':a['body'],'author':a['user']['login'],'url':a['html_url']})
    for a in pages(gh_get('repos/'+repo+'/stargazers?per_page=100',['-H','Accept: application/vnd.github.star+json'])):
        if a['starred_at']>since:items.append({'kind':'star','id':a['user']['id'],'updated':a['starred_at'],'title':'New star','body':'','author':a['user']['login'],'url':a['user']['html_url']})
    seen=set(state.get('seen',[]));out=[]
    for a in items:
        identity=str(a['kind'])+':'+str(a['id'])+':'+a['updated']
        if identity not in seen:out.append(a);seen.add(identity)
    return sorted(out,key=lambda a:a['updated']),sorted(seen)
def render(items,repo,now):
    lines=['# Benchmark follow-up — '+now.strftime('%Y-%m-%d'),'',f'{len(items)} new or updated items since the last check. Nothing was posted automatically.','']
    drafts=[]
    for i,a in enumerate(items,1):
        lines += [f"## {i}. {a['kind']}: {a['title']}",'',f"From **{a['author']}** — {a['url']}",'']
        if a['kind']=='star':lines += ['New star; no reply needed.',''];continue
        body=a['body'].replace('\r','')[:6000]
        lines += ['What they wrote:','',*['> '+s for s in body.splitlines()],'','Suggested reply:','']
        reply=suggestion(a,'https://github.com/'+repo);lines += [reply,'']
        drafts.append({'number':i,'url':a['url'],'kind':a['kind'],'reply':reply})
    if not items:lines+=['No new activity found.','']
    lines+=['These are drafts only. Tell the assistant “send” or “send 1 and 3” after reviewing the file; it should post exactly the selected drafts through gh, with your edits if supplied.','']
    return '\n'.join(lines),drafts
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--force',action='store_true');p.add_argument('--fixture',type=Path);args=p.parse_args()
    if args.fixture:
        x=json.loads(args.fixture.read_text());text,drafts=render(x['items'],x['repository'],datetime.now(TZ));print(text);print(json.dumps(drafts));return
    if not STATE.is_file():raise SystemExit('Publication/follow-up state is not initialized')
    root=ROOT/'followups';root.mkdir(exist_ok=True)
    with (root/'.lock').open('w') as lock:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:return
        state=json.loads(STATE.read_text());now=datetime.now(TZ)
        if state.get('paused'):return
        due=datetime.fromisoformat(state['next_due'])
        if not args.force and now<due:return
        items,seen=collect(state);text,drafts=render(items,state['repository'],now)
        name=now.strftime('%Y-%m-%d');(root/(name+'.md')).write_text(text);(root/(name+'-drafts.json')).write_text(json.dumps(drafts,indent=2)+'\n')
        state.update(last_checked=datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),next_due=(now+timedelta(days=3)).replace(hour=20,minute=0,second=0,microsecond=0).isoformat(),seen=seen)
        STATE.write_text(json.dumps(state,indent=2)+'\n')
        if items and shutil.which('notify-send'):
            env=dict(os.environ);env.setdefault('DBUS_SESSION_BUS_ADDRESS','unix:path=/run/user/'+str(os.getuid())+'/bus')
            subprocess.run(['notify-send','Benchmark follow-up',f'{len(items)} new items — see followups/{name}.md'],env=env,check=False)
if __name__=='__main__':main()
