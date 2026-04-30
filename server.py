"""
Biostats 完整服务器 - 同时提供前端和API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import numpy as np
import base64
import io
import os

app = FastAPI(title="Biostats API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ 数据模型 ============

class SurvivalRequest(BaseModel):
    time: List[float]
    event: List[int]

class SampleSizeRequest(BaseModel):
    endpoint: str = "continuous"
    alpha: float = 0.05
    power: float = 0.80
    mean1: Optional[float] = None
    mean2: Optional[float] = None
    sd: Optional[float] = None

class TTestRequest(BaseModel):
    group1: List[float]
    group2: List[float]

class MetaAnalysisRequest(BaseModel):
    effects: List[float]
    se: List[float]

class BayesianRequest(BaseModel):
    successes: int
    trials: int
    prior_alpha: float = 1.0
    prior_beta: float = 1.0

# ============ 前端页面 ============

@app.get("/", response_class=HTMLResponse)
async def root():
    html_path = os.path.join(os.path.dirname(__file__), "app.html")
    with open(html_path, "r") as f:
        return f.read()

# ============ API路由 ============

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/api")
async def api_info():
    return {
        "name": "Biostats API",
        "version": "1.0.0",
        "endpoints": [
            "POST /api/survival - 生存分析",
            "POST /api/sample-size - 样本量计算",
            "POST /api/t-test - t检验",
            "POST /api/meta-analysis - Meta分析",
            "POST /api/bayesian - 贝叶斯分析",
            "POST /api/visualize/survival - 生存曲线图"
        ]
    }

@app.post("/api/survival")
async def survival_analysis(req: SurvivalRequest):
    time = np.array(req.time)
    event = np.array(req.event)
    
    order = np.argsort(time)
    time = time[order]
    event = event[order]
    
    n = len(time)
    survival = [1.0]
    times = [0]
    at_risk = n
    events_total = 0
    censored_total = 0
    
    for i in range(n):
        if event[i] == 1:
            s = survival[-1] * (at_risk - 1) / at_risk
            events_total += 1
        else:
            s = survival[-1]
            censored_total += 1
        survival.append(s)
        times.append(time[i])
        at_risk -= 1
    
    median_survival = None
    for i, s in enumerate(survival):
        if s <= 0.5:
            median_survival = times[i]
            break
    
    return {
        "times": times,
        "survival_prob": survival,
        "median_survival": median_survival,
        "events": events_total,
        "censored": censored_total,
        "interpretation": f"共{events_total}个事件，{censored_total}个删失。中位生存时间: {median_survival if median_survival else '未达到'}"
    }

@app.post("/api/sample-size")
async def sample_size(req: SampleSizeRequest):
    from scipy import stats
    
    z_alpha = stats.norm.ppf(1 - req.alpha / 2)
    z_beta = stats.norm.ppf(req.power)
    
    if req.endpoint == "continuous" and req.mean1 and req.mean2 and req.sd:
        effect = abs(req.mean1 - req.mean2) / req.sd
        n = ((z_alpha + z_beta) / effect) ** 2 * 2
        n_per_group = int(np.ceil(n))
        
        return {
            "n_per_group": n_per_group,
            "total_n": n_per_group * 2,
            "power": req.power,
            "alpha": req.alpha,
            "effect_size": effect,
            "interpretation": f"每组需要{n_per_group}人，共{n_per_group * 2}人。检验效能{req.power*100:.0f}%，显著性水平{req.alpha}"
        }
    
    raise HTTPException(400, "请提供正确的参数")

@app.post("/api/t-test")
async def t_test(req: TTestRequest):
    from scipy import stats
    
    g1 = np.array(req.group1)
    g2 = np.array(req.group2)
    
    t_stat, p_value = stats.ttest_ind(g1, g2)
    
    pooled_sd = np.sqrt((np.std(g1, ddof=1)**2 + np.std(g2, ddof=1)**2) / 2)
    cohens_d = (np.mean(g1) - np.mean(g2)) / pooled_sd if pooled_sd > 0 else 0
    
    return {
        "t_statistic": float(t_stat),
        "p_value": float(p_value),
        "significant": bool(p_value < 0.05),
        "effect_size": float(cohens_d),
        "group1_mean": float(np.mean(g1)),
        "group2_mean": float(np.mean(g2)),
        "interpretation": f"t={t_stat:.3f}, p={p_value:.4f}。{'有' if p_value < 0.05 else '无'}统计学差异。效应量Cohen's d={cohens_d:.3f}"
    }

@app.post("/api/meta-analysis")
async def meta_analysis(req: MetaAnalysisRequest):
    effects = np.array(req.effects)
    se = np.array(req.se)
    weights = 1 / (se ** 2)
    
    pooled = np.sum(weights * effects) / np.sum(weights)
    pooled_se = np.sqrt(1 / np.sum(weights))
    
    Q = np.sum(weights * (effects - pooled) ** 2)
    k = len(effects)
    df = k - 1
    I2 = max(0, (Q - df) / Q * 100) if Q > 0 else 0
    
    return {
        "pooled_effect": float(pooled),
        "pooled_se": float(pooled_se),
        "ci_lower": float(pooled - 1.96 * pooled_se),
        "ci_upper": float(pooled + 1.96 * pooled_se),
        "heterogeneity": {"Q": float(Q), "I2": float(I2), "df": df},
        "n_studies": k,
        "interpretation": f"合并效应量={pooled:.3f}，95%CI[{pooled-1.96*pooled_se:.3f}, {pooled+1.96*pooled_se:.3f}]。I²={I2:.1f}%"
    }

@app.post("/api/bayesian")
async def bayesian(req: BayesianRequest):
    from scipy import stats
    
    post_alpha = req.prior_alpha + req.successes
    post_beta = req.prior_beta + (req.trials - req.successes)
    
    posterior = stats.beta(post_alpha, post_beta)
    
    return {
        "posterior_mean": float(posterior.mean()),
        "posterior_sd": float(posterior.std()),
        "credible_lower": float(posterior.ppf(0.025)),
        "credible_upper": float(posterior.ppf(0.975)),
        "prior_mean": float(stats.beta(req.prior_alpha, req.prior_beta).mean()),
        "interpretation": f"后验均值={posterior.mean():.3f}，95%可信区间[{posterior.ppf(0.025):.3f}, {posterior.ppf(0.975):.3f}]"
    }

@app.post("/api/visualize/survival")
async def visualize_survival(req: SurvivalRequest):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    
    time = np.array(req.time)
    event = np.array(req.event)
    
    order = np.argsort(time)
    time = time[order]
    event = event[order]
    
    survival = [1.0]
    times = [0]
    at_risk = len(time)
    
    for i in range(len(time)):
        if event[i] == 1:
            survival.append(survival[-1] * (at_risk - 1) / at_risk)
        else:
            survival.append(survival[-1])
        times.append(time[i])
        at_risk -= 1
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.step(times, survival, where='post', linewidth=2, color='#2196F3')
    ax.fill_between(times, survival, alpha=0.1, color='#2196F3', step='post')
    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Survival Probability', fontsize=12)
    ax.set_title('Kaplan-Meier Survival Curve', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 1.05)
    ax.grid(True, alpha=0.3)
    
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    plt.close(fig)
    
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    return {"image": image_base64, "format": "png"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
