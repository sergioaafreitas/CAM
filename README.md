# Machine Learning Course (FGA0083)  
Revisão didática: out/2026

Este repositório contém o material da disciplina **Aprendizado de Máquina (FGA0083)** da Universidade de Brasília, ministrada pelo Prof. Dr. Sergio Antônio Andrade de Freitas.  

## 📘 Visão Geral da Disciplina

A disciplina busca capacitar os estudantes a compreender, aplicar e adaptar métodos de aprendizado de máquina. O conteúdo combina fundamentos teóricos e práticos de regressão, classificação, aprendizado não supervisionado, SVMs, redes neurais e introdução a transformers e LLMs.

### ✳️ Resultados de Aprendizagem Esperados

- Compreender os principais conceitos e técnicas de aprendizado de máquina.
- Aplicar métodos supervisionados e não supervisionados para resolver problemas reais.
- Avaliar, adaptar e comparar algoritmos em diferentes contextos.
- Desenvolver soluções práticas por meio de projetos em grupo com abordagem PBL.

## 🧠 Metodologia

A disciplina utiliza **Aprendizagem Baseada em Projetos (PBL)**. Os estudantes formam grupos para resolver problemas reais com técnicas de ML, combinando teoria e prática.  

Outros instrumentos de avaliação:
- Mini-Trabalhos (MinT)
- Projetos (PBL1, PBL2 e PBL3)
- Avaliações 360°
- Participação colaborativa

## 🧪 Requisitos Técnicos

Certifique-se de ter o Python 3.10 ou superior instalado.

### 📦 Bibliotecas Python utilizadas

```bash
pip install -r requirements.txt
```

**`requirements.txt`:**
```txt
scikit-learn
pandas
numpy
matplotlib
seaborn
minisom
tensorflow
pyarrow
pytest
notebook
```

Outras bibliotecas frequentemente utilizadas:
- scipy
- keras
- pytorch (opcional)
- mlflow (para versionamento de experimentos)

## ⚙️ Ambiente de Desenvolvimento

Você pode usar os seguintes ambientes:

### Ambiente Local
- [Jupyter Notebook](https://jupyter.org/)
- [VS Code + Python Extension](https://code.visualstudio.com/)
- [PyCharm](https://www.jetbrains.com/pycharm/)
- [Anaconda + Spyder](https://www.anaconda.com/)

### Ambiente Remoto
- [Google Colab](https://colab.research.google.com/)
- [Kaggle Kernels](https://www.kaggle.com/kernels)
- [AWS SageMaker](https://aws.amazon.com/sagemaker/)
- [Azure ML Studio](https://azure.microsoft.com/en-us/products/machine-learning/)

## ▶️ Executando os Notebooks

Os 29 arquivos `.ipynb` estão em `src/`. Seus nomes originais foram preservados. Para executá-los:

1. Clone este repositório:
```bash
git clone https://github.com/sergioaafreitas/CAM.git
cd CAM
```

2. Crie um ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate      # Windows
```

3. Instale os pacotes necessários:
```bash
pip install -r requirements.txt
```

Os notebooks que leem arquivos locais procuram `data/` tanto a partir da raiz do repositório quanto de `src/`.

4. Inicie o Jupyter:
```bash
jupyter notebook
```

## 🧪 Executando os testes

Os testes unitários utilizam `pytest`. Após instalar as dependências, basta executar:

```bash
pytest
```

## 📂 Roteiro dos exemplos

| Etapa | Notebooks em `src/` | Questão principal |
| --- | --- | --- |
| Regressão linear | `3.0`, `4.0`, `5.0`, `5.1`, `5.2` | O que significam coeficientes, resíduos, extrapolação e multicolinearidade? |
| Regularização e regressão não linear | `5.3`, os dois `6.0`, `7.0` | Como regularização e escolha de kernel afetam ajuste e erro fora do treino? |
| Classificação básica | `8.0`, `8.1`, `9.0`, `10.0` | Como interpretar probabilidades, erros por classe e protótipos? |
| SVM e projeção | os quatro `11.0` | Como margem, kernel e redução de dimensão mudam o que se vê? |
| Avaliação e seleção | os três `12.0` | Qual métrica responde à pergunta e como evitar vazamento na validação? |
| Redução de dimensão | `13.0` PCA, `13.0` LDA, `13.1` | Qual a diferença entre projeção supervisionada e não supervisionada? |
| Agrupamento | os dois `14.0`, `14.1`, `14.2`, `16.0` | Como escolher grupos, interpretar probabilidades e escalas? |
| Rede neural | `17.0` | A MLP melhora uma linha de base simples? |

Cada notebook identifica o autor, apresenta objetivo, pergunta-guia, interpretação, limite e exercício. Execute primeiro o exemplo; em seguida, altere um parâmetro ou conjunto de dados, registre uma métrica e explique o que a evidência sustenta. Figuras ajustadas com todos os dados servem para explorar padrões e não substituem avaliação em teste.

Dez conjuntos de dados em `data/` estão reservados como extensões nos exercícios: `4.1`, `4.2`, `6.1`, `7.1`, `7.2`, `9.1`, `10.1`, `11.1`, `11.2` e `12.1`. Inspecione colunas, unidades, alvo e valores ausentes antes de modelar. O arquivo `12.1 - dados_comentarios.csv` pode servir a uma atividade nova sobre representação de texto e avaliação de classificação.

**Autor dos notebooks:** Prof. Dr. Sergio Antônio Andrade de Freitas. A autoria aparece no início e nos metadados de cada notebook.

## 📚 Referências Bibliográficas

- Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*.
- Abu-Mostafa, Y. S. et al. (2012). *Learning from Data*.
- Mitchell, T. (1997). *Machine Learning*.
- Géron, A. (2023). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow*.
- Sicsú, A. L. et al. (2023). *Técnicas de machine learning*.
- Vaswani et al. (2017). *Attention Is All You Need*.
- Outras no plano de ensino (vide plano de ensino).

## 👨‍🏫 Contato

Prof. Dr. Sergio Antônio Andrade de Freitas  
📧 sergiofreitas@unb.br  
🔗 [Lattes](http://lattes.cnpq.br/0395549254894676)  
🌐 [CEDIS - UnB](https://cedis.unb.br)

## 📢 Observação

Todos os projetos devem seguir as diretrizes de entrega descritas no plano de ensino. As submissões dos Mini-Trabalhos e checkpoints PBL devem ser realizadas via Microsoft Teams da disciplina.
