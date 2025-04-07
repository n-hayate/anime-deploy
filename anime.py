import streamlit as st
import pandas as pd
import os

# CSVファイルに保存してデータを永続化（アプリを再起動しても情報を維持）する例
CSV_FILE = "anime_log.csv"

def load_data():
    """CSVファイルからデータを読み込み、pandas DataFrameを返す"""
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["タイトル", "ジャンル", "評価", "コメント"])

def save_data(df):
    """pandas DataFrameの内容をCSVファイルに保存"""
    df.to_csv(CSV_FILE, index=False)

def main():
    st.title("My Anime Log")
    st.write("自分が観たアニメのタイトル、評価、感想を管理するアプリです。")

    # 1. CSVファイルからデータをロード
    df = load_data()

    # 2. 入力フォーム
    with st.form("anime_form"):
        st.subheader("作品登録フォーム")

        title = st.text_input("アニメタイトルを入力")
        genre = st.selectbox("ジャンルを選択", [
            "アクション", "コメディ", "ストーリー",
            "ラブコメ", "日常", "SF", "その他"
        ])
        rating = st.slider("評価（10点満点）", 1, 10, 5)
        comment = st.text_area("感想・メモ")

        submitted = st.form_submit_button("登録")
        if submitted:
            # タイトルの空チェック（空の場合は登録しない）
            if title.strip() == "":
                st.warning("タイトルが空欄です。入力してください。")
            else:
                new_row = {
                    "タイトル": title.strip(),
                    "ジャンル": genre,
                    "評価": rating,
                    "コメント": comment.strip()
                }
                # 修正箇所：append()の代わりにconcat()を使用
                new_row_df = pd.DataFrame([new_row])
                df = pd.concat([df, new_row_df], ignore_index=True)
                save_data(df)
                st.success(f"『{title.strip()}』を登録しました！")

    # 3. 登録されたアニメ一覧の表示
    st.subheader("アニメ一覧")

    # 3-1. ジャンルで絞り込み
    all_genres = ["All"] + sorted(df["ジャンル"].unique().tolist())
    selected_genre = st.selectbox("絞り込み（ジャンル）", all_genres)

    if selected_genre == "All":
        filtered_df = df
    else:
        filtered_df = df[df["ジャンル"] == selected_genre]

    # 3-2. タイトルで検索（任意）
    search_text = st.text_input("タイトル検索（部分一致）")
    if search_text:
        filtered_df = filtered_df[filtered_df["タイトル"].str.contains(search_text, case=False, na=False)]

    # 3-3. 表示
    st.dataframe(filtered_df)

    # 4. 削除機能（オプション）
    st.subheader("登録削除機能（オプション）")
    delete_title = st.text_input("削除したいアニメタイトルを正確に入力")
    if st.button("削除"):
        before_count = len(df)
        df = df[df["タイトル"] != delete_title]
        after_count = len(df)

        if after_count < before_count:
            save_data(df)
            st.success(f"『{delete_title}』を削除しました。")
            # ページを再読み込みし、表を更新
            st.experimental_rerun()
        else:
            st.warning("該当タイトルが見つかりませんでした。")

if __name__ == "__main__":
    main()
