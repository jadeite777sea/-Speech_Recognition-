from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from flask import Response
import json
from summary import generator
from sqlalchemy.orm import relationship
import copy

app = Flask(__name__)
api = Api(app)

# 配置 SQLAlchemy 和 MySQL 数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Zy737801%40@127.0.0.1/text'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False  # 这个配置通常无须更改
app.config['JSON_AS_ASCII'] = False  # 确保 Flask 正确处理非 ASCII 字符

db = SQLAlchemy(app)


content_g=""
# 定义数据库模型
class Text(db.Model):
    __tablename__ = 'texts'
    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(255), nullable=False)
    text_content = db.Column(db.Text, nullable=False)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=True)

    def __repr__(self):
        return f'<Text {self.table_name}>'

class Meeting(db.Model):
    __tablename__ = 'meetings'
    id = db.Column(db.Integer, primary_key=True)
    meeting_name = db.Column(db.String(255), nullable=False)
    texts = relationship('Text', backref='meeting', lazy=True)

    def __repr__(self):
        return f'<Meeting {self.meeting_name}>'


# 创建表（如果尚未创建）
with app.app_context():
    db.create_all()
# 定义 Swagger 文档模型
text_get_content_model= api.model('Text', {
    'table_name': fields.String(required=True, description='The name of the table'),
    'text_content': fields.String(required=True, description='The content of the text')
})

text_store_model = api.model('TextStore', {
    'text_name': fields.String(required=True, description='The name of the text'),
    'meeting_name': fields.String(required=True, description='The name of the meeting')
})

@api.route('/store_text')
class StoreText(Resource):
    @api.expect(text_store_model)
    @api.doc(description='Stores a text entry associated with a specific meeting.')
    def post(self):
        try:
            # 从请求中获取文本名称、内容和会议名称
            text_name = request.json.get('text_name')
            meeting_name = request.json.get('meeting_name')

            global content_g
            text_content_g = copy.copy(content_g)
            content_g = ''

            # 查找指定的会议名称
            meeting = Meeting.query.filter_by(meeting_name=meeting_name).first()
            if not meeting:
                return {'message': 'Meeting not found'}, 404

            # 创建文本实例并关联到会议
            new_text = Text(table_name=text_name, text_content=text_content_g, meeting_id=meeting.id)
            db.session.add(new_text)
            db.session.commit()

            return {'message': 'Text stored successfully'}, 201

        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500


    @api.route('/get_text_names_by_meeting')
    class GetTextNamesByMeeting(Resource):
        @api.doc(description='Get all text names for a specific meeting by its name')
        @api.param('meeting_name', 'The name of the meeting', required=True)
        def get(self):
            try:
                # 从请求参数中获取会议名称
                meeting_name = request.args.get('meeting_name', type=str)

                if not meeting_name:
                    return {'message': 'Meeting name must be provided'}, 400

                # 查找指定会议名称的会议
                meeting = Meeting.query.filter_by(meeting_name=meeting_name).first()
                if not meeting:
                    return {'message': 'Meeting not found'}, 404

                # 根据会议ID查找文本
                texts = Text.query.filter_by(meeting_id=meeting.id).with_entities(Text.table_name).all()
                if not texts:
                    return {'message': 'No texts found for the specified meeting'}, 404

                names = [name[0] for name in texts]  # 提取所有的 table_name 并转换为简单的列表
                response_data = {'names': names}
                response_json = json.dumps(response_data)
                return Response(response=response_json, status=200, mimetype='application/json')

            except Exception as e:
                error_data = {'message': str(e)}
                error_json = json.dumps(error_data)
                return Response(response=error_json, status=500, mimetype='application/json')

            

@api.route('/get_text_content/<string:meeting_name>/<string:text_name>')
@api.doc(params={'meeting_name': 'The name of the meeting', 'text_name': 'The name of the text'})
class GetTextContent(Resource):
    @api.response(200, 'Success', text_get_content_model)
    @api.response(404, 'Text not found')
    @api.response(500, 'Internal Server Error')
    @api.doc(description='Get the content of the text by its name and meeting name')
    def get(self, meeting_name, text_name):
        try:
            # 根据会议名称查找会议
            meeting = Meeting.query.filter_by(meeting_name=meeting_name).first()
            if not meeting:
                return {'message': 'Meeting not found'}, 404

            # 查询指定会议ID和文本名称的内容
            text_record = Text.query.filter_by(meeting_id=meeting.id, table_name=text_name).first()
            if text_record:
                # 构建响应数据
                response_data = {
                    'table_name': text_record.table_name,
                    'text_content': text_record.text_content
                }
                return response_data, 200
            else:
                # 如果没有找到对应的记录
                return {'message': 'Text not found for the specified meeting name and text name'}, 404
        except Exception as e:
            # 处理异常情况
            return {'message': str(e)}, 500


