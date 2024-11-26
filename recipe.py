import requests

# API 호출 함수
def fetch_recipes(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # 오류가 있을 경우 예외 발생
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"API 호출 중 오류 발생: {e}")
        return None

# 음식 이름과 재료로 필터링하는 함수
def filter_recipes(data, food_name, ingredient):
    recipes = data.get('COOKRCP01', {}).get('row', [])
    matching_recipes = []

    for recipe in recipes:
        if food_name in recipe['RCP_NM'] and ingredient in recipe['RCP_PARTS_DTLS']:
            matching_recipes.append(recipe)

    return matching_recipes

# 메인 코드
if __name__ == "__main__":
    # API URL
    api_url = "http://openapi.foodsafetykorea.go.kr/api/e6c3d864f85342fa9756/COOKRCP01/json/1/1000"
    
    # API 데이터 가져오기
    data = fetch_recipes(api_url)
    if data:
        # 사용자 입력
        food_name = input("찾고자 하는 음식 이름을 입력하세요: ")
        ingredient = input("필요한 재료를 입력하세요: ")

        # 필터링
        results = filter_recipes(data, food_name, ingredient)

        # 결과 출력
        if results:
            print(f"'{food_name}'와(과) '{ingredient}'를 포함하는 레시피 목록:")
            for idx, recipe in enumerate(results, start=1):
                print(f"\n{idx}. 음식 이름: {recipe['RCP_NM']}")
                print(f"   재료: {recipe['RCP_PARTS_DTLS']}")
                print(f"   레시피:")
                # 만드는 과정 출력 (필드는 JSON 구조에 따라 다를 수 있음)
                for step_idx in range(1, 21):  # 최대 20단계까지 확인
                    step_key = f"MANUAL{str(step_idx).zfill(2)}"
                    step_description = recipe.get(step_key)
                    if step_description:  # 값이 있을 경우 출력
                        print(f"      {step_description}")
        else:
            print(f"'{food_name}'와(과) '{ingredient}'를 포함하는 레시피를 찾을 수 없습니다.")
