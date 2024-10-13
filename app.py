import streamlit as st
import openai
import os
from datetime import date
from utils import verificar_api_key, prompt_inicial
from utils import gerar_recomendacao, salvar_pdf
from dotenv import load_dotenv


# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Carrega a chave API da OpenAI de uma variável de ambiente
openai.api_key = os.getenv('OPENAI_API_KEY')


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
        elif data_inicio < date.today() or data_fim < date.today():
            st.error("As datas não podem ser do passado.")
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
                recomendacao = gerar_recomendacao(user_data)

            if recomendacao:
                st.write('### Recomendação para sua viagem:')
                st.write(recomendacao.replace('$', '\\$').replace('€', '\\€').replace('£', '\\£'))

                # Gera o PDF e exibe o botão para download
                pdf_buffer = salvar_pdf(recomendacao)
                st.download_button(
                    label="Baixar recomendação em PDF",
                    data=pdf_buffer,
                    file_name="guia_viagem.pdf",
                    mime="application/pdf"
                )

            # Botão para refazer a recomendação usando os mesmos inputs
            if st.button('Refazer recomendação'):
                st.experimental_rerun()  # Reinicia a tela


# Verifica se o script está sendo executado diretamente
if __name__ == '__main__':
    main()
