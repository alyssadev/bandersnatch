import json

with open("SegmentMap.json") as f:
  smap = json.load(f)["segments"]

def msToTS(ms):
  s,ms = divmod(ms,1000)
  m,s = divmod(s,60)
  h,m = divmod(m,60)
  return "{:02d}:{:02d}:{:02d}.{:03d}".format(h,m,s,ms)

for _id,segment in smap.items():
  ss = ""
  t = ""
  # working around ffmpeg seek to previous keyframe
  if segment["startTimeMs"] > 0:
    ss = " -ss " + msToTS(segment["startTimeMs"]+40)
  if "endTimeMs" in segment:
    t = " -t {}".format((segment["endTimeMs"]-segment["startTimeMs"])/1000)
  try:
    print("""</dev/null ffmpeg{} -y -i Black.Mirror.Bandersnatch.2018.720p.WEB-DL.x264.DUAL.mp4 -c:v libx264 -c:a aac {} {}.mkv""".format(ss, t, _id))
  except BrokenPipeError:
    break