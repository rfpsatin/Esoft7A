import math
import uuid
from typing import List, Dict, Any, Tuple, Optional

class Logger:
    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    def log(self, message: str, level: str = "INFO"):
        if self.enabled:
            print(f"[{level}] {message}")

# Global logger instance
logger = Logger()

class Element:
    def __init__(self, features: List[float], element_id: Optional[str] = None):
        if not isinstance(features, list) or not all(isinstance(x, (int, float)) for x in features):
            raise ValueError("As Caract devem ser uma lista de numeros.")
        if not features:
            raise ValueError("A lista de Caract nao pode estar vazia.")

        self.id: str = element_id if element_id else str(uuid.uuid4())
        self.features: List[float] = features
        self.is_centroid: bool = False

    def __repr__(self) -> str:
        return f"Element(id={self.id}, features={self.features}, is_centroid={self.is_centroid})"

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "features": list(self.features), "is_centroid": self.is_centroid}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Element':
        el = cls(features=data["features"], element_id=data["id"])
        el.is_centroid = data["is_centroid"]
        return el

class Cluster:
    def __init__(self, cluster_id: str, initial_element_features: List[float]):
        if not initial_element_features:
            raise ValueError("As Caract do elemento inicial nao podem estar vazias para a criacao do cluster.")
        self.id: str = cluster_id
        self.elements: List[Element] = []
        self.virtual_centroid_features: List[float] = list(initial_element_features)

        # Adiciona o elemento inicial que forma o cluster
        initial_element = Element(features=initial_element_features)
        self._add_element_internal(initial_element)
        self._update_centroids()

    def _add_element_internal(self, element: Element):
        if not isinstance(element, Element):
            raise ValueError("Apenas objetos Element podem ser adicionados a um cluster.")
        self.elements.append(element)

    def _recalculate_virtual_centroid(self):
        # Recalcula o centroide virtual do cluster
        if not self.elements:
            self.virtual_centroid_features = [] # Indef se vazio
            return

        num_elements = len(self.elements)
        num_features = len(self.elements[0].features)

        sum_features = [0.0] * num_features
        for element in self.elements:
            if len(element.features) != num_features:
                raise ValueError("Todos os elementos em um cluster devem ter a mesma dimen de Caract.")
            for i in range(num_features):
                sum_features[i] += element.features[i]

        self.virtual_centroid_features = [s / num_elements for s in sum_features]

    def _designate_element_as_centroid(self):
        for el in self.elements:
            el.is_centroid = False

        if not self.elements or not self.virtual_centroid_features:
            return

        closest_element: Optional[Element] = None
        min_dist_sq = float('inf')

        for element in self.elements:
            # Usando a distancia euclidiana quadrada para eficiencia na comparacao
            dist_sq = sum((f1 - f2)**2 for f1, f2 in zip(element.features, self.virtual_centroid_features))
            if dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
                closest_element = element

        if closest_element:
            closest_element.is_centroid = True

    def _update_centroids(self):
        # Auxiliar para consolidar os passos de atualizacao do centroide
        self._recalculate_virtual_centroid()
        self._designate_element_as_centroid()

    def add_element(self, element_features: List[float]) -> Element:
        if not self.elements:
            if not self.virtual_centroid_features:
                self.virtual_centroid_features = list(element_features)

        # Garante que o novo elem tenha a mesma dimen do centroide virtual
        if self.virtual_centroid_features and len(element_features) != len(self.virtual_centroid_features):
            raise ValueError(f"A dimensao das Caract do novo elemento {len(element_features)} nao corresponde a dimensao do centroide do cluster {len(self.virtual_centroid_features)}.")

        new_element = Element(features=element_features)
        new_element.is_centroid = False
        self._add_element_internal(new_element)
        self._update_centroids()
        return new_element

    def remove_element(self, element_id: str) -> bool:
        # Remove um elemento do cluster pelo seu ID
        element_to_remove = next((el for el in self.elements if el.id == element_id), None)

        if element_to_remove:
            self.elements.remove(element_to_remove)
            self._update_centroids() # Recalcular mesmo que o cluster fique vazio
            return True
        return False # Elemento nao encontrado

    def update_element_features(self, element_id: str, new_features: List[float]) -> bool:
        # Atualiza as caract de um elem existente no cluster
        if not isinstance(new_features, list) or not all(isinstance(x, (int, float)) for x in new_features):
            raise ValueError("As novas Caract devem ser uma lista de numeros.")

        found_element = next((el for el in self.elements if el.id == element_id), None)

        if found_element:
            if len(found_element.features) != len(new_features):
                raise ValueError("As novas Caract devem ter a mesma dimen das Caract antigas.")
            found_element.features = new_features
            self._update_centroids()
            return True
        return False # Elemento nao encontrado

    def get_elements_data(self) -> List[Dict[str, Any]]:
        # Retorna uma lista de dicionarios representando os elem no cluster
        return [el.to_dict() for el in self.elements]

    def get_virtual_centroid_features(self) -> List[float]:
        # Retorna uma copia das caracteristicas do centroide virtual do cluster
        return list(self.virtual_centroid_features) if self.virtual_centroid_features else []

    @staticmethod
    def euclidean_distance(features1: List[float], features2: List[float]) -> float:
        # Calcula a distancia Euclidiana entre dois vetores de caract
        if not features1 or not features2: # Lida com casos onde um centroide pode estar temp indef
            return float('inf')
        if len(features1) != len(features2):
            raise ValueError("As Caract devem ter a mesma dimen para o calculo da distancia.")
        return math.sqrt(sum((f1 - f2)**2 for f1, f2 in zip(features1, features2)))

    def __repr__(self) -> str:
        designated_centroid_id = next((el.id for el in self.elements if el.is_centroid), "Nenhum")
        return (f"Cluster(id={self.id}, num_elements={len(self.elements)}, "
                f"virtual_centroid_approx={self.virtual_centroid_features}, "
                f"designated_centroid_element_id={designated_centroid_id})")


