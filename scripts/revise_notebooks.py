"""Aplica a revisão didática aos notebooks da disciplina.

Execute a partir da raiz do repositório: python3 scripts/revise_notebooks.py.
O script é idempotente: notebooks já revisados não são alterados.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTHOR = "Prof. Dr. Sergio Antônio Andrade de Freitas"


def lines(text: str) -> list[str]:
    return text.strip("\n").splitlines(keepends=True)


def markdown(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": lines(text)}


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": lines(text),
    }


# Objetivo, pergunta de interpretação, limite e exercício de transferência.
GUIDES = {
    "3.0 - exemplo.ipynb": (
        "Regressão linear com scikit-learn", "Horas de estudo (h) e nota simulada; identificar inclinação e intercepto.",
        "A reta descreve bem todos os pontos? Examine os resíduos antes de prever outra nota.",
        "A figura e as previsões são feitas nos mesmos dados usados no ajuste; não estimam generalização.",
        "Separe duas observações para teste e compare erro no treino e no teste. Experimente os dados de `data/4.1 - dados_bicicletas.csv` após identificar colunas e unidades."),
    "4.0 - exemplo.ipynb": (
        "Mínimos quadrados em dados sintéticos", "Recuperar aproximadamente nota inicial 5 e ganho de 0,5 por hora.",
        "Quanto os coeficientes estimados se afastam dos parâmetros usados para gerar os dados?",
        "A inversão explícita da matriz normal pode ser instável; o exemplo passa a usar mínimos quadrados numéricos.",
        "Altere o nível de ruído e compare erro e coeficientes. Use `data/4.2 - dados_aluguel_bicicletas.csv` como extensão, documentando as unidades."),
    "5.0 - exemplo.ipynb": (
        "Regressão linear calculada à mão", "Calcular inclinação e intercepto a partir de cinco pares observados.",
        "A previsão para 6 horas está dentro ou fora da faixa de treino?",
        "Cinco observações não bastam para estabelecer capacidade de previsão em outros alunos.",
        "Compare os coeficientes manuais com `LinearRegression` e desenhe resíduos."),
    "5.1 - otimização simples.ipynb": (
        "Reta de mínimos quadrados para carga de CPU", "Estimar tempo de resposta (ms) a partir de carga de CPU (%).",
        "A previsão em 60% é extrapolação? O que o alinhamento perfeito dos cinco pontos esconde?",
        "Os dados perfeitamente lineares são artificiais e não representam a variabilidade de um sistema real.",
        "Introduza ruído e compare previsões. Depois investigue `data/7.1 - dados_consumo_energia.csv`."),
    "5.2 - otimização com regressão múltipla.ipynb": (
        "Regressão múltipla e multicolinearidade", "Explicar vendas por visitantes e investimento em publicidade.",
        "Como interpretar um coeficiente quando a outra variável também varia?",
        "Variáveis perfeitamente dependentes tornam os coeficientes não identificáveis; o exemplo usa variáveis independentes.",
        "Faça publicidade = visitantes + 1000 e observe o posto da matriz; compare a solução com `np.linalg.lstsq`."),
    "5.3 - otimização com regularização Lasso.ipynb": (
        "Seleção de variáveis com Lasso", "Recuperar as variáveis realmente associadas ao alvo sintético.",
        "Quais coeficientes o Lasso reduz a zero e como isso muda com alpha?",
        "O alvo é sintético e contínuo; não representa adesão clínica.",
        "Compare alpha em validação e tente `data/6.1 - dados_elastic_net_regression.csv` como extensão."),
    "6.0 - lasso regression.ipynb": (
        "Regressão Lasso", "Comparar o efeito de alpha no coeficiente e no erro.",
        "Com apenas uma variável, o que a penalidade L1 consegue mostrar?",
        "Use este resultado como ponto de partida; a diferença L1 versus L2 aparece melhor com várias características.",
        "Compare com o notebook Ridge e depois acrescente variáveis correlacionadas."),
    "6.0 - ridge regression.ipynb": (
        "Regressão Ridge", "Comparar o efeito de alpha no coeficiente e no erro.",
        "O que ocorre com o coeficiente quando alpha aumenta?",
        "O exemplo univariado ilustra encolhimento, mas não demonstra seleção de variáveis.",
        "Compare com Lasso nos mesmos dados e repita com múltiplas características."),
    "7.0 - rbf_regression.ipynb": (
        "Regressão com SVR e kernel RBF", "Modelar uma relação não linear e avaliar erro fora do treino.",
        "Onde o modelo erra mais? Como C, gamma e epsilon mudam a curva?",
        "O conjunto de teste deve ser usado para avaliação, não para escolher hiperparâmetros.",
        "Ajuste hiperparâmetros com validação no treino e aplique a técnica a `data/7.2 - dados_previsao_bicicletas.csv`."),
    "8.0 - logistic_regression.ipynb": (
        "Regressão logística binária", "Classificar observações e ler probabilidades e erros por classe.",
        "Quantos positivos o modelo deixa passar? A acurácia resume esse problema?",
        "O limiar 0,5 é uma escolha e deve refletir o custo dos erros.",
        "Varie o limiar usando apenas uma validação separada; compare precisão e recall."),
    "8.1 - saude cardiaca.ipynb": (
        "Saúde cardíaca: avaliação crítica", "Examinar um resultado perfeito em dados didáticos.",
        "A acurácia de 100% se repete em outras divisões? Que informações faltam para uso clínico?",
        "Sem procedência e validação externa, o resultado não sustenta uma aplicação diagnóstica.",
        "Repita a análise com validação estratificada e descreva o que seria necessário para validação externa."),
    "9.0 - iris_dataset.ipynb": (
        "KNN no conjunto Iris", "Testar diferentes valores de k com escala ajustada somente no treino.",
        "O melhor k em validação também funciona no teste?",
        "O gráfico mostra duas variáveis; o modelo usa quatro.",
        "Replique o fluxo em `data/9.1 - dados_telecom_knn.csv`, após verificar o alvo e o tipo das colunas."),
    "10.0 - classificacao prototipos.ipynb": (
        "Classificação pelo centroide mais próximo", "Visualizar protótipos e regiões de decisão.",
        "Quais classes se confundem e por que a distância ao centroide pode falhar?",
        "Um centroide por classe não representa classes multimodais.",
        "Compare KNN nos mesmos dados e explore `data/10.1 - dados_classificacao_prototipos.csv`."),
    "11.0 - exemplo SVM.ipynb": (
        "SVM linear em três dimensões", "Visualizar hiperplano, vetores de suporte e margem.",
        "Quais pontos determinam o hiperplano e o que muda ao alterar C?",
        "A visualização usa dados de treino; inclua teste antes de afirmar generalização.",
        "Avalie em treino e teste e teste `data/11.1 - dados_credito_svm.csv`."),
    "11.0 - SVM com Kernel RBF.ipynb": (
        "SVM com kernel RBF", "Visualizar uma fronteira não linear em `make_moons`.",
        "O que gamma e C alteram na fronteira e nos erros?",
        "Uma fronteira que segue o treino não garante desempenho em novos dados.",
        "Separe teste, compare valores de C/gamma e explore `data/11.2 - dados_ecommerce_svm.csv`."),
    "11.0 - SVM com kernel polinomial.ipynb": (
        "Kernel polinomial em círculos concêntricos", "Comparar graus 2 e 3 na mesma amostra.",
        "Por que grau 2 separa melhor este padrão radial?",
        "A comparação de ajuste no treino é uma demonstração geométrica, não uma avaliação de generalização.",
        "Repita com uma divisão treino/teste e compare com RBF."),
    "11.0 - gerador do gráfico.ipynb": (
        "Projeção PCA de dados com 100 dimensões", "Comparar duas variáveis originais com duas componentes principais.",
        "Quanta variância as duas componentes preservam? As cores entram no ajuste do PCA?",
        "Separação visual não implica melhor classificação; o PCA é não supervisionado.",
        "Compare PCA com LDA e avalie um classificador dentro de pipeline."),
    "12.0 - Critérios de Avaliação.ipynb": (
        "Critérios de avaliação de classificadores", "Ler matriz de confusão, precisão, recall, F1 e importância de atributos.",
        "Quando acurácia pode esconder erros importantes?",
        "Importância de atributo não é uma medida de qualidade preditiva nem prova causalidade.",
        "Crie um alvo desbalanceado e compare as métricas com a classe majoritária. Como extensão, inspecione `data/12.1 - dados_comentarios.csv` e defina uma avaliação de classificação de texto."),
    "12.0 - Evitando sobreajuste.ipynb": (
        "Seleção de atributos sem vazamento", "Comparar validação cruzada com todas as variáveis e com seleção dentro de pipeline.",
        "A pequena diferença entre médias justifica afirmar que selecionar atributos é melhor?",
        "A seleção deve ser ajustada em cada dobra; variações pequenas exigem cautela.",
        "Varie k e profundidade da árvore usando validação aninhada."),
    "12.0 - ganho de informação.ipynb": (
        "Entropia e ganho de informação", "Calcular a redução de incerteza ao dividir uma característica.",
        "O corte na média maximiza o ganho? Compare os tamanhos e classes de cada lado.",
        "O corte didático na média pode ser diferente do escolhido por uma árvore.",
        "Calcule o ganho para vários cortes possíveis e encontre o melhor."),
    "13.0 - PCA copy.ipynb": (
        "PCA no Iris", "Reduzir quatro medidas a duas componentes sem usar o rótulo.",
        "Qual a proporção de variância preservada pelas duas componentes?",
        "A projeção depende da escala das variáveis e não mede desempenho de classificação.",
        "Compare as posições com o notebook LDA e padronize os dados antes do PCA."),
    "13.0 - LDA.ipynb": (
        "LDA no Iris", "Reduzir quatro medidas a duas direções discriminantes usando os rótulos.",
        "Por que há no máximo duas direções para três classes?",
        "Uma figura ajustada em todos os dados não é avaliação em teste.",
        "Compare com PCA e use LDA dentro de pipeline para classificação em teste."),
    "13.1 - LDA german credit data.ipynb": (
        "LDA no German Credit", "Codificar categorias e visualizar a separação entre classes de crédito.",
        "Há sobreposição entre as distribuições? Qual classe é menos frequente?",
        "A projeção exploratória usa todos os dados. Para predição, ajuste transformações só no treino. A codificação gera colunas correlacionadas; usamos covariância regularizada e verificamos se a projeção é finita.",
        "Monte pipeline de codificação, escala e LDA; avalie recall da classe de maior custo."),
    "14.0 - K-means.ipynb": (
        "K-means em dados sintéticos", "Visualizar atribuição rígida e centros de três grupos.",
        "Como a escolha de k altera a inércia e os agrupamentos?",
        "Os eixos são características sintéticas sem unidades físicas.",
        "Compare k=2, 3 e 4 e confronte com o GMM na mesma amostra."),
    "14.0 - gaussiana.ipynb": (
        "Mistura gaussiana em dados sintéticos", "Visualizar centros e probabilidades de pertinência.",
        "Quais pontos têm classificação mais incerta?",
        "As componentes são gaussianas estimadas, não categorias necessariamente reais.",
        "Compare com K-means e varie o número de componentes."),
    "14.1 - Kmeans.ipynb": (
        "Segmentação de clientes com K-means", "Padronizar quatro medidas não redundantes e interpretar quatro segmentos nas unidades originais.",
        "Os grupos diferem principalmente em renda ou em gastos?",
        "As duas dimensões do gráfico não exibem toda a distância usada pelo modelo. `Gastos em Alimentos` é exatamente `Gastos em Roupas + 1000` neste arquivo; duplicá-lo daria peso extra à mesma informação.",
        "Compare k=2 a 6 com silhueta e discuta estabilidade dos perfis."),
    "14.2 - Gauss.ipynb": (
        "Segmentação de clientes com GMM", "Interpretar médias e incerteza de quatro componentes.",
        "Quais clientes têm menor probabilidade da classe atribuída?",
        "Um componente estatístico não deve receber um rótulo de negócio sem examinar seu perfil. `Gastos em Alimentos` é exatamente `Gastos em Roupas + 1000` neste arquivo; duplicá-lo daria peso extra à mesma informação.",
        "Compare BIC para diferentes números de componentes e confronte com K-means."),
    "16.0 - SOM.ipynb": (
        "Mapa auto-organizável no Iris", "Projetar observações em uma grade preservando vizinhança aproximada.",
        "Quantas observações podem ocupar o mesmo neurônio?",
        "O SOM é não supervisionado; cores por espécie servem apenas para interpretação posterior.",
        "Varie o tamanho do mapa e o número de iterações; compare o mapa de distâncias."),
    "17.0 - rede_neural.ipynb": (
        "Rede neural MLP no Iris", "Comparar MLP padronizada com uma linha de base simples.",
        "O ganho sobre a linha de base compensa maior complexidade?",
        "`early_stopping` retira parte do treino para validação; o teste continua reservado.",
        "Varie camadas e semente, registre curva de perda e estabilidade da acurácia."),
}


EXTRA_CODE = {
    "3.0 - exemplo.ipynb": """from sklearn.metrics import mean_absolute_error
