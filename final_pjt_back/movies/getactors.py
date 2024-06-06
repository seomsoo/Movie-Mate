import requests
import json

# TMDB API 키 (Bearer 토큰)
api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1ZmVmMGYyZmMxYmVjMWQwNTI4MTkzNmMzMzJjMDQxMiIsInN1YiI6IjY2M2Q4ZWE5YWIwZDNjOWY5YzUwZDY0NyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.k9KRXAEe9cUbxgzudrpXI5A-bdGh9yPS2atfI4qM41Y'

# 헤더 설정
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json;charset=utf-8'
}

# Actor 모델 데이터 API 요청
# API 결과를 JSON 형식으로 담을 리스트
actor_res = []
unique_actors = set()

for pageNum in range(1, 51):
    url = f'https://api.themoviedb.org/3/movie/popular?language=ko-KR&page={pageNum}'
    response = requests.get(url, headers=headers)
    
    # 응답 상태 코드 확인
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        continue
    
    data = response.json()

    for item in data['results']:
        movie_id = item['id']
        response_details = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?append_to_response=credits',
            headers=headers
        )
        
        # 응답 상태 코드 확인
        if response_details.status_code != 200:
            print(f"Error: {response_details.status_code} for movie ID {movie_id}")
            continue
        
        details = response_details.json()
        actors = details.get('credits', {}).get('cast', [])

        for actor in actors:
            if actor['id'] not in unique_actors:
                unique_actors.add(actor['id'])
                actor_dict = {
                    "model": "movies.actor",
                    "pk": actor['id'],
                    "fields": {
                        "name": actor['name'],
                    }
                }
                actor_res.append(actor_dict)

# JSON 파일로 저장
with open('actors.json', 'w', encoding='utf-8') as f:
    json.dump(actor_res, f, ensure_ascii=False, indent=4)
