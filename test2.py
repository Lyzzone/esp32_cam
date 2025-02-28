import numpy as np
import pathlib
import matplotlib.pyplot as plt

class Dataloader():
    """
        数据读取器
    """  
    def get_data(self):
        with np.load(f"{pathlib.Path(__file__).parent.absolute()}/data/mnist.npz") as f:
            images, labels = f["x_train"], f["y_train"]
        images = images.astype("float16") / 255
        images = np.reshape(images, (images.shape[0], images.shape[1] * images.shape[2]))
        labels = np.eye(10)[labels]
        return images, labels

if __name__ == "__main__":
    # 通过dataloader读取数据
    dataloader = Dataloader()
    images, labels = dataloader.get_data()
    # 将数据从形状 (784,) 转换为 (784, 1)
    # images[10].astype(np.float32)
    # data_reshaped = images[10].reshape((784, 1))

    images[55].tofile('img3.bin')
    # data_reshaped.tofile('img2.bin')

    print(images[55].shape, images[55][550])
    # print(data_reshaped.shape, data_reshaped[550])
    