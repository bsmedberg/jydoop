import crashstatsutils
import json
import jydoop

setupjob = crashstatsutils.dosetupjob([('processed_data', 'json')])

def map(k, processed_data, context):
    if processed_data is None:
        return

    processed = json.loads(processed_data)

    if processed['version'] != '21.0':
        return

    if processed['build'] != '20130423212553':
        return

    for items in (line.split('|') for line in processed.get('dump', '').splitlines()):
        if len(items) != 7:
            continue

        if items[0] == '0' and items[3].startswith('nsFrameManager::ReResolveStyleContext'):
            context.write(k, (k[7:], processed['signature'], int(items[1])))
            return