print(f'Inclinação: {modelo.coef_[0]:.3f}; intercepto: {modelo.intercept_:.3f}')
print(f'MAE no treino: {mean_absolute_error(y, y_pred):.3f}')
print('Resíduos:', np.round(y - y_pred, 2))
from sklearn.model_selection import train_test_split
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
modelo_teste = LinearRegression().fit(X_tr, y_tr)
print(f'MAE em 2 observações reservadas: {mean_absolute_error(y_te, modelo_teste.predict(X_te)):.3f}')
""",
    "4.0 - exemplo.ipynb": """print('Parâmetros usados na geração: intercepto=5; ganho por hora=0.5')
print('Estimativas:', theta_best.ravel().round(3))
print('Erro médio absoluto:', np.mean(np.abs(notas - X_b @ theta_best)).round(3))
""",
    "5.0 - exemplo.ipynb": """from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
modelo_sklearn = LinearRegression().fit([[x] for x in horas_estudadas], notas_obtidas)
print('Coeficientes concordam:', abs(modelo_sklearn.coef_[0] - m) < 1e-12)
print('MAE no treino:', round(mean_absolute_error(notas_obtidas, modelo_sklearn.predict([[x] for x in horas_estudadas])), 3))
print('6 horas é extrapolação:', horas_estudo > max(horas_estudadas))
""",
    "5.1 - otimização simples.ipynb": """print('Faixa observada:', min(carga_cpu), 'a', max(carga_cpu), '%')
