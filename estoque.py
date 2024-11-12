import requests
import json
import os

url = 'https://api.mileexpress.com.br/v1/warehouse/stock'
headers = {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZjY2ODliYWNlMWYyNzIyZmMxNmQ3NjI1MWMxNGIzNjg3NzYzYmZhOTJhZTNiYjMzNDc4MGJmN2ZlN2MxM2YzNGJhNzkxOGU4NjZhNDkwMTkiLCJpYXQiOjE3MzEzNDk4OTcsIm5iZiI6MTczMTM0OTg5NywiZXhwIjoxNzMxNDM2Mjk3LCJzdWIiOiI5MiIsInNjb3BlcyI6WyIqIl19.r6ho_R3pISB8kcKSv6upzoyuoa3kW78fVoKmyjjxAU9U4VeMraAxDvF8kZSw_pSlq2cg8RB583Wszht3xQddc6XU6mZTWkZjjFeTusxuAscqgQy39edfkh0BJkRC9clpYUuWvxfyXcCXY4CidSexnUJ03NmGqZLrifCWj6hmFR51-GoziqodwiTPjPYkSohTNHHO4qtC3rqj3rMsh-WOaTkn1dPr04SbxeNaSgmIIlmmQSEkgiOFtraBUsgLRIY-NmcgqzIo1sCr-PLB6hoLhx2kMgntFH157xGx4O4BNRiM7blc4fb7o_TzjpdqKhiwLvCfIiLtslsPlxWvcd-AHAgarMAUbXqG1cIOWQQ0OxcV4mJ2E_P09KOUQni3LU8sPmLmL-bjyM_9klTom39rvO1fUG_4ZehiXWAw9Cwu36DCTDRngjkXB_tL_LNcag0GBg-o2MpSV5lm5SD9-wsmnPUqbr3BIWj5ve-Z5R62Nx2sxYhvnMl22j_hgsbPdCpX7i6BGQ7GEP41hkB47WrFBmBzFGV7tU7CaIJz2wYDH1XJOs8yPFEfIlhMaIH3c_oGuenWFr1fyM0w3e4ge0jUJn2sQkQTaTkuy6EKIk6TYyEpJ8vcV6y9cimhuppNRSZV9GLadVLVfbPy9oE6BZskA5XxA-mt3_t3UysT-EDDi7Y'
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
