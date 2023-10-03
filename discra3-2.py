import heapq
from collections import defaultdict, Counter
import math

# двубуквеные сочетания
class Node:
    def __init__(self, chars, freq):
        self.chars = chars # Символы (или None для внутренних узлов)
        self.freq = freq # Частота символов (сочетаний)
        self.left = None # Левый потомок узла
        self.right = None # Правый потомок узла
    #  метод __lt__, используется для сравнения узлов при построении кучи
    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(freq_dict):
    heap = [Node(chars, freq) for chars, freq in freq_dict.items()]  # Создаем список узлов из словаря частот
    heapq.heapify(heap)  # Преобразуем список в кучу (heap), чтобы наименьшие частоты были на вершине кучи
    while len(heap) > 1:
        left = heapq.heappop(heap) # Извлекаем узел с следующей наименьшей частотой
        right = heapq.heappop(heap)  # Извлекаем узел с следующей наименьшей частотой
        merged_node = Node(None, left.freq + right.freq) # Создаем новый узел с частотой, равной сумме частот
        merged_node.left = left # Устанавливаем левого потомка для нового узла
        merged_node.right = right # Устанавливаем правого потомка для нового узла
        heapq.heappush(heap, merged_node) # Помещаем новый узел обратно в кучу
    return heap[0] # Возвращаем корневой узел дерева Хаффмана


def build_huffman_code(node, code, mapping):
    if node.chars: # Если узел содержит символы (листовой узел), сохраняем код для символа
        mapping[node.chars] = code
    if node.left: # Рекурсивно обходим левого потомка с добавлением "0" к коду
        build_huffman_code(node.left, code + "0", mapping)
    if node.right: # Рекурсивно обходим правого потомка с добавлением "1" к коду
        build_huffman_code(node.right, code + "1", mapping)


def calculate_avg_code_length(huffman_mapping, char_freq): # Суммируем длины кодов, умноженные на соответствующие частоты символов (сочетаний)
    total_bits = sum(len(huffman_mapping[chars]) * freq for chars, freq in char_freq.items())
    total_chars = sum(char_freq.values()) # Общее количество символов (сочетаний) в тексте
    avg_code_length = total_bits / total_chars # Вычисляем среднюю длину кода как отношение суммарной длины к общему количеству символов
    return avg_code_length # Возвращаем среднюю длину элементарного кода


def calculate_compression_efficiency(original_text, encoded_text):
    original_bits = len(original_text) * 8  # Вычисляем количество бит в исходном тексте, предполагая 8 бит на символ
    encoded_bits = len(encoded_text)  # Вычисляем количество бит в закодированном тексте
    efficiency = (original_bits - encoded_bits) / original_bits * 100 # Вычисляем эффективность сжатия в процентах
    return efficiency # Возвращаем эффективность сжатия


def main():
    text = input("Введите текст для построения схемы алфавитного кодирования Хаффмана: ")

    # Подсчитываем частоту появления двухбуквенных сочетаний в тексте
    char_freq = Counter(text[i:i+2] for i in range(len(text)-1))

    huffman_tree = build_huffman_tree(char_freq)
    huffman_mapping = {}
    build_huffman_code(huffman_tree, "", huffman_mapping)

    avg_code_length = calculate_avg_code_length(huffman_mapping, char_freq)
    print(f"Средняя длина элементарного кода для двухбуквенных сочетаний: {avg_code_length:.2f} бит")

    encoded_text = "".join(huffman_mapping[chars] for chars in [text[i:i+2] for i in range(0,len(text)-1),2])
    print(f"Закодированный текст: {encoded_text}")

    efficiency = calculate_compression_efficiency(text, encoded_text)
    print(f"Эффективность сжатия для двухбуквенных сочетаний: {efficiency:.2f}%")

    decoded_text = ""
    current_code = ""
    for bit in encoded_text:
        current_code += bit
        if current_code in huffman_mapping.values():
            decoded_text += [chars for chars, code in huffman_mapping.items() if code == current_code][0]
            current_code = ""
    print(f"Декодированный текст: {decoded_text}")

    print("Схема алфавитного кодирования Хаффмана для однобуквенных сочетаний:")
    for chars, code in huffman_mapping.items():
        print(f"{chars}: {code}")


if __name__ == "__main__":
    main()
# это какойнибудь текст для обработки дь
