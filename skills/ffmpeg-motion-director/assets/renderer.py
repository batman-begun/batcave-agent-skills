#!/usr/bin/env python3
"""FFmpeg Motion Director v0.4 — approved 15-fx independent motion engine.
Image-space motion composed by numpy/OpenCV and encoded by FFmpeg; no remote service.
Default: one 30-second 854x480 24fps silent H.264 video per image.
"""
from __future__ import annotations
import argparse, json, os, subprocess, sys, time
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageOps
import fx_v04 as fx_old
import fx_v04b as fx_tweak
import fx_new as fx_new
import fx_more as fx_more

W,H=854,480
FPS=24
FX_NAMES = [
    'radial_refraction', 'water_mirage', 'prism_glass', 'cyber_glitch',
    'tile_mosaic', 'shadow_reveal', 'rhythmic_zoom', 'rain_glass',
    'snow_dust', 'petals', 'firestorm', 'bokeh', 'sunbeam',
    'film_burn', 'cinematic_impact'
]
# Retained solely for past v0.3 motion plans. Never choose these for NEW work.
LEGACY_FX={'golden_hour':'sunbeam'}  # Existing v0.3 alias only, explicitly reported.

FX_MAP = {
 'radial_refraction':fx_more.radial_refraction,
 'water_mirage':fx_old.water_mirage,
 'prism_glass':fx_more.prism_glass,
 'cyber_glitch':fx_more.cyber_glitch,
 'tile_mosaic':lambda base,t: fx_new.tile_mosaic(base, t % 6.0),
 'shadow_reveal':fx_tweak.shadow_reveal,
 'rhythmic_zoom':fx_new.rhythmic_zoom,
 'rain_glass':fx_old.rain_glass,
 'snow_dust':fx_tweak.snow_dust,
 'petals':fx_old.petals,
 'firestorm':fx_more.firestorm,
 'bokeh':fx_tweak.bokeh,
 'sunbeam':fx_tweak.sunbeam,
 'film_burn':fx_more.film_burn,
 'cinematic_impact':fx_more.cinematic_impact,
}

def load_image(p):
 with Image.open(p) as raw:
  im=ImageOps.exif_transpose(raw).convert('RGB')
  im=ImageOps.fit(im,(W,H),method=Image.Resampling.LANCZOS,centering=(.5,.5))
  return cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR)

def render(image, output, effect, duration=30.0, fps=FPS, threads=2):
 if effect not in FX_NAMES and effect not in LEGACY_FX:raise ValueError(f'Unknown effect {effect}')
 if duration<=0 or duration>180:raise ValueError('duration must be >0 and <=180')
 if fps<1 or fps>60:raise ValueError('fps must be 1..60')
 actual=LEGACY_FX.get(effect,effect)
 fn=FX_MAP[actual]
 cv2.setNumThreads(max(1,threads))
 src=load_image(image)
 # Prevent stale cached visual content when tile_mosaic is used on a new image.
 fx_new._base_bg_cache=None
 n=round(duration*fps)
 output=Path(output)
 output.parent.mkdir(parents=True,exist_ok=True)
 tmp=output.with_name(output.stem+'.partial.mp4')
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo',
      '-pixel_format','bgr24','-video_size',f'{W}x{H}','-framerate',str(fps),'-i','pipe:0',
      '-an','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',
      '-frames:v',str(n),'-movflags','+faststart',str(tmp)]
 start=time.monotonic()
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
 try:
  for i in range(n):
   frame=fn(src,i/fps)
   if frame.shape!=(H,W,3) or frame.dtype!=np.uint8:
    raise RuntimeError(f'{actual} generated malformed frame #{i}: {frame.shape} {frame.dtype}')
   proc.stdin.write(np.ascontiguousarray(frame).tobytes())
  proc.stdin.close()
  err=proc.stderr.read(); ret=proc.wait()
  if ret:raise RuntimeError('ffmpeg encode failed: '+err.decode(errors='replace')[-2000:])
  os.replace(tmp,output)
  return {'requested_effect':effect,'actual_effect':actual,'frames':n,'seconds':n/fps,'elapsed':round(time.monotonic()-start,2),'file':str(output)}
 except BaseException:
  try: proc.stdin.close() if proc.stdin and not proc.stdin.closed else None
  except OSError:pass
  try: proc.kill()
  except Exception:pass
  proc.wait()
  tmp.unlink(missing_ok=True)
  raise

def probe(path,expected_duration=30.0,expected_frames=720,w=W,h=H):
 cmd=['ffprobe','-v','error','-show_entries','format=duration',
      '-show_entries','stream=codec_name,width,height,nb_frames,pix_fmt,r_frame_rate',
      '-of','json',str(path)]
 p=subprocess.run(cmd,capture_output=True,text=True,check=True)
 j=json.loads(p.stdout)
 s=next((s for s in j['streams'] if s.get('codec_name')=='h264'),None)
 if not s:raise RuntimeError('H264 stream missing')
 if int(s['width'])!=w or int(s['height'])!=h:raise RuntimeError('Wrong dimensions')
 if s['pix_fmt']!='yuv420p':raise RuntimeError('Wrong pixel format')
 if int(s.get('nb_frames',-1))!=expected_frames:raise RuntimeError('Wrong frame count')
 if abs(float(j['format']['duration'])-expected_duration)>.08:raise RuntimeError('Wrong duration')
 p=subprocess.run(['ffmpeg','-hide_banner','-v','error','-i',str(path),'-f','null','-'],capture_output=True,text=True)
 if p.returncode:raise RuntimeError('Full decode failed: '+p.stderr[-1500:])
 return True

if __name__=='__main__':
 ap=argparse.ArgumentParser(description='Render a single image with one of 15 FX')
 ap.add_argument('--image',type=Path,required=True)
 ap.add_argument('--output',type=Path,required=True)
 ap.add_argument('--fx',required=True)
 ap.add_argument('--duration',type=float,default=30.0)
 ap.add_argument('--fps',type=int,default=24)
 args=ap.parse_args()
 r=render(args.image,args.output,args.fx,args.duration,args.fps)
 print(json.dumps(r))
