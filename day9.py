import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random

# Page configuration
st.set_page_config(
    page_title="Car Knowledge Quiz 🚗",
    page_icon="🚗",
    layout="wide"
)

# Custom CSS for quiz styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #FF4B4B;
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .quiz-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        margin: 1rem 0;
        color: white;
    }
    
    .question-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #FF4B4B;
    }
    
    .question-number {
        background: #FF4B4B;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 1rem;
    }
    
    .score-card {
        background: linear-gradient(45deg, #11998e, #38ef7d);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .final-score {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        margin: 2rem 0;
        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
    }
    
    .correct-answer {
        background-color: #d4edda;
        border: 2px solid #155724;
        border-radius: 8px;
        padding: 1rem;
        color: #155724;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .wrong-answer {
        background-color: #f8d7da;
        border: 2px solid #721c24;
        border-radius: 8px;
        padding: 1rem;
        color: #721c24;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .progress-bar {
        background: #e0e0e0;
        border-radius: 10px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        height: 20px;
        transition: width 0.3s ease;
    }
    
    .car-emoji {
        font-size: 2rem;
        margin: 0 0.5rem;
    }
    
    .difficulty-badge {
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-left: 1rem;
    }
    
    .easy { background-color: #28a745; color: white; }
    .medium { background-color: #ffc107; color: black; }
    .hard { background-color: #dc3545; color: white; }
</style>
""", unsafe_allow_html=True)

# Car Quiz Questions Database
CAR_QUESTIONS = [
    {
        "id": 1,
        "question": "Which car manufacturer produces the model 'Mustang'?",
        "options": ["Chevrolet", "Ford", "Dodge", "Plymouth"],
        "correct": 1,
        "difficulty": "easy",
        "explanation": "The Ford Mustang is an iconic American muscle car first introduced in 1964."
    },
    {
        "id": 2,
        "question": "What does 'BMW' stand for?",
        "options": ["Bavarian Motor Works", "Berlin Motor Works", "British Motor Works", "Bavarian Motor Wheels"],
        "correct": 0,
        "difficulty": "medium",
        "explanation": "BMW stands for Bayerische Motoren Werke, which translates to Bavarian Motor Works in English."
    },
    {
        "id": 3,
        "question": "Which car is known as the 'People's Car'?",
        "options": ["Ford Model T", "Volkswagen Beetle", "Chevrolet Corvair", "Mini Cooper"],
        "correct": 1,
        "difficulty": "easy",
        "explanation": "The Volkswagen Beetle was originally called 'Volkswagen' which means 'People's Car' in German."
    },
    {
        "id": 4,
        "question": "What is the top speed of a Bugatti Chiron?",
        "options": ["250 mph", "300 mph", "304 mph", "350 mph"],
        "correct": 2,
        "difficulty": "hard",
        "explanation": "The Bugatti Chiron has a top speed of 304 mph (490 km/h), making it one of the fastest production cars."
    },
    {
        "id": 5,
        "question": "Which company owns Lamborghini?",
        "options": ["Ferrari", "Porsche", "Audi", "Mercedes-Benz"],
        "correct": 2,
        "difficulty": "medium",
        "explanation": "Lamborghini is owned by Audi, which is part of the Volkswagen Group."
    },
    {
        "id": 6,
        "question": "What was the first mass-produced car?",
        "options": ["Ford Model T", "Benz Patent-Motorwagen", "Oldsmobile Curved Dash", "Cadillac Model A"],
        "correct": 0,
        "difficulty": "medium",
        "explanation": "The Ford Model T was the first automobile mass-produced on assembly lines, making cars affordable for the general public."
    },
    {
        "id": 7,
        "question": "Which car has the nickname 'Godzilla'?",
        "options": ["Toyota Supra", "Honda NSX", "Nissan GT-R", "Subaru WRX STI"],
        "correct": 2,
        "difficulty": "medium",
        "explanation": "The Nissan GT-R is nicknamed 'Godzilla' due to its monster-like performance and Japanese origin."
    },
    {
        "id": 8,
        "question": "What does 'GT' typically stand for in car names?",
        "options": ["Great Touring", "Grand Turismo", "Great Technology", "Grand Touring"],
        "correct": 3,
        "difficulty": "easy",
        "explanation": "GT stands for Grand Touring, indicating a high-performance luxury car designed for long-distance driving."
    },
    {
        "id": 9,
        "question": "Which car manufacturer created the rotary engine?",
        "options": ["Toyota", "Honda", "Mazda", "Nissan"],
        "correct": 2,
        "difficulty": "hard",
        "explanation": "Mazda perfected the rotary (Wankel) engine and used it in cars like the RX-7 and RX-8."
    },
    {
        "id": 10,
        "question": "What is the most expensive car ever sold at auction?",
        "options": ["Ferrari 250 GTO", "Mercedes 300 SLR", "Aston Martin DBR1", "Ferrari 335 S"],
        "correct": 1,
        "difficulty": "hard",
        "explanation": "A 1955 Mercedes 300 SLR was sold for $142 million in 2022, making it the most expensive car ever sold."
    },
    {
        "id": 11,
        "question": "Which car brand has a prancing horse logo?",
        "options": ["Lamborghini", "Ferrari", "Porsche", "Maserati"],
        "correct": 1,
        "difficulty": "easy",
        "explanation": "Ferrari's logo features a prancing horse, which was originally the symbol of WWI flying ace Francesco Baracca."
    },
    {
        "id": 12,
        "question": "What does 'AWD' stand for?",
        "options": ["Automatic Wheel Drive", "All Wheel Drive", "Advanced Wheel Drive", "Assisted Wheel Drive"],
        "correct": 1,
        "difficulty": "easy",
        "explanation": "AWD stands for All Wheel Drive, a system that provides power to all four wheels of a vehicle."
    },
    {
        "id": 13,
        "question": "Which car was featured in the movie 'Back to the Future'?",
        "options": ["DeLorean DMC-12", "Pontiac Firebird", "Chevrolet Camaro", "Ford Mustang"],
        "correct": 0,
        "difficulty": "easy",
        "explanation": "The DeLorean DMC-12 was the time machine in the Back to the Future movies, famous for its gull-wing doors."
    },
    {
        "id": 14,
        "question": "What is the fastest accelerating production car (0-60 mph)?",
        "options": ["Tesla Model S Plaid", "Bugatti Chiron", "McLaren 720S", "Porsche 911 Turbo S"],
        "correct": 0,
        "difficulty": "hard",
        "explanation": "The Tesla Model S Plaid can accelerate from 0-60 mph in under 2 seconds, making it one of the fastest accelerating production cars."
    },
    {
        "id": 15,
        "question": "Which country is home to Koenigsegg?",
        "options": ["Germany", "Italy", "Sweden", "Netherlands"],
        "correct": 2,
        "difficulty": "medium",
        "explanation": "Koenigsegg is a Swedish manufacturer of high-performance sports cars, founded by Christian von Koenigsegg."
    }
]

# Initialize session state
def init_session_state():
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'quiz_questions' not in st.session_state:
        st.session_state.quiz_questions = CAR_QUESTIONS.copy()
    if 'quiz_history' not in st.session_state:
        st.session_state.quiz_history = []
    if 'selected_difficulty' not in st.session_state:
        st.session_state.selected_difficulty = "all"

def reset_quiz():
    """Reset quiz to initial state"""
    st.session_state.quiz_started = False
    st.session_state.current_question = 0
    st.session_state.user_answers = {}
    st.session_state.quiz_completed = False
    st.session_state.score = 0
    
    # Filter questions by difficulty if selected
    if st.session_state.selected_difficulty != "all":
        st.session_state.quiz_questions = [
            q for q in CAR_QUESTIONS 
            if q["difficulty"] == st.session_state.selected_difficulty
        ]
    else:
        st.session_state.quiz_questions = CAR_QUESTIONS.copy()
    
    # Shuffle questions for variety
    random.shuffle(st.session_state.quiz_questions)

def calculate_score():
    """Calculate final score"""
    correct_answers = 0
    total_questions = len(st.session_state.quiz_questions)
    
    for q_id, user_answer in st.session_state.user_answers.items():
        question = next(q for q in st.session_state.quiz_questions if q["id"] == q_id)
        if user_answer == question["correct"]:
            correct_answers += 1
    
    return correct_answers, total_questions

def get_performance_message(score_percentage):
    """Get performance message based on score"""
    if score_percentage >= 90:
        return "🏆 Outstanding! You're a true car expert!", "#FFD700"
    elif score_percentage >= 80:
        return "🌟 Excellent! You know your cars well!", "#32CD32"
    elif score_percentage >= 70:
        return "👍 Great job! Solid automotive knowledge!", "#4169E1"
    elif score_percentage >= 60:
        return "👌 Good work! You're on the right track!", "#FFA500"
    elif score_percentage >= 50:
        return "📚 Not bad! Keep learning about cars!", "#FF6347"
    else:
        return "🎯 Keep practicing! Every expert started somewhere!", "#FF69B4"

# Initialize session state
init_session_state()

# Main header
st.markdown('<h1 class="main-header">🚗 Car Knowledge Quiz Game</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.3rem; color: #666;'>Test your automotive expertise with this comprehensive car quiz!</p>", unsafe_allow_html=True)

# Sidebar with quiz info and controls
with st.sidebar:
    st.markdown("### 🎮 Quiz Control Panel")
    
    # Quiz difficulty selection
    difficulty_options = {
        "all": "All Questions (15)",
        "easy": "Easy (5 questions)",
        "medium": "Medium (6 questions)", 
        "hard": "Hard (4 questions)"
    }
    
    selected_diff = st.selectbox(
        "🎯 Choose Difficulty:",
        options=list(difficulty_options.keys()),
        format_func=lambda x: difficulty_options[x],
        key="difficulty_selector"
    )
    
    if selected_diff != st.session_state.selected_difficulty:
        st.session_state.selected_difficulty = selected_diff
        if st.session_state.quiz_started:
            st.warning("⚠️ Changing difficulty will reset your current quiz!")
    
    st.markdown("---")
    
    # Quiz statistics
    if not st.session_state.quiz_started:
        total_questions = len([q for q in CAR_QUESTIONS if st.session_state.selected_difficulty == "all" or q["difficulty"] == st.session_state.selected_difficulty])
        st.metric("📊 Total Questions", total_questions)
        
        difficulty_counts = {}
        for q in CAR_QUESTIONS:
            if st.session_state.selected_difficulty == "all" or q["difficulty"] == st.session_state.selected_difficulty:
                difficulty_counts[q["difficulty"]] = difficulty_counts.get(q["difficulty"], 0) + 1
        
        for diff, count in difficulty_counts.items():
            st.metric(f"{diff.capitalize()}", count)
    
    else:
        # Progress tracking
        progress = (st.session_state.current_question + 1) / len(st.session_state.quiz_questions)
        st.metric("📈 Progress", f"{st.session_state.current_question + 1}/{len(st.session_state.quiz_questions)}")
        st.progress(progress)
        
        # Current score
        current_correct = sum(1 for q_id, answer in st.session_state.user_answers.items() 
                            if answer == next(q for q in st.session_state.quiz_questions if q["id"] == q_id)["correct"])
        st.metric("🎯 Current Score", f"{current_correct}/{len(st.session_state.user_answers)}")
    
    st.markdown("---")
    
    # Quiz history
    if st.session_state.quiz_history:
        st.markdown("### 📈 Recent Scores")
        for i, score in enumerate(st.session_state.quiz_history[-5:]):
            st.markdown(f"**Quiz {len(st.session_state.quiz_history) - len(st.session_state.quiz_history[-5:]) + i + 1}:** {score['correct']}/{score['total']} ({score['percentage']:.1f}%)")

# Main quiz content
if not st.session_state.quiz_started:
    # Welcome screen
    st.markdown("""
    <div class="quiz-container">
        <h2 style="text-align: center; margin-bottom: 2rem;">
            🏁 Ready to Test Your Car Knowledge? 🏁
        </h2>
        <div style="text-align: center;">
            <span class="car-emoji">🚗</span>
            <span class="car-emoji">🏎️</span>
            <span class="car-emoji">🚙</span>
            <span class="car-emoji">🚕</span>
            <span class="car-emoji">🚓</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quiz rules and info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📋 Quiz Rules
        - Multiple choice questions
        - One correct answer per question
        - No time limit
        - Can't go back to previous questions
        - Final score shown at the end
        """)
    
    with col2:
        st.markdown("""
        ### 🎯 Topics Covered
        - Car manufacturers & brands
        - Automotive history
        - Technical specifications
        - Famous cars & models
        - Industry knowledge
        """)
    
    with col3:
        st.markdown("""
        ### 🏆 Scoring
        - **90-100%:** Car Expert! 🏆
        - **80-89%:** Excellent! 🌟
        - **70-79%:** Great! 👍
        - **60-69%:** Good! 👌
        - **50-59%:** Fair! 📚
        - **Below 50%:** Keep Learning! 🎯
        """)
    
    # Start quiz button
    st.markdown("<br>", unsafe_allow_html=True)
    col_start = st.columns([1, 2, 1])
    with col_start[1]:
        if st.button("🏁 START QUIZ 🏁", use_container_width=True, type="primary"):
            reset_quiz()
            st.session_state.quiz_started = True
            st.rerun()

elif st.session_state.quiz_completed:
    # Quiz completion screen
    correct, total = calculate_score()
    percentage = (correct / total) * 100
    message, color = get_performance_message(percentage)
    
    # Save to history
    if not any(h.get('timestamp') == st.session_state.get('current_quiz_timestamp') for h in st.session_state.quiz_history):
        st.session_state.quiz_history.append({
            'correct': correct,
            'total': total,
            'percentage': percentage,
            'difficulty': st.session_state.selected_difficulty,
            'timestamp': datetime.now()
        })
        st.session_state.current_quiz_timestamp = datetime.now()
    
    # Final score display
    st.markdown(f"""
    <div class="final-score">
        <h2>🎉 Quiz Completed! 🎉</h2>
        <h1>{correct}/{total}</h1>
        <h3>({percentage:.1f}%)</h3>
        <p style="margin-top: 1rem; font-size: 1.2rem;">{message}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed results
    st.markdown("### 📊 Detailed Results")
    
    results_data = []
    for i, question in enumerate(st.session_state.quiz_questions):
        user_answer_idx = st.session_state.user_answers.get(question["id"], -1)
        is_correct = user_answer_idx == question["correct"]
        
        results_data.append({
            'Question': f"Q{i+1}",
            'Difficulty': question["difficulty"].capitalize(),
            'Correct': "✅" if is_correct else "❌",
            'Your Answer': question["options"][user_answer_idx] if user_answer_idx >= 0 else "Not answered",
            'Correct Answer': question["options"][question["correct"]]
        })
    
    results_df = pd.DataFrame(results_data)
    st.dataframe(results_df, use_container_width=True)
    
    # Performance analysis
    col_perf1, col_perf2 = st.columns(2)
    
    with col_perf1:
        # Difficulty breakdown
        difficulty_results = {"easy": {"correct": 0, "total": 0}, 
                            "medium": {"correct": 0, "total": 0}, 
                            "hard": {"correct": 0, "total": 0}}
        
        for question in st.session_state.quiz_questions:
            difficulty = question["difficulty"]
            difficulty_results[difficulty]["total"] += 1
            user_answer = st.session_state.user_answers.get(question["id"], -1)
            if user_answer == question["correct"]:
                difficulty_results[difficulty]["correct"] += 1
        
        chart_data = []
        for diff, results in difficulty_results.items():
            if results["total"] > 0:
                chart_data.append({
                    "Difficulty": diff.capitalize(),
                    "Percentage": (results["correct"] / results["total"]) * 100,
                    "Questions": results["total"]
                })
        
        if chart_data:
            fig_diff = px.bar(
                pd.DataFrame(chart_data),
                x="Difficulty",
                y="Percentage",
                title="Performance by Difficulty",
                color="Percentage",
                color_continuous_scale="RdYlGn"
            )
            fig_diff.update_layout(height=400)
            st.plotly_chart(fig_diff, use_container_width=True)
    
    with col_perf2:
        # Score history if available
        if len(st.session_state.quiz_history) > 1:
            history_df = pd.DataFrame([
                {
                    "Quiz": f"Quiz {i+1}",
                    "Score": h["percentage"],
                    "Questions": h["total"]
                }
                for i, h in enumerate(st.session_state.quiz_history)
            ])
            
            fig_history = px.line(
                history_df,
                x="Quiz",
                y="Score",
                title="Score History",
                markers=True
            )
            fig_history.update_layout(height=400)
            st.plotly_chart(fig_history, use_container_width=True)
        else:
            st.info("Complete more quizzes to see your progress history!")
    
    # Review answers
    with st.expander("🔍 Review All Questions & Answers", expanded=False):
        for i, question in enumerate(st.session_state.quiz_questions):
            user_answer_idx = st.session_state.user_answers.get(question["id"], -1)
            is_correct = user_answer_idx == question["correct"]
            
            st.markdown(f"**Question {i+1}:** {question['question']}")
            
            if is_correct:
                st.markdown(f'<div class="correct-answer">✅ Correct! You answered: {question["options"][user_answer_idx]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="wrong-answer">❌ Incorrect. You answered: {question["options"][user_answer_idx] if user_answer_idx >= 0 else "Not answered"}<br>Correct answer: {question["options"][question["correct"]]}</div>', unsafe_allow_html=True)
            
            st.markdown(f"**Explanation:** {question['explanation']}")
            st.markdown("---")
    
    # Action buttons
    col_action1, col_action2 = st.columns(2)
    
    with col_action1:
        if st.button("🔄 Take Quiz Again", use_container_width=True, type="primary"):
            reset_quiz()
            st.session_state.quiz_started = True
            st.rerun()
    
    with col_action2:
        if st.button("🏠 Back to Home", use_container_width=True):
            reset_quiz()
            st.rerun()

else:
    # Quiz in progress
    current_q_idx = st.session_state.current_question
    current_question = st.session_state.quiz_questions[current_q_idx]
    
    # Progress bar
    progress = (current_q_idx + 1) / len(st.session_state.quiz_questions)
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress * 100}%"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Question display
    st.markdown(f"""
    <div class="question-card">
        <span class="question-number">Question {current_q_idx + 1} of {len(st.session_state.quiz_questions)}</span>
        <span class="difficulty-badge {current_question['difficulty']}">{current_question['difficulty'].upper()}</span>
        <h3 style="margin-top: 1rem; color: #333;">{current_question['question']}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Answer options
    st.markdown("### Choose your answer:")
    selected_answer = st.radio(
        "Options:",
        options=range(len(current_question["options"])),
        format_func=lambda x: current_question["options"][x],
        key=f"q_{current_question['id']}"
    )
    
    # Navigation buttons
    col_nav1, col_nav2 = st.columns(2)
    
    with col_nav2:
        if st.button("➡️ Next Question", use_container_width=True, type="primary"):
            # Save answer
            st.session_state.user_answers[current_question["id"]] = selected_answer
            
            # Move to next question or finish
            if current_q_idx < len(st.session_state.quiz_questions) - 1:
                st.session_state.current_question += 1
            else:
                st.session_state.quiz_completed = True
            
            st.rerun()
    
    with col_nav1:
        if st.button("🏠 Quit Quiz", use_container_width=True, type="secondary"):
            if st.button("⚠️ Confirm Quit", type="secondary"):
                reset_quiz()
                st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; margin-top: 2rem; padding: 1rem; background: linear-gradient(45deg, #FF6B6B, #4ECDC4); border-radius: 10px;'>
    <h4 style='color: white; margin: 0;'>🚗 "The best drivers are always learning!" 🚗</h4>
    <p style='color: white; margin: 0.5rem 0 0 0;'>Test your automotive knowledge and become a car expert!</p>
    </div>
    """,
    unsafe_allow_html=True
)