class ClusterManager:
    # Geren uma colecao de clusters
    def __init__(self):
        self.clusters: Dict[str, Cluster] = {} # id_cluster -> Obj Cluster
        self.all_elements_map: Dict[str, Dict[str, Any]] = {} # id_elemento -> {'element_obj': Element, 'cluster_id': str}
        self._next_cluster_id_counter: int = 0

    def _generate_cluster_id(self) -> str:
        self._next_cluster_id_counter += 1
        return f"cluster_{self._next_cluster_id_counter}"

    def create_initial_clusters(self, initial_element_features_list: List[List[float]]):

        # Cria clusters iniciais

        if self.clusters: # Previne reinic se ja estiver populado
            raise Exception("Clusters iniciais ja foram criados ou o gerenciador nao esta vazio.")
        if not initial_element_features_list:
            raise ValueError("E necessario fornecer Caract para pelo menos um elemento inicial.")

        # Verificacao basica de dimen
        if len(initial_element_features_list) > 1:
            first_dim = len(initial_element_features_list[0])
            if not all(len(f) == first_dim for f in initial_element_features_list):
                raise ValueError("Todas as Caract dos elementos iniciais devem ter a mesma dimen.")


        for features in initial_element_features_list:
            cluster_id = self._generate_cluster_id()
            cluster = Cluster(cluster_id=cluster_id, initial_element_features=features)
            self.clusters[cluster_id] = cluster

            # O elemento inicial é criado dentro do construtor do cluster
            initial_element = cluster.elements[0]
            self.all_elements_map[initial_element.id] = {'element_obj': initial_element, 'cluster_id': cluster_id}

        logger.log(f"Inicializados {len(self.clusters)} clusters.")

    def add_new_record_to_system(self, new_element_features: List[float]) -> Tuple[str, str]:
        if not self.clusters:
            raise Exception("Nenhum cluster existe. Crie clusters iniciais primeiro usando 'create_initial_clusters'.")

        any_cluster_id = next(iter(self.clusters))
        expected_dim = len(self.clusters[any_cluster_id].get_virtual_centroid_features())
        if len(new_element_features) != expected_dim:
            raise ValueError(f"A dimensao das Caract do novo elemento {len(new_element_features)} nao corresponde a dimensao esperada pelo sistema {expected_dim}.")


        closest_cluster_id: Optional[str] = None
        min_distance = float('inf')

        for cid, cluster_obj in self.clusters.items():
            # Distancia ao centroide VIRTUAL do cluster
            distance = Cluster.euclidean_distance(new_element_features, cluster_obj.get_virtual_centroid_features())
            if distance < min_distance:
                min_distance = distance
                closest_cluster_id = cid

        if closest_cluster_id:
            target_cluster = self.clusters[closest_cluster_id]
            new_element_obj = target_cluster.add_element(new_element_features) # Adiciona e atualiza centroides dentro do cluster
            self.all_elements_map[new_element_obj.id] = {'element_obj': new_element_obj, 'cluster_id': target_cluster.id}
            logger.log(f"Elemento {new_element_obj.id} adicionado ao cluster {target_cluster.id}.")
            return new_element_obj.id, target_cluster.id
        else:
            raise Exception("Nao foi possivel encontrar o cluster mais proximo. Certifique-se de que os clusters estao inicializados corretamente e as Caract sao validas.")

    def remove_record(self, element_id: str) -> bool:
        if element_id not in self.all_elements_map:
            logger.log(f"Elemento com ID {element_id} nao encontrado no sistema.")
            return False

        record_info = self.all_elements_map[element_id]
        cluster_id = record_info['cluster_id']
        cluster = self.clusters.get(cluster_id)

        if cluster:
            if cluster.remove_element(element_id):
                del self.all_elements_map[element_id]
                logger.log(f"Elemento {element_id} removido do cluster {cluster_id}.")
                if not cluster.elements:
                    pass
                return True
        logger.log(f"Falha ao remover o elemento {element_id} do cluster {cluster_id} (elemento nao esta no cluster ou cluster nao encontrado).")
        return False

    def alter_record_features(self, element_id: str, new_features: List[float]) -> bool:
        if element_id not in self.all_elements_map:
            logger.log(f"Elemento com ID {element_id} nao encontrado para alteracao.")
            return False

        record_info = self.all_elements_map[element_id]
        cluster_id = record_info['cluster_id']
        cluster = self.clusters.get(cluster_id)

        if cluster:
            # Verificacao de dimen para novas Caract
            expected_dim = len(cluster.get_virtual_centroid_features())
            if expected_dim > 0 and len(new_features) != expected_dim : # expected_dim pode ser 0 se o cluster ficou vazio
                 raise ValueError(f"A dimensao das novas Caract {len(new_features)} nao corresponde a dimensao esperada pelo cluster {expected_dim}.")

            if cluster.update_element_features(element_id, new_features):
                logger.log(f"Caract do elemento {element_id} no cluster {cluster_id} atualizadas.")
                return True
        logger.log(f"Falha ao atualizar Caract para o elemento {element_id}.")
        return False

    def get_cluster_details(self, cluster_id: str) -> Optional[Dict[str, Any]]:
        cluster = self.clusters.get(cluster_id)
        if cluster:
            return {
                "id": cluster.id,
                "virtual_centroid_features": cluster.get_virtual_centroid_features(),
                "elements": cluster.get_elements_data(),
                "designated_centroid_id": next((el.id for el in cluster.elements if el.is_centroid), None)
            }
        return None

    def get_all_cluster_details(self) -> Dict[str, Optional[Dict[str, Any]]]:
        return {cid: self.get_cluster_details(cid) for cid in self.clusters}

    def get_element_details(self, element_id: str) -> Optional[Dict[str, Any]]:
        if element_id in self.all_elements_map:
            record_info = self.all_elements_map[element_id]
            element_obj: Element = record_info['element_obj']
            return {
                "element_data": element_obj.to_dict(),
                "cluster_id": record_info['cluster_id']
            }
        return None

