# Biostats — AI-Powered Biostatistics Platform

> Clinical trial design, survival analysis, and statistical inference powered by AI. Built for biopharma teams who need rigorous, publication-ready results — fast.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 What is Biostats?

Biostats is an open-source biostatistics platform that combines classical statistical methods with AI-powered interpretation. It provides:

- **Survival Analysis** — Kaplan-Meier, Cox PH, competing risks
- **Clinical Trial Design** — Sample size, power analysis, adaptive designs
- **Bayesian Methods** — Posterior estimation, Bayesian adaptive trials
- **AI Interpretation** — Plain-language explanations of statistical results
- **Publication Engine** — Auto-generate publication-ready tables and figures

## 🧠 技术哲学：Harness理论

> **在AI领域，Harness（环境设计）比模型本身更重要。优秀的Harness设计（工具链+信息格式+上下文管理+失败恢复+结果验证）能使性能提升64%。**

Biostats的本质是**生物统计Harness**——不是堆更复杂的统计公式，而是设计好从原始数据到发表级结果的全流程：

- **数据处理Harness**：自动识别数据类型→缺失值处理→异常值检测→格式标准化
- **方法选择Harness**：研究设计识别→统计方法推荐→假设检验匹配→结果解读
- **可视化Harness**：数据特征→图表推荐→发表级渲染→报告自动生成
- **质量验证Harness**：假设检查→多重比较校正→敏感性分析→可重复性保证

**护城河来源**：生物统计的Harness设计，而非统计软件本身。

## 💼 商业哲学：红杉论点

> **下一代万亿美元公司是伪装成服务公司的软件公司。从卖工具到卖结果。**

Biostats不卖统计软件或代码模板——卖的是**科研分析的结果**：研究者上传数据，直接获得可发表的统计分析报告。从卖SPSS/R工具到卖一站式科研统计服务。

## 🧭 理论宪法关联

Biostats遵循莫康医学理论宪法（THEORETICAL_CONSTITUTION.md）四卷八章统一框架：

- **认知论**：鉴别诊断式决策 → 数据驱动的研究假设验证
- **方法论**：Harness理论 → 生物统计Harness（数据处理+方法选择+可视化+质量验证）
- **价值论**：红杉论点 → 卖科研统计结果（不是卖统计工具）
- **价值论**：思想基础设施理论 → Level 4 生物统计基础设施

## 🚀 Quick Start

```bash
pip install biostats

# Survival analysis
from biostats import Survival
km = Survival.kaplan_meier(time=[3,6,9,12], event=[1,0,1,1])
km.plot()
km.summary()  # AI-generated plain-language interpretation

# Sample size calculation
from biostats import TrialDesign
design = TrialDesign.two_arm(
    effect_size=0.3, alpha=0.05, power=0.80
)
print(design.sample_size)  # → 176 per arm

# Bayesian analysis
from biostats import Bayesian
posterior = Bayesian.bernoulli(
    successes=45, trials=100, prior_beta=(1, 1)
)
posterior.credible_interval(0.95)  # → (0.353, 0.549)
```

## 📊 Core Modules

| Module | Description | Status |
|--------|-------------|--------|
| `biostats.survival` | KM, Cox PH, Fine-Gray, IPCW | ✅ Stable |
| `biostats.trial` | Sample size, power, adaptive designs | ✅ Stable |
| `biostats.bayesian` | MCMC, conjugate priors, model comparison | ✅ Stable |
| `biostats.regression` | Linear, logistic, Poisson, mixed models | 🔨 Beta |
| `biostats.meta` | Fixed/random effects meta-analysis | 🔨 Beta |
| `biostats.interpret` | AI-powered result interpretation | ✅ Stable |
| `biostats.publish` | Publication-ready tables & figures | 🔨 Beta |

## 🧬 Use Cases

- **Phase II/III Clinical Trials** — Design, interim analysis, sample size re-estimation
- **Real-World Evidence** — Propensity score matching, IPTW, instrumental variables
- **Meta-Analysis** — Forest plots, heterogeneity assessment, publication bias
- **Health Economics** — Cost-effectiveness analysis, QALY estimation
- **Epidemiology** — Incidence rates, standardized mortality ratios, time-series

## 📖 Documentation

Full documentation: [biostats.readthedocs.io](https://biostats.readthedocs.io)

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

**Built with ❤️ by MoKangMedical**
