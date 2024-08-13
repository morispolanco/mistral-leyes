import streamlit as st
import requests

# Configuración de la API de Mistral
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

# Obtener la clave de API de los secretos de Streamlit
api_key = st.secrets["MISTRAL_API_KEY"]

def get_mistral_response(prompt):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "mistral-tiny",  # Ajusta el modelo según tus necesidades
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(MISTRAL_API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

# Interfaz de Streamlit
st.title("Consulta sobre Legislación de Guatemala")

user_question = st.text_input("Ingrese su pregunta sobre la legislación de Guatemala:")

if st.button("Obtener Respuesta"):
    if user_question:
        prompt = f"Responde la siguiente pregunta sobre la legislación vigente de Guatemala: {user_question}"
        response = get_mistral_response(prompt)
        st.write("Respuesta:")
        st.write(response)
    else:
        st.warning("Por favor, ingrese una pregunta.")

# Nota informativa
st.info("Esta aplicación utiliza la API de Mistral para proporcionar información sobre la legislación de Guatemala. La precisión de las respuestas puede variar.")
