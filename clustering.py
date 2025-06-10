# -*- coding: utf-8 -*-

# =====================================================================================
# EXPLICAÇÃO GERAL DO CRITÉRIO DE AGRUPAMENTO
# =====================================================================================
#
# O critério fundamental que este código usa para agrupar os pontos é a **proximidade**.
# A regra principal é: um ponto sempre pertence ao grupo (cluster) cujo centro
# (chamado de centroide, marcado com um "X" no gráfico) está mais perto dele.
#
# COMO A "PROXIMIDADE" É MEDIDA?
# -----------------------------
# Para medir a distância entre um ponto e um centroide, o código usa a **Distância
# Euclidiana**. Pense nela como a distância em linha reta que você mediria com uma
# régua no gráfico.
#
# O QUE FAZ UM PONTO SER "MAIS PRÓXIMO" OU "MAIS DISTANTE"?
# --------------------------------------------------------
# São os **valores de suas características** (suas coordenadas) que determinam a distância.
#
# 1. Características Visuais (Coordenadas X e Y):
#    - Se um ponto tem coordenadas (X=5, Y=5) e o centroide tem (X=5.1, Y=5.1),
#      a diferença entre eles é muito pequena. A distância será MÍNIMA.
#    - Se o ponto tem (X=10, Y=10), a diferença é grande. A distância será MÁXIMA.
#
# 2. Característica "Invisível" (Dado Categórico, ex: Espécie da Flor):
#    - O código é inteligente e converte textos (como "setosa", "versicolor") em
#      números (ex: 0, 1, 2). Isso cria uma "coordenada" extra e invisível.
#    - Se dois pontos são da mesma espécie, a diferença nessa coordenada extra é zero,
#      o que os torna "mais próximos" um do outro.
#    - Se são de espécies diferentes, a diferença aumenta, o que os afasta.
#
# CONCLUSÃO:
# A distância final é uma combinação de todas essas diferenças. Um ponto é
# considerado "próximo" de um centroide se a soma de suas semelhanças
# (tanto visuais no gráfico quanto categóricas "invisíveis") for a menor possível.
# Todo o algoritmo trabalha para garantir que cada ponto esteja sempre no grupo
# do centroide mais próximo, considerando todas as suas características.
#
# =====================================================================================


# --- BIBLIOTECAS UTILIZADAS ---
import tkinter as tk  # Biblioteca padrão do Python para criar interfaces gráficas (GUI).
from tkinter import ttk, messagebox  # Componentes mais modernos (ttk) e caixas de mensagem (messagebox).
import math  # Usada para cálculos matemáticos, como a raiz quadrada (sqrt) na distância euclidiana.
import random  # Usada para embaralhar os dados iniciais e garantir aleatoriedade.
from sklearn.datasets import load_iris  # Usada APENAS para carregar um conjunto de dados inicial para o programa.


# --- ETAPA 1 e 5: ESTRUTURA DE DADOS E MANIPULAÇÃO DE DADOS CATEGÓRICOS ---