print('60% está fora da faixa observada:', carga_cpu_pred > max(carga_cpu))
print('Resíduos no treino:', [round(y - (m * x + b), 2) for x, y in zip(carga_cpu, tempo_resposta)])
""",
    "6.0 - lasso regression.ipynb": """from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.25, random_state=42)
for alpha in (0.01, 0.1, 1.0):
    pipe = make_pipeline(StandardScaler(), Lasso(alpha=alpha))
    mae_cv = -cross_val_score(pipe, X_treino, y_treino, cv=5, scoring='neg_mean_absolute_error').mean()
    pipe.fit(X_treino, y_treino)
    print(f'alpha={alpha}: coeficiente padronizado={pipe[-1].coef_[0]:.2f}, MAE validação={mae_cv:.2f}, MAE teste={mean_absolute_error(y_teste, pipe.predict(X_teste)):.2f}')
""",
    "6.0 - ridge regression.ipynb": """from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.25, random_state=42)
for alpha in (0.01, 0.1, 1.0):
    pipe = make_pipeline(StandardScaler(), Ridge(alpha=alpha))
    mae_cv = -cross_val_score(pipe, X_treino, y_treino, cv=5, scoring='neg_mean_absolute_error').mean()
    pipe.fit(X_treino, y_treino)
    print(f'alpha={alpha}: coeficiente padronizado={pipe[-1].coef_[0]:.2f}, MAE validação={mae_cv:.2f}, MAE teste={mean_absolute_error(y_teste, pipe.predict(X_teste)):.2f}')
""",
    "7.0 - rbf_regression.ipynb": """from sklearn.metrics import mean_absolute_error, root_mean_squared_error
