"""Normalize readable benchmark prose without changing code, paths or measurements."""
from pathlib import Path
import re,subprocess

PLAIN_WORDS='''## In plain words

- On my 2017 i7 PC with two Intel Arc B60 cards, a 125B-class Qwen model ran at about 51–59 output tokens per second.
- The 2-bit-based Qwen configuration was fastest in my Qwen quant comparison. My current Qwen setup scored full marks on the small reasoning, coding, tool and JSON checks.
- Nemotron Bolt-U ran at roughly half Qwen’s speed on the same machine, using different software and cache configurations.
- These are small local tests, not a general model ranking. The tables keep different hardware eras and test settings separate.

'''

def prose(text):
    replacements={
        '1K32K64K120K512-output':'1K/32K/64K/120K inputs, 512-token output',
        '1K32K3 cold reps':'1K/32K inputs, 3 cold reps',
        '1K/32K512-output':'1K/32K inputs, 512-token output',
        'Step0N6':'Step 0 at N6',
        'reps512output':'reps, 512-token output',
        'Bolt-U74B':'Bolt-U 74B',
        'Bolt-N74B':'Bolt-N 74B',
        'Bolt-U1K':'Bolt-U 1K',
        'Bolt-U15/15':'Bolt-U 15/15',
        'Bolt-U17/18':'Bolt-U 17/18',
        'Bolt-N5/5':'Bolt-N 5/5',
        'Qwen1K':'Qwen 1K',
        'Same27B':'Same 27B',
        'Qwen27B':'Qwen 27B',
        'GTX1080Ti11GB':'GTX 1080 Ti 11 GB',
        'GTX1080Ti':'GTX 1080 Ti',
        'the1080Ti':'the 1080 Ti',
        'MTP2/3/4':'MTP 2/3/4',
        'Strata/INT8':'Strata / INT8',
        'llama.cpp/F16':'llama.cpp / F16',
        'F16KV':'F16 KV',
        'INT8KV':'INT8 KV',
        '×B60':' × B60',
        'on2B60s':'on two B60s',
        'vsN5':'vs N5',
        'MedGemma1.5':'MedGemma 1.5',
        'Ornith1.5':'Ornith 1.5',
        'Qwen3-VL8B':'Qwen3-VL 8B',
        'Youtu-VL4B':'Youtu-VL 4B',
        'Gemma4-E4B':'Gemma 4-E4B',
        'B60+1080Ti':'B60 + GTX 1080 Ti',
        'GGUF-declared256K':'GGUF-declared 256K',
        'Bolt-N24':'Bolt-N 24',
        'Ubuntu24':'Ubuntu 24',
        'PCIe3':'PCIe 3',
        'llama.cpp459ab1c':'llama.cpp 459ab1c',
        'llama.cpp7592b61':'llama.cpp 7592b61',
        'cases309':'cases; 309',
        'Benign16/16':'Benign 16/16',
        'coding6×3':'coding 6×3',
        'injection4×3':'injection 4×3',
    }
    for old,new in replacements.items():text=text.replace(old,new)
    words='at|only|and|or|for|the|of|has|have|with|used|use|allow|is|not|one|two|each|raw|become|becomes|facts|quality|tools|JSON|numeric|status|parseable|retrieval|qualification|search|code|reason|complete|completed|optional|Synthetic|Frozen|seeds|seed|patterns|small|approximately|later|controlled|passed|fixed|build|runtime|official|observed|versus|over|reached|averaged|generally|exercised|previously|cache|Temperature|temperature|CUDA|SYCL|Vulkan|Strata|Bionic'
    text=re.sub(r'\b('+words+r')(?=\d)',r'\1 ',text,flags=re.I)
    text=re.sub(r'\b(no|spec|Step|vs)(?=\d)',r'\1 ',text)
    text=re.sub(r'\b(top-p|top-k|min-p)(?=\d)',r'\1 ',text,flags=re.I)
    text=re.sub(r'(?<=\d)(reps|repetitions|runs|cases|requests|tokens|patterns|output|QA|GiB|MiB|GB)\b',r' \1',text)
    text=re.sub(r'(?<=\d)(GiB|MiB|GB)(?=[^A-Za-z]|$)',r' \1',text)
    text=re.sub(r'\ba(?=\d+\s(?:GB|GiB|MiB)\b)','a ',text)
    text=re.sub(r',(?=[A-Za-z])',', ',text)
    text=re.sub(r'(?<=[A-Za-z)]),(?=\d)',', ',text)
    text=re.sub(r',(?=\d)(?!\d{3}(?:\D|$))',', ',text)
    text=re.sub(r':(?=\d)',': ',text)
    text=re.sub(r'(?<=\d),(?=\d+\.\d)',', ',text)
    text=re.sub(r';(?=\S)','; ',text)
    text=re.sub(r'(t/s\.|latency\.)(?=\d)',r'\1 ',text)
    text=re.sub(r'\s/(\d)',r' / \1',text)
    return text

def normalize(text):
    # Protect code and link destinations; exact identifiers remain exact.
    spans=re.split(r'(```[\s\S]*?```|`[^`\n]*`|\]\([^\n)]*\))',text)
    text=''.join(s if i%2 else prose(s) for i,s in enumerate(spans))
    # Separate fences from surrounding prose without inserting blank code lines.
    lines=[];in_fence=False
    for line in text.splitlines():
        if line.startswith('```'):
            if in_fence:
                while lines and not lines[-1]:lines.pop()
                lines.extend([line,''])
            else:
                if lines and lines[-1]:lines.append('')
                lines.append(line)
            in_fence=not in_fence
        elif line or in_fence or not lines or lines[-1]:lines.append(line)
    text='\n'.join(lines).rstrip()+'\n'
    return text

def format_repository(root):
    names=subprocess.check_output(['git','ls-files','-z','*.md'],cwd=root).decode().split('\0')
    changed=[]
    for name in filter(None,names):
        p=root/name;before=p.read_text();text=before
        if name=='inventory.md':
            rows=[]
            for line in text.splitlines():
                cells=line.split('|')
                if len(cells)>4 and cells[3].strip().startswith('~/'):
                    cells[3]=' `'+cells[3].strip()+'` ';line='|'.join(cells)
                rows.append(line)
            text='\n'.join(rows)+'\n'
        if name=='README.md':
            # These lower-case labels are exact exported model identifiers.
            text=re.sub(r'^(\| )((?:qwen|medgemma|internvl|ministral|youtu|gemma)[a-z0-9_-]+)( \|)',r'\1`\2`\3',text,flags=re.M)
        text=normalize(text)
        if name=='README.md' and '## In plain words' not in text:
            marker='**Dual Intel Arc Pro B60 + a 2017 i7-7700K: real local LLM benchmarks**\n\n'
            if marker not in text:raise ValueError('README subtitle not found')
            text=text.replace(marker,marker+PLAIN_WORDS,1)
        if text!=before:p.write_text(text);changed.append(name)
    return changed

if __name__=='__main__':
    for name in format_repository(Path(__file__).resolve().parents[1]):print(name)
