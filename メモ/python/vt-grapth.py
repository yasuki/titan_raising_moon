import matplotlib.pyplot as plt
import numpy as np

# ==========================================
# 1. パラメータ定義 (変更可能エリア)
# ==========================================
DISTANCE_KM = 3.0e9       # 地球-土星間距離: 30億 km
SHIP_MASS_TON = 400       # 船体総重量: 400トン
THRUST_KN = 38            # 最大推力: 38 kN
ISP_SEC = 30000           # 比推力: 30,000秒
G0 = 9.80665              # 重力加速度 (m/s^2)

# 単位変換
dist_m = DISTANCE_KM * 1000
mass_kg = SHIP_MASS_TON * 1000
thrust_n = THRUST_KN * 1000
exhaust_velocity = ISP_SEC * G0

# 加速度 (F = ma => a = F/m)
# ※質量一定(定加速度)モデルのため、全パターンでこの値がベースになります
acceleration = thrust_n / mass_kg

# ==========================================
# 2. 計算ロジック
# ==========================================

def simulate_flight(coast_ratio_distance):
    """
    指定された慣性航行距離の割合に基づいてフライトプランを計算する関数
    """
    
    # 距離の配分
    d_coast = dist_m * coast_ratio_distance
    d_active = dist_m - d_coast
    d_acc = d_active / 2.0
    d_dec = d_active / 2.0
    
    # 1. 加速フェーズ
    t_acc = np.sqrt(2 * d_acc / acceleration)
    v_max = acceleration * t_acc
    
    # 2. 慣性航行フェーズ
    if v_max > 0:
        t_coast = d_coast / v_max
    else:
        t_coast = 0
        
    # 3. 減速フェーズ
    t_dec = t_acc
    
    # 総所要時間
    total_time = t_acc + t_coast + t_dec
    
    # 参考データ計算
    delta_v = v_max * 2
    mass_ratio = np.exp(delta_v / exhaust_velocity)
    fuel_fraction = 1 - (1 / mass_ratio)
    
    # グラフ用データ
    t_points = [0, t_acc, t_acc + t_coast, total_time]
    v_points = [0, v_max, v_max, 0]
    
    return {
        "label": f"Coast {int(coast_ratio_distance*100)}%",
        "total_time_days": total_time / (24 * 3600),
        "v_max_kms": v_max / 1000,
        "acceleration": acceleration,     # 加速度
        "g_force": acceleration / G0,     # G
        "fuel_fraction": fuel_fraction,
        "t_data": t_points,
        "v_data": v_points
    }

# シミュレーション実行
patterns = [0.0, 0.5, 0.9]
results = []

# --- テキスト出力（ヘッダー修正） ---
print(f"{'Pattern':<15} | {'Time (Days)':<12} | {'Max Vel (km/s)':<15} | {'Accel (m/s^2)':<15} | {'G-Force':<10}")
print("-" * 85)

for p in patterns:
    res = simulate_flight(p)
    results.append(res)
    # --- テキスト出力（行修正） ---
    print(f"{res['label']:<15} | {res['total_time_days']:<12.1f} | {res['v_max_kms']:<15.1f} | {res['acceleration']:<15.5f} | {res['g_force']:<10.4f} G")

# ==========================================
# 3. V-Tグラフのプロット
# ==========================================

plt.figure(figsize=(10, 6))
colors = ['#ff4b4b', '#4b4bff', '#4bff4b']

for i, res in enumerate(results):
    t_days = [t / (24 * 3600) for t in res['t_data']]
    v_kms = [v / 1000 for v in res['v_data']]
    
    plt.plot(t_days, v_kms, label=f"{res['label']} ({res['total_time_days']:.1f} days)", 
             color=colors[i], linewidth=2, marker='o')

plt.title(f"Flight Plan: Earth to Saturn (Accel: {acceleration:.4f} m/s^2)", fontsize=16)
plt.xlabel("Time (Days)", fontsize=12)
plt.ylabel("Velocity (km/s)", fontsize=12)
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.legend(fontsize=11)
plt.tight_layout()

plt.show()
