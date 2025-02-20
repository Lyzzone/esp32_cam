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

# 激活函数（sigmoid）
def sigmoid(x):
    if x >= 0:
        return 1 / (1 + math.exp(-x))
    else:
        return math.exp(x) / (1 + math.exp(x))
    
# 矩阵乘法函数
def matmul(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if cols_A != rows_B:
        raise ValueError("矩阵 A 的列数必须等于矩阵 B 的行数")

    # 初始化结果矩阵
    result = [[0.0 for _ in range(cols_B)] for _ in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]

    return result

# 前向传播
def forward_propagation(img, w_i_h, b_i_h, w_h_o, b_h_o):
    # 计算 h_pre
    h_pre = matmul(w_i_h, img)
    h_pre = [[h_pre[i][j] + b_i_h[i][0] for j in range(len(h_pre[0]))] for i in range(len(h_pre))]

    # 激活函数处理
    h = [[sigmoid(x) for x in row] for row in h_pre]

    # 计算 o_pre
    o_pre = matmul(w_h_o, h)
    o_pre = [[o_pre[i][j] + b_h_o[i][0] for j in range(len(o_pre[0]))] for i in range(len(o_pre))]

    # 激活函数处理
    o = [[sigmoid(x) for x in row] for row in o_pre]

    return o

if __name__ == "__main__":
    # 加载图像和矩阵
    img = load_image('img3.bin', 784, 1)  # 图像文件路径
    w_h_o = load_matrix('w_h_o.bin', 10, 20)  # w_h_o 矩阵
    b_i_h = load_matrix('b_i_h.bin', 20, 1)  # b_i_h 矩阵
    b_h_o = load_matrix('b_h_o.bin', 10, 1)  # b_h_o 矩阵
    w_i_h = load_matrix('w_i_h.bin', 20, 784)  # w_i_h 矩阵
    
    # 前向传播
    o = forward_propagation(img, w_i_h, b_i_h, w_h_o, b_h_o)

    # 输出结果
    prediction = [x[0] for x in o].index(max([x[0] for x in o]))  # 输出预测值
    print(f"This figure is predicted to be: {prediction}")