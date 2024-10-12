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
