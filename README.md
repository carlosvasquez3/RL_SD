# **Table of Contents**

- [Overview](#overview)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run)
- [Results](#results)
- [License](#license)
- [Citation](#citation)


# **Overview**

This repository implements ε-greedy reinforcement learning algorithms for policy optimization in complex system dynamics models. The research focuses on applying RL techniques to enhance decision-making in:

- Lotka-Volterra predator-prey dynamics  
- World2 global sustainability model

---

# **Project Structure**
RL_SD/
├── src/
│   ├── egreedy_lotkavolterra.py
│   └── egreedy_world2.py
├── report_helpers/
│   ├── plotting.py
│   └── timing.py
├── models/
│   ├── pyworld2/
│   ├── LotkaVolterra.py
│   ├── run_scenarios.py
│   ├── setup.py
│   ├── updated_data.json
│   ├── world2_switch.py
│   └── World2Lab.py
├── results/
├── requirements.txt
└── README.md
---

# **How to Run**

Follow these steps to set up the environment and execute the experiments.

### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/RL_SD.git
cd RL_SD
```

### **2. Create and Activate a Virtual Environment**
It is recommended to use a dedicated virtual environment to avoid dependency conflicts.

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### **3. Install Dependencies**
Install all required packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```

### **4. Run the Reinforcement Learning Experiments**
Execute the training modules directly from the project root:

**Lotka–Volterra model:**
```bash
python -m src.egreedy_lotkavolterra
```

**World2 sustainability model:**
```bash
python -m src.egreedy_world2
```

### **5. View Results**
All experiment outputs will be automatically stored in the `results/` directory. See [Output Files](#output-files) for details.

**Note:** You can modify experiment parameters (learning rate, epsilon decay, episode count, etc.) directly in the scripts inside the `src/` folder to explore different learning behaviors.
...

---

## **Output Files**
Each experiment generates comprehensive results:

---

## **Licence**
This project is licensed under ......... 

---

## **Citation**
If you use this code in your research, please cite:

---
