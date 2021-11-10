# Treinamento de redes neurais multi-camadas

Os arquivos aqui implementam, além de uma classe para redes neurais, algoritmos para realizar o seu treinamento utilizando o algoritmo do descenso do gradiente.

<dl>
  <dt>`network.py`</dt>
  <dd>Principal arquivo. Implementa a rede e as funções necessárias para a retropropagação e o descenso do gradiente.</dd>
  <dt>`train.py`</dt>
  <dd>Rotinas de treinamento para realizar o treinamento da rede ao longo de múltiplas épocas. Também contém a função de perda utilizada.</dd>
  <dt>`estimator.py`</dt>
  <dd>Wrapper da rede neural como um estimator do scikit-learn.</dd>
  <dt>`grid_search.py`</dt>
  <dd>Usa o método implementado no scikit-learn para realizar os experimentos.</dd>
  <dt>`cv_results.csv`</dt>
  <dd>Resultados dos experimentos.</dd>
  <dt>`utils.py`</dt>
  <dd>Funções auxiliares, principalmente para visualizações.</dd>
</dl>
