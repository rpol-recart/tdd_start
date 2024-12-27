import json

mess = {'Detection': {'cam0': [],
                      'cam1': []},
        'workload': 0}

with open('./tests/sample_messages/sample_message1.json', 'w') as f:
    json.dump(mess, f, indent=4, sort_keys=True)
