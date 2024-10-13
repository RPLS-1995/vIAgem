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
![image](https://github.com/user-attachments/assets/d8044f3c-138c-4502-ad6c-6c66bec29e22)


No exemplo acima, foi pedido para o vIAgem construir um guia para uma viagem a Curitiba entre os dias 18/10/2024 e 20/10/2024, para 1 pessoa de 29 anos
com um orçamento de 1000 reais.
O sistema retornou um guia detalhado, dia a dia, apresentando dicas de passeios, sugestões de locais para refeições, locais de visitação gratuita
e um valor médio de hospedagem. O guia turístico também compartilha links para que o cliente possa conhecer mais sobre algumas atrações e tenha acesso
aos sites para compra de tickets.


## Diferenciais ##
O guia turístico inteligente possui algumas características que o tornam único e especial.
Dentre elas, temos uma adaptação dinâmica dos parâmetros da LLM: Os valores de Temperatura e Top P variam de acordo
com os dados fornecidos pelo cliente. Por exemplo, se a viagem será feita apenas por jovens, o guia de turismo será mais "ousado"
e criativo. Por outro lado, caso a viagem tenha crianças ou sêniors, as sugestões de passeios serão mais "conservadoras".
Abaixo temos um exemplo dessa diferença, com sugestões de passeios ao Japão para viajantes de 19 anos... 

![recomendacao_passeio_19_anos](https://github.com/user-attachments/assets/85275fa2-041f-49db-8590-e9e3be09e38f)

...e para viajantes de 72 anos.
![recomendacao_passeio_senior_72_anos](https://github.com/user-attachments/assets/0f00cc83-b3b2-4d21-94e4-93868989d657)

Outro diferencial do vIAgem é o alerta gerado ao cliente caso este decida ir para uma cidade ou país atualmente em conflito armado.
Pensnado na segurança, o sistema deve avisar o cliente sobre a situação atual e sugerir outros destinos próximos que possam
interessar e que tenham maiores garantias de segurança.
Abaixo temos um exemplo, onde o cliente coloca como destino o Ucrânia, um país envolvido em uma guerra desde 24/02/2022.
Dessa forma, o vIAgem sugere que o cliente visite a vizinha Polônia como alternativa.
![recomendacao_passeio_zona_conflito](https://github.com/user-attachments/assets/638d9b1e-afea-4d34-aff8-215cf7eaaa3e)

Finalmente, o sistema tem a capacidade de interpretar o destino que o usuário deseja conhecer, mesmo com um destino inválido.
Por exemplo, caso o cliente coloque "Pão de Queijo" como destino, o vIAgem deverá supor que o cliente quer visitar Minas Gerais
ou uma cidade do estado brasileiro, famoso por esta comida marcante.
Outro exemplo pode ser visto abaixo, quando o cliente colocou a Prússia como destino, um país que não existe desde 1918 e
que fazia parte do Império Alemão. Dessa forma, sugeriu-se um guia para visitar Berlim, justamente a capital alemã.
![recomendacao_pais_inexistente](https://github.com/user-attachments/assets/d9c05b19-f1a2-4bb1-9f0c-f2789f60300d)


