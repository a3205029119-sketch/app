import streamlit as st
from openai import OpenAI

# 1. 页面配置
st.set_page_config(page_title="AI Assistant", page_icon="🤖")
st.markdown("<h1 style='text-align: center;'>AI Assistant</h1>", unsafe_allow_html=True)

# 2. 侧边栏配置


# 3. 初始化历史记录 (统一使用 "messages" 复数)
if "messages" not in st.session_state:
    st.session_state.messages = [{
            "role": "system", 
            "content": "你是 DeepSeek AI 助手。回答数学问题时，请务必遵守：1. 行内公式用单美元符号 $ 包裹（例如 $x^2$）；2. 独立公式块用双美元符号 $$ 包裹。不要使用 \[ 或 \(。"
        }]

# 4. 渲染历史消息
for msg in st.session_state.messages:
    # 修正：字典取值用 ["role"]
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. 处理用户输入
if prompt := st.chat_input("Ask DeepSeek..."):

    # 检查 API Key 是否存在
    

    # 初始化客户端 (放在这里确保有了 Key 再初始化)
    client = OpenAI(api_key="sk-d5e3cfb804924c01a88c24fe4e33de8d", base_url="https://api.deepseek.com")

    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)
    # 保存用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 获取 AI 回复
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            stream = client.chat.completions.create(
                model="deepseek-chat",
                # 修正：确保这里引用的也是 session_state.messages
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True
            )

            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

            # 保存 AI 回复
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:

            st.error(f"Error: {str(e)}")





