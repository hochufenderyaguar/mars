from requests import put, get

print(put('http://localhost:5000/api/jobs',
          json={'id': 3,
                'team_leader': 1,
                'job': 'job',
                'work_size': 1,
                'collaborators': '1',
                'is_finished': True
                }).json())

print(put('http://localhost:5000/api/jobs',
          json={'team_leader': 1,
                'job': 'job',
                'work_size': 1,
                'collaborators': '1',
                'is_finished': True
                }).json())

print(put('http://localhost:5000/api/jobs',
          json={'id': 999,
                'team_leader': 1,
                'job': 'job',
                'work_size': 1,
                'collaborators': '1',
                'is_finished': True
                }).json())

print(get('http://localhost:5000/api/jobs').json())