print(f'MAE no teste: {mean_absolute_error(y_test, y_pred):.3f}')
print(f'RMSE no teste: {root_mean_squared_error(y_test, y_pred):.3f}')
grade = np.linspace(X.min(), X.max(), 300).reshape(-1, 1)
plt.scatter(X_train, y_train, alpha=0.5, label='Treino')
plt.scatter(X_test, y_test, alpha=0.7, label='Teste')
plt.plot(grade, model_rbf.predict(grade), color='black', label='SVR em grade contínua')
plt.legend(); plt.xlabel('X'); plt.ylabel('y'); plt.show()
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
busca = GridSearchCV(make_pipeline(StandardScaler(), SVR(kernel='rbf')),
                     {'svr__C': [1, 10, 100], 'svr__gamma': [0.01, 0.1, 1], 'svr__epsilon': [0.1, 0.5]},
                     cv=5, scoring='neg_mean_absolute_error')
busca.fit(X_train, y_train)
print('Melhores parâmetros em validação:', busca.best_params_)
print('MAE no teste após seleção:', round(mean_absolute_error(y_test, busca.predict(X_test)), 3))
""",
    "8.0 - logistic_regression.ipynb": """from sklearn.metrics import precision_score, recall_score
X_ajuste, X_valid, y_ajuste, y_valid = train_test_split(X_train, y_train, test_size=0.25, stratify=y_train, random_state=1)
modelo_valid = LogisticRegression(max_iter=1000).fit(X_ajuste, y_ajuste)
prob_valid = modelo_valid.predict_proba(X_valid)[:, 1]
for limiar in (0.3, 0.5, 0.7):
    previsto = (prob_valid >= limiar).astype(int)
    print(f'limiar={limiar}: precisão validação={precision_score(y_valid, previsto, zero_division=0):.2f}; recall validação={recall_score(y_valid, previsto, zero_division=0):.2f}')
print('Escolha o limiar na validação conforme o custo dos erros; preserve o teste para a avaliação final.')
print('Matriz: linhas=real, colunas=previsto; falso negativo=[1,0].')
""",
    "8.1 - saude cardiaca.ipynb": """from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import recall_score
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=42)
pipeline_cv = make_pipeline(StandardScaler(), LogisticRegression(solver='liblinear'))
acuracias = cross_val_score(pipeline_cv, X, y, cv=cv, scoring='accuracy')
print(f'Validação estratificada repetida: média={acuracias.mean():.3f}, mínimo={acuracias.min():.3f}, máximo={acuracias.max():.3f}')
print(f'Recall da classe positiva no teste reservado: {recall_score(y_test, predicoes):.3f}')
""",
    "9.0 - iris_dataset.ipynb": """from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score, StratifiedKFold
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores_k = {}
for k in (1, 3, 5, 9):
    candidato = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k))
    scores_k[k] = cross_val_score(candidato, X_train, y_train, cv=cv).mean()
    print(f'k={k}: acurácia média em validação={scores_k[k]:.3f}')
melhor_k = max(scores_k, key=scores_k.get)
final = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=melhor_k)).fit(X_train, y_train)
print(f'k escolhido={melhor_k}; acurácia no teste reservado={final.score(X_test, y_test):.3f}')
""",
    "10.0 - classificacao prototipos.ipynb": """import numpy as np
from sklearn.neighbors import KNeighborsClassifier
xx, yy = np.meshgrid(np.linspace(X[:,0].min()-1, X[:,0].max()+1, 150),
                     np.linspace(X[:,1].min()-1, X[:,1].max()+1, 150))
grade = np.c_[xx.ravel(), yy.ravel()]
plt.contourf(xx, yy, modelo_prototipos.predict(grade).reshape(xx.shape), alpha=0.3)
plt.scatter(X_test[:,0], X_test[:,1], c=y_test, edgecolor='k', label='Classes reais')
plt.scatter(*modelo_prototipos.centroids_.T, marker='X', s=160, c='red', label='Centroides')
plt.legend(); plt.xlabel('Característica 1'); plt.ylabel('Característica 2'); plt.show()
vizinho = KNeighborsClassifier(n_neighbors=3).fit(X_train, y_train)
print('Acurácia centroide:', modelo_prototipos.score(X_test, y_test))
print('Acurácia KNN:', vizinho.score(X_test, y_test))
""",
    "11.0 - exemplo SVM.ipynb": """from sklearn.model_selection import train_test_split
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
for C in (0.1, 1, 10):
    comparacao = svm.SVC(kernel='linear', C=C).fit(X_treino, y_treino)
    print(f'C={C}: treino={comparacao.score(X_treino, y_treino):.2f}; teste={comparacao.score(X_teste, y_teste):.2f}; vetores de suporte={len(comparacao.support_vectors_)}')
""",
    "11.0 - SVM com Kernel RBF.ipynb": """from sklearn.model_selection import train_test_split
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
for C, gamma in ((0.1, 0.1), (1, 1), (100, 10)):
    comparacao = SVC(kernel='rbf', C=C, gamma=gamma).fit(X_treino, y_treino)
    print(f'C={C}, gamma={gamma}: treino={comparacao.score(X_treino,y_treino):.2f}; teste={comparacao.score(X_teste,y_teste):.2f}; suportes={len(comparacao.support_vectors_)}')
""",
    "11.0 - gerador do gráfico.ipynb": """print('Variância explicada por PC1 e PC2:', pca.explained_variance_ratio_.round(3))
print('Variância total nas duas componentes:', round(pca.explained_variance_ratio_.sum(), 3))
""",
    "12.0 - ganho de informação.ipynb": """from sklearn.tree import DecisionTreeClassifier
