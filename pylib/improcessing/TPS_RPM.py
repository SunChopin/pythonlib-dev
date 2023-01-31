"""
Script Name: TPS_RPM
Author: Xiaoxian Jin
Created: 2021/11/27
Last modified: 2021/11/27
Version: 1
Modification:
Description: Register two sets of points. Two sets of points do not have to have the same number of points.
"""

import numpy as np
import math
import pyvista as pv


def TPS_RPM(V0, X, anneal_rate=0.5, T_init=0.05, T_fac=500, lambda1=1):
    """
    INPUT:
        V0: ndarray(K*3), the source point set
        X: ndarray(N*3), the target point set
        anneal_rate: the annealing rate
        T_init: the initial temperature
        T_fac: T_final=T_init/T_fac
    OUTPUT:
        TPS_RPM results, ndarray(K*3)
    """

    Iter_perT = 5  # 对每个T的最大循环次数
    lambda1_init = lambda1  # 计算d w
    lambda2_init = 0.01

    K = V0.shape[0]  # 待配准点云 K
    N = X.shape[0]  # 目标点云 N
    Dim = V0.shape[1]

    # 归一化
    center_V0 = (sum(V0)/K).reshape((1, Dim))
    V0 = V0 - np.dot(np.ones((K, 1)), center_V0)
    scale_V0 = np.sqrt((sum(np.power(V0, 2))/K).reshape((1, Dim)))
    V0 = V0 / np.dot(np.ones((K, 1)), scale_V0)

    center_X = (sum(X) / N).reshape((1, Dim))
    X = X - np.dot(np.ones((N, 1)), center_X)
    scale_X = np.sqrt((sum(np.power(X, 2)) / N).reshape((1, Dim)))
    X = X / np.dot(np.ones((N, 1)), scale_X)

    # 初始化权重m
    m = np.ones((K, N)) / (K*N)
    T0 = math.pow(max(V0[:, 0]), 2)  # pow求平方
    moutlier = 1 / math.sqrt(T0) * math.exp(-1)
    m_outliers_row = np.ones((1, N)) * moutlier
    m_outliers_col = np.ones((K, 1)) * moutlier

    # 退火
    T = T_init
    T_final = T_init / T_fac

    Vx = V0  # Vx表示f(v),初始值与待配准点云一致
    z = np.concatenate((np.ones((K, 1)), V0), axis=1)

    flag_stop = 0
    while flag_stop != 1:
        for i in range(1, Iter_perT+1):  # 左闭右开区间 1,2,...,Iter_perT
            # nan
            Vx_last = Vx

            # 更新权重矩阵m
            m = ComputeM(Vx, X, K, N, T, moutlier, m_outliers_row, m_outliers_col)

            # 更新变换矩阵
            Vy = np.dot(m, X) / np.dot(np.sum(m, axis=1).reshape((K, 1)), np.ones((1, Dim)))  # Vy 使用权重计算出的目标点云位置

            lambda1 = lambda1_init * K * T
            lambda2 = lambda2_init * K * T

            w, d, PHI = ComputeT(V0, Vy, lambda1, lambda2)  # w:K*(D+1) d:(D+1)*(D+1) PHI:K*K

            # 更新点云
            PHI = ComputePHI(z, z)
            Vx = np.dot(z, d) + np.dot(PHI, w)
            Vx = Vx[:, 1: Dim + 1]

            # nan
            ind_x = np.isnan(Vx)
            Vx[ind_x] = Vx_last[ind_x]

        T = T * anneal_rate

        if T < T_final:
            flag_stop = 1

    # 恢复位置和尺度
    Vx = Vx * np.dot(np.ones((K, 1)), scale_X) + np.dot(np.ones((K, 1)), center_X)

    return Vx


def ComputeM(Vx, X, K, N, T, moutlier, m_outliers_row, m_outliers_col):
    K = Vx.shape[0]  # 待配准点云 K
    N = X.shape[0]  # 目标点云 N
    Dim = Vx.shape[1]

    tmp = np.zeros((K, N))
    for it_dim in range(0, Dim):  # 左闭右开 0,1,2
        tmp = tmp + np.power(np.dot(Vx[:, it_dim:it_dim + 1], np.ones((1, N))) -
                             np.dot(np.ones((K, 1)), np.transpose(X[:, it_dim:it_dim + 1])), 2)
    m_tmp = 1 / math.sqrt(T) * np.exp(-tmp / T)
    # m_tmp = m_tmp + np.random.randn(K, N) * (1 / K) * 0.001

    m = m_tmp
    # normalize accross the outliers as well
    sy = sum(m) + m_outliers_row  # sum 按列求和
    m = m / np.dot(np.ones((K, 1)), sy)  # 权重矩阵m K*N

    # ---2021.10.12新增加 normalize1
    # sy = sum(m) + m_outliers_row  # sum 按列求和
    # m1 = m / np.dot(np.ones((K, 1)), sy)  # 权重矩阵m K*N
    # sx = sum(np.transpose(m)).reshape((K, 1)) + m_outliers_col  # sum 按行求和
    # m2 = m / np.dot(sx, np.ones((1, N)))  # 权重矩阵m K*N
    # m = (m1 + m2)/2

    # ---2021.10.15新增加 normalize2
    # moutlier = 1 / K * 0.1
    # m_outliers_row = np.ones((1, N)) * moutlier
    # m_outliers_col = np.ones((K, 1)) * moutlier
    # m = C_normalize_m(K, N, m, m_outliers_col, m_outliers_row)

    return m


