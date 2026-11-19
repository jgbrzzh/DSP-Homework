# 第三章 · DFT 与 FFT

> 指定作业：**3.1、3.8、3.11、3.14、3.25**。
> 五道题分别练：DFS 周期长度变换、周期输入的 LTI 响应、DFT 圆周对称、插零的 DFT、用 FFT 计算指定单位圆采样。

## 一、先把共同的符号与定义写清

### 1. DTFT、DFS、DFT、FFT 的区别

| 名称 | 处理什么 | 结果是什么 | 本章用途 |
|---|---|---|---|
| DTFT | 一般离散序列 | 连续频率、2π 周期的函数 | 理解频谱、系统响应 |
| DFS | 周期序列 | 一组周期重复的离散系数 | 3.1、3.8 |
| DFT | N 个样本 | N 个频率格点上的数值 | 3.11、3.14、3.25 |
| FFT | 一种快速计算方法 | 与相同点数 DFT 完全相同的结果 | 3.25 |

FFT 不另定义一种变换。3.25 的核心是**先构造正确的 N 点输入**，再做一次 N 点 FFT。

### 2. 统一约定

$$
\boxed{W_N=e^{-j2\pi/N}.}
$$

N 点 DFT 与 IDFT：

$$
X[k]=\sum_{n=0}^{N-1}x[n]W_N^{kn},\qquad
x[n]=\frac1N\sum_{k=0}^{N-1}X[k]W_N^{-kn}.
$$

本讲义的 DFS 使用相同的归一化：

$$
\widetilde X[k]=\sum_{n=0}^{N-1}\widetilde x[n]e^{-j2\pi kn/N},\qquad
\widetilde x[n]=\frac1N\sum_{k=0}^{N-1}\widetilde X[k]e^{j2\pi kn/N}.
$$

区别是 $\widetilde x[n]$ 本来就在全体整数上周期重复；有限长 $x[n]$ 只指定一段样本。第一套 `第2章-1.ppt` 第 7 页直接采用上面的 DFS 口径。

### 3. 模 N 下标是什么

记 $(r)_N$ 为 r 除以 N 的余数，结果取 $0,1,\ldots,N-1$。

例如 N=4 时，$(-1)_4=3$、$(-2)_4=2$。所以圆周反折

$$
x[(-n)_4]=\{x[0],x[3],x[2],x[1]\}.
$$

这与把四个数从右往左写成 $\{x[3],x[2],x[1],x[0]\}$ 不同。

## 二、3.1：同一周期序列改按 2N 周期计算 DFS

### 题目

一个周期为 N 的序列 $\widetilde x[n]$ 也以 2N 为周期。以 N 作为周期长度计算的 DFS 为 $\widetilde X_1[k]$；以 2N 作为周期长度计算的 DFS 为 $\widetilde X_2[k]$。由前者求后者。

**注意**：题目没有改变序列，也没有在原样本之间插零，只是把 DFS 的一个计算周期从 N 点选成 2N 点。

### 推导的关键：把两段 N 点拆开

按定义

$$
\widetilde X_2[k]=\sum_{n=0}^{2N-1}\widetilde x[n]e^{-j2\pi kn/(2N)}.
$$

将后半段令 $n=m+N$，利用 $\widetilde x[m+N]=\widetilde x[m]$：

$$
\begin{aligned}
\widetilde X_2[k]
&=\sum_{m=0}^{N-1}\widetilde x[m]e^{-j\pi km/N}
+\sum_{m=0}^{N-1}\widetilde x[m]e^{-j\pi k(m+N)/N}\\
&=\left(1+e^{-j\pi k}\right)
\sum_{m=0}^{N-1}\widetilde x[m]e^{-j\pi km/N}\\
&=\left(1+(-1)^k\right)
\sum_{m=0}^{N-1}\widetilde x[m]e^{-j\pi km/N}.
\end{aligned}
$$

若 $k=2r$ 为偶数，前因子为 2，指数化为原来 N 点 DFS 的指数：

$$
\widetilde X_2[2r]=2\sum_{m=0}^{N-1}\widetilde x[m]e^{-j2\pi rm/N}
=2\widetilde X_1[r].
$$

若 k 为奇数，前因子为零。

### 最终结果

在 $0\le k\le2N-1$ 内，

