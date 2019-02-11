# Example workflows

## 1. Mitochondria segmentation by use of 2D DNN
Here we try automated mitochondria segmentation by use of a 2-dimentional deep neural network (2D DNN). The target stack of EM images was obtained by Kasthuri et al. ( Cell 162(3):648-61, 2015 ). They used an automatic tape-collecting ultra-microtome system (ATUM) for SEM imaging (ATUM/SEM). This stack was orginally arranged for ISBI 2013 challenge ([SNEMI3D](http://brainiac2.mit.edu/SNEMI3D/)), and we here reuse it. The target brain region is mouse somatosensory cortex, and the EM images are open to public under Open Data Commons Attribution License (ODC-By) v1.0. 

- https://neurodata.io/data/kasthuri15/
- https://opendatacommons.org/licenses/by/1-0/
- http://docs.neurodata.io/kasthuri2015/kasthuri15docs.html

#### Target EM images and ground truth

1. Download the file "Example2DNN.zip" from the link below and unzip it on your UNI-EM installed PC. Copy and paste the unzipped contents to the "data" folder under the UNI-EM ([UNI-EM). Here a training image was stored in "[UNI-EM]/data/_2DNN_training_images", and ground truth segmentation is stored in "[UNI-EM]/data/_2DNN_ground_truth" (**Fig. 1**). We recommend you to make such ground truth segmentation by use of the software Vast lite ( https://software.rc.fas.harvard.edu/lichtman/vast/ ).

<p align="center">
  <img src="https://github.com/urakubo/Dojo-standalone/blob/main0.3/Images/Training_GroundTruth.png" alt="2D DNN Training" width="600">
</p>
<p align="center">
  <font size="5"> <b>Figure 1. Training EM image and mitochondria ground truth segmentation</b> </font>
</p>
<BR>

#### Training and inference by use of 2D DNN

2. Launch the UNI-EM.

3. Select "Segmentation → 2DNN" from the dropdown menu to lauch a dialogue for the training and inference of 2D DNNs (**Fig. 2a**).
	- Select the Training tab (**Fig. 2b**).
	- Confirm that "Image Folder" targets "[UNI-EM]/data/_2DNN_training_images" (**Fig. 2c**), 、Segmentation Folder が "[UNI-EM]/data/_2DNN_ground_truth"であること(**Fig. 2d**)、また Checkpoint Folder ("[UNI-EM]/data/_2DNN_model_tensorflow") が存在することを確認してください(**Fig. 2e**)。
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

<p align="center">
  <img src="https://github.com/urakubo/Dojo-standalone/blob/main0.3/Images/2DNN_Training.png" alt="2D DNN dialog for training" width="600">
</p>
<p align="center">
  <font size="5"> <b>Figure 2. 2D DNN training dialog</b> </font>
</p>
<BR>


#### ● 推論結果の後処理 [二値化およびラベル化]

8. UNI-EM上端のドロップダウンメニューより Plugins → 2D Filters を選択して、2D Filters ダイアログを起動してください(**Fig. 3**)。
	- Binary (二値化) タブを選択してください(**Fig. 3a**)。
	- Target Folder が "[UNI-EM]/data/_2DNN_inference" であることを確認してください(**Fig. 3b**)。
	- Output Folder が "[UNI-EM]/data/_2DNN_segmentation" であることを確認してください(**Fig. 3c**)。
	- Target X, Target Y, Target Z を動かすと Target Folder内画像のサムネイルが Target image に表示されます(**Fig. 3d**)。"Obtain sample output"ボタンをクリックすると、二値化結果が表示されます(**Fig. 3e**)。

9. Binary タブ最下段の Execute をクリックして、二値化を行ってください(**Fig. 3f**)。コンソールに次の様なプログレスメッセージが現れます。
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

<p align="center">
  <img src="https://github.com/urakubo/Dojo-standalone/blob/main0.3/Images/2D_Binary.png" alt="Dialog for binarization" width="600">
</p>
<p align="center">
  <font size="5"> <b>Figure 3. Dialog for binarization</b> </font>
</p>
<BR>

#### ● 推論結果のプルーフリード、視覚化、アノテーション

12. UNI-EM上端のドロップダウンメニューより Dojo → Import EM Stack/Segmentation を選択して、Import Images & Segments ダイアログを起動してください。
	- Source Image Folder を **"[UNI-EM]/data/_2DNN_test_images"** に設定してください。
	- Source Segmentation Folder を **"[UNI-EM]/data/_2DNN_segmentation2"** に設定してください。
	- 分かりやすい場所にフォルダを作成して Destination Dojo Folder に指定してください。フォルダ中にDojo形式でファイルが保存されます。

13. Import Images & Segments ダイアログ最下段の OK をクリックして、Dojoファイルの生成を行ってください。ファイル作成後、Dojo が起動します(**Fig. 4a**)。

14. 下段のSliceバー(**Fig. 4b**)、上段のZoomバー(**Fig. 4c**)、Opacityバー(**Fig. 4d**)を動かしつつ、セグメンテーションの正確さを視覚的に確認してください。 

15. 不正確なセグメンテーションを校正する場合は、ひょうたん形状のAdjustボタンをクリックして(**Fig. 4e**)、Adjustモードにしてください。欠損がある部分に向かってカーソル円(+/-で拡縮)をドラッグすると欠損を埋めることができます。欠損を埋めたのち、Tabボタンを押して変更反映してください。Escボタンを押すとキャンセルになります。また、消しゴムをクリックしたのち(**Fig. 4f**）、余分な部分をドラッグして余分な部分を削ってください。Tabボタンで消去を反映し、Escボタンでキャンセルします。

16. 十分に校正ができたら、セグメンテーションを保存してください。また、UNI-EM上端のドロップダウンメニューより Dojo → Export Segmentation を選択することにより、校正したセグメンテーションファイルをpng/tiff形式で保存することができます。 

17. UNI-EM上端のドロップダウンメニューより Annotator → Open を選択して3D Annotatorを開いてください。セグメンテーションしたミトコンドリアの3次元形状の視覚化・保存、名前づけ（アノテーション）、Markerの設置ができます(**Fig. 4g**)。詳細な使い方は[使い方：3D Annotator](README.ja.md#3D-Annotator)をご覧ください。

<p align="center">
  <img src="https://github.com/urakubo/Dojo-standalone/blob/main0.3/Images/Proof_Annotation.png" alt="Proofreader Dojo and 3D Annotator" width="1000">
</p>
<p align="center">
  <font size="5"> <b>Figure 4. Proofreader Dojo and 3D Annotator</b> </font>
</p>

<BR><BR>

- (参考1) Dr. Torsten Bullmann がミトコンドリアのセグメンテーションのために最適なモデルを探索しています。
	- <https://github.com/tbullmann/imagetranslation-tensorflow>
