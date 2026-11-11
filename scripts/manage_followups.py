"""Manage only this publication's user cron entry; does not post to GitHub."""
from pathlib import Path
import argparse,datetime,json,subprocess
ROOT=Path(__file__).resolve().parents[1]
MARKER='MAHDI_BENCHMARK_FOLLOWUPS'
LINE='0 20 * * * /usr/bin/python3 "$HOME/publish-benchmarks/scripts/followups.py" >> "$HOME/publish-benchmarks/followups/cron.log" 2>&1 # '+MARKER
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['install','pause','resume','remove','status']);a=p.parse_args().action
    old=subprocess.run(['crontab','-l'],capture_output=True,text=True);lines=old.stdout.splitlines() if old.returncode==0 else []
    if a=='status':print('\n'.join(s for s in lines if MARKER in s) or 'No benchmark follow-up cron entry');return
    if a=='install':
        tz=subprocess.run(['timedatectl','show','--property=Timezone','--value'],capture_output=True,text=True,check=True).stdout.strip()
        if tz!='Asia/Kuwait':raise SystemExit('Host timezone differs; choose an equivalent Kuwait20:00 cron schedule before installing')
    backup=Path.home()/'.local/state/mahdi-benchmark-publication';backup.mkdir(parents=True,exist_ok=True)
    (backup/('crontab-before-'+datetime.datetime.now().strftime('%Y%m%dT%H%M%S')+'.txt')).write_text(old.stdout)
    lines=[s for s in lines if MARKER not in s]
    if a in ['install','resume']:lines.append(LINE)
    if a=='pause':lines.append('# PAUSED '+LINE)
    subprocess.run(['crontab','-'],input='\n'.join(lines)+'\n',text=True,check=True)
    state=ROOT/'followup-state.json'
    if state.is_file():
        x=json.loads(state.read_text());x['paused']=a in ['pause','remove'];state.write_text(json.dumps(x,indent=2)+'\n')
    print('Benchmark follow-ups: '+a)
if __name__=='__main__':main()
