import math

from node import Node

class Tree(object):
    def __init__(self, attributes_type, attributes, target_class, instances):
        self.attributes_type = attributes_type
        self.attributes = attributes
        self.target_class = target_class
        self.instances = instances
        self.decision_tree = None

    def createDecisionTree(self):
        self.attributes.remove(self.target_class)

        if self.attributes_type == 'cat':
            self.decision_tree = self.decisionTreeCat(self.instances, self.attributes, self.target_class)
        elif self.attributes_type == 'num':
            self.decision_tree = self.decisionTreeNum(self.instances, self.attributes, self.target_class)
        else:
            print('Erro - Informe o tipo dos atributos.')
            exit(1)


    def getBestAttribute(self, attributes, instances):
        """
        Retorna o atributo com o maior ganho de informação, seguindo o algoritmo ID3.
        """

        original_set_entropy = self.entropy(instances, self.target_class)
        attributes_information_gain = [0 for i in range(len(attributes))]

        for i in range(len(attributes)):
            # Pega todos os valores possíveis para o atributo em questão
            possible_values = self.getDistinctValuesForAttribute(attributes[i], instances)
            avg_entropy = 0

            # Calcula entropia ponderada para cada subset originado a partir do atributo
            for value in possible_values:
                subset = self.getSubsetWithAttributeValue(attributes[i], value, instances)
                entropy = self.entropy(subset, self.target_class)
                weighted_entropy = float(entropy * (len(subset)/len(instances)))
                avg_entropy = avg_entropy + weighted_entropy

            info_gain = original_set_entropy - avg_entropy
            attributes_information_gain[i] = info_gain

        best_attribute_index = attributes_information_gain.index(max(attributes_information_gain))

        return attributes[best_attribute_index]

    def entropy(self, instances, target_class):
        # Medida do grau de aleatoriedade de uma variável, dada em bits
        # Está associada à dificuldade de predizer o atributo alvo a partir
        # do atributo preditivo analisadoself.
        possible_values = self.getDistinctValuesForAttribute(target_class, instances)
        possible_values_count = [0 for i in range(len(possible_values))]

        for i in range(len(possible_values)):
            for j in range(len(instances)):
                if instances[j][target_class] == possible_values[i]:
                    possible_values_count[i] = possible_values_count[i] + 1

        entropy = 0
        for v in possible_values_count:
            percentage_of_values = float(v/len(instances))
            partial_result = float(-1 * percentage_of_values * math.log2(percentage_of_values))
            entropy = float(entropy + partial_result)

        return entropy


    def getMostFrequentClass(self, instances, target_class):
        """
        Retorna a classificação mais frequente para target_class entre as
        instances
        """
        class_values = {}

        for instance in instances:
            value = instance[target_class]

            if value in class_values:
                class_values[value] = class_values[value] + 1
            else:
                class_values[value] = 1

        return self.getItemWithMaxValue(class_values)


    def getItemWithMaxValue(self, items):
        """
        Retorna a chave do dicionário que possui o maior valor associado.
        Exemplo: {'a': 1, 'b': 2, 'c': 3} -> Retorna 'c'
        """
        return max(items, key=items.get)


    def haveSameClass(self, instances, class_to_check):
        """
        Retorna True se todos os elementos de instance têm a mesma classificação para
        class_to_check. False, caso contrário
        """
        class_value = instances[0][class_to_check]

        for instance in instances:
            if not instance[class_to_check] == class_value:
                return False

        return True


    def getDistinctValuesForAttribute(self, attribute, instances):
        """
        Retorna todos os valores distintos para um determinado atributo que estão
        presentes em instances
        """
        distinct_values = []
        for instance in instances:
            if instance[attribute] not in distinct_values:
                distinct_values.append(instance[attribute])

        return distinct_values

    def getSubsetWithAttributeValue(self, attribute, value, instances):
        """
        Retorna subconjunto com todas as intâncias que possuem o mesmo valor 'value'
        para o atributo 'attribute'
        """
        subset = []

        for instance in instances:
            if instance[attribute] == value:
                subset.append(instance)

        return subset

    def decisionTreeCat(self, instances, attributes, target_class, up_edge=None):
        """
        Função recursiva que cria uma árvore de decisão com base no conjunto
        'instances' para atributos CATEGÓRICOS
        """
        node = Node()
        node.up_edge = up_edge

        if self.haveSameClass(instances, target_class):
            # Se todos os exemplos do conjunto possuem a mesma classificação,
            # retorna node como um nó folha rotulado com a classe

            # Pega a classe da primeira instância. Tanto faz, pois todos têm a mesma classe.
            node.value = instances[0][target_class]
            return node

        if len(attributes) == 0:
            # Se L é vazia, retorna node como um nó folha com a classe mais
            # frequente no conjunto de instancias
            value = self.getMostFrequentClass(instances, target_class)
            node.value = value
            return node
        else:
            # Seleciona atributo preditivo da lista de atributos que apresenta melhor critério de divisão
            attribute = self.getBestAttribute(attributes, instances)
            node.value = attribute

            attributes.remove(attribute)

            # Para cada valor V distinto do atributo em questão, considerando os exemplos da lista de instancias:
            distinct_attribute_values = self.getDistinctValuesForAttribute(attribute, instances)

            for attribute_value in distinct_attribute_values:
                subset = self.getSubsetWithAttributeValue(attribute, attribute_value, instances)

                if len(subset) == 0:
                    # Se esse subset for vazio, retorna node como nó folha rotulado
                    # com a classe mais frequente no conjunto
                    value = self.getMostFrequentClass(instances, target_class)
                    node.value = value
                    return node
                else:
                    node.children.append(self.decisionTreeCat(subset, attributes, target_class, attribute_value))

        return node


    def decisionTreeNum(self, instances, attributes, target_class, up_edge=None):
        """
        Função recursiva que cria uma árvore de decisão com base no conjunto
        'instances' para atributos NUMÉRICOS
        """
        node = Node()
        node.up_edge = up_edge

        if self.haveSameClass(instances, target_class):
            # Se todos os exemplos do conjunto possuem a mesma classificação,
            # retorna node como um nó folha rotulado com a classe

            # Pega a classe da primeira instância. Tanto faz, pois todos têm a mesma classe.
            node.value = instances[0][target_class]
            return node

        if len(attributes) == 0:
            # Se L é vazia, retorna node como um nó folha com a classe mais
            # frequente no conjunto de instancias
            value = self.getMostFrequentClass(instances, target_class)
            node.value = value
            return node
        else:
            # Seleciona atributo preditivo da lista de atributos que apresenta melhor critério de divisão
            attribute = self.getBestAttribute(attributes, instances)
            node.value = attribute

            attributes.remove(attribute)

            # Para cada valor V distinto do atributo em questão, considerando os exemplos da lista de instancias:
            distinct_attribute_values = self.getDistinctValuesForAttribute(attribute, instances)

            # Define-se um ponto de corte, gerando dois subconjuntos disjuntos de acordo com testes
            # A <= threshold e A > threshold.
            # Para obter um ponto de corte, ordena a lista de valores possíveis do atributo e
            # toma o ponto médio entre 2 exemplos consecutivos (a_i + a_(i+1))/2 como um possível
            # ponto de corte a ser avaliado pelo critério de seleção. Apenas valores que dividem
            # exemplos de classes diferentes precisam de fato ser avaliados.
            distinct_attribute_values.sort()

            possible_threshold = -1
            for i in xrange(0, len(distinct_attribute_values)-1, 2):
                possible_threshold = distinct_attribute_values[i] + distinct_attribute_values[i+1]






    def printDecisionTree(self):
        self.printTree(self.decision_tree)


    def printTree(self, tree, level=0):
        if tree.up_edge:
            print('    ' * (level - 1) + '+---' * (level > 0) + '[' + tree.up_edge + ']' + tree.value)
        else:
            print('    ' * (level - 1) + '+---' * (level > 0) + tree.value)


        for i in range(len(tree.children)):
            if type(tree.children[i]) is Node:
                self.printTree(tree.children[i], level + 1)
            else:
                print('    ' * level + '+---' + tree.children[i].value)


    def traverse(self, tree):
        if tree.children:
            for i in range(len(tree.children)):
                return self.traverse(tree.children[i])
        else:
            return tree.value
