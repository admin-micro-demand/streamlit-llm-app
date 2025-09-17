from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
load_dotenv()

# --------------------------
# 回答を返す関数
# --------------------------
def get_expert_answer(user_input: str, expert_type: str) -> str:
    """入力テキストと選択値を引数にとり、LLMからの回答を返す"""

    # 専門家ごとのシステムメッセージを定義
    if expert_type == "料理の専門家":
        system_msg = "あなたはプロのシェフです。料理に関する質問に詳しく答えてください。"
    elif expert_type == "フィットネスの専門家":
        system_msg = "あなたはプロのフィットネストレーナーです。筋トレや食事に関する質問に専門的に答えてください。"
    else:
        system_msg = "あなたは親切なアシスタントです。一般的に回答してください。"

    # プロンプトテンプレートを作成
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_msg),
        ("user", "{input}")
    ])

    # LLM呼び出し
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    chain = prompt | llm
    response = chain.invoke({"input": user_input})

    return response.content


# --------------------------
# Streamlit UI
# --------------------------
st.title("🔮 LLM Expert Demo App")

st.write("""
このアプリでは、入力したテキストをLLMに渡し、選んだ専門家の観点から回答を生成します。  
以下の手順で操作してください：
1. 専門家の種類をラジオボタンから選びます  
2. テキストを入力して送信します  
3. 選択した専門家になりきったLLMから回答が返ってきます
""")

# ラジオボタンで専門家を選択
expert_type = st.radio(
    "専門家の種類を選んでください：",
    ["料理の専門家", "フィットネスの専門家"]
)

# 入力フォーム
user_input = st.text_input("質問を入力してください：")

if st.button("送信"):
    if user_input.strip():
        answer = get_expert_answer(user_input, expert_type)
        st.subheader("回答結果")
        st.write(answer)
    else:
        st.warning("テキストを入力してください。")