@api.route('/delete_text_content/<string:meeting_name>/<string:text_name>')
@api.doc(params={'meeting_name': 'The name of the meeting', 'text_name': 'The name of the text'})
class DeleteTextContent(Resource):
    @api.response(200, 'Record deleted successfully')
    @api.response(404, 'Text not found')
    @api.response(500, 'Internal Server Error')
    @api.doc(description='Delete the content of the text by its name and meeting name')
    def delete(self, meeting_name, text_name):
        try:
            # 根据会议名称查找会议
            meeting = Meeting.query.filter_by(meeting_name=meeting_name).first()
            if not meeting:
                return {'message': 'Meeting not found'}, 404

            # 查询并删除指定会议ID和文本名称的记录
            text_record = Text.query.filter_by(meeting_id=meeting.id, table_name=text_name).first()
            if text_record:
                db.session.delete(text_record)
                db.session.commit()
                return {'message': 'Record deleted successfully'}, 200
            else:
                # 如果没有找到对应的记录
                return {'message': 'Text not found for the specified meeting name and text name'}, 404
        except Exception as e:
            # 处理异常情况
            return {'message': str(e)}, 500



@api.route('/get_all_meetings')
class GetAllMeetings(Resource):
    @api.response(200, 'Success')
    @api.response(500, 'Internal Server Error')
    @api.doc(description='Get all meeting names')
    def get(self):
        try:
            # 查询所有会议名称
            meetings = Meeting.query.with_entities(Meeting.meeting_name).all()
            if meetings:
                # 提取会议名称列表
                meeting_names = [meeting[0] for meeting in meetings]
                response_data = {'meetings': meeting_names}
                return response_data, 200
            else:
                # 如果没有会议记录
                return {'message': 'No meetings found'}, 404
        except Exception as e:
            # 处理异常情况
            return {'message': str(e)}, 500
        
# 定义用于API的模型
meeting_create_model = api.model('MeetingCreate', {
    'meeting_name': fields.String(required=True, description='The name of the meeting')
})

@api.route('/create_meeting')
class CreateMeeting(Resource):
    @api.expect(meeting_create_model)
    @api.doc(description='Create a new meeting with a specified name.')
    @api.response(201, 'Meeting created successfully')
    @api.response(400, 'Meeting name already exists')
    @api.response(500, 'Internal Server Error')
    def post(self):
        try:
            # 从请求中获取会议名称
            meeting_name = request.json.get('meeting_name')

            # 检查是否已经存在相同的会议名称
            existing_meeting_by_name = Meeting.query.filter_by(meeting_name=meeting_name).first()

            if existing_meeting_by_name:
                return {'message': f'Meeting with name "{meeting_name}" already exists'}, 400

            # 创建新的会议实例，id 由数据库自动生成
            new_meeting = Meeting(meeting_name=meeting_name)
            db.session.add(new_meeting)
            db.session.commit()

            return {'message': 'Meeting created successfully', 'meeting_id': new_meeting.id}, 201

        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500


# 定义输入模型，用于验证和文档
text_input_model = api.model('TextInput', {
    'content': fields.String(required=True, description='The content to process')
})


# 创建接受文本内容的API
@api.route('/text_summary')
class ProcessText(Resource):
    @api.expect(text_input_model)
    @api.response(200, 'Success')
    @api.response(400, 'Validation Error')
    @api.doc(description='Accept text content, process it, and return the summmary')
    def post(self):
        try:
            # 获取请求中的 JSON 数据
            data = request.json
            content = data.get('content')
            
            # 处理文本内容
            processed_content = generator(content).content

            global content_g

            content_g=copy.copy(processed_content)


            
            # 构建响应数据
            response_data = {'processed_content': processed_content}
            response_json = json.dumps(response_data)
            
            return Response(response=response_json, status=200, mimetype='application/json')
        except Exception as e:
            # 处理异常情况
            error_data = {'message': str(e)}
            error_json = json.dumps(error_data)
            return Response(response=error_json, status=500, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)


