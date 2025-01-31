from flask import Flask, render_template, request, flash, jsonify
from flask_wtf import FlaskForm
from flask_cors import CORS
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
import os
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect  # 新增导入
from jsonFileHandler import *
from actionHandler import *
from stringHandler import *
import uuid
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # 图片上传的目录
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # 允许的文件类型
app.config['JSON_FILE_PATH'] = "json/"
CORS(app, resources={r"/upload": {"origins": "*"}})

# 确保上传目录存在
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# 检查文件扩展名是否允许
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# 定义表单
class RichTextForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/find/', methods=['POST'])
def find():
    totalList = []
    findStr = ''
    suuid = ''
    form = RichTextForm()

    if request.method == 'POST':
        for key in request.form:
            findStr = request.form[key]

    ## convert seach string to list
    search_key_list = str_upper_split_to_list(findStr)

    ## collect file name into a list.
    ## 文件名列表
    file_list = get_json_file_list()
    itemList = []
    for f in file_list:
        ## read json from json file.
        ### This file path should be based on root path.  becasue it's just included by app.py, which is in root path.
        itemListInJson = json_load_from_file(f)
        ## 遍历所有item.
        for k, item in itemListInJson.items():
            totalList.append(item)
            allConditionMeet = True
            for search in search_key_list:
                print("for search")
                print(search)
                print(item["title"])
                if not search_res_as_expected(search, item["title"]):
                    allConditionMeet = False
            if allConditionMeet:
                itemList.append(item)
                if suuid == '':
                    suuid = item['uid']
                    item = itemListInJson[suuid]
                    form.title.data = item['title']
                    form.content.data = item['content']
    return render_template('index.html',  findStr=findStr, form=form, suuid=suuid, itemList=itemList, totalList=totalList)


# 图片上传接口
@app.route('/upload_image', methods=['POST'])
def upload_image():
    print("in upload image")
    if 'upload' not in request.files:
        print("in upload not")

        return jsonify({'error': 'No file part'}), 400
    file = request.files['upload']
    if file.filename == '':
        print("in upload not filename")

        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        print("in upload normal")

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        # 返回图片的 URL
        image_url = f"http://127.0.0.1:5000/static/uploads/{filename}"
        print(image_url)
        return jsonify({'uploaded': 1, 'fileName': filename, 'url': image_url})
    return jsonify({'error': 'File type not allowed'}), 400

# 路由和视图函数
@app.route('/<string:suuid>/', methods=['GET', 'POST'])
def index(suuid):
    f = '1'
    findStr=''
    form = RichTextForm()
    item = dict()
    itemList=[]
    totalList=[]
    dictItems = json_load_from_file(f)
    if suuid not in dictItems:
        suuid = str(uuid.uuid4()).replace('-', '')
        item['title'] = 'ttt'
        item['content'] = 'ccc'
        item['uid'] = suuid
    elif form.validate_on_submit():#//?post?
        item['title'] = form.title.data
        item['content'] = form.content.data
        item['uid'] = suuid
        dictItems[suuid] = item
        json_dump_to_file(f,dictItems)
    else:
        item = dictItems[suuid]
        form.title.data =item['title']
        form.content.data = item['content']

    return render_template('index.html',  findStr=findStr, form=form, suuid=suuid, itemList=itemList, totalList=totalList)

# 路由和视图函数
#@app.route('/', methods=['GET', 'POST'])
#def index():
#    form = RichTextForm()
#    if form.validate_on_submit():
#        title = form.title.data
#        content = form.content.data
#    return render_template('index.html', form = form)

if __name__ == '__main__':
    app.run(debug=True)