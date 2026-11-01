"""Submit the two explicitly authorized video generations once; never regenerate."""
import json
import subprocess
from pathlib import Path

STATE = Path(__file__).with_name('job_state.json')
state = json.loads(STATE.read_text())
project = state['canvasId']
items = [state['items'][k] for k in ('lounge', 'dining')]
assert all(i['videoRuns'] == 0 for i in items), 'Already submitted; use operation status, never run this again.'

def cli(args):
    p = subprocess.run(['dreamina-canvas', *args], capture_output=True, text=True)
    raw = p.stdout.strip() or p.stderr.strip()
    data = json.loads(raw)
    if p.returncode or not data.get('ok'):
        # No credential material appears in the errors returned here.
        raise RuntimeError(json.dumps({'returncode': p.returncode, 'error': data.get('error')}, ensure_ascii=False))
    return data

node_args = [v for i in items for v in ('--node-id', i['videoNodeId'])]
quote = cli(['node', 'quote', '--project-id', project, *node_args])
q = quote['data']
assert q.get('confirmable') and len(q['items']) == 2 and all('maxCredits' in i and 'error' not in i for i in q['items'])
assert 0 <= q['totalMaxCredits'] <= 500, 'User ceiling exceeded; no generation.'
state['quote'] = q
state['quoteRequestId'] = quote.get('meta', {}).get('requestId')
STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2))
approval = cli(['node', 'confirm', '--project-id', project, *node_args, '--credit-ceiling', str(q['totalMaxCredits'])])
token = approval['data']['creditConfirmationToken']
state['authorizedCreditCeilingThisBatch'] = q['totalMaxCredits']
for i in items:
    i['videoRuns'] = 1
    i['dispatchState'] = 'dispatching_do_not_resubmit'
STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2))
submit_args = [v for i in items for v in ('--submit-id', i['videoSubmitId'])]
result = cli(['node', 'run', '--project-id', project, *node_args, *submit_args, '--credit-token', token])
del token, approval
state['submission'] = result['data']
state['submissionRequestId'] = result.get('meta', {}).get('requestId')
for item, response in zip(items, result['data']['items']):
    assert item['videoNodeId'] == response['nodeId']
    item['dispatchState'] = response['state']
    item['resources'] = response.get('resources', [])
STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2))
print(json.dumps({'quotedMaxCredits': q['totalMaxCredits'], 'submission': result['data'], 'requestId': state['submissionRequestId']}, ensure_ascii=False))
