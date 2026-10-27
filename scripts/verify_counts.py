"""Recompute every published token count from its exact source text."""
from pathlib import Path
import csv,hashlib,json,os
import tiktoken

root=Path(__file__).resolve().parents[1]
os.environ.setdefault('TIKTOKEN_CACHE_DIR',str(root/'.tokenizer-cache'))
encodings={name:tiktoken.get_encoding(name) for name in ['o200k_base','cl100k_base']}

def count(text):
    return {name:len(enc.encode(text,disallowed_special=())) for name,enc in encodings.items()}

def require(condition,description):
    if not condition:raise ValueError(description)

total=0
for language in ['zh-CN','en','ja','ko']:
    data=json.loads((root/'data'/f'{language}.json').read_text(encoding='utf-8'))
    cases=json.loads((root/'eval'/f'{language}-cases.json').read_text(encoding='utf-8'))
    require(len(data['entries'])==133,language+': entry count')
    require(len(cases['cases'])==30,language+': seed count')
    for entry in data['entries']:
        require('id' not in entry,language+': entry IDs must be absent')
        for field in ['term','meaning','example']:
            require(entry['token_counts'][field]==count(entry[field]),language+': '+entry['term']+'/'+field)
    for case in cases['cases']:
        for field in ['original','candidate']:
            require(case['token_counts'][field]==count(case[field]),language+': '+case['focus']+'/'+field)
    with (root/'counts'/f'{language}.csv').open(encoding='utf-8-sig',newline='') as stream:
        for row in csv.DictReader(stream):
            require(row['utf8_sha256']==hashlib.sha256(row['text'].encode('utf-8')).hexdigest(),language+': text digest')
            require({name:int(row[name]) for name in encodings}==count(row['text']),language+': CSV count')
            total+=1
manifest=json.loads((root/'counts/measurement.json').read_text(encoding='utf-8'))
require(total==manifest['records'],'measurement record count')
print(json.dumps({'verified_fragments':total,'encodings':list(encodings),'tiktoken_version':tiktoken.__version__}))
