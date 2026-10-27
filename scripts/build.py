from pathlib import Path
import os,sys,json,html,re,hashlib,csv,importlib.metadata
import tiktoken
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate,PageTemplate,Frame,Paragraph,Spacer,PageBreak,Table,TableStyle,KeepTogether,Flowable
from reportlab.platypus.tableofcontents import TableOfContents
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('TIKTOKEN_CACHE_DIR',str(ROOT/'.tokenizer-cache'))
ENC={k:tiktoken.get_encoding(k) for k in ['o200k_base','cl100k_base']}
AUDIT={}
W,H=595.276,841.89;M=43;CW=W-2*M
INK=colors.HexColor('#23353D');NAVY=colors.HexColor('#15313E');TEAL=colors.HexColor('#007D78')
PALE=colors.HexColor('#F1F6F5');LINE=colors.HexColor('#DCE5E6');MUTED=colors.HexColor('#61747B')
DEFAULT_FONTS={
'zh-CN':('C:/Windows/Fonts/msyh.ttc','C:/Windows/Fonts/msyhbd.ttc'),
'en':('C:/Windows/Fonts/arial.ttf','C:/Windows/Fonts/arialbd.ttf'),
'ja':('C:/Windows/Fonts/YuGothM.ttc','C:/Windows/Fonts/YuGothB.ttc'),
'ko':('C:/Windows/Fonts/malgun.ttf','C:/Windows/Fonts/malgunbd.ttf')}
FAMILY={};MAPS={};STYLES={};MISSING=set()
for lang,(reg,bold) in DEFAULT_FONTS.items():
    key=lang.upper().replace('-','_');rn='YJ-'+lang;bn=rn+'-bold'
    pdfmetrics.registerFont(TTFont(rn,os.environ.get('YIJIAN_'+key+'_FONT',reg),subfontIndex=0))
    pdfmetrics.registerFont(TTFont(bn,os.environ.get('YIJIAN_'+key+'_BOLD_FONT',bold),subfontIndex=0))
    pdfmetrics.registerFontFamily(rn,normal=rn,bold=bn,italic=rn,boldItalic=bn)
    FAMILY[lang]=(rn,bn)
    MAPS[rn]=pdfmetrics.getFont(rn).face.charToGlyph
    MAPS[bn]=pdfmetrics.getFont(bn).face.charToGlyph
    styles={}
    for name,size,leading,col,font in [('body',10,16,INK,rn),('small',8.1,12.5,MUTED,rn),
        ('cell',9,14,INK,rn),('term',9.4,14,NAVY,bn),('head',21,28,NAVY,bn),
        ('sub',11.5,17,NAVY,bn),('code',10,17,NAVY,rn),('cover',31,43,NAVY,bn),
        ('toc',10.5,22,NAVY,rn),('index',8.4,13.5,INK,rn)]:
        styles[name]=ParagraphStyle(lang+name,fontName=font,fontSize=size,leading=leading,textColor=col,
            wordWrap='CJK' if lang in ['zh-CN','ja'] else None,spaceAfter=8 if name=='body' else 0,
            splitLongWords=True,keepWithNext=name in ['head','sub'])
    STYLES[lang]=styles

def measure(text,lang,context=''):
    text=str(text)
    key=(lang,text)
    if key not in AUDIT:
        counts={n:len(e.encode(text,disallowed_special=())) for n,e in ENC.items()}
        AUDIT[key]={'language':lang,'text':text,'utf8_sha256':hashlib.sha256(text.encode('utf-8')).hexdigest(),
            **counts,'contexts':set()}
    if context:AUDIT[key]['contexts'].add(context)
    return {n:AUDIT[key][n] for n in ENC}

def badge(text,lang,context=''):
    d=measure(text,lang,context)
    return f'[O {d["o200k_base"]} / C {d["cl100k_base"]}]'

