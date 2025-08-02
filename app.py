!pip install java --quiet
import streamlit as st
import language_tool_python
import random


# Initialize LanguageTool for French
tool = language_tool_python.LanguageTool('fr')

st.title("🇫🇷 French Conversation Practice Bot")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Function to generate a simple conversational reply based on keywords
def generate_reply(user_input):
    user_input_lower = user_input.lower()
    if "bonjour" in user_input_lower:
        return "Bonjour ! Comment ça va aujourd'hui ?"
    elif "ça va" in user_input_lower or "ca va" in user_input_lower:
        return "Ça va bien, merci de demander ! Qu'as-tu prévu aujourd'hui ?"
    elif "m'appelle" in user_input_lower:
        return "Enchanté de te rencontrer ! Quel âge as-tu ?"
    elif "temps" in user_input_lower or "météo" in user_input_lower:
        return "Il fait beau ici aujourd'hui. Et chez toi ?"
    elif "merci" in user_input_lower:
        return "De rien !"
    elif "au revoir" in user_input_lower:
        return "Au revoir ! À la prochaine."
    else:
        # Generic fallback responses
        fallback_responses = [
            "Intéressant ! Peux-tu m'en dire plus ?",
            "C'est bien ! Quels sont tes projets pour cette semaine ?",
            "Très intéressant. Comment te sens-tu à ce sujet ?"
        ]
        return random.choice(fallback_responses)

# User input
user_input = st.text_input("💬 Écris ton message en français et appuie sur Entrée:")

if user_input:
    # Grammar checking
    matches = tool.check(user_input)
    if matches:
        corrected_text = language_tool_python.utils.correct(user_input, matches)
        explanations = []
        for match in matches:
            explanations.append(f"• {match.message} (Incorrect: '{user_input[match.offset:match.offset + match.errorLength]}')")
        explanation_text = "\n".join(explanations)
        correction_feedback = (
            "🤖 J'ai trouvé des petites erreurs :\n\n"
            f"{explanation_text}\n\n"
            f"✅ Voici une correction possible : '{corrected_text}'\n\n"
        )
    else:
        correction_feedback = "✅ Aucune erreur détectée. Bravo pour ta phrase correcte !\n\n"

    # Generate conversational reply
    conversation_reply = generate_reply(user_input)

    # Combine feedback and conversational reply
    bot_response = correction_feedback + f"💬 {conversation_reply}"

    # Update chat history
    st.session_state.chat_history.append(("Tu", user_input))
    st.session_state.chat_history.append(("Bot", bot_response))

# Display chat history
for sender, message in st.session_state.chat_history:
    if sender == "Tu":
        st.markdown(f"**🧑 Tu:** {message}")
    else:
        st.markdown(f"**🤖 Bot:** {message}")


