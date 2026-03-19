import torch
from utils.utils_misc import C_to_K

config = {
    # ===== 环境 =====
    "fmu_path": "fmu/MyITMS-dassl01.fmu",
    "fmu_step_size": 1,
    # ===== 设备 & 训练 =====
    "device": "cuda" if torch.cuda.is_available() else "cpu",
    "log_folder": "runs/",
    "num_episodes": 15,
    "episode_iter": 100,
    "buffer_size": 10000,
    "hidden_dim": 1024,
    "num_layers": 6,
    "actor_lr": 1e-4,
    "critic_lr": 1e-3,
    "gamma": 0.95,
    "tau": 1e-2,
    "batch_size": 24,
    "eval_interval": 1,  # 每n个episode
    "save_interval": 1,  # 每n个episode

    # ===== 观测（每个 agent 一个 list）=====
    "obs_dict": [
        [
            "T_cabin_set",
            "cabinVolume.summary.T",
            "driverPerformance.controlBus.driverBus._acc_pedal_travel",
            "driverPerformance.controlBus.driverBus._brake_pedal_travel",
            "driverPerformance.controlBus.vehicleStatus.vehicle_velocity",
        ],
        [
            "superHeatingSensor.outPort",
            "superCoolingSensor.outPort",
            # "battery.controlBus.batteryBus.battery_SOC[1]",
        ],
        [
            "T_bat_set",
            "battery.Batt_top[1].T",
            "T_motor_set",
            "machine.heatCapacitor.T",
        ],
    ],
    # ===== 动作 =====
    "action_dict": [
        ["RPM_blower"],
        ["RPM_comp"],
        ["RPM_batt", "RPM_motor", "V_three", "V_four"],
    ],
    # ===== 动作约束 =====
    "action_bounds": {
        "RPM_blower": [0, 150],
        "RPM_comp": [0, 3000],
        "RPM_batt": [0, 2000],
        "RPM_motor": [0, 2000],
        "V_three": [0, 1],
        "V_four": [0, 1],
    },
    # ===== 动作离散化 =====
    "action_sep_num": {
        "RPM_blower": 16,
        "RPM_comp": 31,
        "RPM_batt": 21,
        "RPM_motor": 21,
        "V_three": 11,
        "V_four": 11,
    },
    "reward_dict": {"TableDC.Pe": "power_compressor",
                    "TableDC1.Pe": "power_battery",
                    "TableDC2.Pe": "power_motor",
                    "TableDC3.Pe": "power_cabin"},

    # ===== 物理设定 =====
    "T_cabin_set": C_to_K(25),
    "T_bat_set": C_to_K(30),
    "T_motor_set": C_to_K(60),

    # ==== 初始化 ====
    "env_reset_dict": {"MY_socinit": [0.1, 1.0, 0.05],
                       "T_Cabin": [C_to_K(20), C_to_K(40), 5],
                       "MY_battT0": [C_to_K(20), C_to_K(40), 5],
                       "MY_motorT0": [C_to_K(40), C_to_K(80), 5],
                       "RPM_blower": 100,
                       "RPM_comp": 1500,
                       "RPM_batt": 1000,
                       "RPM_motor": 1000,
                       "V_three": 1,
                       "V_four": 1,
                       },
    "drivecycle": "WLTC.txt",

    # ===== I2C =====
    "use_i2c": True,
    "lambda_temp": 10.0,
    "i2c_hidden_dim": 256,
    "prior_buffer_size": 100,
    "prior_buffer_percentile": 80,
    "message_feature_dim": 16,
    "i2c_num_layers": 6,
    "prior_lr": 1e-3,
    "prior_train_iter": 3,
    "prior_train_batch_size": 24,
    "prior_update_frequency": 5,
}