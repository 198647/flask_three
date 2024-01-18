from flask import Flask, request, render_template, jsonify,redirect,url_for
import os

app = Flask(__name__, static_folder='static')

# 设置静态文件夹
app.config['UPLOAD_FOLDER'] = 'static/resources/uploads'

@app.route('/')
def index():
    return render_template('ik_drive_limbs.html')

# 路由用于处理文件上传
@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']

    if uploaded_file.filename != '':
        # 保存上传的文件到指定目录
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)

        # 检查文件类型并构建模型路径
        if uploaded_file.filename.endswith('.fbx'):
            model_path = os.path.join(app.config['UPLOAD_FOLDER'],uploaded_file.filename)            
        else:
            model_path = '/static/resources/models/pg_ik.fbx'
            
        return jsonify({'success': True, 'model_path': model_path})
    else:
        return jsonify({'success': False})


if __name__ == '__main__':
    app.run(debug=True)