#TODO --- Prep KNN (TERMINAR) ---

def normalize_features_for_knn(elements_map: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    logger.log("[KNN Em Progresso] normalize_features_for_knn: Normalizacao de Caract a implementar.")
    return elements_map

def find_k_nearest_neighbors(
    all_elements_map: Dict[str, Dict[str, Any]],
    target_features: List[float],
    k: int
) -> List[Tuple[str, float, Dict[str, Any]]]:
    logger.log(f"[KNN Em Progresso] find_k_nearest_neighbors: Procuraria por {k} vizinhos para as Caract {target_features}.")
    if not all_elements_map:
        logger.log("[KNN Em Progresso] find_k_nearest_neighbors: Nenhum elemento no mapa para pesquisar.")
        return []

    distances: List[Tuple[str, float, Element]] = [] # (id_elemento, distancia, objeto_elemento)

    # Verificacao basica de dimen
    any_el_data = next(iter(all_elements_map.values()))
    expected_dim = len(any_el_data['element_obj'].features)
    if len(target_features) != expected_dim:
        logger.log(f"[KNN Em Progresso] find_k_nearest_neighbors: Incompatibilidade na dimensao das Caract alvo. Esperado {expected_dim}, obtido {len(target_features)}.")
        return []

    for el_id, data_dict in all_elements_map.items():
        element_obj: Element = data_dict['element_obj']
        try:
            dist = Cluster.euclidean_distance(target_features, element_obj.features)
            distances.append((el_id, dist, element_obj))
        except ValueError as e:
            logger.log(f"[KNN Em Progresso] Erro ao calcular distancia para o elemento {el_id}: {e}")
            continue

    distances.sort(key=lambda x: x[1])

    # Preparar resultado para corresponder a saida esperada, talvez id_elemento, distancia e id_cluster do vizinho
    results: List[Tuple[str, float, Dict[str, Any]]] = []
    for el_id, dist, el_obj in distances[:k]:
        neighbor_info = {
            'element_id': el_id,
            'features': el_obj.features,
            'cluster_id': all_elements_map[el_id]['cluster_id']
        }
        results.append((el_id, dist, neighbor_info))

    logger.log(f"[KNN Em Progresso] find_k_nearest_neighbors: Encontrados {len(results)} vizinhos potenciais.")
    return results

def predict_class_with_knn(k_nearest_neighbors_info: List[Tuple[str, float, Dict[str, Any]]]) -> Optional[str]:

    logger.log(f"[KNN Em Progresso] predict_class_with_knn: Faria a predicao com base em {len(k_nearest_neighbors_info)} vizinhos.")
    if not k_nearest_neighbors_info:
        return None

    from collections import Counter
    neighbor_cluster_ids = [info_tuple[2]['cluster_id'] for info_tuple in k_nearest_neighbors_info if info_tuple[2]]
    if not neighbor_cluster_ids:
        logger.log("[KNN Em Progresso] predict_class_with_knn: Nenhum ID de cluster encontrado entre os vizinhos.")
        return None

    majority_vote = Counter(neighbor_cluster_ids).most_common(1)
    prediction = majority_vote[0][0] if majority_vote else None
    logger.log(f"[KNN Em Progresso] predict_class_with_knn: A predicao e '{prediction}'.")
    return prediction


if __name__ == "__main__":
    logger.log("--- Script de Clusterizacao K-means e Preparacao KNN ---")

    manager = ClusterManager()

    logger.log("--- Parte 1: Estrutura e Manipulacao K-means ---")
    try:
        # pontos iniciais: [preco_fechamento, volume_diario, dia_do_ano]
        initial_points = [
            [45000.0, 2000000000.0, 15.0],  # Ex: Dia 15, Preço $45k, Volume $2Bi
            [48000.0, 2500000000.0, 30.0]   # Ex: Dia 30, Preço $48k, Volume $2.5Bi
        ]
        manager.create_initial_clusters(initial_points)
        logger.log("Estado Inicial do Cluster:")
        for cid in manager.clusters:
            logger.log(str(manager.get_cluster_details(cid)))

        element_to_remove_id = None
        if manager.clusters:
            first_cluster_id = next(iter(manager.clusters))
            first_cluster_details = manager.get_cluster_details(first_cluster_id)
            if first_cluster_details and first_cluster_details['elements']:
                element_to_remove_id = first_cluster_details['elements'][0]['id']

        if element_to_remove_id:
            logger.log(f"Tentando remover elemento: {element_to_remove_id}")
            manager.remove_record(element_to_remove_id)
            logger.log(f"Estado do cluster apos remover {element_to_remove_id}:")
            if first_cluster_id: # Checa se o cluster ainda existe
                 logger.log(str(manager.get_cluster_details(first_cluster_id)))
            else:
                 logger.log(f"Cluster {first_cluster_id} nao encontrado, possivelmente removido.")

        else:
            logger.log("Nao foi possivel encontrar um elemento para testar a remocao.")

        element_to_alter_id = None
        target_cluster_id_for_alter = None
        # Encontra outro elemento para alterar
        all_details = manager.get_all_cluster_details()
        for cid_loop, c_details_loop in all_details.items():
            if c_details_loop and c_details_loop['elements']:
                element_to_alter_id = c_details_loop['elements'][0]['id']
                target_cluster_id_for_alter = cid_loop
                break

        if element_to_alter_id and target_cluster_id_for_alter:
            # ovas features: [novo_preco, novo_volume, novo_dia_do_ano]
            new_features_for_alter = [46500.0, 2200000000.0, 20.0]
            logger.log(f"Tentando alterar elemento: {element_to_alter_id} com Caract {new_features_for_alter}")
            manager.alter_record_features(element_to_alter_id, new_features_for_alter)
            logger.log(f"Estado do cluster apos alterar {element_to_alter_id}:")
            logger.log(str(manager.get_cluster_details(target_cluster_id_for_alter)))
        else:
            logger.log("Nao foi possivel encontrar um elemento para testar a alteracao.")


    except Exception as e:
        logger.log(f"Erro durante a demonstracao K-means (Parte 1): {e}", level="ERROR")


    logger.log("--- Parte 2: Atribuicao de Elementos e Calculo de Distancia ---")
    manager_p2 = ClusterManager()
    try:
        # pontos iniciais para Parte 2: [preco_fechamento, volume_diario, dia_do_ano]
        initial_points_p2 = [
            [50000.0, 3000000000.0, 45.0],
            [55000.0, 4000000000.0, 60.0]
        ]
        manager_p2.create_initial_clusters(initial_points_p2)
        logger.log("Estado inicial para a demonstracao da Parte 2:")
        for cid in manager_p2.clusters:
            logger.log(str(manager_p2.get_cluster_details(cid)))

        new_element_data_1 = [51000.0, 3200000000.0, 48.0]
        new_element_data_2 = [54000.0, 3800000000.0, 58.0]
        new_element_data_3 = [52500.0, 3500000000.0, 52.0]

        logger.log(f"Adicionando novo elemento com features {new_element_data_1}:")
        el1_id, c1_id = manager_p2.add_new_record_to_system(new_element_data_1)
        logger.log(f"Elemento {el1_id} adicionado ao cluster {c1_id}. Detalhes do cluster atualizados:")
        logger.log(str(manager_p2.get_cluster_details(c1_id)))

        logger.log(f"Adicionando novo elemento com features {new_element_data_2}:")
        el2_id, c2_id = manager_p2.add_new_record_to_system(new_element_data_2)
        logger.log(f"Elemento {el2_id} adicionado ao cluster {c2_id}. Detalhes do cluster atualizados:")
        logger.log(str(manager_p2.get_cluster_details(c2_id)))

        logger.log(f"Adicionando novo elemento com features {new_element_data_3}:")
        el3_id, c3_id = manager_p2.add_new_record_to_system(new_element_data_3)
        logger.log(f"Elemento {el3_id} adicionado ao cluster {c3_id}. Detalhes do cluster atualizados:")
        logger.log(str(manager_p2.get_cluster_details(c3_id)))

        logger.log("Estado final de todos os clusters (Parte 2):")
        logger.log(str(manager_p2.get_all_cluster_details()))

    except Exception as e:
        logger.log(f"Erro durante a demonstracao da Parte 2: {e}", level="ERROR")

    logger.log("--- Preparacao KNN ---")
    current_elements_for_knn = manager_p2.all_elements_map # Usando os elementos do manager_p2

    if current_elements_for_knn:
        normalized_elements = normalize_features_for_knn(current_elements_for_knn)

        # 2. Def um ponto alvo para KNN
        # [preco, volume, dia_do_ano]
        target_knn_point = [52000.0, 3300000000.0, 50.0]
        if not initial_points_p2: # Fallback caso initial_points_p2 esteja vazio por algum motivo
             if current_elements_for_knn:
                 any_element_id = next(iter(current_elements_for_knn))
                 any_element_features = current_elements_for_knn[any_element_id]['element_obj'].features
                 if any_element_features:
                    target_knn_point = any_element_features # Usa features de um elemento existente como fallback
                 else: # Fallback ainda mais generico se o elemento nao tiver features
                    target_knn_point = [0.0, 0.0, 0.0]


        # 3. Encontrar K vizinhos mais prox
        k_val = 2
        neighbors = find_k_nearest_neighbors(normalized_elements, target_knn_point, k_val)
        logger.log(f"[KNN Demo] Vizinhos encontrados para {target_knn_point} (k={k_val}): {neighbors}")

        # 4. Predizer classe com KNN
        knn_prediction = predict_class_with_knn(neighbors)
        logger.log(f"[KNN Demo] Predicao KNN para {target_knn_point}: {knn_prediction}")
    else:
        logger.log("[KNN Demo] Nenhum elemento disponivel para KNN.")

    logger.log("--- Script finalizado ---")