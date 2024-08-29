from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from flask import Response
import json
from summary import generator
app = Flask(__name__)
api = Api(app)

# 配置 SQLAlchemy 和 MySQL 数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Zy737801%40@127.0.0.1/text'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False  # 这个配置通常无须更改
app.config['JSON_AS_ASCII'] = False  # 确保 Flask 正确处理非 ASCII 字符

db = SQLAlchemy(app)

# 定义数据库模型
class Text(db.Model):
    __tablename__ = 'texts'
    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(255), nullable=False)
    text_content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Text {self.table_name}>'

# 创建表（如果尚未创建）
with app.app_context():
    db.create_all()
# 定义 Swagger 文档模型
text_store_model = api.model('TextModel', {
    'name': fields.String(required=True, description='The name of the text'),
    'text': fields.String(required=True, description='The content of the text')
})

text_get_content_model= api.model('Text', {
    'id': fields.Integer(readonly=True, description='The unique identifier of a text record'),
    'table_name': fields.String(required=True, description='The name of the table'),
    'text_content': fields.String(required=True, description='The content of the text')
})

# 创建 API 接口
@api.route('/store_text')
class StoreText(Resource):
    @api.expect(text_store_model)  # 告诉 Swagger 这个端点期望什么样的请求体
    def post(self):
        try:
            # 从请求中获取长文本和文本名称
            text_name = request.json.get('name')
            long_text = request.json.get('text')

            # 检查是否提供了名称和文本
            if not text_name or not long_text:
                return {'message': 'Text name and content must be provided'}, 400

            # 创建文本实例并存储到数据库中
            new_text = Text(table_name=text_name, text_content=long_text)
            db.session.add(new_text)
            db.session.commit()

            return {'message': 'Text stored successfully'}, 201

        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500
    @api.doc(description='Get all text names')
    def get(self):
        try:
            name_list = Text.query.with_entities(Text.table_name).all()
            names = [name[0] for name in name_list]  # 提取所有的 table_name 并转换为简单的列表
            response_data = {'names':  names}
            response_json = json.dumps(response_data)
            return Response(response=response_json, status=200, mimetype='application/json')
        except Exception as e:
            error_data = {'message': str(e)}
            error_json = json.dumps(error_data)
            return Response(response=error_json, status=500, mimetype='application/json')

@api.route('/get_text_content/<string:table_name>')
@api.doc(params={'table_name': 'The name of the table'})
class GetTextContent(Resource):
    @api.response(200, 'Success', text_get_content_model)
    @api.response(404, 'Table name not found')
    @api.response(500, 'Internal Server Error')
    @api.doc(description='Get the content of the table by its name')
    def get(self, table_name):
        try:
            # 查询指定表名的内容
            text_record = Text.query.filter_by(table_name=table_name).first()
            if text_record:
                # 构建响应数据
                response_data = {
                    'id': text_record.id,
                    'table_name': text_record.table_name,
                    'text_content': text_record.text_content
                }
                return response_data, 200
            else:
                # 如果没有找到对应的记录
                return {'message': 'Table name not found'}, 404
        except Exception as e:
            # 处理异常情况
            return {'message': str(e)}, 500

@api.route('/delete_text_content/<string:table_name>')
@api.doc(params={'table_name': 'The name of the table'})
class DeleteTextContent(Resource):
    @api.response(200, 'Record deleted successfully')
    @api.response(404, 'Table name not found')
    @api.response(500, 'Internal Server Error')
    @api.doc(description='Delete the content of the table by its name')
    def delete(self, table_name):
        try:
            # 查询并删除指定表名的记录
            text_record = Text.query.filter_by(table_name=table_name).first()
            if text_record:
                db.session.delete(text_record)
                db.session.commit()
                return {'message': 'Record deleted successfully'}, 200
            else:
                # 如果没有找到对应的记录
                return {'message': 'Table name not found'}, 404
        except Exception as e:
            # 处理异常情况
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


