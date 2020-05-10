import numpy as np
import matplotlib.pyplot as plt
import collections

def calculate_Distance(data):
    distance_Matrix = np.zeros(shape=(len(data), len(data)))
    for i in range(len(data)):
        for j in range(len(data)):
            if i > j:
                distance_Matrix[i][j] = distance_Matrix[j][i]
            elif i < j:
                distance_Matrix[i][j] = np.sqrt(np.sum(np.power(data[i] - data[j], 2)))
    return distance_Matrix


def dc_Get(distance_Matrix, tolerance):
    temp_Distance = [] #用于存储所有点对的距离
    for i in range(len(distance_Matrix[0])):
        for j in range(i + 1, len(distance_Matrix[0])):
            temp_Distance.append(distance_Matrix[i][j])
    temp_Distance.sort() #对距离进行升序排序
    dc = temp_Distance[int(len(temp_Distance) * tolerance / 100)] #获取第tolerance%的点对距离作为截断距离
    return dc


def density_Get(distance_Matrix, dc):
    #methon_1
    # density = np.zeros(shape=len(distance_Matrix))
    # for i in range(len(distance_Matrix[0])):
    #     for j in range(len(distance_Matrix[0])):
    #         if distance_Matrix[i][j] <= dc:
    #             density[i] += 1
    # return density
    #methon_2
    density = np.zeros(shape=len(distance_Matrix))
    for index, node in enumerate(distance_Matrix):
        density[index] = np.sum(np.exp(-(node / dc) ** 2))
    return density

def detal_Get(density, distance_Matrix):
    detal_ls = np.zeros(shape=len(distance_Matrix))#detal_ls存储每个点的detal值
    closest_Distance = np.zeros(shape=len(distance_Matrix), dtype=np.int32)#closest_Distance存储比当前点密度高的点集中最近的距离点的索引
    for index, node in enumerate(distance_Matrix):
        density_Larger_Than_Node = np.squeeze(np.argwhere(density > density[index]))#存储比当前点密度大的点
        if density_Larger_Than_Node.size != 0:#如果有密度大于自己的点
            #所有密度大于自己的点与自己的距离集合（一维数组或者一个数）
            distance_Between_Larger_Node = distance_Matrix[index][density_Larger_Than_Node]
            detal_ls[index] = np.min(distance_Between_Larger_Node)
            min_Distance_Index = np.squeeze(np.argwhere(distance_Between_Larger_Node == detal_ls[index]))
            #存在多个密度大于自己且距离自己最近的点时，选择一个点
            if min_Distance_Index.size >= 2:
                min_Distance_Index = np.random.choice(a=min_Distance_Index)
            if distance_Between_Larger_Node.size > 1:
                closest_Distance[index] = density_Larger_Than_Node[min_Distance_Index]
            else:
                closest_Distance[index] = density_Larger_Than_Node
        #对于最大密度的点
        else:
            detal_ls[index] = np.max(distance_Matrix)
            closest_Distance[index] = index
    return detal_ls, closest_Distance


def show_DensityDetal_And_Dataset(density, detal_Ls, data):
    plt.figure(num=1, figsize=(15, 9))
    #第一个子图为detal-density散点图
    ax1 = plt.subplot(121)
    for i in range(len(data)):
        plt.scatter(x=density[i], y=detal_Ls[i], c='r', marker='o', s=50)
    plt.xlabel('density')
    plt.ylabel('detal')
    plt.title('num_Cluster')
    plt.sca(ax1)
    #第二个子图为原始数据点的散点图
    ax2 = plt.subplot(122)
    for j in range(len(data)):
        plt.scatter(x=data[j, 0], y=data[j, 1], marker='o', c='b', s=50)
    plt.xlabel('axis_x')
    plt.ylabel('axis_y')
    plt.title('set_Data')
    plt.sca(ax2)
    plt.show()


