### Linear problem modelization :



Lets consider the graph $G = (V, W,E)$, $W$ represents the weights of the nodes in $V$.

Lets consider : $N(i) = \left\{ j\in V | \quad (i,j) \in E\right\}$ 
$$
\begin{split}
Minimize & \quad &\sum_i x_i w_i \\
&& x_i + \sum_{j\in N(i)} x_j \ge 1 & \quad & \forall i \in V \\
&& x_i \ge0  && \forall i \in V 
\end{split}
$$








## Some results :

**Using nx.dominating_set =>**  27k

**Using strict ratio method =>** 31k

**Using probabilistic ratio method with 1s =>** 27k

**Using probabilistic ratio method mixed with nx.dominating_set with 30s =>**  25k





**Using LP with prob for 100 sec =>** 19k







### Best with default cbc 4 threads:



```
**********  For :  graph_100_100
Min weight = 1052.0      1       Real weight = 1052
Total time = 0.31s
**********  For :  graph_100_1000
Min weight = 201.0       1       Real weight = 201
Total time = 2.37s
**********  For :  graph_100_250
Min weight = 632.0       1       Real weight = 632
Total time = 1.22s
**********  For :  graph_100_500
Min weight = 347.0       1       Real weight = 347
Total time = 1.33s
**********  For :  graph_250_1000
Min weight = 1057.0      1       Real weight = 1057
Total time = 98.61s
**********  For :  graph_250_250
Min weight = 2575.0      1       Real weight = 2575
Total time = 0.18s
**********  For :  graph_250_500
Min weight = 1731.0      1       Real weight = 1731
Total time = 2.13s
**********  For :  graph_500_1000
Min weight = 3631.0      1       Real weight = 3631
Total time = 53.07s
**********  For :  graph_500_500
Min weight = 5320.0      1       Real weight = 5320
Total time = 0.21s
**********  For :  graph_50_1000
Min weight = 40.0        1       Real weight = 40
Total time = 0.23s
**********  For :  graph_50_250
Min weight = 163.0       1       Real weight = 163
Total time = 0.45s
**********  For :  graph_50_50
Min weight = 526.0       1       Real weight = 526
Total time = 0.14s
**********  For :  graph_50_500
Min weight = 86.0        1       Real weight = 86
Total time = 0.32s
Sum of weights =  17361
Total time : 160.88719487190247 s
```