print('Classes antes:', np.bincount(y))
print('Classes à esquerda:', np.bincount(left_split, minlength=len(np.unique(y))))
print('Classes à direita:', np.bincount(right_split, minlength=len(np.unique(y))))
arvore = DecisionTreeClassifier(max_depth=1, criterion='entropy', random_state=42).fit(X[:, [3]], y)
print(f'Corte da árvore: {arvore.tree_.threshold[0]:.3f}; corte na média: {mean_petal_width:.3f}')
""",
    "13.0 - PCA copy.ipynb": """from sklearn.preprocessing import StandardScaler
X_padronizado = StandardScaler().fit_transform(X)
pca_padronizado = PCA(n_components=2).fit(X_padronizado)
print('Variância explicada sem escala:', pca.explained_variance_ratio_.round(3))
print('Variância explicada com escala:', pca_padronizado.explained_variance_ratio_.round(3))
""",
    "13.0 - LDA.ipynb": """print('Classes:', len(set(y)), '; máximo de componentes LDA:', len(set(y)) - 1)
print('Proporção discriminante nas direções:', lda.explained_variance_ratio_.round(3))
""",
    "13.1 - LDA german credit data.ipynb": """print('Distribuição das classes (1=bom, 0=mau):', y.value_counts().sort_index().to_dict())
print('Características após codificação:', X.shape[1])
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
X_raw = data.drop(columns='Good_Bad')
numericas = X_raw.select_dtypes(include='number').columns.tolist()
categoricas = X_raw.select_dtypes(exclude='number').columns.tolist()
preparacao = ColumnTransformer([
    ('numericas', StandardScaler(), numericas),
    ('categoricas', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categoricas),
])
X_treino, X_teste, y_treino, y_teste = train_test_split(
    X_raw, y, test_size=0.25, random_state=42, stratify=y)
modelo_credito = make_pipeline(preparacao, LDA(solver='lsqr', shrinkage='auto'))
with np.errstate(divide='ignore', over='ignore', invalid='ignore'):
    modelo_credito.fit(X_treino, y_treino)
    previsto = modelo_credito.predict(X_teste)
    scores_credito = modelo_credito.decision_function(X_teste)
assert np.isfinite(scores_credito).all(), 'Pontuações não finitas no LDA'
print('Matriz de confusão (0=mau, 1=bom):')
print(confusion_matrix(y_teste, previsto, labels=[0, 1]))
print(classification_report(y_teste, previsto, labels=[0, 1], target_names=['mau', 'bom']))
""",
    "14.0 - K-means.ipynb": """for k in (2, 3, 4):
    candidato = KMeans(n_clusters=k, random_state=0, n_init=10).fit(X)
    print(f'k={k}: inércia={candidato.inertia_:.1f}')
""",
    "14.0 - gaussiana.ipynb": """for k in (2, 3, 4):
    candidato = GaussianMixture(n_components=k, random_state=0).fit(X)
    print(f'componentes={k}: BIC={candidato.bic(X):.1f}')
""",
    "14.1 - Kmeans.ipynb": """import numpy as np
from sklearn.metrics import silhouette_score
for k in range(2, 7):
    with np.errstate(divide='ignore', over='ignore', invalid='ignore'):
        candidato = KMeans(n_clusters=k, random_state=0, n_init=10).fit(X_scaled)
        silhueta = silhouette_score(X_scaled, candidato.labels_)
    assert np.isfinite(silhueta), 'Silhueta não finita'
    print(f'k={k}: silhueta={silhueta:.3f}')
""",
    "14.2 - Gauss.ipynb": """probabilidades = gmm.predict_proba(X_scaled)
print('Tamanhos dos grupos:', data['Cluster'].value_counts().sort_index().to_dict())
print('Perfis médios nas unidades originais:')
print(data.groupby('Cluster')[X.columns].mean().round(1))
print('Menor confiança da atribuição:', round(probabilidades.max(axis=1).min(), 3))
for k in range(2, 7):
    candidato = GaussianMixture(n_components=k, random_state=0).fit(X_scaled)
    print(f'componentes={k}: BIC={candidato.bic(X_scaled):.1f}')
""",
    "16.0 - SOM.ipynb": """plt.figure(figsize=(6, 5))
plt.imshow(som.distance_map().T, cmap='bone_r', origin='lower')
plt.colorbar(label='Distância média aos neurônios vizinhos')
plt.title('Mapa de distâncias do SOM'); plt.xlabel('X'); plt.ylabel('Y'); plt.show()
""",
    "17.0 - rede_neural.ipynb": """from sklearn.linear_model import LogisticRegression
base = Pipeline([('scaler', StandardScaler()), ('modelo', LogisticRegression(max_iter=1000))])
base.fit(X_train, y_train)
print(f'Acurácia da regressão logística no mesmo teste: {accuracy_score(y_test, base.predict(X_test)):.2f}')
print(f'Épocas da MLP: {pipeline[-1].n_iter_}; melhor validação interna: {pipeline[-1].best_validation_score_:.2f}')
import matplotlib.pyplot as plt
plt.plot(pipeline[-1].loss_curve_)
plt.xlabel('Época'); plt.ylabel('Perda no treino'); plt.title('Curva de perda da MLP'); plt.show()
""",
}

MULTIVARIATE_REGULARIZATION = """# Extensão: variáveis correlacionadas tornam L1 e L2 mais fáceis de comparar.
import numpy as np
from sklearn.linear_model import Lasso, Ridge
rng_comparacao = np.random.default_rng(42)
X_multi = np.column_stack([
    X[:, 0],
    X[:, 0] + rng_comparacao.normal(scale=0.1, size=len(X)),
    rng_comparacao.normal(size=len(X)),
])
X_multi_treino, X_multi_teste, y_multi_treino, y_multi_teste = train_test_split(
    X_multi, y, test_size=0.25, random_state=42)
