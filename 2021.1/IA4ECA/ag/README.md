# Exercício de Algorítmos Genéticos

## Uso

O código `ag.py` possui uma CLI simples e executa tanto a resolução do exercício quanto a geração dos gráficos requisitados. Por padrão, o gráfico da aptidão em função do valor do cromossomo para cada membro da população não é gerado, mas pode ser habilitado através da opção `--show-gens`.

## Modificações

Eu encontrei bastante instabilidade utilizando a abordagem proposta de codificação binária a partir do valor em ponto flutuante. Então, modifiquei as funções `get_bits` e `get_float` para realizarem um mapeamento entre os valores dentro do domínio do problema e inteiros de `L` bits na base 2 (número binário utilizado para mutação e cruzamento).

Eu acho que 32 bits é muito mais do que o necessário para representar a resolução de ponto flutuante para o intervalo (0, pi), mas não experimentei com valores menores.

## Experimentos

Os gráficos dos experimentos estão organizados na pasta `experiments` na ordem em que foram realizados. Eu estipulei um _budget_ de 25000 avaliações da função de aptidão e comecei pelo ajuste da proporção entre tamanho da população e número de gerações. Os parâmetros utilizados foram codificados nos nomes das imagens na ordem: tamanho da população, número de gerações, taxa de cruzamento e taxa de mutação. As duas últimas foram adicionadas sem a separação das casas decimais.

Todos os experimentos foram executados 10 vezes e o resultado é a média dessas execuções, inclusive para os limites da região sombreada.