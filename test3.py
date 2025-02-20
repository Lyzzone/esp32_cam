import math
import struct

# 读取图像：
def load_image(file_path, rows, cols):
    # 打开二进制文件
    with open(file_path, 'rb') as f:
        # 初始化矩阵
        matrix = [[0.0 for _ in range(cols)] for _ in range(rows)]
        
        for i in range(rows):
            for j in range(cols):
                # 每次读取 2 字节（16 位）
                data = f.read(2)
                if not data:
                    raise ValueError("文件数据不足以填充矩阵")
                
                # 将 2 字节数据解析为 uint16
                uint16_value = struct.unpack('<H', data)[0]  # 小端字节序
                
                # 将 uint16 转换为 float16（手动转换）
                float_value = float16_to_float(uint16_value)
                
                # 将值存入矩阵
                matrix[i][j] = float_value
        
        return matrix

def float16_to_float(uint16_value):
    # 将 uint16 转换为 float16 的位表示
    sign = (uint16_value >> 15) & 0x01
    exponent = (uint16_value >> 10) & 0x1F
    fraction = uint16_value & 0x3FF

    # 处理特殊情况（如无穷大和 NaN）
    if exponent == 0x1F:
        if fraction == 0:
            return float('inf') if sign == 0 else float('-inf')
        else:
            return float('nan')

    # 转换为 float32
    if exponent == 0:
        if fraction == 0:
            return 0.0 if sign == 0 else -0.0
        else:
            # 非规范化数
            exponent = -14
            fraction = fraction / 1024.0
    else:
        # 规范化数
        exponent -= 15
        fraction = (fraction / 1024.0) + 1.0

    # 计算最终的浮点数值
    return (-1 if sign else 1) * fraction * (2.0 ** exponent)


# 读取二进制矩阵
def load_matrix(file_path, rows, cols):
    """
    从二进制文件读取数据，并按指定的行列数构成矩阵。
    
    :param file_path: 文件路径
    :param rows: 矩阵的行数
    :param cols: 矩阵的列数
    :return: 返回一个嵌套的列表（矩阵）
    """
    data = []
    
    # 打开文件并读取二进制数据
    with open(file_path, 'rb') as file:
        while True:
            byte_data = file.read(8)  # 每次读取8字节（双精度浮点数的大小）
            if not byte_data:
                break  # 文件读取完毕，退出循环
            value = struct.unpack('d', byte_data)  # 解包为双精度浮点数
            data.append(value[0])  # 将浮点数加入数据列表

    # 检查读取的数据是否符合要求
    if len(data) != rows * cols:
        raise ValueError(f"读取的数据数量 {len(data)} 不匹配指定的矩阵大小 {rows}x{cols}")

    # 将数据重新组织成矩阵
    matrix = [data[i:i + cols] for i in range(0, len(data), cols)]
    
    return matrix

# # 假设 w_i_h 是 (20, 784) 的矩阵，img 是 (784, 1) 的矩阵
# w_i_h = [[0] * 784 for _ in range(20)]  # 初始化为零的矩阵（20, 784）
# img = [[0] for _ in range(784)]  # 初始化为零的矩阵（784, 1）

# # 假设填充一些非零数据
# img[100] = [1.5]
# img[500] = [2.5]

# w_i_h[0][100] = 0.5
# w_i_h[0][500] = 1.0
# w_i_h[1][100] = 1.0
# w_i_h[1][500] = 1.5

# w_i_h = load_matrix('w_i_h.bin', 20, 784)  # w_i_h 矩阵
# img = load_image('img3.bin', 784, 1)  # 图像文件路径
# # 步骤 1: 找出 img 中非零的索引
# non_zero_indices = [i for i in range(784) if img[i][0] != 0]

# # 步骤 2: 提取 w_i_h 中与非零元素对应的列
# # 这里我们保留 w_i_h 中对应的列
# w_i_h_sparse = [[w_i_h[row][index] for index in non_zero_indices] for row in range(20)]

# # 步骤 3: 计算矩阵乘法
# # 进行 (20, k) 乘 (k, 1) 的矩阵乘法，其中 k 是 non_zero_indices 的长度
# result = []
# for row in range(20):
#     value = sum(w_i_h_sparse[row][i] * img[non_zero_indices[i]][0] for i in range(len(non_zero_indices)))
#     result.append(value)

# # 输出结果
# print("计算结果：")
# print(result)

w_h_o = load_matrix('w_h_o.bin', 10, 20)  # w_h_o 矩阵
print(w_h_o)