class Registro:
    """
    Esta classe é o "molde" para cada ponto de dado individual.
    Ela guarda todas as informações de um único ponto no gráfico.
    """
    def __init__(self, caracteristicas, dados_categoricos=None, nome_ponto=""):
        # Garante que as características principais (como coordenadas X e Y) são numéricas.
        if not all(isinstance(x, (int, float)) for x in caracteristicas):
            raise ValueError("Características devem ser numéricas.")

        # --- ATRIBUTOS DO PONTO ---
        self.caracteristicas = list(caracteristicas)  # Lista de valores numéricos (ex: [X, Y]).
        self.dados_categoricos = dados_categoricos or {}  # Dicionário para dados em texto (ex: {'especie': 'setosa'}).
        self.nome_ponto = nome_ponto  # Um nome único para identificar o ponto, ex: "Ponto_10".
        self.cluster = None  # Referência para o objeto Cluster ao qual este ponto pertence. Inicia como None.
        self.eh_centroide = False  # Uma flag (True/False) que indica se este ponto é o centro de um cluster.
        self.cor = "#000000"  # Cor que o ponto terá no gráfico. Inicia como preto.

    def obter_valores_quantitativos(self, mapa_categorico):
        """
        Esta é uma função crucial para a Etapa 5.
        Ela converte a combinação de dados numéricos e categóricos em uma única lista de números,
        permitindo que a distância seja calculada.
        """
        # Começa com a lista de características que já são numéricas.
        valores_numericos = list(self.caracteristicas)

        # Itera sobre os dados categóricos (ex: 'especie': 'setosa').
        for chave, valor in self.dados_categoricos.items():
            # 'chave' seria 'especie', 'valor' seria 'setosa'.
            if chave in mapa_categorico:
                # Se a categoria (ex: 'setosa') já foi mapeada para um número antes...
                if valor in mapa_categorico[chave]:
                    # ...apenas pega o número correspondente e adiciona à lista.
                    valores_numericos.append(mapa_categorico[chave][valor])
                else:
                    # Se for uma categoria nova (ex: 'nova-especie')...
                    # CORREÇÃO APLICADA AQUI:
                    # Verifica se o dicionário da categoria está vazio.
                    if not mapa_categorico[chave]:
                        novo_id = 0 # Se for o primeiro valor para esta chave, o ID é 0.
                    else:
                        # Senão, pega o maior ID existente e soma 1 para criar o próximo.
                        novo_id = max(mapa_categorico[chave].values()) + 1

                    # Mapeia a nova categoria para o novo ID numérico.
                    mapa_categorico[chave][valor] = novo_id
                    valores_numericos.append(novo_id)
            else:
                # Se a característica categórica (ex: 'cor_petala') nunca foi vista antes...
                # ...cria uma nova entrada no mapa e atribui o primeiro ID como 0.
                mapa_categorico[chave] = {valor: 0}
                valores_numericos.append(0)

        # Retorna a lista completa de características convertidas para números.
        return valores_numericos

    def __repr__(self):
        """Método especial para representação em texto do objeto, útil para debug."""
        return f"Ponto({self.nome_ponto}, Carac:{self.caracteristicas}, Cat:{self.dados_categoricos}, Cluster:{self.cluster.id if self.cluster else None})"


class Cluster:
    """
    Esta classe representa um grupo de pontos (Registros).
    Ela gerencia os pontos que pertencem a ela e seu próprio centroide.
    """
    def __init__(self, id, cor, centroide_inicial):
        self.id = id  # ID numérico do cluster (ex: 0, 1, 2...).
        self.cor = cor  # Cor que todos os pontos deste cluster terão no gráfico.
        self.registros = []  # Lista que armazena todos os objetos Registro deste cluster.
        self.centroide = centroide_inicial  # O ponto central do cluster.
        self.centroide.eh_centroide = True  # Marca o registro inicial como sendo um centroide.
        self.adicionar_registro(self.centroide)  # O próprio centroide também faz parte da lista de registros.

    def adicionar_registro(self, registro):
        """Adiciona um ponto (Registro) a este cluster."""
        self.registros.append(registro)
        registro.cluster = self  # Informa ao ponto a qual cluster ele agora pertence.
        registro.cor = self.cor  # Pinta o ponto com a cor do cluster.

    def remover_registro(self, registro):
        """Remove um ponto (Registro) deste cluster."""
        if registro in self.registros:
            self.registros.remove(registro)
            registro.cluster = None  # O ponto agora não pertence a nenhum cluster.
            return True
        return False

    def recalcular_centroide(self, mapa_categorico):
        """
        Recalcula a posição do centroide.
        Isto é feito calculando a média das coordenadas de todos os pontos no cluster.
        """
        if not self.registros:
            return  # Não faz nada se o cluster estiver vazio.

        # Pega o número de coordenadas visuais (ex: 2 para X e Y).
        num_dimensoes_visuais = len(self.registros[0].caracteristicas)
        soma_caracteristicas_visuais = [0] * num_dimensoes_visuais

        # Soma as coordenadas de todos os pontos do cluster.
        for registro in self.registros:
            valores_visuais = registro.caracteristicas
            for i in range(num_dimensoes_visuais):
                soma_caracteristicas_visuais[i] += valores_visuais[i]

        # Divide a soma pelo número de pontos para obter a média.
        media_caracteristicas = [s / len(self.registros) for s in soma_caracteristicas_visuais]

        # Cria um novo Registro "virtual" para ser o centroide.
        # Ele não é um dos pontos de dados originais, mas um ponto calculado.
        self.centroide = Registro(media_caracteristicas, nome_ponto=f"Centroide_{self.id}")
        self.centroide.eh_centroide = True
        self.centroide.cor = self.cor
        self.centroide.cluster = self

    def __repr__(self):
        """Representação em texto do objeto Cluster."""
        return f"Cluster({self.id}, Cor:{self.cor}, Registros:{len(self.registros)})"