$$
\boxed{
\widetilde X_2[k]=\begin{cases}
2\widetilde X_1[k/2],&k\text{ 为偶数},\\
0,&k\text{ 为奇数}.
\end{cases}}
$$

之后按 2N 周期延拓。原谱线保留在新频率格点的偶数位置，新增的奇数格点没有成分。

### 为什么系数加倍却没有使原信号幅度加倍

因为逆变换的系数也从 $1/N$ 变为 $1/(2N)$：

$$
\frac1{2N}\cdot2\widetilde X_1[r]
=\frac1N\widetilde X_1[r].
$$

若有人把“傅里叶级数系数”定义成 $c_N[k]=\widetilde X_1[k]/N$，则新系数满足 $c_{2N}[2r]=c_N[r]$，而不是加倍。两种记法都可成立，但不能混用定义。

### 一眼检查与推广

选常数序列 $\widetilde x[n]\equiv1$：N 点求和的 DC 为 N，2N 点求和的 DC 为 2N，验证了因子 2。

改按 qN 周期计算时，同理得到

$$
\widetilde X_q[k]=\begin{cases}
q\widetilde X_1[k/q],&k\equiv0\pmod q,\\
0,&\text{其他}.
\end{cases}
$$

**大题记忆线**：定义 → 拆成两段 → 用时域周期性 → 提取 $1+(-1)^k$ → 分奇偶。

## 三、3.8：周期输入通过 LTI 系统后的输出

### 题目与必要条件

周期为 N 的 $\widetilde x[n]$ 通过系统 $H(z)$，用其 DFS 系数 $\widetilde X[k]$ 表示输出 $\widetilde y[n]$。

本题按 LTI 系统解释，并要求相关频率处的响应存在。一个足够条件是 $h[n]$ 绝对可和，即系统 BIBO 稳定；这样周期输入的卷积有意义。讨论的是周期稳态/对全时域周期输入的零状态响应，不额外叠加任意初值产生的自然响应。

### 先处理扫描题面的符号

扫描页把目标式写为

$$
\frac1N\sum_{k=0}^{N-1}H(W_N^k)\widetilde X[k]W_N^{-nk}.
$$

但对课件明确采用的 $W_N=e^{-j2\pi/N}$ 和 $H(z)=\sum_mh[m]z^{-m}$，与 $W_N^{-nk}=e^{j2\pi kn/N}$ 对应的系统增益应当是

$$
\boxed{H(e^{j2\pi k/N})=H(W_N^{-k}).}
$$

因此**扫描目标式与本课件约定存在一处符号不一致**。下文用明确的指数形式推导，不把这个符号差异悄悄忽略。作答时可先写明 W 的定义，再写推导与指数形式结果；若老师采用其他定义，应整套核对正、逆变换，不能只改单个符号。

### 方法一：复指数是 LTI 系统的特征输入

先看单个复指数 $e^{j\omega_kn}$，其中 $\omega_k=2\pi k/N$：

$$
\begin{aligned}
\sum_{m=-\infty}^{\infty}h[m]e^{j\omega_k(n-m)}
&=e^{j\omega_kn}\sum_mh[m]e^{-j\omega_km}\\
&=H(e^{j\omega_k})e^{j\omega_kn}.
\end{aligned}
$$

它通过系统后频率不变，只乘一个复数增益。再把输入用逆 DFS 展开：

$$
\widetilde x[n]=\frac1N\sum_{k=0}^{N-1}\widetilde X[k]e^{j\omega_kn}.
$$

利用线性逐项通过系统，得到

$$
\boxed{
\widetilde y[n]=\frac1N\sum_{k=0}^{N-1}
H(e^{j2\pi k/N})\widetilde X[k]e^{j2\pi kn/N}.
}
$$

等价地，在本讲义 W 约定下：

$$
\boxed{
\widetilde y[n]=\frac1N\sum_{k=0}^{N-1}
H(W_N^{-k})\widetilde X[k]W_N^{-kn}.
}
$$

### 方法二：从卷积直接代入，适合卷面证明

$$
\begin{aligned}
\widetilde y[n]
&=\sum_mh[m]\widetilde x[n-m]\\
&=\sum_mh[m]\frac1N\sum_{k=0}^{N-1}
\widetilde X[k]e^{j\omega_k(n-m)}\\
&=\frac1N\sum_{k=0}^{N-1}\widetilde X[k]e^{j\omega_kn}
\underbrace{\sum_mh[m]e^{-j\omega_km}}_{H(e^{j\omega_k})}.
\end{aligned}
$$

