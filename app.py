from flask import Flask, request, render_template, jsonify,redirect,url_for,send_file,send_from_directory
import os

app = Flask(__name__, static_folder='static')

# 设置静态文件夹
app.config['UPLOAD_FOLDER'] = 'static/resources/uploads'
# app.config['MODELS_FOLDER'] = 'static/resources/models'
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
            name = uploaded_file.filename
        else:
            model_path = '/static/resources/models/pg_ik_Modify_parent.fbx'
            
        return jsonify({'success': True, 'model_path': model_path,'name':name})
    else:
        return jsonify({'success': False})

@app.route('/download/<filename>')
def download_file(filename):
    # 第一个文件夹
    first_directory = os.path.join(app.root_path, 'static', 'resources', 'models')
    # 第二个文件夹
    second_directory = os.path.join(app.root_path, 'static', 'resources', 'uploads')

    # 检查文件是否在第一个文件夹中
    if os.path.exists(os.path.join(first_directory, filename)):
        return send_from_directory(first_directory, filename, as_attachment=True)
    # 检查文件是否在第二个文件夹中
    elif os.path.exists(os.path.join(second_directory, filename)):
        return send_from_directory(second_directory, filename, as_attachment=True)
    # 如果文件在两个文件夹中都不存在
    else:
        return 'File not found', 404


if __name__ == '__main__':
    app.run(debug=True)
