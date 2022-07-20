from flask import Flask, request
from flask_restful import Api, Resource, reqparse, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f"Video(name={self.name}, views={self.views}, likes={self.likes})"


video_args = reqparse.RequestParser()
video_args.add_argument(
    "name", type=str, help="Name of the video is required", required=True)
video_args.add_argument(
    "views", type=int, help="Number if views is required", required=True)
video_args.add_argument(
    "likes", type=str, help="Number of likes is required", required=True)

resource_field = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}


class CreateVideo(Resource):
    @marshal_with(resource_field)
    def get(self):
        videos = VideoModel.query.all()
        return videos, 200

    @marshal_with(resource_field)
    def post(self):
        args = video_args.parse_args()
        video = VideoModel(name=args['name'],
                           views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201


class Video(Resource):
    @marshal_with(resource_field)
    def get(self, video_id):
        result = VideoModel.query.get(video_id)
        return result

    @marshal_with(resource_field)
    def patch(self, video_id):
        args = video_args.parse_args()
        video = VideoModel.query.get(video_id)

        if 'views' in args:
            video.views = args['views']

        db.session.add(video)
        db.session.commit()

        return video, 200

    def delete(self, video_id):
        video = VideoModel.query.get(video_id)
        db.session.delete(video)
        db.session.commit()
        return '', 204


api.add_resource(CreateVideo, '/video/')
api.add_resource(Video, '/video/<int:video_id>')

app.run(port=4000, debug=True)
