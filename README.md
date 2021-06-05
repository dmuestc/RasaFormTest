# 查分小机器人

# 脚本     
sh action.sh 启动Action Server 

sh train.sh 是训练NLU和CORE 

sh run.sh 是启动rasa shell启动交互 

## 运行步骤
1. 安装rasa 1.10.12和rasa X 0.32: https://rasa.com/docs/rasa/user-guide/installation/  
2. 训练模型:

``rasa train --data data/stories.md data/nlu.md -c config.yml -d domain.yml --out models/``

3. 打开一个终端，启动Action Server:

``rasa run actions --actions dialog.actions.actions --port 5055``

4. 运行rasa x 和机器人交互:

``rasa x``
