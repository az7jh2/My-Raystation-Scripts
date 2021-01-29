# Copy Beamset

## 功能

将当前选中的射束集复制到指定的CT序列上

## 限制

* 只适用于3D-CRT和SMLC计划，只适用于光子线计划
* 射野未考虑楔形板和挡块、Bolus

## 原理

* 脚本新建一个计划（命名为Copiedplan），并在指定CT上新建一个射束集（命名为Copied），复制原射束集的加速器、模式（光子或电子）、患者位置（如HFS）、治疗分次，其中治疗技术手动指定为‘Conformal’。
*  在Copied射束集中不断新建射野，每一个射野对应原来射束集中某射野的一个子野，即复制该射野的能量、中心点坐标以及子野的MU数（通过射野MU*子野权重计算得到，并四舍五入到小数点后2位）、Jaw位置和所有Leaf位置

## 注意

1. 脚本运行后，手动选择射野角度相同的射野，Merge beams。然后Set default grid并Compute剂量

2. 不论之前计划是3D-CRT还是SMLC，复制后的射束集治疗技术均为‘Conformal’，即BeamSets.PlanGenerationTechnique为Conformal（而不是Imrt），否则无法Merge beams。DeliveryTechnique仍为'SMLC'

3. 计划可以建立在新的CT（如CBCT）上，并计算剂量。在原CT上复制生成的计划，经过对比，SMLC和3D-CRT的Dose Diff为0，只是射野的MU数因舍入误差而略微不同

## 脚本运行方式更新

新增一个在RayStation中运行的文件，其他文件改为pyc格式（编译与平台有关，Ironpython 2.7.1编译不成功）
路径定义在该文件中

## 测试

GUI测试通过，脚本测试通过
运行脚本时偶尔会出现RayStation崩溃的现象
同一CT上的beamset复制，SMLC测试通过，剂量无差异
不同CT上的beamset复制，SMLC测试，与RayStation的compute on additional sets相比，在外轮廓边缘处存在一些剂量微小差异
产生该差异的原因很有可能是dose grid的变化

## 注意

在载入某个计划下，运行脚本会出现RayStation崩溃的现象