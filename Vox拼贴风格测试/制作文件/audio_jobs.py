exec(open(__file__.replace('audio_jobs.py','generate.py')).read().split('cmd=sys.argv[1]')[0])
items={
'vo1':('tts','家的好风景，只在眼前吗？'),
'vo2':('tts','让清新，翻山越岭。'),
'vo3':('tts','不开窗，也能换一口新鲜空气。'),
'vo4':('tts','璀璨 Mini 新风系统。'),
'vo5':('tts','让家自在呼吸，让生活慢下来。'),
'vo6':('tts','理想空气，源自璀璨。'),
'music':('music','30秒高端家居品牌摄影拼贴动画配乐，纯器乐，不要人声。聪明、轻盈、温暖、有探索感，像精致Vox mixed media商业解释片而非煽情广告。100 BPM，温暖短音原声钢琴、木质马林巴、轻拨弦、低调圆润贝斯、极轻干爽刷鼓和木质敲击，富有小而巧的切分律动，和声高级。前2秒一个清晰轻巧引子，3-12秒渐进律动，12秒轻巧切换，16-22秒温暖展开，23-25秒自然落在温暖完整和弦并留下尾韵。声音清洁有呼吸感，旋律少留出旁白空间，不要爵士独奏，不要口哨，不要鸟叫，不要音效，不要史诗弦乐，不要强烈电子舞曲。')}
for key,(mode,prompt) in items.items():
 if key not in s['jobs']:
  a=['node','create','audio','--title',key,'--mode',mode,'--prompt',prompt]
  if mode=='tts':a+=['--voice-name','优雅女声']
  else:a+=['--model','seed_music_1.0','--duration','30']
  d=cli(*a);s['jobs'][key]={'nodeId':d['data']['node']['nodeId'],'submitId':str(uuid.uuid4()),'prompt':prompt,'kind':'audio'};save()
 j=s['jobs'][key]
 if not j.get('submitted'):
  d=cli('node','quote','--node-id',j['nodeId']);cost=d['data']['totalMaxCredits'];assert s['reserved']+cost<=1000;print('QUOTE',key,cost,flush=True)
  conf=cli('node','confirm','--node-id',j['nodeId'],'--credit-ceiling',cost)
  j.update(reserved=cost,submitted='submitting');s['reserved']+=cost;save()
  d=cli('node','run','--node-id',j['nodeId'],'--submit-id',j['submitId'],'--credit-token',conf['data']['creditConfirmationToken']);j['submitted']='accepted';j['requestId']=d.get('meta',{}).get('requestId');save();print('ACCEPTED',key,flush=True)
