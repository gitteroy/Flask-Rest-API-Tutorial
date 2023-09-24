from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

videos = {
    1 : 
    {
        'name' : 'lord of the rings',
        'views' : 12,
        'likes' : 20
    },
    2 : 
    {
        'name' : 'return of the kings',
        'views' : 1,
        'likes' : 0
    }
}

@app.route('video', methods=["POST"])
def create_video():
    try:
        data = request.get_json()
        name = data.get('name')
        if name is None:
            return "Name is missing!", 400 # Bad Request
        views = data.get('views', 0)
        likes = data.get('likes', 0)
        video_id = str(uuid.uuid4())
    except:
        return "Error", 500

@app.route('/video/<int:video_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_video(video_id: int):
    if request.method == 'GET':
        try:
            if video_id in videos:
                print(videos[video_id])
                return jsonify(videos[video_id])
        except KeyError as e:
            return f"Video not found: {str(e)}", 404
        except TypeError as e:
            return f"TypeError: {str(e)}", 500
            
    elif request.method == 'PUT':
        data = request.get_json()
        try:
            if video_id in videos:
                video = videos[video_id]
                if 'name' in data: 
                    video['name'] = data['name']
                if 'views' in data: 
                    video['views'] = data['views']
                if 'likes' in data: 
                    video['likes'] = data['likes']
                return jsonify(video), 200
            else:
                return f"Video not found!", 404
        except Exception as e:
            return f"Error: {str(e)}", 500

    elif request.method == "DELETE":
        try:
            if video_id in videos:
                del videos[video_id]
                return "", 204
            else:
                return "Video not found!", 404
        except Exception as e:
            return f"Error: {str(e)}", 500
        
if __name__ == '__main__':
    app.run(debug=True)