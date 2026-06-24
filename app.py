import streamlit as st
import re
import random

st.set_page_config(
    page_title="AI Notes Summarizer + Quiz Generator",
    page_icon="📚",
    layout="wide"
)

st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        color: #4B4DED;
    }
    .sub-title {
        text-align: center;
        font-size: 18px;
        color: #555;
        margin-bottom: 30px;
    }
    .box {
        padding: 20px;
        border-radius: 15px;
        background-color: #f7f7ff;
        border: 1px solid #ddd;
        margin-bottom: 15px;
    }
    .footer {
        text-align: center;
        color: #777;
        font-size: 14px;
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📚 AI Notes Summarizer + Quiz Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Paste your study notes and get short summaries + quiz questions instantly.</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Settings")
    summary_length = st.selectbox("Summary length", ["Short", "Medium", "Detailed"])
    quiz_count = st.slider("Number of quiz questions", 3, 10, 5)
    st.markdown("---")
    st.info("Future earning ideas: Ads, premium PDF upload, subscription, college notes packs.")


def clean_text(text):
    text = re.sub(r"\s+", " ", text).strip()
    return text


def split_sentences(text):
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if len(s.strip()) > 20]


def summarize_notes(text, level):
    sentences = split_sentences(clean_text(text))
    if not sentences:
        return "Please paste longer notes for a better summary."

    if level == "Short":
        n = min(4, len(sentences))
    elif level == "Medium":
        n = min(7, len(sentences))
    else:
        n = min(12, len(sentences))

    # Simple extractive summary: chooses important-looking sentences
    keywords = ["important", "because", "therefore", "means", "defined", "used", "type", "example", "function", "process"]
    scored = []
    for sentence in sentences:
        score = len(sentence.split())
        score += sum(10 for word in keywords if word in sentence.lower())
        scored.append((score, sentence))

    top_sentences = [s for _, s in sorted(scored, reverse=True)[:n]]
    return "\n".join([f"• {s}" for s in top_sentences])


def get_keywords(text):
    words = re.findall(r"\b[A-Za-z]{5,}\b", text.lower())
    stopwords = {
        "there", "their", "about", "which", "would", "could", "should", "these", "those",
        "because", "where", "while", "after", "before", "using", "between", "through",
        "important", "example", "study", "notes", "chapter", "topic"
    }
    words = [w for w in words if w not in stopwords]
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    return [w for w, _ in sorted(freq.items(), key=lambda x: x[1], reverse=True)[:20]]


def generate_quiz(text, count):
    keywords = get_keywords(text)
    sentences = split_sentences(clean_text(text))
    if len(keywords) < 3 or len(sentences) < 3:
        return []

    quiz = []
    used = set()
    for keyword in keywords:
        related = [s for s in sentences if keyword in s.lower()]
        if not related or keyword in used:
            continue
        sentence = random.choice(related)
        question = sentence.replace(keyword, "________", 1)
        options = [keyword]
        distractors = [k for k in keywords if k != keyword]
        random.shuffle(distractors)
        options += distractors[:3]
        random.shuffle(options)
        quiz.append({
            "question": question,
            "answer": keyword,
            "options": options
        })
        used.add(keyword)
        if len(quiz) >= count:
            break
    return quiz


col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("✍️ Paste your notes")
    notes = st.text_area(
        "Enter your notes here:",
        height=350,
        placeholder="Example: Machine learning is a branch of AI that allows computers to learn from data..."
    )
    generate = st.button("Generate Summary & Quiz", type="primary")

with col2:
    st.subheader("💡 How students can use this")
    st.markdown("""
    <div class="box">
    ✅ Revise long notes quickly<br>
    ✅ Create practice MCQs<br>
    ✅ Prepare for exams faster<br>
    ✅ Useful for school, college, and competitive exams
    </div>
    """, unsafe_allow_html=True)

    st.subheader("💰 Monetization ideas")
    st.markdown("""
    <div class="box">
    1. Free version with ads<br>
    2. Premium PDF upload<br>
    3. ₹49/month student plan<br>
    4. Sell subject-wise notes packs<br>
    5. Affiliate links for courses/books
    </div>
    """, unsafe_allow_html=True)

if generate:
    if not notes.strip():
        st.warning("Please paste your notes first.")
    else:
        st.markdown("---")
        st.header("📝 Summary")
        st.success(summarize_notes(notes, summary_length))

        st.header("🧠 Quiz Questions")
        quiz = generate_quiz(notes, quiz_count)
        if not quiz:
            st.warning("Paste longer notes to generate better quiz questions.")
        else:
            for i, q in enumerate(quiz, start=1):
                with st.expander(f"Question {i}"):
                    st.write(q["question"])
                    choice = st.radio("Choose an answer:", q["options"], key=f"q{i}")
                    if st.button("Check answer", key=f"check{i}"):
                        if choice == q["answer"]:
                            st.success("Correct ✅")
                        else:
                            st.error(f"Wrong. Correct answer: {q['answer']}")

st.markdown('<div class="footer">Made for students | Version 1.0</div>', unsafe_allow_html=True)
