project: 段落修改
## 2. Related Work
### 2.1 Self-Supervised Pretraining in 3D Medical Imaging

现有3D医学图像自监督预训练方法主要依赖掩码重建、对比学习或体积上下文预测任务。**掩码图像建模**方面，MAE~\citep{he2022masked}提出随机掩码自编码器重建策略，成为视觉自监督的奠基性工作；SimMIM~\citep{xie2022simmim}进一步简化了掩码重建流程，无需额外的tokenizer即可实现有效预训练。GMIM~\citep{qi2024gmim}将自适应掩码建模引入3D医学图像，根据解剖结构动态调整掩码策略，提升了重建任务对组织边界的敏感性，但其仍局限于单域（人类CT）预训练，未建立跨物种迁移机制。

**3D医学图像预训练基础模型**方面，MIS-FM~\citep{wang2023mis}利用11万张无标注CT构建通用3D分割基础模型，展示了大规模自监督预训练的强大表征能力，但其预训练目标为通用重建，未显式编码解剖结构先验，且仅在人类数据上验证。Rubik's Cube+~\citep{zhuang2020rubik}将3D jigsaw重组作为自监督任务，通过恢复打乱的三维块空间顺序学习结构布局，与本文的jigsaw预训练任务动机一致；然而其采用CNN backbone，未探索Transformer架构下的jigsaw设计，且同样缺乏跨域迁移的考量。

SwinUNETR~\citep{he2023swinunetr}采用随机掩码图像建模预训练Swin Transformer，在BTCV等人类CT分割基准上表现优异，但其重建目标对组织边界等细粒度语义不敏感，且预训练与下游分割任务存在语义鸿沟。VoCo~\citep{xie2023voco}提出体积上下文预测，通过预测随机采样块的相对位置学习空间布局，然而其预训练目标仅建模局部块的空间关系，未显式编码解剖结构的全局语义。更重要的是，上述方法仅在人类CT上训练，缺乏向动物成像域的知识迁移机制；直接将其微调至猪CT时，因显著的解剖差异（脂肪-肌肉-骨骼分布、器官布局）导致高层语义特征严重偏移。

值得注意的是，Kolesnikov et al.~\citep{kolesnikov2019revisiting}指出，代理任务精度与下游任务性能在跨架构比较中并非正相关，这进一步说明单纯追求预训练任务精度不足以保证分割性能，预训练目标与下游任务的语义对齐更为关键。**跨视图语义对齐**方面，MoCo~\citep{he2020momentum}与SimCLR~\citep{chen2020simple}通过最大化不同增强视图间的一致性学习判别性表示，为对比学习奠定基础；DINO~\citep{caron2021emerging}引入自蒸馏机制实现跨视图语义一致性，其教师-学生架构与动量更新策略与本文的online assignment任务动机高度契合。然而，上述对比学习方法主要针对自然图像设计，未考虑3D医学图像中解剖结构的空间刚性约束，且缺乏向动物域的迁移机制。

**与上述方法不同**，本文以VoCo的人类CT预训练权重为初始化，但不做简单微调。通过设计解剖感知的自监督任务（jigsaw空间重组与跨视图语义对齐），在猪CT数据上重新激活人类结构先验，使预训练目标与下游分割任务在语义层面紧密耦合，从而弥合预训练与分割之间的语义鸿沟。

------

### 2.2 Cross-Domain Transfer for Animal CT Analysis

将人类医学模型迁移至动物CT面临显著的解剖域差距。**域适应方法**方面，对抗性特征对齐是主流策略，PnP-AdaNet~\citep{dou2019pnp}通过插件式对抗网络实现跨模态特征对齐，但需在特征层面对齐复杂解剖流形，计算成本高且需同时访问源域与目标域数据；基于CycleGAN的无监督域适应~\citep{zhu2017unpaired}通过在图像层面进行风格迁移缓解域差距，但可能扭曲解剖结构的几何一致性，且训练过程不稳定。近期，无源域适应方法如ProtoContra-SFDA~\citep{li2023protocontra}通过原型锚定实现特征对齐，无需同时访问双域数据，但其依赖目标域的伪标签质量，在标注极度稀缺的场景下可靠性不足。上述方法的共同局限在于：未充分利用大规模无标注数据中的结构先验，且未建立从人类医学知识到动物解剖的有效迁移通道。

**猪CT表型分析**方面，早期工作主要依赖传统图像处理方法。Gangsei et al.~\citep{gangsei2016atlas}构建了猪CT图谱分割的经典框架，为后续研究奠定了解剖结构参考标准，但其依赖手工标注与规则驱动，难以扩展至大规模数据。Deep learning for pig skeleton segmentation from CT~\citep{matthews2018deep}首次将深度学习引入猪CT分割，验证了CNN在动物骨骼提取中的有效性，但仅针对单一组织类型，未探索多组织联合分割。Automated method to quantify composition of live pigs via CT~\citep{pons2021automated}采用DNN实现猪体成分（肌肉、脂肪、骨骼）的自动定量，与本文的系统目标直接相关，但其依赖大量精细标注进行监督训练，未解决标注瓶颈问题。近期，Deep learning-driven automated carcass segmentation in pigs~\citep{billah2025deep}提出了大规模猪CT深度学习分割方案，在数据充足条件下取得了优异性能，但其方法仍为纯监督学习，对标注量的需求与实际应用场景中的标注稀缺性形成尖锐矛盾。

