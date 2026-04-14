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
