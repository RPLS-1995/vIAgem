import openai
import streamlit as st
from random import uniform
from prompts import PROMPT_INICIAL
from prompts import construir_prompt_guia_turistico
from fpdf import FPDF
from io import BytesIO


MODEL = "gpt-4-turbo"


# Função para verificar a chave API da OpenAI
def verificar_api_key():
    if not openai.api_key:
        st.error("A chave da API OpenAI não foi encontrada. Verifique as configurações.")
        return False
    return True


# Função para ajustar a temperatura e top_p dinamicamente
def ajustar_parametros(user_data):
    # Ajuste baseado no número de pessoas e nas idades da pessoa mais nova e mais velha
    if min(user_data['idade_pessoas']) < 18 or max(user_data['idade_pessoas']) > 60:
        temperatura = uniform(0.3, 0.5)
        top_p = 0.85
    elif min(user_data['idade_pessoas']) > 18 or max(user_data['idade_pessoas']) < 30:
        temperatura = uniform(0.9, 1.0)
        top_p = 1.0
    else:
        temperatura = uniform(0.65, 1.0)
        top_p = 0.95

    if user_data['num_pessoas'] <= 2:
        temperatura = temperatura + 0.1
    elif 5 < user_data['num_pessoas'] <= 15:
        temperatura = temperatura - 0.05
    elif user_data['num_pessoas'] > 15:
        temperatura = temperatura - 0.15
    return temperatura, top_p


# Função para gerar a recomendação da LLM com base no input do usuário
def gerar_recomendacao(user_data):
    temperatura, top_p = ajustar_parametros(user_data)

    # Cria as mensagens para o modelo gpt-4-turbo
    messages = [
        {
            "role": "system",
            "content": construir_prompt_guia_turistico(user_data, temperatura, top_p)
        }
    ]

    try:
        # Chamada à API da OpenAI usando o modelo gpt-4-turbo
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=messages,
            temperature=temperatura,
            top_p=top_p
        )

        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        st.error(f"Ocorreu um erro ao gerar a recomendação: {e}")
        return None


# Função para gerar uma mensagem inicial assim que o sistema for carregado
def prompt_inicial():
    # Prompt que será enviado automaticamente ao iniciar o sistema
    messages = [
        {
            "role": "system",
            "content": PROMPT_INICIAL
        }
    ]

    try:
        # Chamada à API da OpenAI usando o modelo gpt-4-turbo
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=messages
        )

        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        st.error(f"Ocorreu um erro ao gerar o prompt inicial: {e}")
        return None


# Função para salvar o texto em PDF e retornar o arquivo para download
def salvar_pdf(texto):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 10, texto)

    # Salva o conteúdo do PDF no formato de string de bytes
    pdf_output = pdf.output(dest='S').encode('latin1')

    # Retorna o conteúdo do PDF como bytes
    return BytesIO(pdf_output)
