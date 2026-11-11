"""Offline archive summary. No network, model generation, or configuration access."""
from pathlib import Path
import json
def main():
    root=Path(__file__).resolve().parents[1]
    manifest=json.loads((root/'source-manifest.json').read_text())
    topics=sorted({Path(v['public_file']).parts[1] for v in manifest})
    missing=[v['public_file'] for v in manifest if not (root/v['public_file']).is_file()]
    if missing:raise SystemExit('Missing exported evidence: '+str(missing))
    print(json.dumps({'topics':topics,'provenance_linked_exports':len(manifest),'missing':missing},indent=2))
if __name__=='__main__':main()
