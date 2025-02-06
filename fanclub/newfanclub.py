import psycopg2

def connect_db():
    conn = psycopg2.connect(
        dbname="fanclub_new", user="fanclub_user", password="1111", host="localhost", port="5432"
    )
    cur = conn.cursor()
    cur.execute("SET client_encoding TO 'UTF8';")  # クライアント側のエンコーディングをUTF-8に設定
    conn.commit()
    return conn

def register():
    conn = connect_db()
    cur = conn.cursor()
    
    print("新規登録")
    username = input("ユーザー名: ")
    email = input("メール: ")
    role = "customer"  # 顧客アカウントのみ登録可能
    
    cur.execute("INSERT INTO members (username, email, role) VALUES (%s, %s, %s)", 
                (username, email, role))
    conn.commit()
    print("登録完了")
    
    cur.close()
    conn.close()

def login():
    conn = connect_db()
    cur = conn.cursor()
    
    print("ログイン")
    username = input("ユーザー名: ")
    email = input("メール: ")
    
    cur.execute("SELECT id, role FROM members WHERE username = %s AND email = %s", (username, email))
    user = cur.fetchone()
    
    if user:
        print("ログイン成功")
        user_id, role = user
        if username == "staff" and email == "staff@ac.jp":
            staff_menu()
        else:
            customer_menu(user_id)
    else:
        print("ログイン失敗")
    
    cur.close()
    conn.close()

def customer_menu(user_id):
    while True:
        print("1. 自分の情報を見る\n2. 自分の情報を更新\n3. 自分のアカウントを削除\n4. ログアウト")
        choice = input("選択: ")
        
        if choice == "1":
            view_member(user_id)
        elif choice == "2":
            update_member(user_id)
        elif choice == "3":
            delete_member(user_id)
            break
        elif choice == "4":
            break
        else:
            print("無効な入力")

def staff_menu():
    while True:
        print("1. 会員一覧を見る\n2. 会員情報を更新\n3. 会員を削除\n4. ログアウト")
        choice = input("選択: ")
        
        if choice == "1":
            view_all_members()
        elif choice == "2":
            member_id = input("更新する会員ID: ")
            update_member(member_id)
        elif choice == "3":
            member_id = input("削除する会員ID: ")
            delete_member(member_id)
        elif choice == "4":
            break
        else:
            print("無効な入力")

def view_member(user_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM members WHERE id = %s", (user_id,))
    member = cur.fetchone()
    if member:
        print("会員情報: ", tuple(str(col) for col in member))  # 明示的にUTF-8で表示
    else:
        print("該当する会員が見つかりません")
    cur.close()
    conn.close()

def view_all_members():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT username FROM members")  # メンバーの名前を取得
    rows = cur.fetchall()
    for row in rows:
        try:
            # EUC_JP → UTF-8 変換
            print(row[0].encode("euc_jp").decode("utf-8"))
        except UnicodeDecodeError as e:
            print(f"エラー: {e} - 該当データ: {row[0]}")  # デコードエラー時の処理
    cur.close()
    conn.close()

def update_member(user_id):
    conn = connect_db()
    cur = conn.cursor()
    new_email = input("新しいメール: ")
    cur.execute("UPDATE members SET email = %s WHERE id = %s", (new_email, user_id))
    conn.commit()
    print("更新完了")
    cur.close()
    conn.close()

def delete_member(user_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM members WHERE id = %s AND role = 'customer'", (user_id,))
    conn.commit()
    print("削除完了")
    cur.close()
    conn.close()

def main():
    while True:
        print("1. ログイン\n2. 新規登録\n3. 終了")
        choice = input("選択: ")
        
        if choice == "1":
            login()
        elif choice == "2":
            register()
        elif choice == "3":
            break
        else:
            print("無効な入力")

if __name__ == "__main__":
    main()
