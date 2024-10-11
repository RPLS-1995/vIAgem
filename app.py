import streamlit as st
import openai
import os
from datetime import date
from random import uniform
from prompts import PROMPT_INICIAL
from prompts import construir_prompt_guia_turistico
from fpdf import FPDF
from io import BytesIO

# Carrega a chave API da OpenAI de uma variável de ambiente
openai.api_key = os.getenv('OPENAI_API_KEY')

MODEL = "gpt-4-turbo"


# Função para verificar a chave API da OpenAI
def verificar_api_key():
    if not openai.api_key:
        st.error("A chave da API OpenAI não foi encontrada. Verifique as configurações.")
        return False
    return True


# Função para ajustar a temperatura e top_p dinamicamente
def ajustar_parametros(user_data):
    # Ajuste simples baseado no número de pessoas e orçamento
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
    idade_pessoas = st.text_input('Idades da pessoa mais nova e da pessoa mais velha (separadas por vírgula)', placeholder='Ex: 18, 62')
    orcamento_max = st.number_input('Orçamento Máximo (em reais)', min_value=100)

    # Botão de envio
    if st.button('Planejar Viagem'):
        if not destino or not data_inicio or not data_fim or not idade_pessoas or orcamento_max <= 0:
            st.error("Por favor, preencha todos os campos corretamente.")
        elif data_inicio > data_fim:
            st.error("A data inicial deve ser anterior à data final.")
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

            # Exibe um "pop-up" temporário durante a geração da recomendação
            with st.spinner('Estamos planejando sua viagem! Aguarde alguns segundos...'):
                recomendacao = gerar_recomendacao(user_data).replace("œ","oe")

            if recomendacao:
                st.write('### Recomendação para sua viagem:')
                st.write(recomendacao.replace('$', '\\$'))

                # Gera o PDF e exibe o botão para download
                pdf_buffer = salvar_pdf(recomendacao)
                st.download_button(
                    label="Baixar recomendação em PDF",
                    data=pdf_buffer,
                    file_name="guia_viagem.pdf",
                    mime="application/pdf"
                )

# Verifica se o script está sendo executado diretamente
if __name__ == '__main__':
    main()
