import requests
import json
import os

url = 'https://api.mileexpress.com.br/v1/warehouse/stock'
headers = {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiOTlhYjlkZDk3YmNiYmUwMTc0YzBjMTQ0ZDA5MTliMjRjMWM0YTUzNzZhNzY2ZjhmODIwMWRkMmIxOTIxN2FkNDE3ZGZlYmFkNWZlOGNlNTMiLCJpYXQiOjE3MzE1MDU4MjcsIm5iZiI6MTczMTUwNTgyNywiZXhwIjoxNzMxNTkyMjI3LCJzdWIiOiI5MiIsInNjb3BlcyI6WyIqIl19.Ff5IwSTvOuk5Etckd2Lvx4iexnQ0twBYj2UALKLJkFo-PAjl3rexGjh4QZy9st9jsv_ZZC9TaWajTg9YsIsxeB-Xw5gM-qCo2aQc7NFpaw1IuhPuAQFfZwyDS_BwMG2tmqhaExKoexKYUD5hsh61DWUkq6TdmnhlbIDOix9WsT0txXUA1e3GTQLUGCnorgJpCuGKxNz4JVnKYBlkmynFPpTmZk2CmOg-qGa7TeNFAYVdNZ5JBbvPXbUu5b8nXcdy5pF-W33MOgbIyDleIFuVgOWEjpsep4VJBWH1wgbXcs3B5ectHxcB2roYBHTh5DtSx69j4N9Sz9BO1BQliRYWdnmBzhPzBSp4E5x-fSF9DWlAuS-M2G3_m-5zq67hmS5r4iUC55xKFduFcvYOKj8UAKOjBADWw3YBSg4pPX7UDxajLUDy8sAnyi-MABoCHdSyRJo_I_Ci2jgc2klPx_lRs7cPX7YPVJa0wo-DXAu4tHD3US57HArIseS_KJ5aQD2wmdkccW62cO4zgK_hElqTuY-iQtFptiS-KAlTR0WRocT4GFkVM_Nx2E9YKNqwKe3a5PBmblz-FKZ4KuaYCsWKoY8kMeC6GQnc6-zUc52ysljoCE5R86Jr_IauXNmFqVoL05Jzb6erYs5VeFJqFya5oLRv836aKMh_TLvOpwW0iTY'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Define the file path for the JSON output in the specified folder
    file_path = os.path.join('E:\\Mile_Express\\Estoque', 'response.json')

    # Write the JSON response to a file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(response.json(), f, ensure_ascii=False, indent=4)

    print(f"Response saved to {file_path}")
else:
    print(f"Error: {response.status_code} - {response.text}")