def markup(text,lang):
    rn=FAMILY[lang][0];parts=[];buf='';current=rn
    for ch in str(text):
        target=rn
        if ch not in '\n\r\t' and ord(ch) not in MAPS[rn]:
            target=next((FAMILY[fb][0] for fb in ['ja','zh-CN','ko','en'] if ord(ch) in MAPS[FAMILY[fb][0]]),rn)
            if ord(ch) not in MAPS[target]:MISSING.add(ch)
        if target!=current:
            if buf:parts.append((current,buf))
            current=target;buf=''
        buf+=ch
    if buf:parts.append((current,buf))
    return ''.join((f'<font name="{f}">' if f!=rn else '')+html.escape(t).replace('\n','<br/>')+
        ('</font>' if f!=rn else '') for f,t in parts)

def P(text,lang,style='body',count=False,context=''):
    value=markup(text,lang)
    if count:value+=' <font size="7.2" color="#007D78">'+badge(text,lang,context)+'</font>'
    return Paragraph(value,STYLES[lang][style])

def mdcount(text,lang,context=''):
    return str(text)+' '+badge(text,lang,context)

def anchor(category,term):
    return 'term-'+hashlib.sha256((category+'\0'+term).encode('utf-8')).hexdigest()[:20]

class Switch(Flowable):
    def __init__(self,label,lang):super().__init__();self.width=0;self.height=0;self.label=label;self.lang=lang
    def draw(self):pass

class Doc(BaseDocTemplate):
    def __init__(self,path,lang,status,guide=False):
        self.edition_lang=lang;self.status=status;self.guide=guide;self.term_pages={};self.section_pages={}
        super().__init__(str(path),pagesize=(W,H),leftMargin=M,rightMargin=M,topMargin=62,bottomMargin=52,
            title=('意简 / ' if lang=='zh-CN' else 'YIJIAN / ')+('使用说明' if guide else 'Token dictionary')+' v0.4',
            author='Yijian project',creator='Yijian / ReportLab / tiktoken',pageCompression=1)
        self.addPageTemplates(PageTemplate(id='main',frames=[Frame(M,52,CW,H-114,leftPadding=0,rightPadding=0,
            topPadding=0,bottomPadding=0,id='content')],onPage=self.decorate))
    def beforeDocument(self):self.current='';self.current_lang=self.edition_lang
    def decorate(self,c,doc):
        lang=self.current_lang;rn,bn=FAMILY[lang]
        c.saveState();c.setFillColor(TEAL);c.rect(0,H-7,W,7,fill=1,stroke=0)
        c.setFont(rn,7.5);c.setFillColor(MUTED)
        label=('意简' if lang=='zh-CN' else 'YIJIAN')+(' / '+self.current if self.current else '')
        c.drawString(M,H-33,label)
        c.drawRightString(W-M,H-33,({'zh-CN':'四语说明','en':'Usage','ja':'使い方','ko':'사용법'}[lang] if self.guide else {'zh-CN':'中文','en':'English','ja':'日本語','ko':'한국어'}[lang])+' / v0.4')
        c.setStrokeColor(LINE);c.line(M,41,W-M,41)
        c.setFont(rn,7);c.drawString(M,27,'O: o200k_base / C: cl100k_base')
        c.drawRightString(W-M,27,str(doc.page));c.restoreState()
    def afterFlowable(self,f):
        if isinstance(f,Switch):self.current=f.label;self.current_lang=f.lang
        if hasattr(f,'section_key'):
            self.canv.bookmarkPage(f.section_key)
            self.canv.addOutlineEntry(f.getPlainText(),f.section_key,0,False)
            self.section_pages[f.section_key]=self.page
            if f.section_key!='contents':self.notify('TOCEntry',(0,f.getPlainText(),self.page,f.section_key))
        if hasattr(f,'entry_key'):
            self.canv.bookmarkPage(f.entry_key);self.term_pages[f.entry_key]=self.page

def heading(story,text,key,lang,newpage=True):
    if newpage:story.extend([Switch(text,lang),PageBreak()])
    item=P(text,lang,'head');item.section_key=key
    story.extend([item,Spacer(1,16)])

