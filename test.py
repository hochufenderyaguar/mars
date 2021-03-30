from requests import get, post, delete

print(get('http://localhost:5000/api/v2/users').json())
print(get('http://localhost:5000/api/v2/users/1').json())
print(post('http://localhost:5000/api/v2/users', json={'surname': 'a',
                                                       'name': 'a',
                                                       'age': 1,
                                                       'position': 'a',
                                                       'speciality': 'a',
                                                       'address': 'a',
                                                       'email': 'a',
                                                       'hashed_password': 'a'}).json())
