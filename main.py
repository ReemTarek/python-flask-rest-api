from flask import Flask, abort
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///datbase.db'
db = SQLAlchemy(app)
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable= False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(id={i},name= {name}, views = {views}, likes = {likes})" 
db.create_all()

video_put_args= reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes of the video", required=True)

video_update_args= reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes of the video")
resource_fields ={
    'id': fields.Integer,
    'name':fields.String,
    'views':fields.Integer,
    'likes':fields.Integer
}
videos={}

def abort_video_not_found(video_id):
    if video_id not in videos:
        abort(404, "video id is not found...!")
def abort_video_found(video_id):
    if video_id in videos:
        abort(409, "video already exits...!")
class Video(Resource):
    @marshal_with(resource_fields) #serialize objects
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, 'not found')
        return result

    @marshal_with(resource_fields) #serialize objects
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409,'video id taken.....')
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201
    @marshal_with(resource_fields) #serialize objects
    def patch(self,video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, 'not found')
        if  args['name']:
            result.name = args['name']
        
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']
        db.session.commit()

        return result
        

    def delete(self, video_id):
        abort_video_not_found(video_id)
        del videos[video_id]
        return 204

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)