for tipo in (Lasso(alpha=1), Ridge(alpha=1)):
    modelo_multi = make_pipeline(StandardScaler(), tipo).fit(X_multi_treino, y_multi_treino)
    print(f'{tipo.__class__.__name__}: coeficientes={np.round(modelo_multi[-1].coef_, 2)}, '
          f'MAE teste={mean_absolute_error(y_multi_teste, modelo_multi.predict(X_multi_teste)):.2f}')
"""
for regularization_notebook in ("6.0 - lasso regression.ipynb", "6.0 - ridge regression.ipynb"):
    EXTRA_CODE[regularization_notebook] += MULTIVARIATE_REGULARIZATION


def replace_once(source: str, old: str, new: str, name: str) -> str:
    if old not in source:
        raise ValueError(f"Trecho não encontrado em {name}: {old[:80]!r}")
    return source.replace(old, new, 1)


def main() -> None:
    paths = sorted((ROOT / "src").glob("*.ipynb"))
    assert {p.name for p in paths} == set(GUIDES)
    for path in paths:
        notebook = json.loads(path.read_text(encoding="utf-8"))
        if notebook.get("metadata", {}).get("cam_didactic_revision") == 1:
            continue
        title, objective, question, limit, exercise = GUIDES[path.name]
        header = markdown(
            f"# {title}\n\n**Autor:** {AUTHOR}  \n**Material da disciplina:** FGA0083 — Aprendizado de Máquina, UnB\n\n"
            f"## Objetivo e dados\n\n{objective}\n\n"
            f"**Pergunta-guia:** {question}\n\n"
            "Execute as células na ordem e interprete os resultados antes de fazer o exercício."
        )
        source_cells = [
            cell for cell in notebook["cells"]
            if cell["cell_type"] != "code" or "".join(cell.get("source", [])).strip()
        ]
        notebook["cells"] = [header, *source_cells]
        body = next(c for c in notebook["cells"] if c["cell_type"] == "code")
        source = "".join(body["source"])
        source = revise_code(path.name, source)
        body["source"] = lines(source)
        body["execution_count"] = None
        body["outputs"] = []
        if path.name == "8.1 - saude cardiaca.ipynb":
            # A conclusão antiga traz números de uma única execução; tornar a leitura cautelosa.
            notebook["cells"][-1]["source"] = lines(
                "## Discussão\n\nA tabela é didática e a procedência dos registros não está documentada "
                "neste repositório. Uma acurácia perfeita em uma divisão isolada exige investigação: "
                "verifique separação das classes, validação estratificada repetida e dados externos. "
                "Sem isso, não há evidência para uso clínico. Observe especialmente falsos negativos "
                "e o custo de cada tipo de erro."
            )
            # Remover saídas antigas de células que mudaram semanticamente.
            for cell in notebook["cells"]:
                if cell["cell_type"] == "code":
                    cell_source = "".join(cell["source"])
                    cell_source = cell_source.replace(
                        "test_size=0.3, random_state=42)",
                        "test_size=0.3, random_state=42, stratify=y)",
                    )
                    cell_source = cell_source.replace(
                        "sns.countplot(x='DoencaCardiaca', data=df_dados, palette='viridis')",
                        "sns.countplot(x='DoencaCardiaca', hue='DoencaCardiaca', data=df_dados, palette='viridis', legend=False)",
                    )
                    cell["source"] = lines(cell_source)
                    cell["execution_count"] = None
                    cell["outputs"] = []
        if path.name in EXTRA_CODE:
            notebook["cells"].append(markdown("## Investigação complementar\n\nCompare a nova medida com a figura ou o resultado anterior. Explique qualquer diferença observada."))
            notebook["cells"].append(code(EXTRA_CODE[path.name]))
        notebook["cells"].append(markdown(
            f"## Interpretação e limites\n\n{limit}\n\n"
            f"## Exercício\n\n{exercise}\n\n"
            "Registre a hipótese, a mudança realizada, a métrica ou figura observada e uma conclusão "
            "que os dados de fato sustentem."
        ))
        notebook["metadata"]["authors"] = [{"name": AUTHOR}]
        notebook["metadata"]["cam_didactic_revision"] = 1
        path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(path.name)


def revise_code(name: str, source: str) -> str:
    if name == "4.0 - exemplo.ipynb":
        source = replace_once(source,
            "theta_best = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(notas)",
            "theta_best = np.linalg.lstsq(X_b, notas, rcond=None)[0]\nprint(f'Intercepto estimado: {theta_best[0, 0]:.3f}; ganho/hora: {theta_best[1, 0]:.3f}')",
            name)
    elif name == "5.2 - otimização com regressão múltipla.ipynb":
        source = '''import numpy as np
from sklearn.linear_model import LinearRegression

# Visitantes e investimento em publicidade variam independentemente.
# Assim podemos discutir o efeito de uma variável mantendo a outra fixa.
visitantes = np.array([1000, 1500, 2000, 2500, 3000, 1200, 1800, 2600])
publicidade = np.array([2000, 1800, 3300, 2600, 4500, 3800, 2100, 4000])
X = np.column_stack([visitantes, publicidade])
Y = 1000 + 0.8 * visitantes + 0.6 * publicidade + np.array([30, -20, 10, -40, 20, -10, 40, -30])

X_b = np.column_stack([np.ones(len(X)), X])
print(f'Posto da matriz: {np.linalg.matrix_rank(X_b)} de {X_b.shape[1]} colunas')
beta = np.linalg.lstsq(X_b, Y, rcond=None)[0]
modelo = LinearRegression().fit(X, Y)
print(f'Intercepto: {beta[0]:.2f}; visitantes: {beta[1]:.3f}; publicidade: {beta[2]:.3f}')
print('Confere com scikit-learn:', np.allclose(beta[1:], modelo.coef_))
novo = np.array([[3500, 4500]])
print(f'Vendas previstas: R$ {modelo.predict(novo)[0]:.2f}')

# Contraprova: com publicidade = visitantes + 1000, perde-se um grau de liberdade.
X_colinear = np.column_stack([visitantes, visitantes + 1000])
X_colinear_b = np.column_stack([np.ones(len(X)), X_colinear])
print(f'Posto com colinearidade perfeita: {np.linalg.matrix_rank(X_colinear_b)} de 3')
'''
    elif name == "5.3 - otimização com regularização Lasso.ipynb":
        source = '''import numpy as np
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error

rng = np.random.default_rng(0)
X = rng.normal(size=(300, 10))
# Somente três das dez variáveis geram o alvo contínuo.
y = 3 * X[:, 0] - 2 * X[:, 3] + 1.5 * X[:, 7] + rng.normal(scale=0.5, size=300)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
resultados_cv = {}
for alpha in (0.01, 0.1, 1.0):
    modelo = make_pipeline(StandardScaler(), Lasso(alpha=alpha, max_iter=10000))
    rmse_cv = -cross_val_score(modelo, X_train, y_train, cv=5,
                              scoring='neg_root_mean_squared_error').mean()
    resultados_cv[alpha] = rmse_cv
    print(f'alpha={alpha}: RMSE validação={rmse_cv:.3f}')
melhor_alpha = min(resultados_cv, key=resultados_cv.get)
modelo_final = make_pipeline(StandardScaler(), Lasso(alpha=melhor_alpha, max_iter=10000))
modelo_final.fit(X_train, y_train)
rmse_teste = np.sqrt(mean_squared_error(y_test, modelo_final.predict(X_test)))
print(f'alpha escolhido={melhor_alpha}; RMSE no teste reservado={rmse_teste:.3f}')
print('Coeficientes:', np.round(modelo_final[-1].coef_, 2))
'''
    elif name == "12.0 - Critérios de Avaliação.ipynb":
        source = '''import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.3, stratify=iris.target, random_state=42)
rf = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_train, y_train)
y_pred = rf.predict(X_test)
precisao, recall, f1, suporte = precision_recall_fscore_support(
    y_test, y_pred, labels=[0, 1, 2], zero_division=0)
print('Acurácia:', round(accuracy_score(y_test, y_pred), 3))
print('Matriz de confusão (linhas=reais, colunas=previstas):')
print(confusion_matrix(y_test, y_pred))
for classe, p, r, f, n in zip(iris.target_names, precisao, recall, f1, suporte):
    print(f'{classe}: precisão={p:.2f}, recall={r:.2f}, F1={f:.2f}, suporte={n}')

# Importância auxilia a discutir o modelo, mas não mede qualidade nem causalidade.
plt.barh(iris.feature_names, rf.feature_importances_)
plt.xlabel('Importância da característica no modelo')
plt.title('Importância estimada pela floresta aleatória')
plt.show()
'''
    elif name == "11.0 - SVM com kernel polinomial.ipynb":
        source = '''import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_circles
from sklearn.svm import SVC

X, y = make_circles(n_samples=100, factor=0.1, noise=0.1, random_state=42)
xx, yy = np.meshgrid(np.linspace(-1.5, 1.5, 160), np.linspace(-1.5, 1.5, 160))
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, (titulo, modelo) in zip(axes, [
    ('Polinomial grau 2', SVC(kernel='poly', degree=2)),
    ('Polinomial grau 3', SVC(kernel='poly', degree=3)),
    ('RBF', SVC(kernel='rbf')),
]):
    modelo.fit(X, y)
    Z = modelo.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    ax.contourf(xx, yy, Z, alpha=0.5, cmap='coolwarm')
    ax.scatter(X[:, 0], X[:, 1], c=y, cmap='coolwarm', edgecolor='k', s=25)
    ax.scatter(modelo.support_vectors_[:, 0], modelo.support_vectors_[:, 1],
               s=70, facecolors='none', edgecolors='black')
    ax.set_title(f'{titulo}: acerto treino={modelo.score(X, y):.2f}')
    ax.set_xlabel('Característica 1')
    ax.set_ylabel('Característica 2')
plt.tight_layout()
plt.show()
'''
    elif name == "12.0 - Evitando sobreajuste.ipynb":
        source = '''import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.pipeline import make_pipeline

iris = load_iris()
X, y = iris.data, iris.target
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
modelos = {
    'Todas as características': DecisionTreeClassifier(random_state=42),
    'Duas melhores, seleção em cada dobra': make_pipeline(
        SelectKBest(f_classif, k=2), DecisionTreeClassifier(random_state=42)),
}
for titulo, modelo in modelos.items():
    scores = cross_val_score(modelo, X, y, cv=cv, scoring='accuracy')
    print(f'{titulo}: média={scores.mean():.3f}, desvio={scores.std():.3f}, dobras={np.round(scores, 3)}')
'''
    elif name == "14.1 - Kmeans.ipynb":
        source = source.replace(
            "'Gastos em Roupas', 'Gastos em Alimentos', 'Gastos em Eletrônicos'",
            "'Gastos em Roupas', 'Gastos em Eletrônicos'",
        )
        source = replace_once(source,
            "plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=200, alpha=0.75, marker='X', label='Centroides')",
            "centroids_originais = scaler.inverse_transform(centroids)\nplt.scatter(centroids_originais[:, 0], centroids_originais[:, 1], c='red', s=200, alpha=0.75, marker='X', label='Centroides')",
            name)
        source = source.replace("kmeans = KMeans(n_clusters=4, random_state=0)", "kmeans = KMeans(n_clusters=4, random_state=0, n_init=10)")
        source += "\nprint('Tamanho dos grupos:', data['Cluster'].value_counts().sort_index().to_dict())\nprint(data.groupby('Cluster')[X.columns].mean().round(1))\n"
    elif name in {"6.0 - lasso regression.ipynb", "6.0 - ridge regression.ipynb"}:
        source = source.replace(
            "plt.plot(X, y_pred_lasso, color='green'",
            "plt.plot(X[X[:, 0].argsort()], y_pred_lasso[X[:, 0].argsort()], color='green'",
        ).replace(
            "plt.plot(X, y_pred, color='red'",
            "plt.plot(X[X[:, 0].argsort()], y_pred[X[:, 0].argsort()], color='red'",
        )
    elif name == "11.0 - exemplo SVM.ipynb":
        source = source.replace(
            "ax.plot_surface(xx, yy, zz, alpha=0.5)",
            "ax.plot_surface(xx, yy, zz, alpha=0.5, shade=False)\nax.scatter(*model.support_vectors_.T, s=130, facecolors='none', edgecolors='black', label='Vetores de suporte')\nax.legend()",
        )
    elif name == "11.0 - SVM com Kernel RBF.ipynb":
        source = source.replace(
            "plt.title('SVM com Kernel RBF')",
            "plt.scatter(model_rbf.support_vectors_[:, 0], model_rbf.support_vectors_[:, 1], s=100, facecolors='none', edgecolors='black', label='Vetores de suporte')\nplt.legend()\nplt.title('SVM com Kernel RBF')",
        )
    elif name == "14.2 - Gauss.ipynb":
        source = source.replace(
            "'Gastos em Roupas', 'Gastos em Alimentos', 'Gastos em Eletrônicos'",
            "'Gastos em Roupas', 'Gastos em Eletrônicos'",
        )
    elif name == "8.1 - saude cardiaca.ipynb":
        source = source.replace("%matplotlib inline\n", "")
    elif name == "13.1 - LDA german credit data.ipynb":
        source = source.replace("plt.legend(loc='best', title='Classe')\n", "")
        source = source.replace("import pandas as pd\n", "import pandas as pd\nimport numpy as np\n")
        source = source.replace("lda = LDA(n_components=1)", "lda = LDA(n_components=1, solver='eigen', shrinkage='auto')")
        source = source.replace("X_r2 = lda.fit_transform(X, y)",
                                "with np.errstate(divide='ignore', over='ignore', invalid='ignore'):\n    X_r2 = lda.fit_transform(X, y)\nassert np.isfinite(X_r2).all(), 'Projeção LDA não finita'")
    elif name == "16.0 - SOM.ipynb":
        source = source.replace("learning_rate=0.5)", "learning_rate=0.5, random_seed=42)")
        source = source.replace("som.train_random(X, 100)", "som.train_random(X, 1000)")
        source += "\nprint(f'Neurônios ocupados: {len(set(map(tuple, coordinates)))} de 100')\n"
    elif name == "14.0 - K-means.ipynb":
        source = source.replace("KMeans(n_clusters=3)", "KMeans(n_clusters=3, random_state=0, n_init=10)")
        source = source.replace("plt.xlabel('Altura')", "plt.xlabel('Característica sintética 1')").replace("plt.ylabel('Peso')", "plt.ylabel('Característica sintética 2')")
        source += "\nprint('Inércia:', round(kmeans.inertia_, 2))\n"
    elif name == "14.0 - gaussiana.ipynb":
        source = source.replace("GaussianMixture(n_components=3)", "GaussianMixture(n_components=3, random_state=0)")
        source = source.replace("plt.xlabel('Altura')", "plt.xlabel('Característica sintética 1')").replace("plt.ylabel('Peso')", "plt.ylabel('Característica sintética 2')")
        source += "\nprob = gmm.predict_proba(X)\nprint('Menor confiança em uma atribuição:', round(prob.max(axis=1).min(), 3))\n"
    elif name == "17.0 - rede_neural.ipynb":
        source = source.replace("pipeline.fit(X_train, y_train)",
                                "with np.errstate(divide='ignore', over='ignore', invalid='ignore'):\n    pipeline.fit(X_train, y_train)\nassert np.isfinite(pipeline[-1].loss_curve_).all(), 'Perda não finita na MLP'")
        source = source.replace("y_pred = pipeline.predict(X_test)",
                                "with np.errstate(divide='ignore', over='ignore', invalid='ignore'):\n    y_pred = pipeline.predict(X_test)\nassert np.isin(y_pred, np.unique(y_train)).all(), 'Classe prevista desconhecida'")
    return source


if __name__ == "__main__":
    main()
