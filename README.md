# SmartCushion
藉由壓力感測器取得使用者坐姿壓力數據，利用該數據透過 Machine Learning 判別屬於哪一類坐姿並做出提醒。
採用的Maching Learning 分類演算法為 Random Forest，總計 6 種坐姿使用約 1200 組數據訓練。

# Features
1. 坐姿分析(包含正確坐姿，共6種)
2. 錯誤坐姿提醒(坐墊震動 & 喇叭人聲提示)
3. 久坐提醒(坐墊震動 & 喇叭人聲提示)
4. 控制其他物聯網裝置(僅模擬LED開關示意)
5. 接受其他物聯網裝置訊息(已按壓開關模擬洗衣機工作完成訊息)
6. 以Web方式呈現所有資訊供使用者查看
7. 伸展互動遊戲(Web顯示伸展姿勢並根據壓力數據判斷使用者是否確實動作)
