from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello_world():
    return jsonify({
        "message": "Hello World",
        "status": "success",
        "version": "1.0.0"
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "hello-world-service"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
    
# 添加此函数以便在测试中使用
def run_app():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)