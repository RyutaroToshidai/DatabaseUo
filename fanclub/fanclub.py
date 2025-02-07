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
    
    cur.execute("SELECT * FROM members WHERE username = %s OR email = %s", (username, email))
    existing_user = cur.fetchone()
    
    if existing_user:
        print("すでに作成済みです")
    else:
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
        print("会員情報: ", tuple(str(col) for col in member))  
    else:
        print("該当する会員が見つかりません")
    cur.close()
    conn.close()

def view_all_members():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT id, username, email, role FROM members")
    members = cur.fetchall()
    
    if members:
        print("すべての会員情報:")
        for member in members:
            print(f"ID: {member[0]}, ユーザー名: {member[1]}, メールアドレス: {member[2]}, 役職: {member[3]}")
    else:
        print("会員が見つかりません。")
    
    cur.close()
    conn.close()


def view_member(user_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT id, username, email FROM members WHERE id = %s", (user_id,))
    member = cur.fetchone()
    if member:
        print("会員情報: ")
        print(f"ID: {member[0]}")
        print(f"ユーザー名: {member[1]}")
        print(f"メールアドレス: {member[2]}")
    else:
        print("該当する会員が見つかりません")
    cur.close()
    conn.close()

def delete_member(user_id):
    conn = connect_db()
    cur = conn.cursor()

    # アカウントの存在確認
    cur.execute("SELECT role FROM members WHERE id = %s", (user_id,))
    user = cur.fetchone()

    if not user:
        print("該当するアカウントが存在しません。")
    elif user[0] == "staff":
        print("管理者アカウントは削除できません。")
    else:
        confirmation = input("本当に削除しますか？ (y/n): ")
        if confirmation.lower() == "y":
            cur.execute("DELETE FROM members WHERE id = %s AND role = 'customer'", (user_id,))
            conn.commit()
            print("削除完了")
        else:
            print("削除をキャンセルしました。")
    
    cur.close()
    conn.close()

def update_member(user_id):
    conn = connect_db()
    cur = conn.cursor()

    # アカウントの存在確認
    cur.execute("SELECT role FROM members WHERE id = %s", (user_id,))
    user = cur.fetchone()

    if not user:
        print("該当するアカウントが存在しません。")
    elif user[0] == "staff":
        print("管理者アカウントは変更できません。")
    else:
        new_username = input("新しいユーザー名: ")
        new_email = input("新しいメールアドレス: ")
        cur.execute("UPDATE members SET username = %s, email = %s WHERE id = %s", 
                    (new_username, new_email, user_id))
        conn.commit()
        print("更新完了")

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