def block(story,title,text,lang):
    whole={'zh-CN':'整段','en':'Whole block','ja':'全体','ko':'전체'}[lang]
    measure(text,lang,'template-whole')
    rows=[[P(title,lang,'sub')]]
    for line in text.split('\n'):rows.append([P(line,lang,'code',True,'template-line')])
    rows.append([P(whole+': '+badge(text,lang,'template-whole'),lang,'small')])
    table=Table(rows,colWidths=[CW])
    table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PALE),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),13),('RIGHTPADDING',(0,0),(-1,-1),13),
        ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
        ('TOPPADDING',(0,0),(-1,0),12),('BOTTOMPADDING',(0,-1),(-1,-1),12)]))
    story.extend([table,Spacer(1,15)])

def glossary(story,lang,L,entries,category,key,doc):
    title=L['sections'][{'field':3,'action':4,'logic':5,'phrase':6}[category]]
    heading(story,title,key,lang)
    story.extend([P(L['glossary_note'],lang,'small'),Spacer(1,12)])
    widths=[118,190,CW-308]
    data=[[P(h,lang,'small') for h in L['heads']]]
    table=Table(data,colWidths=widths)
    table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PALE),('LINEBELOW',(0,0),(-1,-1),.6,TEAL),
        ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
    table.keepWithNext=True;story.append(table)
    for row_index,e in enumerate([x for x in entries if x['category']==category]):
        if category=='logic' and row_index==12:story.append(PageBreak())
        row=Table([[P(e['term'],lang,'term',True,'term'),P(e['meaning'],lang,'cell',True,'meaning'),
            P(e['example'],lang,'cell',True,'example')]],colWidths=widths)
        row.entry_key=anchor(category,e['term'])
        row.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),
            ('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),
            ('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,-1),.35,LINE)]))
        story.append(row)

def build_dictionary(lang):
    source=ROOT/'data'/f'{lang}.json';data=json.loads(source.read_text(encoding='utf-8'));entries=data['entries']
    casefile=ROOT/'eval'/f'{lang}-cases.json';case_data=json.loads(casefile.read_text(encoding='utf-8'));cases=case_data['cases']
    L=json.loads((ROOT/'locales'/f'{lang}.json').read_text(encoding='utf-8'))
    G=json.loads((ROOT/'locales'/f'{lang}-usage.json').read_text(encoding='utf-8'))
    for e in entries:e['token_counts']={f:measure(e[f],lang,f) for f in ['term','meaning','example']}
    for case in cases:case['token_counts']={f:measure(case[f],lang,'case-'+f) for f in ['original','candidate']}
    data['measurement']={'library':'tiktoken','version':tiktoken.__version__,'encodings':list(ENC),'scope':'exact text only; no normalization; annotations excluded'}
    source.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    casefile.write_text(json.dumps(case_data,ensure_ascii=False,indent=2),encoding='utf-8')
    out=ROOT/'docs'/lang;out.mkdir(parents=True,exist_ok=True)
    doc=Doc(out/'dictionary.pdf',lang,L['status']);story=[]
    story.extend([Spacer(1,22),P('意简' if lang=='zh-CN' else 'YIJIAN',lang,'cover'),Spacer(1,25),
        P(L['title'],lang,'cover'),Spacer(1,18),P(L['subtitle'],lang,'sub'),Spacer(1,28),
        P(L['intro'],lang),Spacer(1,18)])
    block(story,L['status'],L['map_note'],lang)
    story.extend([Spacer(1,22),P('v0.4 / 2026-10-27',lang,'small')])
    heading(story,L['sections'][0],'contents',lang)
    story.extend([P(L['map'],lang),Spacer(1,14)])
    toc=TableOfContents();toc.levelStyles=[STYLES[lang]['toc']];toc.dotsMinLevel=0;story.append(toc)
    story.extend([Spacer(1,18),P(G['legend'],lang,'small')])
    heading(story,L['sections'][1],'quick',lang)
    block(story,L['quick_title'],L['quick'],lang)
    block(story,L['quick_example_title'],L['quick_example'],lang)
    story.append(P(L['quick_note'],lang))
    heading(story,L['sections'][2],'rules',lang)
    for title,body in L['rules']:
        story.extend([P(title,lang,'sub'),Spacer(1,5),P(body,lang,'body',True,'rule'),Spacer(1,9)])
    block(story,L['card_title'],L['card'],lang)
    for cat,key in [('field','fields'),('action','actions'),('logic','logic'),('phrase','phrases')]:
        glossary(story,lang,L,entries,cat,key,doc)
    heading(story,L['sections'][7],'examples',lang)
    for i,(title,body,note) in enumerate(L['examples']):
        if i==2:story.append(PageBreak())
        block(story,title,body,lang);story.extend([P(note,lang),Spacer(1,12)])
    story.append(P(L['fallback'],lang,'small'))
    heading(story,L['sections'][8],'evaluation',lang)
    block(story,L['cost_title'],L['cost'],lang)
    for title,body in L['eval_steps']:
        story.extend([P(title,lang,'sub'),Spacer(1,5),P(body,lang),Spacer(1,6)])
    story.append(P(L['eval_status'],lang,'small'))
    heading(story,L['sections'][9],'cases',lang)
    story.extend([P(L['cases_note'],lang,'small'),Spacer(1,12)])
    for case_index,case in enumerate(cases):
        if case_index and case_index%5==0:story.append(PageBreak())
        story.append(KeepTogether([P(case['focus'],lang,'sub'),Spacer(1,5),
            P(L['original'],lang,'small'),P(case['original'],lang,'cell',True,'case-original'),Spacer(1,5),
            P(L['candidate'],lang,'small'),P(case['candidate'],lang,'cell',True,'case-candidate'),Spacer(1,5),
            P(L['checks']+': '+'; '.join(case['assertions']),lang,'small'),Spacer(1,18)]))
    heading(story,L['sections'][10],'index',lang)
    story.extend([P(L['index_note'],lang,'small'),Spacer(1,12)])
    class IndexCell(Paragraph):
        def __init__(self,e):self.e=e;super().__init__(' ',STYLES[lang]['index'])
        def wrap(self,aW,aH):
            e=self.e;key=anchor(e['category'],e['term']);page=doc.term_pages.get(key,'?')
            token=badge(e['term'],lang,'term')
            page_label={'zh-CN':'页','en':'p.','ja':'頁','ko':'쪽'}[lang]
            text=f'<link href="#{key}" color="#007D78">'+markup(e['term'],lang)+'</link>'
            text+=f' <font size="7">{token} · {page_label} {page}</font>'
            Paragraph.__init__(self,text,STYLES[lang]['index']);return super().wrap(aW,aH)
    # Three index pages allow full phrases, counts, and page numbers without clipping.
    for start in range(0,len(entries),45):
        if start:story.append(PageBreak())
        subset=entries[start:start+45];half=(len(subset)+1)//2
        rows=[[IndexCell(subset[i]),IndexCell(subset[i+half]) if i+half<len(subset) else ''] for i in range(half)]
        tab=Table(rows,colWidths=[CW/2,CW/2]);tab.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
            ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),12),
            ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)]));story.append(tab)
    heading(story,L['sections'][11],'release',lang)
    for title,body in L['release']:story.extend([P(title,lang,'sub'),Spacer(1,5),P(body,lang),Spacer(1,7)])
    for label,url in [('tiktoken','https://github.com/openai/tiktoken'),
        ('Token counting examples','https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb')]:
        if lang=='zh-CN':label='分词器官方项目' if label=='tiktoken' else '官方计数示例'
        story.append(Paragraph(f'<link href="{url}" color="#007D78">{markup(label,lang)}</link>',STYLES[lang]['small']))
    doc.multiBuild(story,maxPasses=10)
    # Editable reading source; numbers here follow the same raw-text boundaries as PDF.
    md=['# '+('意简' if lang=='zh-CN' else 'YIJIAN'),'','> '+L['status'],'',L['intro'],'',L['map_note'],'',
        '## '+L['sections'][1],'']
    def mdblock(title,text):
        md.extend(['### '+title,'','```text',text,'```','',G['whole']+': '+badge(text,lang,'template-whole'),''])
        for line in text.split('\n'):md.extend([mdcount(line,lang,'template-line'),''])
    mdblock(L['quick_title'],L['quick']);mdblock(L['quick_example_title'],L['quick_example'])
    md.extend([L['quick_note'],'','## '+L['sections'][2],''])
    for title,body in L['rules']:md.extend(['### '+title,'',mdcount(body,lang,'rule'),''])
    mdblock(L['card_title'],L['card'])
    for n,cat in [(3,'field'),(4,'action'),(5,'logic'),(6,'phrase')]:
        md.extend(['## '+L['sections'][n],'',L['glossary_note'],'','| '+' | '.join(L['heads'])+' |','| --- | --- | --- |'])
        for e in entries:
            if e['category']==cat:
                md.append('| '+' | '.join(mdcount(e[f],lang,f).replace('|','&#124;') for f in ['term','meaning','example'])+' |')
        md.append('')
    md.extend(['## '+L['sections'][7],''])
    for title,body,note in L['examples']:mdblock(title,body);md.extend([note,''])
    md.extend([L['fallback'],'','## '+L['sections'][8],'']);mdblock(L['cost_title'],L['cost'])
    for title,body in L['eval_steps']:md.extend(['### '+title,'',body,''])
    md.extend([L['eval_status'],'','## '+L['sections'][9],'',L['cases_note'],''])
    for case in cases:md.extend(['### '+case['focus'],'',L['original']+': '+mdcount(case['original'],lang,'case-original'),'',
        L['candidate']+': '+mdcount(case['candidate'],lang,'case-candidate'),'',L['checks']+': '+'; '.join(case['assertions']),''])
    md.extend(['## '+L['sections'][11],''])
    for title,body in L['release']:md.extend(['### '+title,'',body,''])
    (out/'dictionary.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    reader=PdfReader(out/'dictionary.pdf');texts=[p.extract_text() for p in reader.pages]
    assert len(doc.term_pages)==133
    assert not re.search(r'YJ-\d|T-\d','\n'.join(texts))
    for e in entries:
        page=doc.term_pages[anchor(e['category'],e['term'])]
        assert re.sub(r'\s+','',e['term']) in re.sub(r'\s+','',texts[page-1])
    return {'language':lang,'pages':len(reader.pages),'entries':len(entries),'cases':len(cases),
        'section_pages':doc.section_pages,'term_pages':doc.term_pages}

def build_usage():
    path=ROOT/'docs'/'usage-four-languages.pdf'
    doc=Doc(path,'zh-CN','',guide=True);story=[];fullmd=[]
    story.extend([Spacer(1,30),P('意简', 'zh-CN','cover'),Spacer(1,18),P('四语使用说明','zh-CN','cover'),Spacer(1,20)])
    for lang,label in [('zh-CN','中文使用说明'),('ko','한국어 사용법'),('ja','日本語の使い方'),('en','English usage guide')]:
        story.extend([P(label,lang,'sub'),Spacer(1,10)])
    story.extend([Spacer(1,25),P('O: o200k_base / C: cl100k_base','en'),P('v0.4 / 2026-10-27','en','small')])
    # Same meaning in four languages, each independently measured as a whole.
    for lang in ['zh-CN','ko','ja','en']:
        G=json.loads((ROOT/'locales'/f'{lang}-usage.json').read_text(encoding='utf-8'))
        heading(story,G['title'],'usage-'+lang,lang)
        story.extend([P(G['legend'],lang,'small'),Spacer(1,16)])
        md=['# '+G['title'],'',G['legend'],'']
        for section_index,(title,body) in enumerate(G['sections']):
            if section_index==5:story.append(PageBreak())
            story.append(KeepTogether([P(title,lang,'sub'),Spacer(1,5),P(body,lang,'body',True,'usage-explanation'),Spacer(1,8)]))
            md.extend(['## '+title,'',mdcount(body,lang,'usage-explanation'),''])
        block(story,G['example_title'],G['example'],lang)
        story.append(P(G['example_note'],lang))
        md.extend(['## '+G['example_title'],'','```text',G['example'],'```','',G['whole']+': '+badge(G['example'],lang,'template-whole'),'',G['example_note'],''])
        folder=ROOT/'docs'/lang;folder.mkdir(exist_ok=True)
        (folder/'USAGE.md').write_text('\n'.join(md)+'\n',encoding='utf-8');fullmd+=md+['---','']
    doc.multiBuild(story,maxPasses=10)
    (ROOT/'USAGE.md').write_text('\n'.join(fullmd)+'\n',encoding='utf-8')
    return {'file':'docs/usage-four-languages.pdf','pages':len(PdfReader(path).pages)}

def export_counts():
    folder=ROOT/'counts';folder.mkdir(exist_ok=True)
    for lang in DEFAULT_FONTS:
        with (folder/f'{lang}.csv').open('w',encoding='utf-8-sig',newline='') as f:
            wr=csv.DictWriter(f,fieldnames=['language','contexts','text','utf8_sha256','o200k_base','cl100k_base']);wr.writeheader()
            for (lc,text),r in AUDIT.items():
                if lc==lang:wr.writerow({**r,'contexts':'; '.join(sorted(r['contexts']))})
    encinfo={n:{'vocabulary_size':e.n_vocab,'mergeable_rank_count':len(e._mergeable_ranks),
        'pattern_sha256':hashlib.sha256(e._pat_str.encode('utf-8')).hexdigest()} for n,e in ENC.items()}
    manifest={'date':'2026-10-27','tiktoken_version':tiktoken.__version__,'encoding_details':encinfo,
        'unicode_normalization':False,'disallowed_special':[],'count_scope':'exact original Unicode string; annotations excluded',
        'records':len(AUDIT),'cross_model_execution_runs':0,'native_independent_review':False}
    (folder/'measurement.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'TOKEN-COUNTING.md').write_text('''# 计数口径 / Counting method

日期：2026-10-27。tiktoken版本：'''+tiktoken.__version__+'''.

O = `o200k_base`；C = `cl100k_base`。方法：`len(encoding.encode(text, disallowed_special=()))`。文本中的特殊标记样式按普通字符串处理，不解释为消息协议的特殊token。

计数保留原标点、大小写、空格和显式换行，不作Unicode归一化；排版自动折行不改变计数原文。每个标注仅对应其相邻的文字；数字标注、标题标签等不计入该片段。模板有逐行和整段两种计数，两者不能用加法互换。

Counts preserve original punctuation, case, spaces, and explicit newlines without Unicode normalization. Badges and visual line wrapping are excluded. Whole templates are encoded independently from their lines. Message wrappers, system prompts, tools, and extra rounds are separate costs.

本次实测不向任何模型发送文档。两种公开分词器不代表所有模型；跨模型执行准确率尚未测试。数字是文本长度测量，不是理解准确率、压缩成功率或全局最优证明。

No documents were sent to a model for this measurement. The two encodings do not represent every model. Task execution and translation accuracy remain separate, unvalidated results.

`counts/*.csv` 保存准确计数原文、UTF-8 SHA-256与两种结果；`measurement.json`记录分词器版本及词表规模。运行 `python scripts/build.py` 重新计数并构建。

来源：[tiktoken官方项目](https://github.com/openai/tiktoken)；[官方计数示例](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb)。
''',encoding='utf-8')
    return manifest

if __name__=='__main__':
    reports=[build_dictionary(lang) for lang in DEFAULT_FONTS]
    usage=build_usage();manifest=export_counts()
    assert not MISSING,sorted(MISSING)
    (ROOT/'counts/build-report.json').write_text(json.dumps({'dictionaries':reports,'usage':usage,'missing_glyphs':[]},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'dictionaries':[{k:v for k,v in r.items() if k not in ['term_pages','section_pages']} for r in reports],
        'usage':usage,'measured_fragments':manifest['records'],'tiktoken_version':tiktoken.__version__},ensure_ascii=True))
