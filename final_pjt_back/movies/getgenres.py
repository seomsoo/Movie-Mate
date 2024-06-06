import requests
import json

# TMDB API 키 (Bearer 토큰)
api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1ZmVmMGYyZmMxYmVjMWQwNTI4MTkzNmMzMzJjMDQxMiIsInN1YiI6IjY2M2Q4ZWE5YWIwZDNjOWY5YzUwZDY0NyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.k9KRXAEe9cUbxgzudrpXI5A-bdGh9yPS2atfI4qM41Y'

# 헤더 설정
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json;charset=utf-8'
}

# 장르 데이터 API 요청
url = 'https://api.themoviedb.org/3/genre/movie/list?language=ko-KR'
response = requests.get(url, headers=headers)

# 응답 상태 코드 확인
if response.status_code != 200:
    print(f"Error: {response.status_code}")
else:
    data = response.json()

    # API 결과를 JSON 형식으로 담을 리스트
    genres_res = []

    for item in data['genres']:
        genre_dict = {
            "model": "movies.genre",
            "pk": item['id'],
            "fields": {
                "name": item['name'],
            }
        }
        genres_res.append(genre_dict)

    # JSON 파일로 저장
    with open('genres.json', 'w', encoding='utf-8') as f:
        json.dump(genres_res, f, ensure_ascii=False, indent=4)
    print("Genres data saved to genres.json")
