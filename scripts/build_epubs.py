import json,zipfile,html,uuid,sys
from pathlib import Path
S=Path(__file__).resolve().parents[1]
D=Path(sys.argv[1]); ED=D/'ebook'
book=json.loads((S/'book.json').read_text())
CH=book['chapters'];TEXT=book['text'];DUR={int(n):v for n,v in book['durations'].items()};E=lambda x:html.escape(str(x),quote=True)
def clock(s):return f'{int(s)//3600:02}:{int(s)//60%60:02}:{s%60:06.3f}'
def make(path,nums,title,chapters):
 bookid='urn:uuid:'+str(uuid.uuid5(uuid.NAMESPACE_URL,'pencil-or-pickle-readaloud-'+str(nums)));
 manifest=['<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>'];spine=[];meta=[];total=0
 with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  z.writestr('mimetype','application/epub+zip',compress_type=zipfile.ZIP_STORED)
  z.writestr('META-INF/container.xml','<?xml version="1.0" encoding="UTF-8"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
  for n in nums:
   image=ED/'pages'/f'page-{n:03}.jpg';w,h=943,1333;has=bool(DUR[n]);name=f'page-{n:03}.xhtml';sid=f'p{n}';audio=f'audio/page-{n:03}.mp3';smil=f'page-{n:03}.smil'
   imgprop=' properties="cover-image"' if n==3 else ''
   manifest.append(f'<item id="img{n}" href="images/page-{n:03}.jpg" media-type="image/jpeg"{imgprop}/>')
   mo=f' media-overlay="mo{n}"' if has else ''
   manifest.append(f'<item id="{sid}" href="{name}" media-type="application/xhtml+xml"{mo}/>');spine.append(f'<itemref idref="{sid}"/>')
   z.write(image,f'EPUB/images/page-{n:03}.jpg')
   body=f'''<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en"><head><title>{E(title)} — Page {n}</title><meta name="viewport" content="width={w}, height={h}"/><style>html,body{{margin:0;padding:0;width:{w}px;height:{h}px;overflow:hidden;background:white}}img{{display:block;width:{w}px;height:{h}px}}.sr{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0)}}.epub-media-overlay-active{{background:transparent;color:inherit}}</style></head><body><div id="page"><span epub:type="pagebreak" id="pagebreak" title="{n}" class="sr">Page {n}</span><img src="images/page-{n:03}.jpg" alt="Original illustrated page {n}"/><p class="sr">{E(TEXT.get(str(n),''))}</p></div></body></html>'''
   z.writestr('EPUB/'+name,body)
   if has:
    z.write(ED/'audio'/f'page-{n:03}.mp3','EPUB/'+audio)
    manifest.extend([f'<item id="a{n}" href="{audio}" media-type="audio/mpeg"/>',f'<item id="mo{n}" href="{smil}" media-type="application/smil+xml"/>'])
    meta.append(f'<meta property="media:duration" refines="#mo{n}">{clock(DUR[n])}</meta>');total+=DUR[n]
    z.writestr('EPUB/'+smil,f'''<?xml version="1.0" encoding="UTF-8"?><smil xmlns="http://www.w3.org/ns/SMIL" xmlns:epub="http://www.idpf.org/2007/ops" version="3.0"><body><seq id="s{n}" epub:textref="{name}"><par id="par{n}"><text src="{name}#page"/><audio src="{audio}" clipBegin="0.000s" clipEnd="{DUR[n]:.3f}s"/></par></seq></body></smil>''')
  toc='<li><a href="page-003.xhtml">Title page</a></li>' if 3 in nums else ''
  if 2 in nums:toc+='<li><a href="page-002.xhtml">Copyright and acknowledgments</a></li>'
  for c in chapters:toc+=f'<li><a href="page-{c["pages"][0]:03}.xhtml">Chapter {c["number"]}: {E(c["title"])}</a><ol><li><a href="page-{c["activities"][0]:03}.xhtml">Activities</a></li></ol></li>'
  for n,label in [(102,'Meet the characters'),(103,'About the project team'),(105,'Contributors')]:
   if n in nums:toc+=f'<li><a href="page-{n:03}.xhtml">{label}</a></li>'
  page_list=''.join(f'<li><a href="page-{n:03}.xhtml#pagebreak">{n}</a></li>' for n in nums)
  z.writestr('EPUB/nav.xhtml',f'''<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en"><head><title>Contents</title></head><body><nav epub:type="toc" id="toc"><h1>{E(title)}</h1><ol>{toc}</ol></nav><nav epub:type="page-list" hidden="hidden"><h2>Original pages</h2><ol>{page_list}</ol></nav><nav epub:type="landmarks" hidden="hidden"><h2>Landmarks</h2><ol><li><a epub:type="cover" href="page-003.xhtml">Cover</a></li><li><a epub:type="bodymatter" href="page-{chapters[0]['pages'][0]:03}.xhtml">Begin reading</a></li></ol></nav></body></html>''')
  rights='Book copyright © 2026 Amy Hutchison, Brittany Adams, Kristie Gutierrez, and Erdogan Kaya. Illustrations and book design © 2026 Rebeca J. Pintos.'
  opf=f'''<?xml version="1.0" encoding="UTF-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id" xml:lang="en"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="book-id">{bookid}</dc:identifier><dc:title>{E(title)}</dc:title><dc:language>en</dc:language><dc:creator>The DCoaD Literacies Lab and Friends</dc:creator><dc:contributor>Rebeca J. Pintos, illustrations and book design</dc:contributor><dc:rights>{E(rights)}</dc:rights><dc:description>Original static illustrated pages with page-by-page read-aloud narration generated with ElevenLabs. Activities and credits included. Adult voices perform the character roles.</dc:description><meta property="dcterms:modified">2026-09-22T21:00:00Z</meta><meta property="rendition:layout">pre-paginated</meta><meta property="rendition:orientation">portrait</meta><meta property="rendition:spread">none</meta><meta property="media:duration">{clock(total)}</meta>{''.join(meta)}</metadata><manifest>{''.join(manifest)}</manifest><spine page-progression-direction="ltr">{''.join(spine)}</spine></package>'''
  z.writestr('EPUB/package.opf',opf)
 print(path.name,len(nums),'pages,',clock(total),'audio',flush=True)

make(D/'Pencil_or_Pickle_read_aloud.epub',[3,2]+list(range(4,104))+[105],'Pencil or Pickle? — Read-Aloud Edition',CH)
(ED/'chapters').mkdir(exist_ok=True)
for c in CH:make(ED/'chapters'/f'{c["number"]:02}_{c["slug"]}.epub',[3,2]+list(range(c['pages'][0],c['activities'][1]+1))+[102,103,105],c['title']+' — Pencil or Pickle?', [c])
