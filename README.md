# Machine Learning Course (FGA0083)  
Release: Mar/2025  

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

Os arquivos `.ipynb` estão numerados conforme o conteúdo didático (por exemplo, `03 - Regressão - Introdução`, `11.0 - SVM`, `14.0 - K-means`). Para executá-los:

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

Os notebooks que leem arquivos CSV locais foram preparados para funcionar tanto com o diretório atual na raiz do repositório quanto dentro de `src/`.

4. Inicie o Jupyter:
```bash
jupyter notebook
```

## 🧪 Executando os testes

Os testes unitários utilizam `pytest`. Após instalar as dependências, basta executar:

```bash
pytest
```

## 📂 Estrutura do Repositório

```
├── 01 - Introdução ao Aprendizado de Máquina.pptx
├── 02 - Conceitos básicos e ambiente de desenvolvimento.pptx
├── 03 - Regressão - Introdução.pptx
├── 5.x, 6.x, 7.x, ... (Notebooks com exemplos de regressão, classificação, SVM, etc.)
├── glossario.pdf
├── guia_projetos_ml.pdf
├── plano_de_ensino.pdf
├── requirements.txt
└── README.md
```

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
