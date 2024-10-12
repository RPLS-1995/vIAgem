# Projeto vIAgem

Este projeto visa desenvolver um guia turístico inteligente, que retorna um guia completo de viagem
a um cliente a partir de dados fornecidos na entrada.
Para isso, utilizou-se uma LLM e dois Prompts criados do zero, para que
diferentes cenários fossem analisados e que um conjunto de regras e padrões fossem adotados pelo sistema.


## Escolha da LLM ##
Após algumas pesquisas e a partir de experiências anteriores, optou-se por uma LLM bastante consolidada no mercado. 
Dessa forma, foram testadas duas LLMs da OpenAI: A **gpt-3.5-turbo** e a **gpt-4-turbo**.
Embora a gpt-3.5-turbo tenha apresentado respostas mais rápidas e seu custo seja inferior,
a gpt-4-turbo apresentou uma série de vantagens decisivas, como:
- Uma maior capacidade de gerar respostas mais elaboradas, e não somente com Bullet Points.
- Uma maior variedade de dados retornados no guia turístico, como mais links sobre os pontos turísiticos e venda de tickets.
- Uma melhor adaptação para produzir respostas a partir de destinos inexistentes ou em regiões de conflito.
- Um fornecimento mais detalhado sobre os custos envolvidos para cada dia da viagem.

Além disso, o gpt-4-turbo tem informações mais atualizadas com relação ao gpt-3.5-turbo, o que pode ser visto [aqui](https://platform.openai.com/docs/models/gpt-4-turbo-and-gpt-4).
Por fim, segundo a própria OpenAI, essa LLM
"can solve difficult problems with greater accuracy than any of our previous models, thanks to its broader general knowledge and advanced reasoning capabilities.".

Dessa vez os resultados foram muito superiores com a **gpt-4-turbo** e assim ela foi adotada para esse projeto.

## Como baixar e executar ##
Para este projeto os códigos foram implementados na linguagem Python (e revisados com flake8) e as execuções acontecem com o uso de Docker. O principal objetivo
do Docker é garantir que o projeto vIAgem possa ser executado em qualquer máquina, independente de sua configuração.
IMPORTANTE: Aqui o sistema operacional a ser usado é o Linux.
Assim os passos para execução do sistema podem ser vistos abaixo:
1. Abra um terminal no computador e baixe o repositório usando o comando "git clone https://github.com/RPLS-1995/vIAgem.git"
2. Abra uma IDE de sua preferência e entre na pasta do repositório clonado. Com o Docker instalado, execute o comando "sudo docker compose build".
Este comando fará que com as bibliotecas contidas no arquivo requirements.txt sejam instaladas na máquina.
3. Após o comando acima ser concluído, digite o comando "sudo docker compose up". Este comando irá criar e executa os contâiners necessários do projeto.
4. Quando essa mensagem aparecer no terminal, significa que o sistema está pronto para uso. ![image](https://github.com/user-attachments/assets/99fde4bd-9cfd-4d1f-9b8e-c4f7892c29e7)

Assim, abra uma página no navegador de sua preferência com a URL http://172.18.0.2:8501 e aguarde a página do guia turístico ser totalmente carregada.
5. Caso o navegador exiba uma página Web similar a esta, significa que o projeto vIAgem está pronto para uso! ![image](https://github.com/user-attachments/assets/14e0f1f6-19a3-492c-9a2e-9bc77872c267)


## Explorando o vIAgem ##
Conforme explicado anteriormente, o guia turístico inteligente irá ler os dados de entrada fornecidos pelo cliente e responder
com um guia turístico personalizado. Esses dados de entrada, todos obrigatórios, são:

- A cidade, o estado ou o país de destino
- A data de início da viagem
- A data de término da viagem
- O número de pessoas que irão viajar
- As idades da pessoa mais nova e da pessoa mais velha
- O orçamento máximo para a viagem (em reais).

Para iniciar a interação com o vIAgem, o cliente deve preencher os campos acima e clicar no botão "Plnajear Viagem". As imagens abaixo mostram
os campos preenchidos e o resultado retornado pelo sistema.
![image](https://github.com/user-attachments/assets/99d69c9e-1440-461e-912f-8f04c6e73f8b)
![image](https://github.com/user-attachments/assets/3edab690-494b-40cf-8c52-a48ca6f48c61)
![image](https://github.com/user-attachments/assets/d7529610-878c-49ba-a9bb-e64808c05649)





