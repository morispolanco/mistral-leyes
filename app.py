import streamlit as st
import requests
import json

# Configuración de las APIs
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
SERPER_API_URL = "https://google.serper.dev/search"

# Obtener las claves de API de los secretos de Streamlit
mistral_api_key = st.secrets["MISTRAL_API_KEY"]
serper_api_key = st.secrets["SERPER_API_KEY"]

def get_search_results(query):
    headers = {
        "X-API-KEY": serper_api_key,
        "Content-Type": "application/json"
    }
    
    data = {
        "q": query
    }
    
    response = requests.post(SERPER_API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_mistral_response(prompt):
    headers = {
        "Authorization": f"Bearer {mistral_api_key}",
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
        # Realizar búsqueda web
        search_results = get_search_results(f"legislación Guatemala {user_question}")
        
        if search_results:
            # Extraer información relevante de los resultados de búsqueda
            relevant_info = "\n".join([result.get('snippet', '') for result in search_results.get('organic', [])[:3]])
            
            # Crear prompt enriquecido para Mistral
            prompt = f"""Responde la siguiente pregunta sobre la legislación vigente de Guatemala: {user_question}
            
            Información adicional de la búsqueda web:
            {relevant_info}
            
            Por favor, utiliza esta información adicional para proporcionar una respuesta más completa y actualizada."""
            
            response = get_mistral_response(prompt)
            st.write("Respuesta:")
            st.write(response)
            
            # Mostrar fuentes de la búsqueda web
            st.subheader("Fuentes de información:")
            for result in search_results.get('organic', [])[:3]:
                st.write(f"- [{result.get('title', 'Fuente')}]({result.get('link', '#')})")
        else:
            st.error("No se pudieron obtener resultados de búsqueda. Proporcionando una respuesta basada solo en el conocimiento del modelo.")
            prompt = f"Responde la siguiente pregunta sobre la legislación vigente de Guatemala: {user_question}"
            response = get_mistral_response(prompt)
            st.write("Respuesta:")
            st.write(response)
    else:
        st.warning("Por favor, ingrese una pregunta.")

# Nota informativa
st.info("Esta aplicación utiliza la API de Mistral y búsqueda web para proporcionar información sobre la legislación de Guatemala. La precisión de las respuestas puede variar.")
