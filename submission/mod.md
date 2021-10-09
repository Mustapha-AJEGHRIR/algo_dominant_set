### Linear problem modelization :



Lets consider the graph $G = (V, W,E)$, $W$ represents the weights of the nodes in $V$.

Lets consider : $N(i) = \left\{ j\in V | \quad (i,j) \in E\right\}$ 
$$
\begin{split}
Minimize & \quad &\sum_i x_i w_i \\
&& x_i + \sum_{j\in N(i)} x_j \ge 1 & \quad & \forall i \in V \\
&& x_i >0  && \forall i \in V 
\end{split}
$$








## Some results :

**Using nx.dominating_set =>**  27k

**Using strict ratio method =>** 31k

**Using probabilistic ratio method with 1s =>** 27k

**Using probabilistic ratio method mixed with nx.dominating_set with 30s =>**  25k

