import collections
import heapq
import math

# Функция для вычисления энтропии, приходящейся на одну букву
def calculate_entropy(text):
    letter_count = collections.Counter(text)
    total_letters = len(text)
    entropy = 0

    for letter, count in letter_count.items():
        probability = count / total_letters
        entropy -= probability * math.log2(probability)

    return entropy

# Функция для равномерного кодирования
def uniform_encoding(text):
    alphabet_size = len(set(text))                    #set(text) - уникальные символы в тексте
    code_length = math.ceil(math.log2(alphabet_size)) #math.log2(alphabet_size) для вычисления минимальной длины кода в битах
    return code_length                                #math.ceil - функция округления , кол-во бит должно быть целым число

# Класс для узла дерева Шеннона-Фано
class Node:
    def __init__(self, symbol, probability): # конструктор
        self.symbol = symbol                 # символ
        self.probability = probability       # вероятность появления символа в тексте
        self.left = None                     # Левое поддерево
        self.right = None                    # Правое поддерево

    def __lt__(self, other):                 # метод для сравнения узлов по их вероятности
        return self.probability < other.probability

# Функция для построения схемы алфавитного кодирования методом Шеннона-Фано
def build_shannon_fano_tree(text):
    letter_count = collections.Counter(text)        # Подсчитываем частоту каждого символа в тексте
    probability_dict = {symbol: count / len(text) for symbol, count in letter_count.items()} # Вычисляем вероятность каждого символа

    # Создаем список узлов и инициализируем его вероятностями
    nodes = [Node(symbol, probability) for symbol, probability in probability_dict.items()]

    # Строим дерево Шеннона-Фано
    while len(nodes) > 1:
        nodes.sort()          # Сортируем узлы по вероятностям (в порядке возрастания)
        left = nodes.pop(0)   # Извлекаем узел с самой низкой вероятностью из начала списка
        right = nodes.pop(0)  # Извлекаем следующий узел с самой низкой вероятностью
        merged = Node(None, left.probability + right.probability) # Создаем новый узел, объединяя left и right
        merged.left = left
        merged.right = right
        nodes.append(merged) # Добавляем объединенный узел обратно в список

    return nodes[0] # Возвращаем корневой узел

# Функция для получения кодов из дерева Шеннона-Фано
def get_shannon_fano_codes(node, current_code="", code_dict={}):
    if node.symbol is not None:
        code_dict[node.symbol] = current_code  # Если узел - листовой, сохраняем код символа в словарь
    if node.left is not None:
        get_shannon_fano_codes(node.left, current_code + "0", code_dict) # Рекурсивно обходим левое поддерево с добавлением "0" к текущему коду
    if node.right is not None:
        get_shannon_fano_codes(node.right, current_code + "1", code_dict) # Рекурсивно обходим правое поддерево с добавлением "1" к текущему коду
 # 1 и 0 для правильного построения кодов для символов в дереве
# Функция для кодирования текста с использованием схемы кодирования
def encode_text(text, code_dict):
    encoded_text = ""
    for symbol in text:
        encoded_text += code_dict[symbol] # Добавляем код символа в закодированный текст
    return encoded_text

# Функция для декодирования текста с использованием схемы кодирования
def decode_text(encoded_text, code_dict):
    decoded_text = "" # Инициализируем пустой текущий код
    current_code = ""
    for bit in encoded_text:
        current_code += bit # Добавляем следующий бит к текущему коду
        for symbol, code in code_dict.items():
            if current_code == code: # Если текущий код соответствует коду символа
                decoded_text += symbol # Добавляем символ в декодированный текст
                current_code = "" # Сбрасываем текущий код
                break
    return decoded_text

if __name__ == "__main__":
    input_text = input("Введите текст для обработки: ")

    print("Ваши данные:")

    # Вычисляем энтропию
    entropy = calculate_entropy(input_text)
    print(f"Энтропия: {entropy} (бит/символ)")
    print("================")

    # Равномерное кодирование
    uniform_code_length = uniform_encoding(input_text)
    print(f"Длина кода при равномерном кодировании: {uniform_code_length} (бит/символ)")
    print("================")

    # Строим схему Шеннона-Фано и получаем коды
    shannon_fano_tree = build_shannon_fano_tree(input_text)
    code_dict = {}
    get_shannon_fano_codes(shannon_fano_tree, code_dict=code_dict) # получаем коды для символов из дерева Шеннона-Фано

    # Кодирование текста
    encoded_text = encode_text(input_text, code_dict)
    print(f"Закодированный текст: {encoded_text}")
    print("================")

    # Декодирование текста
    decoded_text = decode_text(encoded_text, code_dict)
    print(f"Декодированный текст: {decoded_text}")
    print("================")

    # Эффективность сжатия
    original_length = len(input_text) * 8  # Переводим в биты
    encoded_length = len(encoded_text)
    compression_ratio = original_length / encoded_length
    print(f"Эффективность сжатия: {compression_ratio:.2f}")
    print("================")

    # Строим схему Шеннона-Фано для двухбуквенных сочетаний
    bigram_count = collections.Counter([input_text[i:i + 2] for i in range(len(input_text) - 1)])
    bigram_probability_dict = {bigram: count / (len(input_text) - 1) for bigram, count in bigram_count.items()}
    bigram_nodes = [Node(bigram, probability) for bigram, probability in bigram_probability_dict.items()]
    bigram_tree = build_shannon_fano_tree(input_text)
    bigram_code_dict = {}
    get_shannon_fano_codes(bigram_tree, code_dict=bigram_code_dict)

    # Вычисляем среднюю длину элементарного кода для двухбуквенных сочетаний
    average_bigram_code_length = sum(len(bigram_code_dict[bigram]) * bigram_count[bigram]
                                     for bigram in bigram_code_dict) / (len(input_text) - 1)
    print(f"Средняя длина элементарного кода для двухбуквенных сочетаний: {average_bigram_code_length:.2f} бит")
    print("================")

    # Эффективность сжатия для двухбуквенных сочетаний
    bigram_encoded_text = encode_text(input_text, bigram_code_dict)
    bigram_original_length = (len(input_text) - 1) * 8  # Переводим в биты
    bigram_encoded_length = len(bigram_encoded_text)
    bigram_compression_ratio = bigram_original_length / bigram_encoded_length
    print(f"Эффективность сжатия для двухбуквенных сочетаний: {bigram_compression_ratio:.2f}")
