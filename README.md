# 📊 Biostats — AI驱动的生物统计分析平台

> 为临床试验和生物医学研究提供AI辅助的统计分析。面向生物制药团队，提供严谨的、可发表级的分析结果——快速、准确、可重复。

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-alpha-orange.svg)]()

---

## 🎯 一句话

**Biostats = 临床试验统计分析的AI副驾驶。** 上传数据，自动获得样本量估算、生存分析、Meta分析、贝叶斯推断——全部可发表。

---

## 🧬 核心功能

### 1. 📐 样本量计算
- 两组平行设计样本量估算
- 生存终点样本量（Schoenfeld公式）
- 非劣效/等效性设计
- 检验效能反算
- 适应性设计样本量再估计

### 2. 📈 生存分析
- **Kaplan-Meier** — 生存曲线估计与置信区间
- **Cox比例风险回归** — 多因素风险比估计
- **Log-rank检验** — 两组生存曲线比较
- **竞争风险** — Fine-Gray模型
- **IPCW** — 逆概率删失加权

### 3. 🏥 临床试验设计
- 随机化方案生成（简单/区组/分层/最小化）
- 盲法设计（单盲/双盲/三盲）
- 适应性设计（成组序贯、样本量再估计）
- 篮式试验/伞式试验/平台试验设计
- 中期分析计划

### 4. 🔬 统计推断
- 假设检验（t检验/卡方/Fisher精确/ANOVA）
- 置信区间估计
- 多重比较校正（Bonferroni/Holm/BH-FDR）
- 非参数检验（Wilcoxon/Mann-Whitney/Kruskal-Wallis）
- Bootstrap置信区间

### 5. 📊 Meta分析
- 固定效应模型（Mantel-Haenszel/Inverse Variance）
- 随机效应模型（DerSimonian-Laird/REML）
- 异质性检验（Q统计量/I²/τ²）
- 发表偏倚检测（Funnel plot/Egger检验/Begg检验）
- 亚组分析与Meta回归

### 6. 🧠 贝叶斯分析
- Beta-Binomial共轭分析（二项比例）
- Normal-Normal共轭分析（正态均值）
- 蒙特卡洛模拟
- 贝叶斯临床试验设计
- 贝叶斯适应性随机化

### 7. 📉 数据可视化
- Kaplan-Meier生存曲线（带置信区间）
- 森林图（Meta分析/亚组分析）
- 瀑布图（疗效瀑布图）
- 贝叶斯后验分布图
- 出版级图表（符合期刊要求）

### 8. 📝 报告生成
- CONSORT流程图（RCT报告）
- STROBE清单（观察性研究）
- 自动化统计分析报告
- AI驱动的结果解读（自然语言）
- 可导出HTML/PDF/Word

---

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────────┐
│                  Biostats 平台                    │
├─────────────┬─────────────┬─────────────────────┤
│   CLI 工具   │  Python API  │    Web 界面          │
├─────────────┴─────────────┴─────────────────────┤
│                 核心分析引擎                        │
├──────────┬──────────┬──────────┬────────────────┤
│ 生存分析  │ 试验设计  │ 贝叶斯   │  Meta分析      │
│ (lifelines)│ (scipy) │ (scipy)  │ (statsmodels) │
├──────────┴──────────┴──────────┴────────────────┤
│              数据处理层 (pandas/numpy)             │
├─────────────────────────────────────────────────┤
│              可视化层 (matplotlib/seaborn)         │
├─────────────────────────────────────────────────┤
│              AI解读层 (LLM结果解释)                │
└─────────────────────────────────────────────────┘
```

### 技术栈

| 层级 | 技术 | 用途 |
|------|------|------|
| 语言 | Python 3.10+ | 核心开发语言 |
| 统计 | scipy, statsmodels, lifelines | 统计计算 |
| 数据 | pandas, numpy | 数据处理 |
| 可视化 | matplotlib, seaborn | 图表渲染 |
| 贝叶斯 | PyMC, ArviZ | 贝叶斯建模 |
| 机器学习 | scikit-learn | 辅助建模 |
| CLI | argparse | 命令行工具 |
| 打包 | setuptools, pyproject.toml | 包管理 |

---

## 🚀 快速开始

### 安装

```bash
# 从 PyPI 安装
pip install biostats

