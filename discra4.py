# НЕ РАБОТАЕТ
# НЕ РАБОТАЕТ
# НЕ РАБОТАЕТ
# НЕ РАБОТАЕТ




def calculate_parity_bits(data_bits): 
    r = 1 # Инициализируем количество проверочных битов равным 1
    while 2 ** r < len(data_bits) + r + 1:
        r += 1 # Увеличиваем количество проверочных битов, пока не достигнем условия
    return r # Возвращаем количество проверочных битов

def generate_hamming_code(data_bits):
    m = len(data_bits) # Определяем количество информационных битов
    r = calculate_parity_bits(data_bits) # Вычисляем количество проверочных битов

    # Создаем порождающую матрицу (G)
    G = [[0] * (m + r) for _ in range(m)] # Создаем матрицу размером (m x (m + r)) и заполняем нулями
    for i in range(m): 
        for j in range(r):
            G[i][j] = (i + 1) & (1 << j) != 0 # Заполняем элементы матрицы согласно шаблону
        for j in range(m):
            G[i][r + j] = data_bits[j] # Добавляем информационные биты в матрицу G

    # Создаем проверочную матрицу (H)
    H = [[0] * (m + r) for _ in range(r)] # Создаем матрицу размером (r x (m + r)) и заполняем нулями
    for i in range(r):
        for j in range(m): 
            H[i][j] = (i + 1) & (1 << j) != 0  # Заполняем элементы матрицы согласно шаблону
        H[i][m + i] = 1 # Заполняем элементы диагонали матрицы H единицами
 
    return G, H # Возвращаем порождающую и проверочную матрицы

def encode_hamming(data_bits, G):
    m = len(data_bits) # Определяем количество информационных битов
    r = len(G[0]) - m # Определяем количество проверочных битов на основе порождающей матрицы
    encoded_data = [0] * (m + r) # Инициализируем кодовое слово нулями
    
    for i in range(m): 
        for j in range(m + r):
            encoded_data[j] += data_bits[i] * G[i][j] # Умножаем информационные биты на элементы порождающей матрицы
            encoded_data[j] %= 2  # Применяем операцию по модулю 2 к результатам

    return encoded_data # Возвращаем кодовое слово

def introduce_error(encoded_data):
    error_position = 1  # Внесем ошибку в первый бит кодового вектора
    encoded_data[error_position] = 1 - encoded_data[error_position] # Меняем бит на противоположный
    return encoded_data, error_position # Возвращаем кодовое слово с ошибкой и позицию ошибки

def calculate_syndrome(encoded_data, H):
    r = len(H)  # Определяем количество проверочных битов (длина строк в матрице H)
    syndrome = [0] * r # Инициализируем синдром нулями
    
    for i in range(r):
        for j in range(len(encoded_data)): 
            syndrome[i] += encoded_data[j] * H[i][j] # Умножаем кодовое слово на элементы проверочной матрицы
            syndrome[i] %= 2 # Применяем операцию по модулю 2 к результату

    return syndrome # Возвращаем синдром ошибки

def correct_error(encoded_data, error_position, syndrome, H):
    error_index = sum(2 ** i for i, bit in enumerate(syndrome)) # Вычисляем индекс ошибочного бита из синдрома
    corrected_bit_position = error_index - 1 # Определяем позицию ошибочного бита
    # Меняем значение ошибочного бита на противоположное
    encoded_data[corrected_bit_position] = 1 - encoded_data[corrected_bit_position] 
    return encoded_data # Возвращаем кодовое слово с исправленной ошибкой

# Запрашиваем у пользователя количество информационных битов
num_data_bits = int(input("Введите количество информационных разрядов: "))
data_bits = [int(bit) for bit in input("Введите информационные биты (0 и 1 чередуются): ")]

# Генерируем порождающую и проверочную матрицы
G, H = generate_hamming_code(data_bits)

# Кодируем информационные биты
encoded_data = encode_hamming(data_bits, G)

# Внесем ошибку в кодовое слово
encoded_data_with_error, error_position = introduce_error(encoded_data)

# Рассчитываем синдром
syndrome = calculate_syndrome(encoded_data_with_error, H)

# Исправляем ошибку и получаем исправленное кодовое слово
corrected_encoded_data = correct_error(encoded_data_with_error, error_position, syndrome, H)

print("Информационные биты:", data_bits)
print("Кодовое слово с ошибкой:", encoded_data_with_error)
print("Синдром ошибки:", syndrome)
print("Исправленное кодовое слово:", corrected_encoded_data)
print("Порождающая матрица G: ",G)
print("Проверочная матрица H: ",H)