即得上式。这里一个和为有限和；在上述收敛条件下交换求和成立。

### 本题还应读出的两个结论

$$
\boxed{\widetilde Y[k]=H(e^{j2\pi k/N})\widetilde X[k].}
$$

1. 每根离散谱线单独乘以系统在该频率的响应。
2. 输出仍以 N 为一个周期，但**基波周期可能缩短**，例如系统滤掉部分谱线，或输出恒为零。

### 用一拍延迟检查正负号

取 $h[n]=\delta[n-1]$，则 $H(z)=z^{-1}$，输入 $e^{j\omega_kn}$ 应输出 $e^{-j\omega_k}e^{j\omega_kn}$。

- 正确代入 $H(e^{j\omega_k})=e^{-j\omega_k}$，得到延迟。
- 若误代入 $H(e^{-j\omega_k})$，则得到 $e^{j\omega_k}$，变成超前。

例如 $N=4$、$\widetilde x[n]=\sin(\pi n/2)$ 时，一拍延迟的实际输出为 $-\cos(\pi n/2)$。若按题面误代，算出的却是 $+\cos(\pi n/2)$。取 $n=0$ 就能直接看出差别。

## 四、3.11：证明实圆周偶/奇序列的 DFT 对称性

### 题目

证明：若 N 点实序列满足 $x[n]=x[N-n]$，则 $X[k]$ 为实且偶对称；若满足 $x[n]=-x[N-n]$，则 $X[k]$ 为纯虚且奇对称。

这里 $N-n$ 必须按模 N 理解，即 $x[(N-n)_N]$，特别是 $n=0$ 时对应自己。

### 第一步：由实序列得到共轭对称

由于 $x[n]\in\mathbb R$，

$$
\begin{aligned}
X^*[k]
&=\sum_{n=0}^{N-1}x[n]e^{j2\pi kn/N}\\
&=X[(-k)_N].
\end{aligned}
$$

因此

$$
\boxed{X[(-k)_N]=X^*[k].}
$$

“实序列”只保证共轭对称，本身不保证频谱全实。

### 第二步：圆周反折带来频域反折

令 $v[n]=x[(-n)_N]$，对其做 DFT，并换元 $m=(-n)_N$。n 遍历一个周期时 m 也恰好遍历一个周期：

$$
\begin{aligned}
V[k]
&=\sum_{n=0}^{N-1}x[(-n)_N]e^{-j2\pi kn/N}\\
&=\sum_{m=0}^{N-1}x[m]e^{j2\pi km/N}\\
&=X[(-k)_N].
\end{aligned}
$$

### 第三步：分别合并偶、奇条件

**实圆周偶序列**满足 $v[n]=x[n]$，故

$$
X[(-k)_N]=X[k].
$$

再与共轭对称结合：

$$
X[k]=X[(-k)_N]=X^*[k].
$$

因此

$$
\boxed{X[k]\in\mathbb R,\qquad X[k]=X[(-k)_N].}
$$

**实圆周奇序列**满足 $v[n]=-x[n]$，故

$$
X[(-k)_N]=-X[k].
$$

与共轭对称结合：

$$
X^*[k]=-X[k].
$$

这表示实部为零，因此

$$
\boxed{X[k]\in j\mathbb R,\qquad X[k]=-X[(-k)_N].}
$$

这里“纯虚”允许数值为零。

### 用三角函数再理解一遍

$$
X[k]=\sum_nx[n]\cos\frac{2\pi kn}{N}
-j\sum_nx[n]\sin\frac{2\pi kn}{N}.
$$

圆周偶 x 与奇正弦相乘后，配对相消，虚部为零；圆周奇 x 与偶余弦相乘后配对相消，实部为零。这是上面代数证明的直观解释。

### 固定点不可漏

圆周奇序列在反折后仍落回自己的位置必须为零：

$$
x[0]=0;\qquad N\text{ 为偶数时， }x[N/2]=0.
$$

频域同理，奇频谱满足 $X[0]=0$，偶数 N 时 $X[N/2]=0$。

### 四点例子

