import matplotlib.pyplot as plt


def plot_file(file_name):
    with open(file_name + '.txt', 'r') as file:
        raw_data = file.readlines()
        X = [int(chain.split(';')[0]) for chain in raw_data]
        Y = [int(chain.split(';')[1]) for chain in raw_data]
        plt.scatter(X, Y)


plot_file('10')
plt.show()