在猪CT表型分析中，现有工作主要采用监督学习方法~\citep{olsen2017review}，其有效性受限于稀缺的精细标注数据与猪体型的显著变异。据我们所知，**目前尚无工作探索将人类医学CT的大规模自监督预训练知识系统性地迁移至猪CT分割任务**，以同时解决标注稀缺与域差距问题。

**本文首次提出"人类先验引导的自监督迁移"策略**。核心思想是：人类解剖学的结构知识（如器官空间布局规律、组织界面特征）可作为有效的跨物种归纳偏置，通过自监督预训练任务在猪CT数据上重新激活和适配这些先验，而非从头学习或简单复制特征。这既保留了自监督学习对无标注数据的利用能力，又通过人类先验的引入增强了对动物解剖结构的理解。

------

### 2.3 Research Gap and Our Contribution

综合上述分析，现有研究存在以下空白：

1. **机制空白**：MAE、SimMIM、GMIM、VoCo等自监督预训练方法及MIS-FM等基础模型均未设计跨物种知识迁移机制，无法将人类CT预训练模型有效适配至动物域；
2. **任务空白**：现有自监督任务（掩码重建、体积上下文预测、跨视图对比）未显式引入解剖结构先验，导致预训练表示与下游分割任务语义脱节；
3. **应用空白**：猪CT分割领域虽有监督学习方法取得进展，但缺乏利用大规模无标注数据与外部知识迁移的系统性方案，标注瓶颈严重制约了深度学习方法的部署。

针对上述空白，本文贡献如下：

- 提出一种**人类先验引导的自监督预训练框架**，将人类CT预训练模型中的结构知识作为归纳偏置，通过多任务自监督学习在猪CT数据上重新激活和适配这些先验；
- 设计**解剖感知的预训练任务**（jigsaw空间重组与跨视图语义对齐），使预训练目标与下游分割任务在语义层面紧密耦合；
- 在猪CT数据集上验证所提框架在**极少标注条件**下的分割性能，证明跨物种知识迁移的有效性。

------

## 补充文献BibTeX引用键对照表

表格



| 文献                                | 建议BibTeX Key      | 备注                                     |
| :---------------------------------- | :------------------ | :--------------------------------------- |
| He et al., 2022 (MAE)               | `he2022masked`      | CVPR 2022                                |
| Xie et al., 2022 (SimMIM)           | `xie2022simmim`     | CVPR 2022                                |
| Qi et al., 2024 (GMIM)              | `qi2024gmim`        | *Computers in Biology and Medicine*      |
| Wang et al., 2023 (MIS-FM)          | `wang2023mis`       | arXiv:2306.16925                         |
| Zhuang et al., 2020 (Rubik's Cube+) | `zhuang2020rubik`   | arXiv:2007.08826                         |
| He et al., 2020 (MoCo)              | `he2020momentum`    | CVPR 2020                                |
| Chen et al., 2020 (SimCLR)          | `chen2020simple`    | ICML 2020                                |
| Caron et al., 2021 (DINO)           | `caron2021emerging` | ICCV 2021                                |
| Dou et al., 2019 (PnP-AdaNet)       | `dou2019pnp`        | MICCAI 2019                              |
| Zhu et al., 2017 (CycleGAN)         | `zhu2017unpaired`   | ICCV 2017                                |
| Li et al., 2023 (ProtoContra-SFDA)  | `li2023protocontra` | MICCAI 2023                              |
| Gangsei et al., 2016                | `gangsei2016atlas`  | 猪CT图谱                                 |
| Matthews et al., 2018               | `matthews2018deep`  | *Translational Animal Science*           |
| Pons et al., 2021                   | `pons2021automated` | ScienceDirect                            |
| Billah et al., 2025                 | `billah2025deep`    | *Artificial Intelligence in Agriculture* |
| Olsen et al., 2017                  | `olsen2017review`   | 现有引用                                 |

------

## 关键修改总结

表格



| 修改项                              | 处理方式                                 |
| :---------------------------------- | :--------------------------------------- |
| 补充MAE/SimMIM/GMIM                 | 2.1开头，形成"通用→医学"方法演进         |
| 补充MIS-FM                          | 作为"基础模型"代表，与VoCo形成对比       |
| 补充Rubik's Cube+                   | 直接关联本文jigsaw任务动机               |
| 补充MoCo/SimCLR/DINO                | 支撑跨视图语义对齐的方法动机             |
| 补充PnP-AdaNet/CycleGAN/ProtoContra | 为"对抗方法计算成本高"提供具体引用       |
| 补充猪CT具体工作                    | 从传统→深度学习→最新进展，形成应用背景   |
| 修正Kolesnikov引用格式              | 统一为`\citep{kolesnikov2019revisiting}` |
| 统一Gap/Contribution表述            | 三个空白分别对应三个贡献，一一回应       |

需要我帮你进一步调整某个文献的讨论深度，或者生成完整的BibTeX条目吗？

