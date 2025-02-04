import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# .envファイルから環境変数を読み込む
load_dotenv()

app = Flask(__name__)

# PostgreSQLデータベースの設定
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemyオブジェクトの初期化
db = SQLAlchemy(app)

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the Fan Club API! Use /members to see the list.'})

# ユーザーモデルの定義（会員情報）
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    membership_level = db.Column(db.String(50), nullable=False)  # 例: "Regular", "VIP"

    def __repr__(self):
        return f'<User {self.username}>'

# ファンクラブの会員登録API
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        new_user = User(
            username=data['username'],
            email=data['email'],
            membership_level=data['membership_level']
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# 会員リストの取得
@app.route('/members', methods=['GET'])
def get_members():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email, 'membership_level': user.membership_level} for user in users])

# 個別の会員情報取得
@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    user = User.query.get(id)
    if user:
        return jsonify({'id': user.id, 'username': user.username, 'email': user.email, 'membership_level': user.membership_level})
    else:
        return jsonify({'error': 'User not found'}), 404

# 会員情報の削除
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_member(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404

# アプリの起動
if __name__ == '__main__':
    app.run(debug=True)
