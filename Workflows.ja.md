# 適用事例

## 2次元DNNによるミトコンドリアのセグメンテーション
UNI-EMを用いて行うセグメンテーションの一例として、2次元DNNによるミトコンドリアのセグメンテーションを行います。

1. 下の Example2DNN.zip をダウンロードして展開してください。dataフォルダの中身をUNI-EMフォルダ（[UNI-EM]）中のdataフォルダに置いてください。"[UNI-EM]/data/_2DNN_training_images" にトレーニング画像、"[UNI-EM]/data/_2DNN_ground_truth" に教師セグメンテーションが入っています（図）。教師セグメンテーションの作成にはVast liteの使用をお勧めします ( https://software.rc.fas.harvard.edu/lichtman/vast/ )。近いうちにDojoでも作成できるようにする予定です。

#### ● 教師セグメンテーションに基づいた2次元DNNのトレーニングと推論を行います。

2. UNI-EMを起動してください。

3. UNI-EM上端のドロップダウンメニューより Segmentation → 2DNN を選択して、2D DNNダイアログを起動してください。
	- Training タブを選択してください。
	- Image Folder が"[UNI-EM]/data/_2DNN_training_images" であること、Segmentation Folder が "[UNI-EM]/data/_2DNN_ground_truth"であること、また Checkpoint Folder ("[UNI-EM]/data/_2DNN_model_tensorflow") が存在することを確認してください。
	- ミトコンドリアのセグメンテーションにはResnetが最適であるため（参考１）、中段 Generator タブにて resnet を選択し、 N res blocks を 16 に設定します。
	- 必要であれば、右列下段の "Save Parameters" をクリックしてパラメータを保存してください。"Load Parameters" をクリックすると保存したパラメータを呼び出すことができます。

4. Training タブ最下段の Execute をクリックして、トレーニングを開始してください。コンソールに起動に関するメッセージが現れたのち、プログレスメッセージが現れます（下）。トレーニング時間はNIVIDA GTX1070 GPUを搭載したPCで6分程度です。"saving model"と表示されたら、Trainingは終了です。トレーニング期間中、Segmentation → Tensorboard を選択して、"[UNI-EM]/data/_2DNN_model_tensorflow" フォルダを指定すると、トレーニングの進捗をグラフ表示することができます。 
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
	- 最上段のImage Folder が "[UNI-EM]/data/_2DNN_test_images" であること、Output Segmentation Folder "[UNI-EM]/data/_2DNN_inference" であること、Checkpoint Folder が"[UNI-EM]/data/_2DNN_model_tensorflow" であることを確認してください。

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
7. Output Segmentation Folder "[UNI]/data/_2DNN_inference" に推論結果ファイル 0000.png, 0001.png, ..., 0099.png が保存されていることを確認してください。

#### ● 推定結果に対して、二値化およびラベル化による後処理を行います。

8. UNI-EM上端のドロップダウンメニューより Plugins → 2D Filters を選択して、2D Filters ダイアログを起動してください。
	- Binary (二値化) タブを選択してください。
	- Target Folder が "[UNI-EM]/data/_2DNN_inference" であることを確認してください。
	- Output Folder が "[UNI-EM]/data/_2DNN_segmentation" であることを確認してください。
	- Target X, Target Y, Target Z を動かすと Target Folder内画像のサムネイルが Target image に表示されます。"Obtain sample output"ボタンをクリックすると、二値化結果が表示されます。

9. Binary タブ最下段の Execute をクリックして、二値化を行ってください。コンソールに次の様なプログレスメッセージが現れます。
```2D Binarization
        Target Folder:  [UNI-EM]/data/_2DNN_inference
        Output Folder:  [UNI-EM]/data/_2DNN_segmentation
        No: 0
        No: 1
        ...
        ...
        No: 98
        No: 99
        Binary was executed!
```

#### ● 後処理した推論セグメンテーションのプルーフリード、視覚化、アノテーションを行います。

10. UNI-EM上端のドロップダウンメニューより Dojo → Import EM Stack/Segmentation を選択して、Import Images & Segments ダイアログを起動してください。
	- Source Image Folder を ## "[UNI-EM]/data/_2DNN_" ## に設定してください。
	- Source Segmentation Folder を ## "[UNI-EM]/data/_2DNN_segmentation2" ## に設定してください。
	- Destination Dojo Folder を分かりやすい場所に指定してください。フォルダ中にDojo形式でファイルが保存されます。

11. Import Images & Segments ダイアログ最下段の OK をクリックして、Dojoファイルの生成を行ってください。
```3D Labeling
        Target Folder:  [UNI-EM]/data/_2DNN_segmentation
        Output Folder:  [UNI-EM]/data/_2DNN_segmentation2
        Loading images ...
        Saving images ...
        Label was executed!
```



- (参考1) Dr. Torsten Bullmann ミトコンドリアのセグメンテーションのために最適なモデルを探索しました。
	- <https://github.com/tbullmann/imagetranslation-tensorflow>