$$
\{2,1,0,1\}\overset{\mathrm{DFT}_4}{\longleftrightarrow}\{4,2,0,2\},
$$

是实圆周偶到实圆周偶；

$$
\{0,1,0,-1\}\overset{\mathrm{DFT}_4}{\longleftrightarrow}\{0,-2j,0,2j\},
$$

是实圆周奇到纯虚圆周奇。

反过来，普通左右对称数组 $\{1,2,2,1\}$ 的 DFT 是 $\{6,-1-j,0,-1+j\}$，并不全实。因为它关于 $n=(N-1)/2$ 对称，不是关于圆周原点对称。

**大题记忆线**：实 → 共轭对称；圆周偶/奇 → 频域偶/奇；两条件合并 → 全实/纯虚。

## 五、3.14：时域插零后做 rN 点 DFT

### 题目

已知 N 点有限长序列 $x[n]$ 的 N 点 DFT 为 $X[k]$。每两点之间插入 $r-1$ 个零，按 rN 点表示新序列

$$
y[n]=\begin{cases}
x[n/r],&n=rm,\ m=0,1,\ldots,N-1,\\
0,&\text{其他},
\end{cases}
$$

求其 **rN 点 DFT** 与 X 的关系。r 为正整数；最后一组后的零也计入 rN 点数组。

### 完整推导

$$
\begin{aligned}
Y[k]
&=\sum_{n=0}^{rN-1}y[n]e^{-j2\pi kn/(rN)}\\
&=\sum_{m=0}^{N-1}x[m]e^{-j2\pi k(rm)/(rN)}\\
&=\sum_{m=0}^{N-1}x[m]e^{-j2\pi km/N}.
\end{aligned}
$$

这是原 N 点 DFT 的表达式，但新 k 取 $0,1,\ldots,rN-1$。原表达式对 k 以 N 为周期，所以

$$
\boxed{Y[k]=X[(k)_N],\qquad 0\le k\le rN-1.}
$$

即把原 N 个 DFT 值**完整重复 r 遍**，无额外 r 或 1/r 系数。

### 小例子

N=3，r=2，若 $x=\{1,2,3\}$，则

$$
y=\{1,0,2,0,3,0\},
$$

其 6 点 DFT 为

$$
Y=\{X[0],X[1],X[2],X[0],X[1],X[2]\}.
$$

### 与“尾部补零”务必分开

| 操作 | 新时域样本 | rN 点 DFT 的含义 |
|---|---|---|
| 点间插零，本题 | 原样本改放到 rm | $Y[k]=X[(k)_N]$，旧 DFT 重复 r 遍 |
| 尾部补零 | 原样本仍放在 m | 对同一个原 DTFT 更密采样；仅 $Y[rk]=X[k]$ 保证对应 |

第一章 1.4（4）给出连续频率关系 $Y(e^{j\omega})=X(e^{jr\omega})$；把 $\omega$ 取为 $2\pi k/(rN)$，也立即得到本题结果。

**大题记忆线**：新 DFT 定义 → 只保留 $n=rm$ → 约去 r → 标明新 k 范围与模 N 周期。

## 六、3.25：用一次 N 点 FFT 求单位圆 N 个样值

### 题目

x 为 M 点有限长序列，$0\le n\le M-1$，其 z 变换为

$$
X(z)=\sum_{n=0}^{M-1}x[n]z^{-n}.
$$

要求在

$$
z_k=e^{j2\pi k/N},\qquad k=0,1,\ldots,N-1
$$

处的全部样值。分别讨论 $N\le M$ 与 $N>M$，说明如何用一次 N 点 FFT 得到。

### 起点：代入单位圆采样点

$$
X(z_k)=\sum_{n=0}^{M-1}x[n]e^{-j2\pi kn/N}.
$$

这与 N 点 DFT 的指数核完全一致，问题只在于原输入有 M 点，而 FFT 需要 N 点。

### （1）N≤M：先按模 N 折叠相加

把原下标写成

$$
n=m+qN,\qquad 0\le m\le N-1.
$$

因为整数 k、q 满足

$$
e^{-j2\pi k(m+qN)/N}=e^{-j2\pi km/N},
$$

所以相隔 N 个样本对每个目标频率格点都有相同的指数因子，可以先相加。

构造 N 点序列

