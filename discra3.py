import heapq
from collections import defaultdict, Counter
import math

# однобуквеные сочетания
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(freq_dict):
    heap = [Node(char, freq) for char, freq in freq_dict.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged_node = Node(None, left.freq + right.freq)
        merged_node.left = left
        merged_node.right = right
        heapq.heappush(heap, merged_node)
    return heap[0]


def build_huffman_code(node, code, mapping):
    if node.char:
        mapping[node.char] = code
    if node.left:
        build_huffman_code(node.left, code + "0", mapping)
    if node.right:
        build_huffman_code(node.right, code + "1", mapping)


def calculate_avg_code_length(huffman_mapping, char_freq):
    total_bits = sum(len(huffman_mapping[char]) * freq for char, freq in char_freq.items())
    total_chars = sum(char_freq.values())
    avg_code_length = total_bits / total_chars
    return avg_code_length


def calculate_compression_efficiency(original_text, encoded_text):
    original_bits = len(original_text) * 8  # Assuming 8 bits per character
    encoded_bits = len(encoded_text)
    efficiency = (original_bits - encoded_bits) / original_bits * 100
    return efficiency


def main():
    text = input("Введите текст для построения схемы алфавитного кодирования Хаффмана: ")
    char_freq = Counter(text)

    huffman_tree = build_huffman_tree(char_freq)
    huffman_mapping = {}
    build_huffman_code(huffman_tree, "", huffman_mapping)

    avg_code_length = calculate_avg_code_length(huffman_mapping, char_freq)
    print(f"Средняя длина элементарного кода: {avg_code_length:.2f} бит")

    encoded_text = "".join(huffman_mapping[char] for char in text)
    print(f"Закодированный текст: {encoded_text}")

    efficiency = calculate_compression_efficiency(text, encoded_text)
    print(f"Эффективность сжатия: {efficiency:.2f}%")

    decoded_text = ""
    current_code = ""
    for bit in encoded_text:
        current_code += bit
        if current_code in huffman_mapping.values():
            decoded_text += [char for char, code in huffman_mapping.items() if code == current_code][0]
            current_code = ""
    print(f"Декодированный текст: {decoded_text}")

    print("Схема алфавитного кодирования Хаффмана для однобуквенных сочетаний:")
    for char, code in huffman_mapping.items():
        print(f"{char}: {code}")


if __name__ == "__main__":
    main()
# это какойнибудь текст для обработки дь