# 从源码安装
git clone https://github.com/MoKangMedical/Biostats.git
cd Biostats
pip install -e .
```

### 基本用法

#### 生存分析

```python
from biostats import Survival
import numpy as np

# Kaplan-Meier 生存曲线
time = np.array([3, 6, 9, 12, 15, 18, 21, 24])
event = np.array([1, 0, 1, 1, 0, 1, 1, 0])

km = Survival.kaplan_meier(time, event)
print(km.summary())
# 输出: Kaplan-Meier Analysis Summary:
#   • Total events: 5 | Censored: 3
#   • Median survival: 15.0
#   • 8 subjects analyzed

km.plot()  # 生成生存曲线图
```

#### 样本量计算

```python
from biostats import TrialDesign

# 两组平行设计
design = TrialDesign.two_arm(
    effect_size=0.3,
    alpha=0.05,
    power=0.80
)
print(design.sample_size_per_arm)  # → 176
print(design.summary())
# 输出: Trial Design Summary (Two-arm parallel):
#   • Sample size: 176 per arm (352 total)
#   • Power: 80% | Alpha: 0.050
#   • Effect size: 0.300

# 生存终点样本量
surv_design = TrialDesign.survival(
    hazard_ratio=0.7,
    alpha=0.05,
    power=0.80
)
```

#### 贝叶斯分析

```python
from biostats import Bayesian

# Beta-Binomial 共轭分析
posterior = Bayesian.bernoulli(
    successes=45,
    trials=100,
    prior_beta=(1, 1)  # 无信息先验
)
print(posterior.credible_interval(0.95))
# → (0.353, 0.549)

# 两组比例比较
comparison = Bayesian.compare_rates(
    successes_a=45, trials_a=100,
    successes_b=30, trials_a=100
)
print(f"P(A > B) = {comparison['prob_a_greater']:.1%}")
```

### CLI 使用

```bash
# 生存分析
biostats survival --data trial.csv --time survival_time --event death --group treatment

# 样本量计算
biostats trial --type superiority --alpha 0.05 --power 0.80 --effect-size 0.5

# 快速分析（自动检测数据类型）
biostats quick --data trial.csv

# 启动 Web 界面
biostats serve --port 8501
```

---

## 💼 应用场景

### 临床试验（I-IV期）
- **I期**：剂量递增设计、MTD估计、贝叶斯自适应设计
- **II期**：Simon两阶段设计、单臂/随机化设计
- **III期**：优效/非劣效/等效设计、中期分析、数据监查
- **IV期**：上市后安全性监测、真实世界证据

### 观察性研究
- 队列研究：发病率、累积发病率、生存分析
- 病例对照研究：OR估计、条件Logistic回归
- 横断面研究：患病率、关联分析

### Meta分析
- 干预措施Meta分析（RCT汇总）
- 诊断准确性Meta分析
- 网络Meta分析（间接比较）
- 个体患者数据Meta分析（IPD-MA）

### 真实世界证据（RWE）
- 倾向性评分匹配（PSM）
- 逆概率加权（IPTW）
- 工具变量分析
- 断点回归设计

### 健康经济学
- 成本效果分析（CEA）
- QALY估算
- 预算影响分析
- 马尔可夫模型

---

## 📁 项目结构

```
Biostats/
├── biostats/              # 核心Python包
│   ├── __init__.py        # 包初始化
│   ├── __main__.py        # CLI入口
│   ├── survival.py        # 生存分析模块
│   ├── trial.py           # 临床试验设计模块
│   └── bayesian.py        # 贝叶斯分析模块
├── src/                   # 扩展源码
│   ├── sample_size.py     # 样本量计算（详细版）
│   ├── survival.py        # 生存分析（详细版）
│   ├── meta_analysis.py   # Meta分析模块
│   └── visualization.py   # 数据可视化模块
├── data/                  # 参考数据
│   ├── test-types.json    # 统计检验类型参考
│   └── trial-designs.json # 临床试验设计类型参考
├── examples/              # 使用案例
│   └── clinical-trial.md  # 临床试验分析案例
├── docs/                  # 文档
├── pyproject.toml         # 项目配置
├── setup.py               # 安装脚本
└── README.md              # 本文件
```

---

## 📊 统计检验速查表

| 研究目的 | 数据类型 | 推荐检验 | 模块 |
|---------|---------|---------|------|
| 两组均数比较 | 连续、正态 | 独立t检验 | scipy.stats |
| 两组均数比较 | 连续、非正态 | Mann-Whitney U | scipy.stats |
| 多组均数比较 | 连续、正态 | 单因素ANOVA | scipy.stats |
| 多组均数比较 | 连续、非正态 | Kruskal-Wallis | scipy.stats |
| 两组率比较 | 二分类 | 卡方/Fisher精确 | scipy.stats |
| 生存曲线比较 | 时间-事件 | Log-rank | biostats.survival |
| 多因素生存 | 时间-事件 | Cox回归 | biostats.survival |
| 诊断准确性 | 二分类 | ROC/AUC | sklearn |
| 趋势检验 | 有序分类 | Cochran-Armitage | statsmodels |

详细检验类型参考：[`data/test-types.json`](data/test-types.json)

---

## 🏥 临床试验设计速查表

| 设计类型 | 适用场景 | 样本量方法 | 参考 |
|---------|---------|-----------|------|
| 两组平行 | 优效性检验 | 两样本t检验公式 | Chow et al. |
| 交叉设计 | 自身对照 | 配对设计公式 | Jones & Kenward |
| 非劣效 | 阳性对照 | 非劣效公式 | Julious |
| 适应性设计 | 不确定性大 | 条件效能 | Jennison & Turnbull |
| 篮式试验 | 多瘤种 | Simon两阶段 | Simon |
| 平台试验 | 多方案比较 | 贝叶斯自适应 | Berry et al. |

详细设计类型参考：[`data/trial-designs.json`](data/trial-designs.json)

---

## 🧪 运行测试

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/ -v

# 带覆盖率
pytest tests/ --cov=biostats --cov-report=html

# 代码检查
ruff check biostats/
mypy biostats/
```

