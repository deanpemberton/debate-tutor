import os
import random
import streamlit as st
from core import Debate, GRADES, MOOTS
from providers import DemoProvider, OpenAIProvider

st.set_page_config(page_title="Debate Practice", page_icon="🎙️")
st.title("🎙️ Debate Practice")
st.caption("For practice outside controlled competition debates.")
live = bool(os.getenv("OPENAI_API_KEY"))
provider = OpenAIProvider() if live else DemoProvider()
if not live:
    st.info("Demo mode: type speeches to test the flow. Add OPENAI_API_KEY to enable voice and AI.")

if "debate" not in st.session_state:
    with st.form("setup"):
        grade = st.selectbox("Auckland schools practice preset", list(GRADES))
        side = st.radio("Your side", ["Affirmative (go first)", "Negative (respond)"])
        moot = st.text_input("Your moot (blank for a suggested one)")
        replies = st.checkbox("Include reply speeches")
        start = st.form_submit_button("Start debate", type="primary")
    st.caption("Advanced-grade live points of information are not yet supported.")
    if start:
        st.session_state.debate = Debate(moot.strip() or random.choice(MOOTS), grade,
                                         side.split()[0], replies)
        st.rerun()
    st.stop()

debate = st.session_state.debate
st.subheader(debate.moot)
st.write(f"**{debate.grade}** · You are **{debate.student_side}** · "
         f"{len(debate.speeches)}/{len(debate.turns)} speeches complete")
for i, (turn, speech) in enumerate(zip(debate.turns, debate.speeches)):
    with st.expander(f"{i+1}. {turn.side} {turn.role}"):
        st.write(speech)
        if st.session_state.get(f"audio_{i}"):
            st.audio(st.session_state[f"audio_{i}"], format="audio/mp3")
if debate.speeches and debate.turns[len(debate.speeches)-1].side != debate.student_side:
    last_audio = st.session_state.get(f"audio_{len(debate.speeches)-1}")
    if last_audio:
        st.write("**Listen to the opponent's latest speech:**")
        st.audio(last_audio, format="audio/mp3", autoplay=True)

turn = debate.current
if turn:
    st.markdown(f"### {turn.side}: {turn.role}")
    st.write(f"Target: **{turn.minutes:g} minutes**. A shorter practice speech is fine.")
    if turn.side == debate.student_side:
        recording = st.audio_input("Record your speech", key=f"record_{len(debate.speeches)}")
        if recording and st.button("Transcribe recording"):
            if recording.size > 25_000_000:
                st.error("Recording exceeds the 25 MB limit. Try a shorter one.")
            else:
                try:
                    st.session_state.draft = provider.transcribe(recording.getvalue())
                    st.rerun()
                except Exception as exc:
                    st.error(f"Transcription failed: {exc}")
        with st.form(f"student_{len(debate.speeches)}"):
            draft = st.text_area("Check and correct the transcript (or type a speech)",
                                 value=st.session_state.get("draft", ""), height=180)
            confirmed = st.form_submit_button("Confirm speech", type="primary")
        if confirmed:
            if draft.strip() and not draft.startswith("[Demo transcript:"):
                debate.add(draft)
                st.session_state.pop("draft", None)
                st.rerun()
            else:
                st.warning("Enter or correct the speech before confirming.")
    elif st.button("Generate opposing speech", type="primary"):
        try:
            with st.spinner("Preparing response…"):
                speech = provider.opponent(debate)
                audio = provider.speak(speech)
                if audio:
                    st.session_state[f"audio_{len(debate.speeches)}"] = audio
                debate.add(speech)
            st.rerun()
        except Exception as exc:
            st.error(f"Could not generate speech: {exc}")
else:
    st.success("Debate complete")
    if st.button("Get coaching feedback", type="primary"):
        try:
            with st.spinner("Reviewing…"):
                st.session_state.feedback = provider.judge(debate)
        except Exception as exc:
            st.error(f"Feedback failed: {exc}")
    if st.session_state.get("feedback"):
        st.markdown(st.session_state.feedback)
        st.download_button("Download transcript and feedback",
            debate.transcript() + "\n\nFEEDBACK\n" + st.session_state.feedback,
            file_name="debate-practice.txt")

if st.button("Start a new debate"):
    st.session_state.clear()
    st.rerun()
