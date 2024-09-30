import streamlit as st
import openai
import os
from datetime import date
from prompts import PROMPT_INICIAL
from prompts import construir_prompt_guia_turistico

# Carrega a chave API da OpenAI de uma variável de ambiente
openai.api_key = os.getenv('OPENAI_API_KEY')

# Função para verificar a chave API da OpenAI
def verificar_api_key():
    if not openai.api_key:
        st.error("A chave da API OpenAI não foi encontrada. Verifique as configurações.")
        return False
    return True

# Função para ajustar a temperatura e top_p dinamicamente
def ajustar_parametros(user_data):
    # Ajuste simples baseado no número de pessoas e orçamento
    temperatura = 0.5 + (min(user_data['num_pessoas'], 10) / 20)  # Quanto mais pessoas, maior a temperatura
    top_p = min(user_data['orcamento_max'] / 1000, 1)  # Quanto maior o orçamento, maior o top_p
    return temperatura, top_p

# Função para gerar a recomendação da LLM com base no input do usuário
def gerar_recomendacao(user_data):
    temperatura, top_p = ajustar_parametros(user_data)

    # Cria as mensagens para o modelo gpt-3.5-turbo
    messages = [
        {
            "role": "system",
            "content": construir_prompt_guia_turistico(user_data, temperatura, top_p)
        }
    ]

    try:
        # Chamada à API da OpenAI usando o modelo gpt-3.5-turbo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.2,
            top_p=1
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
        # Chamada à API da OpenAI usando o modelo gpt-3.5-turbo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        st.error(f"Ocorreu um erro ao gerar o prompt inicial: {e}")
        return None

# Função principal do Streamlit
def main():
    # Verifica a chave da API
    if not verificar_api_key():
        return

    # Gera o prompt inicial na inicialização do sistema
    st.title('Agente de Viagens Inteligente')

    # Verifica se já exibimos o prompt inicial. Se não, executa-o
    if 'mensagem_inicial' not in st.session_state:
        mensagem_inicial = prompt_inicial()
        st.session_state.mensagem_inicial = mensagem_inicial if mensagem_inicial else "O assistente está pronto para ajudar você a planejar sua viagem!"

        # Exibe o prompt inicial (apenas uma vez)
        st.write("### Mensagem Inicial do Assistente:")
        st.write(st.session_state.mensagem_inicial)

    # Campos para o usuário preencher
    destino = st.text_input('Destino', placeholder='Ex: Paris, Nova York, Tóquio')
    data_inicio = st.date_input('Data de Início', value=date.today())
    data_fim = st.date_input('Data de Fim', value=date.today())
    num_pessoas = st.number_input('Número de Pessoas', min_value=1, value=1)
    idade_pessoas = st.text_input('Idade de Cada Pessoa (separadas por vírgula)', placeholder='Ex: 25, 30, 18')
    orcamento_max = st.number_input('Orçamento Máximo (em reais)', min_value=100)

    # Botão de envio
    if st.button('Planejar Viagem'):
        if not destino or not data_inicio or not data_fim or not idade_pessoas or orcamento_max <= 0:
            st.error("Por favor, preencha todos os campos corretamente.")
        else:
            # Converte as idades para uma lista
            idades = [int(idade.strip()) for idade in idade_pessoas.split(',') if idade.strip().isdigit()]

            # Dados do usuário
            user_data = {
                'destino': destino,
                'data_inicio': data_inicio,
                'data_fim': data_fim,
                'num_pessoas': num_pessoas,
                'idade_pessoas': idades,
                'orcamento_max': orcamento_max
            }

            # Gera a recomendação e exibe para o usuário
            recomendacao = gerar_recomendacao(user_data)

            if recomendacao:
                st.write('### Recomendação para sua viagem:')
                st.write(recomendacao)

# Verifica se o script está sendo executado diretamente
if __name__ == '__main__':
    main()
