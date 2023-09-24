import requests

BASE = "http://127.0.0.1:5000/"

# PUT
video_id = 123
# headers = {"Content-Type":"application/json"}
data = {'name':'lolol', 'views':4, 'likes':0}
files = {'image': ('image.jpg', open('image.jpg', 'rb'))}

response = requests.put(BASE + f"video/{video_id}", data=data, files=files)
print(response.json())

# LIST
response = requests.get(BASE + "videos")
if response.status_code == 200:
    video_list = response.json()
    print("List of Videos:")
    for video in video_list:
        print(f"Video ID: {video['id']}, Name: {video['name']}, Views: {video['views']}, Likes: {video['likes']}")
else:
    print(f"Error: {response.status_code} - {response.text}")

# DELETE
response = requests.delete(BASE + "video/123")
print("Successfully deleted.") if response.status_code == 204 else print(f"Failed: {response.status_code}")

# GET
BASE = "http://127.0.0.1:5000/"

params = {'param1':'value1', 'param2': 123}
response = requests.get(BASE + "video/1", params=params)
print(response.json(), response.status_code)