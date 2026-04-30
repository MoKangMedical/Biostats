"""
Biostats API - 真正可运行的版本
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import numpy as np
import base64
import io

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
    design: str = "superiority"
    endpoint: str = "continuous"
    alpha: float = 0.05
    power: float = 0.80
    mean1: Optional[float] = None
    mean2: Optional[float] = None
    sd: Optional[float] = None
    p1: Optional[float] = None
    p2: Optional[float] = None
    hazard_ratio: Optional[float] = None

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

# ============ 根路由 ============

@app.get("/")
async def root():
    return {
        "name": "Biostats API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "survival": "/api/survival",
            "sample_size": "/api/sample-size",
            "t_test": "/api/t-test",
            "meta_analysis": "/api/meta-analysis",
            "bayesian": "/api/bayesian",
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

# ============ 生存分析 ============

@app.post("/api/survival")
async def survival_analysis(req: SurvivalRequest):
    """Kaplan-Meier 生存分析"""
    time = np.array(req.time)
    event = np.array(req.event)
    
    # 排序
    order = np.argsort(time)
    time = time[order]
    event = event[order]
    
    # 计算生存曲线
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
    
    # 中位生存时间
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

# ============ 样本量计算 ============

@app.post("/api/sample-size")
async def sample_size(req: SampleSizeRequest):
    """样本量计算"""
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
    
    elif req.endpoint == "binary" and req.p1 and req.p2:
        effect = abs(req.p1 - req.p2)
        p_pool = (req.p1 + req.p2) / 2
        n = ((z_alpha * np.sqrt(2 * p_pool * (1 - p_pool)) + 
              z_beta * np.sqrt(req.p1 * (1 - req.p1) + req.p2 * (1 - req.p2))) / effect) ** 2
        n_per_group = int(np.ceil(n))
        
        return {
            "n_per_group": n_per_group,
            "total_n": n_per_group * 2,
            "power": req.power,
            "alpha": req.alpha,
            "interpretation": f"每组需要{n_per_group}人，共{n_per_group * 2}人"
        }
    
    elif req.endpoint == "survival" and req.hazard_ratio:
        effect = np.log(req.hazard_ratio)
        d = ((z_alpha + z_beta) / effect) ** 2 * 4
        total_n = int(np.ceil(d / 0.5))
        n_per_group = int(np.ceil(total_n / 2))
        
        return {
            "n_per_group": n_per_group,
            "total_n": total_n,
            "power": req.power,
            "alpha": req.alpha,
            "interpretation": f"需要{total_n}个事件，预计总样本量{int(total_n/0.5)}"
        }
    
    raise HTTPException(400, "请提供正确的参数")

# ============ t检验 ============

@app.post("/api/t-test")
async def t_test(req: TTestRequest):
    """两样本t检验"""
    from scipy import stats
    
    g1 = np.array(req.group1)
    g2 = np.array(req.group2)
    
    t_stat, p_value = stats.ttest_ind(g1, g2)
    
    # Cohen's d
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

# ============ Meta分析 ============

@app.post("/api/meta-analysis")
async def meta_analysis(req: MetaAnalysisRequest):
    """Meta分析"""
    effects = np.array(req.effects)
    se = np.array(req.se)
    weights = 1 / (se ** 2)
    
    pooled = np.sum(weights * effects) / np.sum(weights)
    pooled_se = np.sqrt(1 / np.sum(weights))
    
    # Q统计量
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

# ============ 贝叶斯分析 ============

@app.post("/api/bayesian")
async def bayesian(req: BayesianRequest):
    """Beta-Binomial贝叶斯分析"""
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

# ============ 可视化 ============

@app.post("/api/visualize/survival")
async def visualize_survival(req: SurvivalRequest):
    """生成生存曲线图"""
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

# ============ 导出 ============

@app.post("/api/export/csv")
async def export_csv(data: Dict[str, Any]):
    """导出为CSV"""
    import csv
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Parameter", "Value"])
    
    for key, value in data.items():
        writer.writerow([key, value])
    
    content = output.getvalue()
    return {"content": base64.b64encode(content.encode()).decode(), "filename": "results.csv"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