# --- CLASSE PRINCIPAL DA APLICAÇÃO ---

class KMeansApp:
    """
    Esta classe controla toda a aplicação: a interface gráfica e a lógica do K-means.
    """
    def __init__(self, root):
        self.root = root  # A janela principal da aplicação.
        self.root.title("Trabalho de Clusterização K-means")
        self.root.geometry("1200x800")

        # --- Atributos de Estado da Aplicação ---
        self.clusters = []  # Lista que armazena todos os objetos Cluster.
        self.todos_registros = []  # Lista com absolutamente todos os pontos de dados.
        self.ponto_selecionado = None  # Guarda o ponto que o usuário clica no gráfico.

        # Mapa global para converter dados de texto em números. Garante consistência.
        # Ex: {'especie': {'setosa': 0, 'versicolor': 1}}
        self.mapa_categorico = {'especie': {}}

        # Paleta de cores para os clusters. Quando um novo cluster é criado, ele pega a próxima cor da lista.
        self.cores_clusters = ["#FF6347", "#4682B4", "#32CD32", "#FFD700", "#6A5ACD", "#D2691E", "#00CED1"]

        # --- Inicialização ---
        self._inicializar_gui()  # Monta os botões, caixas de texto e o canvas.
        self._carregar_dados_iniciais_iris()  # Carrega os dados da Íris para começar.
        self.redesenhar_canvas()  # Desenha os pontos e centroides na tela pela primeira vez.

    def _inicializar_gui(self):
        """Cria e organiza todos os elementos visuais (widgets) da interface."""
        # Frame principal que contém tudo.
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas: a área branca à esquerda onde o gráfico é desenhado.
        self.canvas = tk.Canvas(main_frame, bg="white", width=800, height=700)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # "bind" associa um evento (clique do botão esquerdo do mouse) a uma função.
        self.canvas.bind("<Button-1>", self.selecionar_ponto_no_canvas)

        # Frame de controles: o painel da direita com todas as opções.
        controles_frame = ttk.Frame(main_frame, padding="10", width=350)
        controles_frame.pack(side=tk.RIGHT, fill=tk.Y)
        controles_frame.pack_propagate(False) # Impede o frame de encolher.

        # --- Seção para adicionar um novo ponto ---
        add_frame = ttk.LabelFrame(controles_frame, text="Adicionar Novo Ponto", padding="10")
        add_frame.pack(fill=tk.X, pady=5)
        # Caixas de entrada para as coordenadas e a categoria do novo ponto.
        ttk.Label(add_frame, text="Característica 1 (X):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.entry_x = ttk.Entry(add_frame)
        self.entry_x.grid(row=0, column=1, sticky=tk.EW)
        ttk.Label(add_frame, text="Característica 2 (Y):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.entry_y = ttk.Entry(add_frame)
        self.entry_y.grid(row=1, column=1, sticky=tk.EW)
        ttk.Label(add_frame, text="Categórico (Espécie):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.entry_cat = ttk.Entry(add_frame)
        self.entry_cat.grid(row=2, column=1, sticky=tk.EW)
        # Botão que chama a função para adicionar o ponto.
        ttk.Button(add_frame, text="Adicionar Ponto", command=self.adicionar_novo_ponto).grid(row=3, columnspan=2, pady=10)

        # --- Seção para o ponto selecionado ---
        selected_frame = ttk.LabelFrame(controles_frame, text="Ponto Selecionado", padding="10")
        selected_frame.pack(fill=tk.X, pady=5)
        self.label_ponto_selecionado = ttk.Label(selected_frame, text="Nenhum ponto selecionado.")
        self.label_ponto_selecionado.pack()
        self.btn_remover = ttk.Button(selected_frame, text="Remover Ponto Selecionado", state=tk.DISABLED, command=self.remover_ponto_selecionado)
        self.btn_remover.pack(pady=5)

        # --- Seção para a Análise de Dispersão (Etapa 4) ---
        dispersion_frame = ttk.LabelFrame(controles_frame, text="Análise de Dispersão", padding="10")
        dispersion_frame.pack(fill=tk.X, pady=5)
        ttk.Label(dispersion_frame, text="Limiar de Distância:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.entry_limiar = ttk.Entry(dispersion_frame)
        self.entry_limiar.grid(row=0, column=1, sticky=tk.EW)
        self.entry_limiar.insert(0, "1.5")
        ttk.Label(dispersion_frame, text="Qtd. de Pontos (k):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.entry_k = ttk.Entry(dispersion_frame)
        self.entry_k.grid(row=1, column=1, sticky=tk.EW)
        self.entry_k.insert(0, "3")
        ttk.Button(dispersion_frame, text="Analisar e Criar Novo Cluster", command=self.analisar_e_criar_novo_cluster).grid(row=2, columnspan=2, pady=10)

        # --- Seção de Informações dos Clusters ---
        info_frame = ttk.LabelFrame(controles_frame, text="Informações dos Clusters", padding="10")
        info_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.info_text = tk.Text(info_frame, wrap=tk.WORD, height=10) # Caixa de texto para mostrar dados.
        self.info_text.pack(fill=tk.BOTH, expand=True)

    def _carregar_dados_iniciais_iris(self):
        """Carrega os dados da base Iris e cria os 2 clusters iniciais, como pedido no trabalho."""
        iris = load_iris()
        # Usaremos apenas as duas primeiras características (comprimento e largura da sépala) para poder visualizar em 2D.
        dados = iris.data[:, :2]
        nomes_especies = iris.target_names

        # Embaralha os índices dos dados para que os pontos iniciais não sejam sempre os mesmos.
        indices_embaralhados = list(range(len(dados)))
        random.shuffle(indices_embaralhados)

        # Pega os dois primeiros pontos aleatórios para iniciar os clusters.
        ponto1_idx = indices_embaralhados[0]
        ponto2_idx = indices_embaralhados[1]

        # Cria os objetos Registro para esses dois pontos.
        registro1 = Registro(
            caracteristicas=dados[ponto1_idx],
            dados_categoricos={'especie': nomes_especies[iris.target[ponto1_idx]]},
            nome_ponto=f"Ponto_{len(self.todos_registros)}"
        )
        self.todos_registros.append(registro1)
        registro2 = Registro(
            caracteristicas=dados[ponto2_idx],
            dados_categoricos={'especie': nomes_especies[iris.target[ponto2_idx]]},
            nome_ponto=f"Ponto_{len(self.todos_registros)}"
        )
        self.todos_registros.append(registro2)

        # Cria os dois clusters iniciais, cada um contendo um dos pontos.
        self.clusters.append(Cluster(id=0, cor=self.cores_clusters[0], centroide_inicial=registro1))
        self.clusters.append(Cluster(id=1, cor=self.cores_clusters[1], centroide_inicial=registro2))

        # Adiciona o restante dos dados da base Iris ao sistema.
        for i in indices_embaralhados[2:]:
            novo_registro = Registro(
                caracteristicas=dados[i],
                dados_categoricos={'especie': nomes_especies[iris.target[i]]},
                nome_ponto=f"Ponto_{len(self.todos_registros)}"
            )
            self.todos_registros.append(novo_registro)
            # Atribui cada novo ponto ao cluster mais próximo.
            self.atribuir_registro_ao_cluster(novo_registro)

        # Após adicionar todos, recalcula os centroides e reorganiza os clusters para um estado mais estável.
        self.recalcular_todos_centroides()
        self.reorganizar_clusters()

    # --- ETAPA 2: ATRIBUIÇÃO DE ELEMENTOS E CÁLCULO DE DISTÂNCIA ---

    def calcular_distancia_euclidiana(self, ponto_a, ponto_b):
        """
        Calcula a distância em linha reta entre dois pontos (ponto_a e ponto_b).
        Esta é a fórmula: sqrt( (x2-x1)^2 + (y2-y1)^2 + ... )
        """
        # Pega a lista de TODAS as características numéricas (incluindo as categóricas convertidas).
        valores_a = ponto_a.obter_valores_quantitativos(self.mapa_categorico)
        valores_b = ponto_b.obter_valores_quantitativos(self.mapa_categorico)

        distancia = 0
        num_dimensoes = min(len(valores_a), len(valores_b)) # Evita erros se os pontos tiverem dimensões diferentes.
        # Soma o quadrado das diferenças para cada dimensão.
        for i in range(num_dimensoes):
            distancia += (valores_a[i] - valores_b[i]) ** 2
        # Retorna a raiz quadrada da soma.
        return math.sqrt(distancia)

    def atribuir_registro_ao_cluster(self, registro):
        """
        Esta função decide a qual cluster um ponto pertence.
        A regra é: o ponto pertence ao cluster cujo centroide está mais próximo.
        """
        if not self.clusters: # Verificação de segurança.
            messagebox.showerror("Erro", "Nenhum cluster foi inicializado.")
            return

        # Calcula a distância do 'registro' para o centroide de CADA cluster.
        distancias = [self.calcular_distancia_euclidiana(registro, c.centroide) for c in self.clusters]
        # Encontra o índice da menor distância na lista.
        cluster_mais_proximo_idx = distancias.index(min(distancias))
        # Pega o objeto Cluster correspondente a esse índice.
        cluster_alvo = self.clusters[cluster_mais_proximo_idx]

        # Se o registro já estava em um cluster, remove-o de lá antes de mover.
        if registro.cluster and registro.cluster != cluster_alvo:
            registro.cluster.remover_registro(registro)
            cluster_alvo.adicionar_registro(registro)
        elif not registro.cluster: # Se o registro é novo e não tem cluster.
            cluster_alvo.adicionar_registro(registro)

        return cluster_alvo

    # --- ETAPA 3: RECÁLCULO DO CENTROIDE E REORGANIZAÇÃO ---

    def recalcular_todos_centroides(self):
        """Simplesmente chama a função de recalcular o centroide para cada cluster existente."""
        for cluster in self.clusters:
            cluster.recalcular_centroide(self.mapa_categorico)

    def reorganizar_clusters(self):
        """
        Esta é uma parte essencial do K-means. Garante que os clusters estejam estáveis.
        Funciona em um loop:
        1. Recalcula os centroides.
        2. Reatribui TODOS os pontos para o seu centroide mais próximo.
        3. Repete até que nenhum ponto mude de cluster em uma rodada completa.
        """
        houve_mudanca = True
        max_iteracoes = 10  # Um limite de segurança para evitar loops infinitos.

        while houve_mudanca and max_iteracoes > 0:
            self.recalcular_todos_centroides() # Passo 1
            houve_mudanca = False # Assume que não haverá mudanças nesta rodada.

            # Reatribui cada ponto (Passo 2).
            for registro in self.todos_registros:
                cluster_anterior = registro.cluster
                novo_cluster = self.atribuir_registro_ao_cluster(registro)
                # Se um ponto mudou de cluster, marca que houve mudança para continuar o loop.
                if cluster_anterior and novo_cluster and cluster_anterior.id != novo_cluster.id:
                    houve_mudanca = True
            max_iteracoes -= 1

        self.recalcular_todos_centroides() # Recalcula uma última vez após a estabilização.
        self.redesenhar_canvas() # Atualiza o gráfico com o resultado final.

    def adicionar_novo_ponto(self):
        """Função chamada pelo botão 'Adicionar Ponto' na interface."""
        try:
            # Pega os valores digitados pelo usuário.
            x = float(self.entry_x.get())
            y = float(self.entry_y.get())
            cat = self.entry_cat.get() or "desconhecido"
        except ValueError:
            messagebox.showerror("Erro de Entrada", "Por favor, insira valores numéricos para as características.")
            return

        # Cria um novo objeto Registro.
        novo_registro = Registro(
            caracteristicas=[x, y],
            dados_categoricos={'especie': cat},
            nome_ponto=f"Ponto_{len(self.todos_registros)}"
        )
        self.todos_registros.append(novo_registro)

        # Atribui o novo ponto a um cluster.
        self.atribuir_registro_ao_cluster(novo_registro)

        # Reorganiza TUDO para garantir que a adição do novo ponto não desestabilizou os clusters.
        self.reorganizar_clusters()

        # Limpa as caixas de entrada para o próximo ponto.
        self.entry_x.delete(0, tk.END)
        self.entry_y.delete(0, tk.END)
        self.entry_cat.delete(0, tk.END)

    def remover_ponto_selecionado(self):
        """Função chamada pelo botão 'Remover Ponto Selecionado'."""
        if not self.ponto_selecionado:
            return

        cluster_do_ponto = self.ponto_selecionado.cluster
        if cluster_do_ponto:
            # Medida de segurança: não permite remover o último ponto de um cluster, para não o destruir.
            if len(cluster_do_ponto.registros) <= 1:
                messagebox.showwarning("Aviso", "Não é possível remover o último ponto de um cluster.")
                return

            cluster_do_ponto.remover_registro(self.ponto_selecionado)
            self.todos_registros.remove(self.ponto_selecionado)

        self.ponto_selecionado = None # Desseleciona o ponto.
        self.label_ponto_selecionado.config(text="Nenhum ponto selecionado.")
        self.btn_remover.config(state=tk.DISABLED)

        # Reorganiza os clusters, pois a remoção de um ponto muda a média do seu cluster.
        self.reorganizar_clusters()

    # --- ETAPA 4: ANÁLISE DE DISPERSÃO E CRIAÇÃO DE NOVOS CLUSTERS ---

    def analisar_e_criar_novo_cluster(self):
        """
        Implementa a lógica da Etapa 4: encontrar pontos "infelizes" e criar um novo cluster com eles.
        """
        try:
            limiar = float(self.entry_limiar.get())
            k = int(self.entry_k.get())
        except ValueError:
            messagebox.showerror("Erro de Entrada", "Limiar e K devem ser valores numéricos.")
            return

        pontos_distantes = []
        for cluster in self.clusters:
            for registro in cluster.registros:
                if registro.eh_centroide: continue # Ignora os centroides virtuais.

                dist_propria = self.calcular_distancia_euclidiana(registro, cluster.centroide)
                # Verifica se o ponto está mais longe do seu centroide do que o limiar definido.
                if dist_propria > limiar:
                    # Encontra o centroide de OUTRO cluster que esteja mais próximo.
                    dist_outros = [self.calcular_distancia_euclidiana(registro, outro.centroide) for outro in self.clusters if outro.id != cluster.id]

                    if dist_outros:
                        dist_min_outro = min(dist_outros)
                        # O critério do trabalho: um ponto é candidato se está longe do seu centro E perto de outro.
                        # Uma razão alta (dist_propria / dist_min_outro) indica um bom candidato.
                        pontos_distantes.append((dist_propria / dist_min_outro, registro))

        # Ordena os candidatos: os com a maior razão (os mais "infelizes") vêm primeiro.
        pontos_distantes.sort(key=lambda x: x[0], reverse=True)

        # Pega os 'k' melhores candidatos para formar o novo cluster.
        candidatos_para_novo_cluster = [p[1] for p in pontos_distantes[:k]]

        if not candidatos_para_novo_cluster:
            messagebox.showinfo("Análise", "Nenhum ponto atendeu aos critérios para formar um novo cluster.")
            return

        if len(self.cores_clusters) <= len(self.clusters):
            messagebox.showwarning("Aviso", "Não há mais cores disponíveis para novos clusters.")
            return

        # Prepara para criar o novo cluster.
        novo_id = len(self.clusters)
        nova_cor = self.cores_clusters[novo_id]
        centroide_novo_cluster = candidatos_para_novo_cluster[0] # O primeiro candidato será o centroide inicial.

        # Remove os pontos de seus clusters antigos.
        for ponto in candidatos_para_novo_cluster:
            if ponto.cluster:
                ponto.cluster.remover_registro(ponto)

        # Cria o novo cluster.
        novo_cluster = Cluster(id=novo_id, cor=nova_cor, centroide_inicial=centroide_novo_cluster)
        # Adiciona os outros candidatos (se houver).
        if len(candidatos_para_novo_cluster) > 1:
            for ponto in candidatos_para_novo_cluster[1:]:
                novo_cluster.adicionar_registro(ponto)

        self.clusters.append(novo_cluster)

        # Com um novo cluster na jogada, é essencial reorganizar tudo.
        self.reorganizar_clusters()
        messagebox.showinfo("Sucesso", f"Novo cluster {novo_id} criado com {len(candidatos_para_novo_cluster)} pontos.")

    # --- Funções da Interface Gráfica (GUI) ---

    def redesenhar_canvas(self):
        """Limpa e redesenha todos os pontos e centroides no canvas. Chamada a cada atualização."""
        self.canvas.delete("all") # Apaga tudo do canvas.

        if not self.todos_registros: return
        # Encontra os valores mínimos e máximos de X e Y para ajustar a escala do desenho.
        min_x = min(r.caracteristicas[0] for r in self.todos_registros) - 1
        max_x = max(r.caracteristicas[0] for r in self.todos_registros) + 1
        min_y = min(r.caracteristicas[1] for r in self.todos_registros) - 1
        max_y = max(r.caracteristicas[1] for r in self.todos_registros) + 1

        def escalar_ponto(x, y):
            """Converte as coordenadas dos dados para as coordenadas de pixels do canvas."""
            canvas_w = self.canvas.winfo_width()
            canvas_h = self.canvas.winfo_height()
            escala_x = (canvas_w - 40) / (max_x - min_x) if (max_x - min_x) != 0 else 1
            escala_y = (canvas_h - 40) / (max_y - min_y) if (max_y - min_y) != 0 else 1
            # A coordenada Y é invertida porque no canvas o (0,0) é no canto superior esquerdo.
            return 20 + (x - min_x) * escala_x, canvas_h - 20 - (y - min_y) * escala_y

        # Desenha cada ponto como uma bolinha (oval).
        for registro in self.todos_registros:
            x, y = escalar_ponto(*registro.caracteristicas)
            cor_borda = "red" if registro == self.ponto_selecionado else "black" # Borda vermelha se selecionado.
            # Cria o oval e adiciona tags para poder identificá-lo depois.
            ponto_id = self.canvas.create_oval(x-4, y-4, x+4, y+4, fill=registro.cor, outline=cor_borda, width=2, tags=registro.nome_ponto)
            self.canvas.addtag_withtag("registro", ponto_id)

        # Desenha cada centroide como um "X" grande e em negrito.
        for cluster in self.clusters:
            cx, cy = escalar_ponto(*cluster.centroide.caracteristicas)
            self.canvas.create_text(cx, cy, text="X", font=("Arial", 16, "bold"), fill=cluster.cor)

        self.atualizar_info_clusters() # Atualiza o painel de informações.

    def selecionar_ponto_no_canvas(self, event):
        """Função chamada quando o usuário clica no canvas."""
        # Encontra o item gráfico mais próximo de onde o mouse clicou.
        item_clicado_ids = self.canvas.find_closest(event.x, event.y)
        if not item_clicado_ids: return

        item_clicado = item_clicado_ids[0]
        tags = self.canvas.gettags(item_clicado) # Pega as tags do item (ex: "Ponto_10", "registro").

        # Se o item clicado tem a tag "registro", então é um ponto de dados.
        if "registro" in tags:
            nome_ponto_tag = [t for t in tags if t.startswith("Ponto_")]
            if not nome_ponto_tag: return
            nome_ponto = nome_ponto_tag[0]

            # Encontra o objeto Registro correspondente ao nome do ponto.
            ponto_encontrado = next((r for r in self.todos_registros if r.nome_ponto == nome_ponto), None)

            if ponto_encontrado:
                self.ponto_selecionado = ponto_encontrado # Armazena o ponto selecionado.
                # Mostra as informações do ponto no painel da direita.
                info = (f"Nome: {ponto_encontrado.nome_ponto}\n"
                        f"Coords: {[round(c, 2) for c in ponto_encontrado.caracteristicas]}\n"
                        f"Espécie: {ponto_encontrado.dados_categoricos.get('especie', 'N/A')}\n"
                        f"Cluster: {ponto_encontrado.cluster.id if ponto_encontrado.cluster else 'Nenhum'}")
                self.label_ponto_selecionado.config(text=info)
                self.btn_remover.config(state=tk.NORMAL) # Ativa o botão de remover.
                self.redesenhar_canvas() # Redesenha para mostrar a borda vermelha.

    def atualizar_info_clusters(self):
        """Atualiza a caixa de texto com as informações atuais de cada cluster."""
        self.info_text.config(state=tk.NORMAL) # Habilita a edição do texto.
        self.info_text.delete(1.0, tk.END) # Apaga o texto antigo.
        for cluster in self.clusters:
            # Monta a string com as informações do cluster.
            info = (f"Cluster {cluster.id} (Cor: {cluster.cor})\n"
                    f"  - Pontos: {len(cluster.registros)}\n"
                    f"  - Centroide: {[round(c, 2) for c in cluster.centroide.caracteristicas]}\n\n")
            self.info_text.insert(tk.END, info) # Insere o novo texto.
        self.info_text.config(state=tk.DISABLED) # Desabilita a edição para o usuário.

# --- PONTO DE ENTRADA DO PROGRAMA ---
if __name__ == "__main__":
    # Esta parte só é executada quando o script é rodado diretamente.

    # Cria a janela principal da interface.
    root = tk.Tk()
    # Cria uma instância da nossa classe de aplicação.
    app = KMeansApp(root)

    # Função para o gráfico se adaptar quando o tamanho da janela muda.
    def on_resize(event):
        app.redesenhar_canvas()

    # Um pequeno delay de 100ms para garantir que a janela foi criada antes do primeiro desenho.
    root.after(100, app.redesenhar_canvas)
    # Associa o evento de redimensionar a janela à função on_resize.
    root.bind("<Configure>", on_resize)

    # Inicia o loop principal da aplicação, que a mantém aberta e responsiva.
    root.mainloop()