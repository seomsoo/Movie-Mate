import requests
import json
from datetime import datetime

# TMDB API 키 (Bearer 토큰)
api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1ZmVmMGYyZmMxYmVjMWQwNTI4MTkzNmMzMzJjMDQxMiIsInN1YiI6IjY2M2Q4ZWE5YWIwZDNjOWY5YzUwZDY0NyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.k9KRXAEe9cUbxgzudrpXI5A-bdGh9yPS2atfI4qM41Y'

# 헤더 설정
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json;charset=utf-8'
}

# Movie 모델 데이터 API 요청
# API 결과를 JSON 형식으로 담을 리스트
movie_res = []

for pageNum in range(1, 51):
    url = f'https://api.themoviedb.org/3/movie/popular?language=ko-KR&page={pageNum}'
    response = requests.get(url, headers=headers)
    
    # 응답 상태 코드 확인
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        continue
    
    data = response.json()

    for item in data['results']:
        try:
            movie_id = item['id']
            
            # 영화 세부 정보 요청
            response_details = requests.get(
                f'https://api.themoviedb.org/3/movie/{movie_id}?language=ko-KR&append_to_response=credits,keywords',
                headers=headers
            )
            
            # 응답 상태 코드 확인
            if response_details.status_code != 200:
                print(f"Error: {response_details.status_code} for movie ID {movie_id}")
                continue
            
            details = response_details.json()
            actors = [actor['id'] for actor in details.get('credits', {}).get('cast', [])[:5]]  # 상위 5명의 배우만 가져옴
            keywords = [keyword['name'] for keyword in details.get('keywords', {}).get('keywords', [])]  # 키워드 목록
            
            release_date = item.get('release_date', None)
            if not release_date:
                release_date = None
            else:
                try:
                    datetime.strptime(release_date, '%Y-%m-%d')
                except ValueError:
                    release_date = None


            movie_dict = {
                "model": "movies.movie",
                "pk": item['id'],
                "fields": {
                    "title": item['title'],
                    "released_date": release_date,
                    "overview": item.get('overview', ""),
                    "poster_path": item.get('poster_path', ""),
                    "vote_average": item.get('vote_average', 0),
                    "vote_count": item.get('vote_count', 0),
                    "popularity": item.get('popularity', 0),
                    "runtime": details.get('runtime', 0),  # runtime 정보를 세부 요청에서 가져옴
                    "genres": item.get('genre_ids', []),  # 장르 ID 리스트
                    "actors": actors,  # 배우 ID 리스트
                    "words": ", ".join(keywords),  # 키워드 목록을 문자열로 변환하여 저장
                    "like_users": [],  # 사용자 데이터는 별도로 가져와야 합니다.
                }
            }
            movie_res.append(movie_dict)
        except Exception as e:
            print(f"Error processing movie {item['id']}: {e}")
            continue

# JSON 파일로 저장
with open('movies.json', 'w', encoding='utf-8') as f:
    json.dump(movie_res, f, ensure_ascii=False, indent=4)
