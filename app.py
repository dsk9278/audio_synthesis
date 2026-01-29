from google.cloud import texttospeech

import streamlit as st


def synthesize_speach(text, lang='日本語', gender='default'):
    gender_type = {
        'default' : texttospeech.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED,
        'male' : texttospeech.SsmlVoiceGender.MALE,
        'female' : texttospeech.SsmlVoiceGender.FEMALE,
        'neutral' : texttospeech.SsmlVoiceGender.NEUTRAL,
    }

    lang_code = {
        '英語' : 'en-US',
        '日本語' : 'ja-JP'
    }

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=lang_code[lang], ssml_gender=gender_type[gender]
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response


st.title('音声出力アプリ')
st.markdown('### データ準備')

input_option = st.selectbox(
    '入力データの選択',
    (
         '直接入力',
         'テキストファイルを選択'
    )
)
input_data = None

if input_option == '直接入力':
    input_data = st.text_area('テキストを入力してください。')

else:
    uploaded_file = st.file_uploader('テキストファイルを選択してください。', type=['txt'])
    if uploaded_file is not None:
        content = uploaded_file.read()
        input_data = content.decode('utf-8')

if input_data is not None:
    st.markdown('#### 入力データの確認')
    st.write(input_data)
    st.markdown('### 音声合成パラメータ設定')
    st.subheader('言語と話者の性別選択')
    lang = st.selectbox(
        '言語を選択してください。',
        (
            '英語',
            '日本語'
        )
    )
    gender = st.selectbox(
        '話者の性別を選択してください。',
        (
            'default',
            'male',
            'female',
            'neutral'
        )
    )
    st.markdown('### 音声合成実行')
    st.write('こちらのパラメータで音声ファイルの合成を行いますか？')
    if st.button('開始'):
        comment = st.empty()
        comment.text('音声合成中...')
        response = synthesize_speach(input_data,lang=lang, gender=gender)
        st.audio(response.audio_content)
        comment.text('音声合成が完了しました。')
