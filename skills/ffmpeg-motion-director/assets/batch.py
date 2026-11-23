#!/usr/bin/env python3
"""FFmpeg Motion Director v0.4 batch orchestrator.
Accepts 1..N photos from direct image paths, directories, and/or image ZIPs.
Automatically splits 5 videos per batch, with 1..4 videos in final remainder.
The agent visually assigns fx_override after inspecting contact sheets; NEVER cycle blindly.
Only renders requested --batch; each completed batch produces a verified ZIP.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,math,re,shutil,subprocess,sys,zipfile
from datetime import datetime,timezone
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps,ImageFile
from renderer import FX_NAMES,LEGACY_FX,probe

EXTS={'.png','.jpg','.jpeg','.webp','.bmp','.tif','.tiff'}
FX=set(FX_NAMES)|set(LEGACY_FX)
FIELDS=['id','image_filename','clip_filename','fx_override','visual_notes','original_filename']
MAX_FILES=600
MAX_EACH=100*1024*1024
MAX_TOTAL=2*1024**3
Image.MAX_IMAGE_PIXELS=100_000_000
ImageFile.LOAD_TRUNCATED_IMAGES=False

def nat(s):return [int(x) if x.isdigit() else x.lower() for x in re.split(r'(\d+)',str(s))]
def sha256(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for c in iter(lambda:f.read(1024*1024),b''):h.update(c)
 return h.hexdigest()
def read_csv(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write_csv(p,rows,cols=FIELDS):
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(rows)

def gather(inputs):
 """Return ordered [(original filename,image bytes)] without silently duplicating."""
 gathered=[];total=0
 def accept(label,filename,blob):
  nonlocal total
  ext=Path(filename).suffix.lower()
  if ext not in EXTS:raise ValueError(f'Not a supported image: {label}')
  if len(blob)>MAX_EACH:raise ValueError('Image exceeds 100MiB: '+label)
  total+=len(blob)
  if total>MAX_TOTAL:raise ValueError('Total uncompressed image size exceeds 2GiB')
  try:
   with Image.open(io.BytesIO(blob)) as im:
    if getattr(im,'n_frames',1)>1: raise ValueError('Animated image not supported: '+label)
    im.verify()
   with Image.open(io.BytesIO(blob)) as im:
    im.load()
  except Exception as e:raise ValueError(f'Invalid image {label}: {e}') from e
  gathered.append((label,ext,blob))
  if len(gathered)>MAX_FILES:raise ValueError(f'Maximum {MAX_FILES} images per job')

 def consume(p):
  p=Path(p)
  if p.is_dir():
   entries=sorted((v for v in p.rglob('*') if v.is_file() and not v.name.startswith('.') and v.suffix.lower() in EXTS),key=lambda q:nat(str(q.relative_to(p))))
   if not entries:raise ValueError('No images in folder '+str(p))
   for child in entries:accept(f'{p.name}/{child.relative_to(p)}',child.name,child.read_bytes())
  elif p.suffix.lower()=='.zip':
   with zipfile.ZipFile(p) as z:
    bad=z.testzip()
    if bad:raise ValueError('ZIP CRC failure: '+bad)
    entries=[e for e in z.infolist() if not e.is_dir() and '__MACOSX' not in e.filename and not Path(e.filename).name.startswith('.') and e.filename.lower().endswith(tuple(EXTS))]
    entries.sort(key=lambda e:nat(e.filename))
    if not entries:raise ValueError('No readable images in ZIP '+str(p))
    for e in entries:
     if e.file_size>MAX_EACH:raise ValueError('ZIP image exceeds 100MiB: '+e.filename)
     if e.flag_bits & 0x1:raise ValueError('Password-protected image in ZIP: '+e.filename)
     accept(f'{p.name}::{e.filename}',e.filename,z.read(e))
  elif p.is_file():accept(p.name,p.name,p.read_bytes())
  else:raise FileNotFoundError(str(p))
 for p in inputs:consume(p)
 if not gathered:raise ValueError('No valid images provided')
 return gathered

def contact_sheets(root,rows):
 out=root/'contact_sheets';out.mkdir(exist_ok=True)
 cw,ch=260,190
 for start in range(0,len(rows),10):
  subset=rows[start:start+10]
  sheet=Image.new('RGB',(cw*5,ch*2),(18,22,28));d=ImageDraw.Draw(sheet)
  for i,row in enumerate(subset):
   with Image.open(root/'images'/row['image_filename']) as raw:
    im=ImageOps.fit(ImageOps.exif_transpose(raw).convert('RGB'),(cw-12,ch-28))
   x=(i%5)*cw+6;y=(i//5)*ch+5
   sheet.paste(im,(x,y));d.text((x+4,y+ch-24),f"{row['id']}  {row['original_filename'][:27]}",fill=(250,250,250))
  sheet.save(out/f'images_{start+1:03d}_to_{start+len(subset):03d}.jpg',quality=88)

def prepare(a):
 root=a.project.resolve()
 if root.exists():raise SystemExit('Project already exists (refusing to overwrite): '+str(root))
 inputs=([a.zip] if a.zip else [])+(a.input or [])
 if not inputs:raise SystemExit('Provide --input image1.jpg [image2.png ...] or --zip images.zip')
 images=gather(inputs)
 if a.expect is not None and len(images)!=a.expect:
  raise SystemExit(f'Expected {a.expect} images but found {len(images)}')
 root.mkdir(parents=True);imgdir=root/'images';imgdir.mkdir()
 rows=[]; h=hashlib.sha256()
 for i,(label,ext,data) in enumerate(images,1):
  ident=f'S{i:03d}'
  filename=f'{ident}{ext}'
  (imgdir/filename).write_bytes(data)
  h.update(i.to_bytes(4,'big'));h.update(label.encode());h.update(hashlib.sha256(data).digest())
  rows.append({'id':ident,'image_filename':filename,'clip_filename':f'{ident}_30s.mp4',
               'fx_override':'','visual_notes':'','original_filename':label})
 write_csv(root/'motion_plan.csv',rows)
 source={'image_count':len(rows),'batch_size':5,'batch_count':math.ceil(len(rows)/5),
         'batch_sizes':[min(5,len(rows)-i) for i in range(0,len(rows),5)],
         'source_sha256':h.hexdigest(),'input_names':[str(p) for p in inputs]}
 (root/'source.json').write_text(json.dumps(source,indent=2,ensure_ascii=False),encoding='utf-8')
 contact_sheets(root,rows)
 print(json.dumps({'status':'PREPARED','image_count':len(rows),'batches':source['batch_sizes'],
                   'project':str(root),'plan':str(root/'motion_plan.csv'),
                   'contact_sheets':[str(p) for p in sorted((root/'contact_sheets').glob('*.jpg'))]},ensure_ascii=False))
 print('NEXT: inspect EVERY image, choose visual-compatible fx_override and visual_notes. Render batch 1 ONLY.')

def still_qc(root,subset,batch,duration):
 out=root/'qc_previews';out.mkdir(exist_ok=True)
 cw,ch=272,170
 sheet=Image.new('RGB',(cw*3,ch*len(subset)),(18,22,28));d=ImageDraw.Draw(sheet)
 for i,row in enumerate(subset):
  source=root/'videos'/row['clip_filename']
  for j,sec in enumerate((.12*duration,.5*duration,.87*duration)):
   r=subprocess.run(['ffmpeg','-v','error','-ss',f'{sec:.3f}','-i',str(source),'-frames:v','1','-f','image2pipe','-vcodec','png','-'],capture_output=True)
   if r.returncode:raise RuntimeError('Cannot extract QC sample: '+row['id'])
   with Image.open(io.BytesIO(r.stdout)) as im:
    thumb=ImageOps.fit(im.convert('RGB'),(cw-10,ch-25))
   x=j*cw+5;y=i*ch+4
   sheet.paste(thumb,(x,y));d.text((x+5,y+ch-23),f"{row['id']} {row['fx_override']} | {sec:.1f}s",fill=(248,248,248))
 path=out/f'BATCH_{batch:02d}_qc.jpg';sheet.save(path,quality=88)
 return path

def save_report(path,records):
 cols=['id','image_filename','clip_filename','planned_effect','actual_effect','status','duration','fps','source_sha256','plan_effect','note']
 write_csv(path,[records[k] for k in sorted(records,key=nat)],cols)

def report_data(path):
 if not path.is_file():return {}
 return {r['id']:r for r in read_csv(path)}

def render(a):
 root=a.project.resolve()
 if not (root/'source.json').is_file():raise SystemExit('Missing prepared source.json')
 source=json.loads((root/'source.json').read_text())
 rows=read_csv(root/'motion_plan.csv')
 if len(rows)!=source['image_count']:raise SystemExit('motion_plan count mismatch')
 count=source['batch_count']
 if not 1<=a.batch<=count:raise SystemExit(f'--batch must be between 1 and {count}')
 subset=rows[(a.batch-1)*5:a.batch*5]
 for r in subset:
  if r['fx_override'] not in FX:raise SystemExit(f"{r['id']}: choose one of 15 FX, not a blind fallback")
  if not r['visual_notes'].strip():raise SystemExit(f"{r['id']}: missing visual_notes")
  if not (root/'images'/r['image_filename']).is_file():raise SystemExit(f"{r['id']}: missing source image")
 out=root/'videos';out.mkdir(exist_ok=True)
 report_path=root/'render_report.csv'
 records=report_data(report_path)
 expframes=round(a.duration*a.fps); expsecs=expframes/a.fps
 if abs(a.duration-expsecs)>0.00001:raise SystemExit('duration*fps must yield whole number of frames')
 for r in subset:
  clip=out/r['clip_filename'];ident=r['id'];fx=r['fx_override'];old=records.get(ident)
  if clip.is_file() and not a.force:
   if not old or old['plan_effect']!=fx or float(old['duration'])!=a.duration or int(old['fps'])!=a.fps:
    raise SystemExit(f'{ident}: existing clip differs from plan; use --force to replace explicitly')
   probe(clip,expsecs,expframes)
   status='CACHED_VERIFIED'; actual=old['actual_effect']
  else:
   cmd=[sys.executable,str(Path(__file__).with_name('renderer.py')),'--image',str(root/'images'/r['image_filename']),
        '--output',str(clip),'--fx',fx,'--duration',str(a.duration),'--fps',str(a.fps)]
   print(f"Rendering {ident} {fx}...",flush=True)
   cp=subprocess.run(cmd,capture_output=True,text=True)
   if cp.returncode:raise RuntimeError(f'{ident} render failed: '+cp.stderr[-2200:])
   actual=json.loads(cp.stdout.strip().splitlines()[-1])['actual_effect']
   probe(clip,expsecs,expframes)
   status='PASSED_FULL_DECODE'
  records[ident]={'id':ident,'image_filename':r['image_filename'],'clip_filename':r['clip_filename'],
                   'planned_effect':fx,'actual_effect':actual,'status':status,'duration':str(a.duration),
                   'fps':str(a.fps),'source_sha256':source['source_sha256'],'plan_effect':fx,'note':r['visual_notes']}
  save_report(report_path,records)
  print(f'{ident}: {status} ({actual})',flush=True)
 q=still_qc(root,subset,a.batch,a.duration)
 checkpoint={'engine':'FFMD-v0.4.0','batch':a.batch,'image_count':len(rows),
             'batch_count':count,'batch_size':len(subset),'batch_sizes':source['batch_sizes'],
             'source_sha256':source['source_sha256'],'plan_sha256':sha256(root/'motion_plan.csv'),
             'status':'PASSED_TECHNICAL_QC','requires_human_visual_qc':True,
             'next_batch':a.batch+1 if a.batch<count else None,
             'clips':[{'id':r['id'],'name':r['clip_filename'],'effect':records[r['id']]['actual_effect']} for r in subset]}
 (root/'checkpoint.json').write_text(json.dumps(checkpoint,indent=2,ensure_ascii=False),encoding='utf-8')
 archive=root/f'BATCH_{a.batch:02d}_{len(subset)}_videos.zip'
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=4) as z:
  for r in subset:z.write(out/r['clip_filename'],r['clip_filename'])
  z.write(root/'motion_plan.csv','motion_plan.csv')
  z.write(root/'source.json','source.json')
  z.write(report_path,'render_report.csv')
  z.write(root/'checkpoint.json','checkpoint.json')
  z.write(q,'qc_preview.jpg')
 with zipfile.ZipFile(archive) as z:
  if z.testzip() is not None:raise RuntimeError('ZIP CRC verification failed')
  if len([n for n in z.namelist() if n.endswith('.mp4')])!=len(subset):raise RuntimeError('ZIP MP4 count mismatch')
 print(json.dumps({'status':'PASSED_TECHNICAL_QC','batch':a.batch,'clips':len(subset),
                   'archive':str(archive),'qc_preview':str(q),'next_batch':checkpoint['next_batch']},ensure_ascii=False))
 print('STOP after current batch. Inspect QC visually. Proceed only on explicit user Next.')

def status(a):
 root=a.project.resolve()
 source=json.loads((root/'source.json').read_text())
 report=report_data(root/'render_report.csv')
 rows=read_csv(root/'motion_plan.csv')
 done=set(report)
 state={'project':str(root),'count':len(rows),'batches':source['batch_sizes'],
        'rendered':len(done),'remaining':len(rows)-len(done),'rendered_ids':sorted(done,key=nat),
        'unplanned_ids':[r['id'] for r in rows if not r['fx_override']],
        'batch_zips':sorted(p.name for p in root.glob('BATCH_*_videos.zip'))}
 print(json.dumps(state,indent=2,ensure_ascii=False))

def main():
 ap=argparse.ArgumentParser(description='FFMD v0.4: single/multi-image and ZIP batch runner')
 sub=ap.add_subparsers(dest='command',required=True)
 pp=sub.add_parser('prepare');pp.add_argument('--input',type=Path,nargs='+');pp.add_argument('--zip',type=Path)
 pp.add_argument('--project',type=Path,required=True);pp.add_argument('--expect',type=int)
 rr=sub.add_parser('render');rr.add_argument('--project',type=Path,required=True);rr.add_argument('--batch',type=int,required=True)
 rr.add_argument('--duration',type=float,default=30.0);rr.add_argument('--fps',type=int,default=24);rr.add_argument('--force',action='store_true')
 ss=sub.add_parser('status');ss.add_argument('--project',type=Path,required=True)
 a=ap.parse_args()
 try:
  if a.command=='prepare':prepare(a)
  elif a.command=='render':render(a)
  else:status(a)
 except (RuntimeError,ValueError,zipfile.BadZipFile,FileNotFoundError,PermissionError) as e:
  print('ERROR:',e,file=sys.stderr);raise SystemExit(1)

if __name__=='__main__':main()
