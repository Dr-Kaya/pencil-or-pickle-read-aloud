"""Build the original-page reader and downloadable narrated EPUBs."""
from pathlib import Path
import sys, shutil, zipfile, subprocess, json, re

source=Path(__file__).resolve().parents[1]
target=Path(sys.argv[1] if len(sys.argv)>1 else '_site').resolve()
target.mkdir(parents=True,exist_ok=True)
for name in ['index.html','favicon.svg','.nojekyll']:
    shutil.copy2(source/name,target/name)
shutil.copytree(source/'ebook',target/'ebook',dirs_exist_ok=True)
for archive in sorted((source/'assets').glob('*.zip')):
    with zipfile.ZipFile(archive) as z:
        for name in z.namelist():
            p=Path(name)
            assert not p.is_absolute() and '..' not in p.parts and p.parts[0]=='ebook',name
        z.extractall(target)
assert len(list((target/'ebook/pages').glob('*.jpg')))==106
assert len(list((target/'ebook/audio').glob('*.mp3')))==103
subprocess.run([sys.executable,str(source/'scripts/build_epubs.py'),str(target)],check=True)
for ref in re.findall(r'(?:href|src)="([^"]+)"',(target/'index.html').read_text()):
    if not ref.startswith(('https:','#')):
        assert (target/ref).exists(),ref
print('Ready: 106 original pages, 103 recordings, 7 read-aloud EPUBs.')
