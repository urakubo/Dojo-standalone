# 適用事例

## 2次元DNNによるミトコンドリアのセグメンテーション
UNI-EMを用いて行うセグメンテーションの一例として、2次元DNNによるミトコンドリアのセグメンテーションを行います。

1. 下の Example2DNN.zip をダウンロードして展開してください。dataフォルダの中身をUNI-EMフォルダ（[UNI-EM]）中のdataフォルダに置いてください。"[UNI-EM]/data/_2DNN_training_images" にトレーニング画像、"[UNI-EM]/data/_2DNN_ground_truth" に教師セグメンテーションが入ります(**Fig. 1**)。教師セグメンテーションの作成にはVast liteの使用をお勧めします ( https://software.rc.fas.harvard.edu/lichtman/vast/ )。近いうちにDojoでも作成できるようにする予定です。

<img style="text-align:center;"><img src="Training_GroundTruth.png" alt="2D DNN Training" width="600"></img>
<figcaption> <font size="5">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  <b>Figure 1. Training image and ground truth segmentation</b> </font> </figcaption>



#### ● 2次元DNNのトレーニングと推論

2. UNI-EMを起動してください。

3. UNI-EM上端のドロップダウンメニューより Segmentation → 2DNN を選択して、2D DNNダイアログを起動してください(**Fig. 2a**)。
	- Training タブを選択してください(**Fig. 2b**)。
	- Image Folder が"[UNI-EM]/data/_2DNN_training_images" であること(**Fig. 2c**)、Segmentation Folder が "[UNI-EM]/data/_2DNN_ground_truth"であること(**Fig. 2d**)、また Checkpoint Folder ("[UNI-EM]/data/_2DNN_model_tensorflow") が存在することを確認してください(**Fig. 2e**)。
	- ミトコンドリアのセグメンテーションにはResnetが最適であるため（参考１）、中段 Generator タブにて resnet を選択し(**Fig. 2f**)、 N res blocks を 16 に設定します(**Fig. 2g**)。
	- 必要であれば、右列下段の "Save Parameters" をクリックしてパラメータを保存してください。"Load Parameters" をクリックすると保存したパラメータを呼び出すことができます。

4. Training タブ最下段の Execute をクリックして、トレーニングを開始してください(**Fig. 2g**)。コンソールに起動に関するメッセージが現れたのち、プログレスメッセージが現れます（下）。トレーニング時間はNIVIDA GTX1070 GPUを搭載したPCで6分程度です。"saving model"と表示されたら、Trainingは終了です。トレーニング期間中、Segmentation → Tensorboard を選択して、"[UNI-EM]/data/_2DNN_model_tensorflow" フォルダを指定すると、トレーニングの進捗をグラフ表示することができます。 
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
5. 2D DNNダイアログのInferenceタブを選択してください(**Fig. 2b**)。
	- 最上段のImage Folder が "[UNI-EM]/data/_2DNN_test_images" であること、Output Segmentation Folder "[UNI-EM]/data/_2DNN_inference" であること、Checkpoint Folder が"[UNI-EM]/data/_2DNN_model_tensorflow" であることを確認してください。

6. Inferenceタブ最下段の Execute をクリックして、推論を開始してください。コンソールに起動に関するメッセージが現れたのち、次の様なプログレスメッセージが現れます。"evaluated image 0099"と表示されたら、Inferenceは終了です。
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

<img style="text-align:center;"><img src="https://github.com/urakubo/Dojo-standalone/blob/main0.3/Images/2DNN_Training.png" alt="2D DNN dialog for training" width="600"></img>
<figcaption> <font size="5">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  <b>Figure 2. 2D DNN Training</b> </font> </figcaption>



#### ● 推論結果の後処理 [二値化およびラベル化]

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

10. UNI-EM上端のドロップダウンメニューより Plugins → 3D Filters を選択して、3D Filters ダイアログを起動してください。
	- Label (ラベルづけ) タブを選択してください。
	- Target Folder を **"[UNI-EM]/data/_2DNN_segmentation"** に設定してください。
	- Output Folder を **"[UNI-EM]/data/_2DNN_segmentation2"** に設定してください。

11. Label タブ最下段の Execute をクリックして、ラベルづけを行ってください。コンソールに次の様なプログレスメッセージが現れます。
```3D Labeling
        Target Folder:  [UNI-EM]/data/_2DNN_segmentation
        Output Folder:  [UNI-EM]/data/_2DNN_segmentation2
        Loading images ...
        Saving images ...
        Label was executed!
```
#### ● 推論結果のプルーフリード、視覚化、アノテーション

12. UNI-EM上端のドロップダウンメニューより Dojo → Import EM Stack/Segmentation を選択して、Import Images & Segments ダイアログを起動してください。
	- Source Image Folder を **"[UNI-EM]/data/_2DNN_test_images"** に設定してください。
	- Source Segmentation Folder を **"[UNI-EM]/data/_2DNN_segmentation2"** に設定してください。
	- 分かりやすい場所に Destination Dojo Folder を作成・指定してください。フォルダ中にDojo形式でファイルが保存されます。

13. Import Images & Segments ダイアログ最下段の OK をクリックして、Dojoファイルの生成を行ってください。ファイル作成後、Dojo が起動します（図1）。

14. 下段のSliceバー、上段のZoomバー、Opacityバーを動かしつつ、セグメンテーションの正確さを視覚的に確認してください。 

15. 不正確なセグメンテーションがある場合は、ひょうたん形状のAdjustボタンをクリックして、欠損がある部分を補強したり、過剰な部分を削ったりするプルーフリード（校正）を行ってください（図）。

16. 十分に校正ができたら、セグメンテーションを保存してください。また、UNI-EM上端のドロップダウンメニューより Dojo → Import Segmentation を選択することにより、校正したセグメンテーションファイルをpng/tiff形式で保存することができます。 

17. UNI-EM上端のドロップダウンメニューより Annotator → Open を選択して3D Annotatorを開いてください。セグメンテーションしたミトコンドリアの3次元形状の視覚化・保存、名前づけ（アノテーション）、Markerの設置ができます（図）。詳細な使い方は[使い方：3D Annotator](#3D-Annotator)をご覧ください。


- (参考1) Dr. Torsten Bullmann がミトコンドリアのセグメンテーションのために最適なモデルを探索しています。
	- <https://github.com/tbullmann/imagetranslation-tensorflow>