def show_Decision_Graph(density, detal_Ls):
    #  由于密度和最短距离两个属性的数量级可能不一样，分别对两者做归一化使结果更平滑
    normal_Density = (density - np.min(density)) / (np.max(density) - np.min(density))
    normal_Detal = (detal_Ls - np.min(detal_Ls)) / (np.max(detal_Ls) - np.min(detal_Ls))
    gamma = normal_Density * normal_Detal
    plt.figure(num=2, figsize=(15, 10))
    plt.scatter(x=range(len(detal_Ls)), y=-np.sort(-gamma), c='k', marker='o', s=-np.sort(-gamma) * 100)
    plt.xlabel('data_num')
    plt.ylabel('gamma')
    plt.title('Guarantee The Leader')
    plt.show()
    return gamma


def clustering(clusters_Num, cluster_Centre_Ls):
    for i in range(len(clusters_Num)):
            while clusters_Num[i] not in cluster_Centre_Ls:
                j = clusters_Num[i]
                clusters_Num[i] = clusters_Num[j]
    cluster_Belong = clusters_Num[:]
    return cluster_Belong  #归属


def show_Result(cluster_Belong, data, cluster_Centre_Ls):
    colors = [
        'cyan', 'green', 'blue', 'magenta', 'chocolate',
        'forestgreen', 'aquamarine', 'darkslateblue', 'lime', 'yellow',
        'greenyellow', 'brown', 'red','orange','gray',
        'coral', 'plum', 'burlywood', 'bisque', 'cadetblue',
        'saddlebrown','darkgray', 'rosybrown', 'olivedrab', 'powderblue',
        'turquoise', 'thistle', 'springgreen', 'steelblue', 'darkgreen',
        'mediumspringgreen', 'whitesmoke', 'darksalmon','slategray', 'darkseagreen',
        'azure', 'lawngreen', 'deepskyblue', 'honeydew', 'indianred',
        'darkslategray', 'ivory', 'dodgerblue', 'darkorchid', 'forestgreenblack',

    ]

    # 画最终聚类效果图
    leader_Color = {}
    main_Leaders = dict(collections.Counter(cluster_Belong)).keys()
    for index, i in enumerate(main_Leaders):
        leader_Color[i] = index
    plt.figure(num=3, figsize=(15, 10))
    i = 1
    for node, class_ in enumerate(cluster_Belong):
        #  标出每一类的聚类中心点
        if node in cluster_Centre_Ls:
            plt.scatter(x=data[node, 0], y=data[node, 1], marker="o", s=100, c='r')
            plt.text(data[node, 0], data[node, 1], str(i), ha = 'center',fontsize=15,c='K')
            i += 1
        else:
            plt.scatter(x=data[node, 0], y=data[node, 1], c=colors[leader_Color[class_]], marker='o', s=100)
    plt.title('The Result Of Cluster')
    plt.show()


def main(data):
    distance_Matrix = calculate_Distance(data) #获取距离矩阵，distance[i][j]表示第i个元素和第j个元素之间的欧式距离
    tolerance = 2 #tolerance%用于寻找截断距离，我们本代码中设为2，据论文介绍，截断距离的对聚类的影响不太大
    dc = dc_Get(distance_Matrix, tolerance) #dc为截断距离，本行进行获取dc
    density = density_Get(distance_Matrix, dc) #按照论文公式（1）进行计算每个点的local density
    detal_Ls, closest_Distance = detal_Get(density, distance_Matrix) #detal_ls存储每个点的detal值，closest_distance存储比当前点密度高的点集中最近的距离点的索引
    show_DensityDetal_And_Dataset(density, detal_Ls, data) #展示density-detal散点图和原始data图
    density_Multiply_Detal_Sort = show_Decision_Graph(density, detal_Ls) #展示决策图，返回标准化后的density和detal乘积（已经进行排序）
    clusters_Num = int(input('input clusters num:')) #根据决策图输入聚类数
    cluster_Centre_Ls = np.argsort(-density_Multiply_Detal_Sort)[: clusters_Num] #获取聚类中心点的集合
    cluster_Belong = clustering(closest_Distance, cluster_Centre_Ls)  # 确定各点的最终归属（哪个司令）
    show_Result(cluster_Belong, data, cluster_Centre_Ls)  # 展示结果


if __name__ == '__main__':
    pathname = r'data\Jain.txt'
    data = np.loadtxt(pathname, delimiter='	', usecols=[0, 1])
    main(data)