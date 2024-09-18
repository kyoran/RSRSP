# RSRSP - Representative Selection with Rotating-Segmentation Perception

## Bibtex
If this work is helpful for your research, please consider citing the following BibTeX entry.
```
@article{xie2023consensus,
  title={Consensus enhancement for multi-agent systems with rotating-segmentation perception},
  author={Xie, Guangqiang and Xu, Haoran and Li, Yang and Hu, Xianbiao and Wang, Chang-Dong},
  journal={Applied Intelligence},
  volume={53},
  number={5},
  pages={5750--5765},
  year={2023},
  publisher={Springer}
}
```


## Prerequisites


- Python 3.5 (or higher)
- NumPy
- Matplotlib

## Introduction

In the MAS with dynamic topology, each agent has a limited sensing range and only interacts with its perceived neighbors within the sensing range, so as to carry out convergence evolution.
The state of each agent can be described as encompassing position, speed, opinion value, etc.
Then, the MAS’s network topology will dynamically change according to the state change of the agent during the convergence evolution.

In this paper, we follow a simple rationale that there must be redundancy in the communication of the MAS, which calls for an **effective consensus protocol with neighbor selection strategies to enhance consensus of the MAS**. Specifically, this paper proposes **a new distributed consensus framework based on two neighbor selection strategies**, where each agent evolves by only referencing the state of some representative neighbors. The main contributions of this paper are summarized as:

- We provide a novel Representative Selection with Rotating-Segmentation Perception (RSRSP) strategy to select representative neighbors in each sector of perception-based communication region. Specifically, the communication region is segmented into several sectors with optimal rotation angle, then agents select the nearest neighbor in each sector for convergence evolution.
- We design a distributed switching strategy to switch from RSRSP to SAN when the system is fully connected. Specifically, agents adopt RSRSP for the convergence evolution before the system is fully connected. Once the communication topology reaches full connectivity, all agents will switch from RSRSP to traditional SAN synchronously through the proposed distributed synchronization algorithm.
- The stability of the proposed framework is analyzed with the common Lyapunov function under undirected and dynamic communication topology.

Fig. 1 shows the operation process of the RSRSP strategy.
The upper right corner of the figure shows the list of the number of neighbors in each sector and the variance of the list.
When the variance is the smallest, the RSRSP strategy stops rotating.

<div align=center>
    <img src="https://github.com/kyoran/RSRSP/blob/main/gif/diagram.gif" width="50%">
    <br>
    <b>Fig 1. Illustration of the proposed strategy</b>
</div>

To quickly understand the idea of the proposed strategy, we can using the following simple command:
```
python3 run_demo.py
```

Then, we can convert images in /example folder into an animated GIF by using:
```
python3 convert2gif.py
```

## Comparisons

In Fig. 2, <i>120</i> agents are randomly distributed in the square <i>[-4, 4] × [-4, 4]</i>. Fig. 3 and Fig. 4 shows the comparison between the original communication topology and the topology after using RSRSP. 

<div align=center>
    <table border="0">
        <tr>    
            <td align="center" colspan="2"><img src="https://github.com/kyoran/RSRSP/blob/main/compare/init.png" width="50%"/><br><b><i>Fig 2. Init State</i></b></td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kyoran/RSRSP/blob/main/compare/C.png"/><br><b><i>Fig 3. Original Communication Topology</i></b></td>
            <td align="center"><img src="https://github.com/kyoran/RSRSP/blob/main/compare/A.png"/><br><b><i>Fig 4. Communication Topology based on RSRSP</i></b></td>
        </tr>
    </table>
</div>

## Parameter Settings

The initial distribution of the MASs is called $DAS(n,R)$. All agents distribute in a circular region of radius $R$,
and the number of agents that distribute randomly in each sector is the same.
All agents are randomly distributed in $DAS(n,R)$.
The MASs evolve under same initial topology using three strategies (i.e., SAN, Strategy1, Strategy2) respectively.
We evaluate the convergence performance by the number of clusters when the MAS is stable. A smaller cluster number indicates better convergence performance. 
We present some necessary parameter settings used in this paper as follows.

|  Parameter   | Meaning  | Value |
| :-----| :----- | :----- |
| episode_num  | simulation times | 50 |
| n  | agent number | 50 |
| R  | agents initially distribute in a circular region of radius  | 1 |
| circle_center  | agents initially distribute in a circular region centered at circle_center | np.array([0, 0]) |
| r_c  | sensing range (communication range) | 1 |
| alpha  | gaining parameter in the MAS | 1/n |
| done_threshold  | tolerance which measures the convergence | 0.02 |
| delta_rotate  | rotation angle of each rotation | 1 |
| base_vec  | basis vector of X-axis | np.array([1, 0]) |
| base_sector_ranges  | reference angle of the initial 4 sectors | np.array([0, 90, 180, 270])|

*Remark: We can get results faster by reducing the accuracy (i.e., increasing delta_rotate)*
