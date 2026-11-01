exec(open(__file__.replace('audio_jobs.py','generate.py')).read().split('cmd=sys.argv[1]')[0])
items={'vo1': ('tts', '空调开着，就在换气？'), 'vo2': ('tts', '普通空调，主要循环调温。'), 'vo3': ('tts', '新风系统，引入室外空气。'), 'vo4': ('tts', '一个管冷暖，一个管换气。'), 'vo5': ('tts', '璀璨 Mini 新风，让家自在呼吸。')}
for key,(mode,prompt) in items.items():
 if key not in s['jobs']:
  a=['node','create','audio','--title',key,'--mode',mode,'--prompt',prompt]
  if mode=='tts':a+=['--voice-name','优雅女声']
  else:a+=['--model','seed_music_1.0','--duration','30']
  d=cli(*a);s['jobs'][key]={'nodeId':d['data']['node']['nodeId'],'submitId':str(uuid.uuid4()),'prompt':prompt,'kind':'audio'};save()
 j=s['jobs'][key]
 if not j.get('submitted'):
  d=cli('node','quote','--node-id',j['nodeId']);cost=d['data']['totalMaxCredits'];assert s['reserved']+cost<=928;print('QUOTE',key,cost,flush=True)
  conf=cli('node','confirm','--node-id',j['nodeId'],'--credit-ceiling',cost)
  j.update(reserved=cost,submitted='submitting');s['reserved']+=cost;save()
  d=cli('node','run','--node-id',j['nodeId'],'--submit-id',j['submitId'],'--credit-token',conf['data']['creditConfirmationToken']);j['submitted']='accepted';j['requestId']=d.get('meta',{}).get('requestId');save();print('ACCEPTED',key,flush=True)
