import psycopg2

# データベース接続情報
DB_NAME = "fanclub_db"
DB_USER = "fanclub_admin"
DB_PASSWORD = "password123"
DB_HOST = "localhost"
DB_PORT = "5432"

def connect_db():
    """データベースに接続する"""
    return psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )

def add_member():
    """会員を新規登録する"""
    name = input("名前を入力してください: ")
    email = input("メールアドレスを入力してください: ")
    phone = input("電話番号を入力してください: ")

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO members (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
    conn.commit()
    cur.close()
    conn.close()
    print("会員が登録されました！")

def list_members():
    """会員一覧を表示する"""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM members")
    members = cur.fetchall()
    cur.close()
    conn.close()

    print("\n=== 会員一覧 ===")
    for member in members:
        print(f"ID: {member[0]}, 名前: {member[1]}, メール: {member[2]}, 電話: {member[3]}, 入会日: {member[4]}")
    print("================\n")

def update_member():
    """会員情報を更新する"""
    member_id = input("更新する会員のIDを入力してください: ")
    new_name = input("新しい名前を入力してください (変更なしの場合はEnter): ")
    new_email = input("新しいメールアドレスを入力してください (変更なしの場合はEnter): ")
    new_phone = input("新しい電話番号を入力してください (変更なしの場合はEnter): ")

    conn = connect_db()
    cur = conn.cursor()

    if new_name:
        cur.execute("UPDATE members SET name = %s WHERE id = %s", (new_name, member_id))
    if new_email:
        cur.execute("UPDATE members SET email = %s WHERE id = %s", (new_email, member_id))
    if new_phone:
        cur.execute("UPDATE members SET phone = %s WHERE id = %s", (new_phone, member_id))

    conn.commit()
    cur.close()
    conn.close()
    print("会員情報が更新されました！")

def delete_member():
    """会員を削除する"""
    member_id = input("削除する会員のIDを入力してください: ")

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM members WHERE id = %s", (member_id,))
    conn.commit()
    cur.close()
    conn.close()
    print("会員が削除されました！")

def main():
    """メニューを表示し、ユーザーの操作を受け付ける"""
    while True:
        print("\n=== ファンクラブ会員管理システム ===")
        print("1: 会員を追加")
        print("2: 会員一覧を表示")
        print("3: 会員情報を更新")
        print("4: 会員を削除")
        print("5: 終了")
        
        choice = input("選択してください: ")

        if choice == "1":
            add_member()
        elif choice == "2":
            list_members()
        elif choice == "3":
            update_member()
        elif choice == "4":
            delete_member()
        elif choice == "5":
            print("システムを終了します。")
            break
        else:
            print("無効な選択です。もう一度試してください。")

if __name__ == "__main__":
    main()