---

## 📖 文档

- [完整文档](https://biostats.readthedocs.io) — 在线文档
- [临床试验案例](examples/clinical-trial.md) — 从数据到报告的完整流程
- [API参考](docs/api.md) — 模块接口说明
- [统计方法参考](docs/methods.md) — 算法与公式

---

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解指南。

### 贡献方式
- 🐛 报告Bug
- 💡 提出新功能
- 📝 改进文档
- 🧪 添加测试用例
- 🔧 提交代码修复

---

---

## 🔗 相关项目

| 项目 | 定位 |
|------|------|
| [OPC Platform](https://github.com/MoKangMedical/opcplatform) | 一人公司全链路学习平台 |
| [Digital Sage](https://github.com/MoKangMedical/digital-sage) | 与100位智者对话 |
| [Cloud Memorial](https://github.com/MoKangMedical/cloud-memorial) | AI思念亲人平台 |
| [天眼 Tianyan](https://github.com/MoKangMedical/tianyan) | 市场预测平台 |
| [MediChat-RD](https://github.com/MoKangMedical/medichat-rd) | 罕病诊断平台 |
| [MedRoundTable](https://github.com/MoKangMedical/medroundtable) | 临床科研圆桌会 |
| [DrugMind](https://github.com/MoKangMedical/drugmind) | 药物研发数字孪生 |
| [MediPharma](https://github.com/MoKangMedical/medi-pharma) | AI药物发现平台 |
| [Minder](https://github.com/MoKangMedical/minder) | AI知识管理平台 |
| [Biostats](https://github.com/MoKangMedical/Biostats) | 生物统计分析平台 |

## 📄 许可证

MIT License — 详见 [LICENSE](LICENSE)

---

## 🙏 致谢

- [lifelines](https://lifelines.readthedocs.io/) — 生存分析库
- [scipy](https://scipy.org/) — 科学计算库
- [statsmodels](https://www.statsmodels.org/) — 统计模型库
- [PyMC](https://www.pymc.io/) — 贝叶斯建模库
- [ArviZ](https://python.arviz.org/) — 贝叶斯可视化库

---

## 📬 联系我们

- GitHub: [MoKangMedical/Biostats](https://github.com/MoKangMedical/Biostats)
- Issues: [提交问题](https://github.com/MoKangMedical/Biostats/issues)

---

**Built with ❤️ by MoKangMedical**

*让每一个临床试验都有严谨的统计分析。*