$$
\boxed{
v[m]=\sum_{q\ge0,\ m+qN<M}x[m+qN],\qquad m=0,\ldots,N-1.
}
$$

然后

$$
\begin{aligned}
X(z_k)
&=\sum_{m=0}^{N-1}\left(\sum_{q\ge0,\ m+qN<M}x[m+qN]\right)e^{-j2\pi km/N}\\
&=\sum_{m=0}^{N-1}v[m]e^{-j2\pi km/N}.
\end{aligned}
$$

故

$$
\boxed{X(z_k)=\operatorname{DFT}_N\{v[m]\}[k].}
$$

对 v 做一次 N 点 FFT 即得到全部指定样值。$N=M$ 时每组只有一个样本，折叠退化为直接使用原序列。

### 数值例子：M=7，N=4

取 $x=\{1,2,3,4,5,6,7\}$，按余数分组：

| 新下标 m | 合并的原样本 | v[m] |
|---|---|---|
| 0 | x[0]+x[4] | 6 |
| 1 | x[1]+x[5] | 8 |
| 2 | x[2]+x[6] | 10 |
| 3 | x[3] | 4 |

所以只需对 $v=\{6,8,10,4\}$ 做 4 点 FFT，得到

$$
\{28,-4-4j,4,-4+4j\}.
$$

这些正是原七点序列的 z 变换在四个指定单位圆点上的样值。若直接截取 $\{1,2,3,4\}$ 去做 FFT，连 DC 都会从正确的 28 变成 10。

![3.25：原样本按模 N 折叠成 FFT 输入](assets/3-25_按模折叠.png)

### （2）N>M：尾部补零到 N 点

构造

$$
v[m]=\begin{cases}
x[m],&0\le m\le M-1,\\
0,&M\le m\le N-1.
\end{cases}
$$

于是

$$
\boxed{\operatorname{DFT}_N\{v\}[k]
=\sum_{m=0}^{M-1}x[m]e^{-j2\pi km/N}=X(z_k).}
$$

做一次 N 点 FFT 即可。

### 两种情况的统一表达

若把有限支撑外的 x 都视为零，则都可写为

$$
\boxed{v[m]=\sum_{q\in\mathbb Z}x[m+qN],\quad0\le m<N.}
$$

N≥M 时不会把不同的非零样本叠在一起；N<M 时同一余数类的样本可能叠加，称为时域混叠。

**这里时域混叠不妨碍求出指定频率样值**：题目要的是 N 个 $X(z_k)$，不是要求用这 N 个数唯一恢复原来的 M 个样本。恢复目标与求值目标必须分清。

### FFT 点数不能随意换

题目指定 N 个等距采样点，就需要相应的 N 点 DFT。不能为了使用基二算法，随意把 N 换成下一个 2 的幂并声称频率格点不变。N 不是 2 的幂时，数学上的 N 点 DFT 仍然成立，可使用适用点数的 FFT 方法。

**大题记忆线**：代 $z_k$ → 比较 M、N → 长则按模 N 相加，短则尾部补零 → 一次 N 点 FFT。

## 七、五题总对照：不要把“零插到哪里”记混

| 题目 | 时域操作 | 频域结果 |
|---|---|---|
| 3.1 | 同一 N 周期序列，用 2N 点表示一个周期 | 新 DFS 奇数格点为零，偶数格点为旧系数的 2 倍 |
| 3.14 | 每个原样本后插 r−1 个零 | 新 rN 点 DFT 是旧 N 点 DFT 的 r 次重复 |
| 3.25，N>M | 样本位置不变，只在尾部补零 | 同一个原 DTFT 上的 N 个频率采样 |
| 3.25，N<M | 下标同余的原样本相加 | 得到原 z 变换在 N 个指定单位圆点的值 |

## 八、本章闭卷检查

1. 3.1 中不看书推到 $1+(-1)^k$，说明为何有因子 2。
2. 3.8 写出卷积、逆 DFS 展开，指出内层求和就是频率响应，并用一拍延迟查正负号。
3. 3.11 写出“共轭对称 + 圆周偶/奇”的两条等式，再合并结论。
4. 3.14 令 $n=rm$，说明为何不是旧 DFT 末尾补零。
5. 3.25 给一个 M>N 且 M 不是 N 整倍数的例子，正确合并最后不足一组的样本。
