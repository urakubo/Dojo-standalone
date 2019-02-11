# 適用事例

### 2次元DNNによるミトコンドリアのセグメンテーション
UNI-EMを用いて行うセグメンテーションの一例として、2次元DNNによるミトコンドリアのセグメンテーションを行います。

1. 下の Example2DNN.zip をダウンロードして展開してください。dataフォルダの中身をUNI-EMフォルダ（[UNI-EM]）中のdataフォルダに置いてください。"_2DNN_training_images" にトレーニング画像、"_2DNN_ground_truth" に教師セグメンテーションが入っています（図）。教師セグメンテーションの作成にはVast liteの使用をお勧めします ( https://software.rc.fas.harvard.edu/lichtman/vast/ )。近いうちにDojoでも作成できるようにする予定です。

2. UNI-EMを起動してください。

3. UNI-EM上端のドロップダウンメニューより Segmentation → 2DNN を選択して、2D DNNダイアログを起動してください。
	- Training タブを選択してください。
	- 最上段のImage Folder 右列の "Browse..."をクリックしてトレーニング画像が存在すること、Segmentation Folder 右列の "Browse..."をクリックして教師セグメンテーション画像が存在することを確認してください。また Checkpoint Folder ("[UNI-EM]/data/_2DNN_model_tensorflow") が存在することを確認してください。
	- ミトコンドリアのセグメンテーションにはResnetが最適であるため（参考１）、中段 Generator タブにて resnet を選択し、 N res blocks を 16 に設定します。
	- 必要であれば、右列下段の "Save Parameters" をクリックしてパラメータを保存してください。"Load Parameters" をクリックすると保存したパラメータを呼び出すことができます。

4. Training タブ最下段の Execute をクリックして、トレーニングを開始してください。コンソールに起動に関するメッセージが現れたのち、プログレスメッセージが現れます（下）。トレーニング時間はNIVIDA GTX1070 GPUを搭載したPCで6分程度でした。"saving model"と表示されたら、Trainingは終了です。トレーニング期間中、Segmentation → Tensorboard を選択して、"[UNI-EM]/data/_2DNN_model_tensorflow" フォルダを指定すると、トレーニングの進捗をグラフ表示することができます。 
```2D DNN Training
        progress  epoch 49  step 1  image/sec 5.2  remaining 6m
        discrim_loss 0.49639216
        gen_loss_GAN 0.41848987
        gen_loss_classic 0.13485438
        recording summary
        progress  epoch 99  step 1  image/sec 5.5  remaining 5m
        discrim_loss 0.69121116
        gen_loss_GAN 0.73412275
        gen_loss_classic 0.13613938
        ...
        ...
        progress  epoch 1999  step 1  image/sec 7.3  remaining 0m
        discrim_loss 0.715416
        gen_loss_GAN 2.1579466
        gen_loss_classic 0.04729831
        saving model
```
5. 2D DNNダイアログのInferenceタブを選択してください。
	- 最上段のImage Folder右列の "Browse..."をクリックして推論用画像が存在すること、Output Segmentation Folder "[UNI-EM]/data/_2DNN_model_inference" が存在すること、Checkpoint Folder が"[UNI-EM]/data/_2DNN_model_tensorflow" であることを確認してください。
6. Inferenceタブ最下段の Execute をクリックして、Inferenceを開始してください。コンソールに起動に関するメッセージが現れたのち、次の様なプログレスメッセージが現れます。"evaluated image 0099"と表示されたら、Inferenceは終了です。
```2D DNN Inference
        parameter_count = 68334848
        loading all from checkpoint
        evaluated image 0000
        evaluated image 0001
        evaluated image 0002
        ...
        ...
        evaluated image 0097
        evaluated image 0098
        evaluated image 0099
```
7. Output Segmentation Folder "[UNI]/data/_2DNN_model_inference" に推論結果ファイル 0000.png, 0001.png, ..., 0099.png が存在することを確認してください。

続いて、推定結果に対して、二値化およびラベル化による後処理を行います。
8. UNI-EM上端のドロップダウンメニューより Plugins → 2D Filters を選択して、2D Filters ダイアログを起動してください。
	- Training タブを選択してください。

- (参考1) Dr. Torsten Bullmann ミトコンドリアのセグメンテーションのために最適なモデルを探索しています。
	- <https://github.com/tbullmann/imagetranslation-tensorflow>
