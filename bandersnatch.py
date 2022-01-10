#!/usr/bin/env python3
from random import Random, randrange
import json
from sys import stderr, maxsize, argv
from os import environ

seed = randrange(maxsize)
if environ.get("SEED", "").isdigit():
    seed = int(environ.get("SEED"))
random = Random(seed)

debug = True if environ.get("DEBUG") else False

with open("bandersnatch.json") as f:
  bandersnatch = json.load(f)

with open("segmentmap.json") as f:
  smap = json.load(f)["segments"]

with open("state_descriptions.json") as f:
  state_desc = json.load(f)

initial_state = { "p_sp": True, "p_tt": True, "p_8a": False, "p_td": True, "p_cs": False, "p_w1": False, "p_2b": False, "p_3j": False, "p_pt": False, "p_cd": False, "p_cj": False, "p_sj": False, "p_sj2": False, "p_tud": False, "p_lsd": False, "p_vh": False, "p_3l": False, "p_3s": False, "p_3z": False, "p_ps": "n", "p_wb": False, "p_kd": False, "p_bo": False, "p_5v": False, "p_pc": "n", "p_sc": False, "p_ty": False, "p_cm": False, "p_pr": False, "p_3ad": False, "p_s3af": False, "p_nf": False, "p_np": False, "p_ne": False, "p_pp": False, "p_tp": False, "p_bup": False, "p_be": False, "p_pe": False, "p_pae": False, "p_te": False, "p_snt": False, "p_8j": False, "p_8d": False, "p_8m": False, "p_8q": False, "p_8s": False, "p_8v": False, "p_vs": "n", "p_scs": False, "p_3ab": False, "p_3ac": False, "p_3aj": False, "p_3ah": False, "p_3ak": False, "p_3al": False, "p_3af": False, "p_5h": False, "p_5ac": False, "p_5ag": False, "p_5ad": False, "p_6c": False, "length": 0 }
state = dict(initial_state)

info = bandersnatch["videos"]["80988062"]["interactiveVideoMoments"]["value"]
moments = info["momentsBySegment"]
preconditions = info["preconditions"]
segmentGroups = info["segmentGroups"]
thumbnails = info["choicePointNavigatorMetadata"]["choicePointsMetadata"]["choicePoints"]

segmentMap = {}
for segmentList in moments.values():
    for _segment in segmentList:
        for _choice in _segment.get("choices", []):
            if "segmentId" in _choice and "text" in _choice:
                segmentMap[_choice["segmentId"]] = _choice["text"].title()

def msToTS(ms):
  s,ms = divmod(ms,1000)
  m,s = divmod(s,60)
  h,m = divmod(m,60)
  return "{:02d}:{:02d}:{:02d}.{:03d}".format(h,m,s,ms)

def conditionHandler(cond):
    global state
    if not cond:
        return True
    if cond[0] == "persistentState":
        return state[cond[1]]
    if cond[0] == "not":
        return not all(conditionHandler(c) for c in cond[1:])
    if cond[0] == "and":
        return all(conditionHandler(c) for c in cond[1:])
    if cond[0] == "eql":
        return conditionHandler(cond[1]) == cond[2]
    if cond[0] == "or":
        return any(conditionHandler(c) for c in cond[1:])

def groupHandler(group, segment=None):
    out = []
    if segment:
        group.append(segment)
    for item in group:
        if type(item) is str and conditionHandler( preconditions.get(item,[]) ):
            out.append(item)
        if type(item) is dict:
            if "segmentGroup" in item:
                out += groupHandler(segmentGroups[item["segmentGroup"]])
            if "precondition" in item:
                if conditionHandler( preconditions.get(item["precondition"],[]) ):
                    out.append(item["segment"])
#    if debug: print("out="+repr(out),file=stderr)
    return out

def updateState(persistent):
    global state
    for k,v in persistent.items():
        if debug:
          if state[k] != v: print(f"{k} [{state_desc[k]}]: {v} (changed)",file=stderr)
          else: print(f"{k} [{state_desc[k]}]: {v} (unchanged)",file=stderr)
        state[k] = v

def followTheStory(segment):
    global state
    global history
    global random
    possibilities = []
    if segment in moments:
        m = moments[segment]
        for moment in m:
            if moment["type"] == "notification:playbackImpression":
                updateState(moment.get("impressionData",{}).get("data", {}).get("persistent", {}))
            if moment["type"] == "scene:cs_bs":
                for option in moment["choices"]:
                    if segment != "1A": updateState(moment.get("impressionData",{}).get("data", {}).get("persistent", {}))
                    if "segmentId" in option:
                        p = groupHandler([option["segmentId"]])
                    elif "sg" in option:
                        p = groupHandler(segmentGroups[option["sg"]])
                    elif moment["trackingInfo"]["optionType"] == "fakeOption":
                        continue
                    else:
                        raise Exception(option["id"])
                    possibilities += p
            if moment["type"] == "notification:action":
                possibilities.append(segment)
    if segment in segmentGroups:
        possibilities += groupHandler(segmentGroups[segment])
    if debug: print("poss="+repr(possibilities),file=stderr)
    if not possibilities:
#        raise Exception("hoi")
        possibilities += groupHandler(segmentGroups["respawnOptions"])
        if debug: print("respawn="+repr(possibilities),file=stderr)
    return random.choice(possibilities)

def get_segment_info(segment):
    _ = thumbnails.get(segment, {})
    return {"id": segment, "url": _["image"]["styles"]["backgroundImage"][4:-1] if "image" in _ else "", "caption": _.get("description", "No caption"), "chose": segmentMap.get(segment, "No caption ({})".format(segment))}

def bandersnatch():
    global state
    concat, options = [], []
    state = dict(initial_state)
    current_segment = "1A"
    while True:
      state["length"] += smap[current_segment]["endTimeMs"] - smap[current_segment]["startTimeMs"]
      if current_segment[:3].lower() == "0cr":

          options.append(get_segment_info(current_segment))
          concat.append(current_segment)
          if debug: print(f"chose={current_segment}",file=stderr)

          options.append(get_segment_info("IDNT"))
          concat.append('IDNT')
          if debug: print(f"chose=IDNT",file=stderr)

          state["length"] += 10
          break
      options.append(get_segment_info(current_segment))
      concat.append(current_segment)
      if debug: print(f"chose={current_segment}",file=stderr)
      current_segment = followTheStory(current_segment)
      if current_segment is None:
        break
    return concat, options, msToTS(state["length"])

if __name__ == "__main__":
  concat,options,length = bandersnatch()
  if len(argv) == 1 or argv[1] != "-no":
    with open(f"out/{seed}.txt", "w") as f:
      f.write("\n".join(f"file '../segments/{_id}.mp4'" for _id in concat))
  print(f"{seed} {length}")