def C_normalize_m (K, N, m, m_outliers_col, m_outliers_row):
    norm_threshold = 0.05
    norm_maxit = 10

    norm_it = 0
    flag = 0
    while flag == 0:
        sy = sum(m) + m_outliers_row  # sum 按列求和
        m = m / np.dot(np.ones((K, 1)), sy)  # 权重矩阵m K*N
        m_outliers_row = m_outliers_row / sy

        sx = sum(np.transpose(m)).reshape((K, 1)) + m_outliers_col  # sum 按行求和
        m = m / np.dot(sx, np.ones((1, N)))  # 权重矩阵m K*N
        m_outliers_col = m_outliers_col / sx

        pre_err = np.dot(np.transpose(sx - 1), (sx-1)) + np.dot((sy-1), np.transpose(sy - 1))
        err = (pre_err / (K + N))

        if err < np.power(norm_threshold, 2):
            flag = 1

        norm_it = norm_it + 1
        if norm_it >= norm_maxit:
            flag = 1
    return m


def ComputeT(V, Y, lambda1, lambda2):
    K = V.shape[0]  # V.shape=Y.shape
    D = V.shape[1]

    V = np.concatenate((np.ones((K, 1)), V), axis=1)
    Y = np.concatenate((np.ones((K, 1)), Y), axis=1)

    # 计算PHI
    PHI = ComputePHI(V, V)

    # 计算QR
    q, r = np.linalg.qr(V, mode="complete")
    q1 = q[:, 0:D+1]  # K*(D+1)
    q2 = q[:, D+1:K]  # N*(K-D-1) K*(K-D-1)?
    R = r[0:D+1, 0:D+1]  # (D+1)*(D+1)

    # 计算w d
    pre_gamma = np.dot(np.dot(np.transpose(q2), PHI), q2) + lambda1 * np.eye(K-D-1)  # (K-D-1)*(K-D-1)
    gamma = np.dot(np.dot(np.linalg.inv(pre_gamma), np.transpose(q2)), Y)  # (K-D-1)*(D+1)
    w = np.dot(q2, gamma)  # K*(D+1)

    pre_A1 = np.dot(np.transpose(R), R) + lambda2 * np.eye(D+1)  # (D+1)*(D+1)
    pre_A2 = Y - np.dot(np.dot(PHI, q2), gamma)  # K*(D+1)
    pre_A3 = np.dot(np.dot(np.transpose(R), np.transpose(q1)), pre_A2) - np.dot(np.transpose(R), R)  # (D+1)*(D+1)
    A = np.dot(np.linalg.inv(pre_A1), pre_A3)  # (D+1)*(D+1)
    d = A + np.eye(D+1)  # (D+1)*(D+1)

    return w, d, PHI


def ComputePHI(V, Y):
    n = V.shape[0]
    m = Y.shape[0]
    D = V.shape[1]

    # 计算PHI
    PHI = np.zeros((n, m))
    for it_dim in range(1, D):
        tmp = np.dot(V[:, it_dim:it_dim + 1], np.ones((1, m))) - np.dot(np.ones((n, 1)), np.transpose(Y[:, it_dim:it_dim + 1]))
        tmp = tmp * tmp
        PHI = PHI + tmp
    if D-1 == 3:
        PHI = - np.sqrt(PHI)
    elif D-1 == 2:
        mask = np.zeros((n, m))
        mask[PHI < 1e-10] = 1
        PHI = 0.5 * PHI * np.log(PHI + mask) * (1 - mask)
    return PHI


# ---------------test-------------
if __name__ == "__main__":

    path_V0 = "F:/copy/标准/Crown Unn4.stl"
    path_X = "F:/copy/UNN4/1 (14).5.stl"
    mesh_V0 = pv.read(path_V0)
    mesh_V0 = mesh_V0.decimate_boundary(target_reduction=1-(1500/mesh_V0.n_points))
    V0 = np.array(mesh_V0.points, dtype='float64')
    mesh_X = pv.read(path_X)
    mesh_X = mesh_X.decimate_boundary(target_reduction=1-(1500/mesh_X.n_points))
    X = np.array(mesh_X.points, dtype='float64')

    import time
    start = time.time()

    result = TPS_RPM(V0, X)  # 调用函数

    end = time.time()
    total_time = end - start
    print(total_time)
    print(time.strftime("%H:%M:%S", time.gmtime(total_time)))

    mesh_V = mesh_V0.copy()
    mesh_V.points = result

    p = pv.Plotter()
    p.add_mesh(mesh_V0, color="Crimson", show_edges=True, opacity=0.3)
    p.add_mesh(mesh_X, color="mintcream", show_edges=True, opacity=1)
    p.add_mesh(mesh_V, color="green", show_edges=True, opacity=1)
    p.show()
