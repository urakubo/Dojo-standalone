# 適用事例

### 2次元DNNによるミトコンドリアのセグメンテーション
UNI-EMを用いて行うセグメンテーションの一例として、2次元DNNによるミトコンドリアのセグメンテーションを行います。

1. 下の Example2DNN.zip をダウンロードして展開してください。dataフォルダの中身をUNI-EMフォルダ（[UNI-EM]）中のdataフォルダに置いてください。"_2DNN_training_images" にトレーニング画像、"_2DNN_ground_truth" に教師セグメンテーションが入っています（図）。教師セグメンテーションの作成にはVast liteの使用をお勧めします ( https://software.rc.fas.harvard.edu/lichtman/vast/ )。近いうちにDojoでも作成できるようにする予定です。

2. 続いて、UNI-EMを起動します。コントロールパネル上端のドロップダウンメニューよりSegmentation → 2DNNを選択して、2D DNNダイアログを起動して、Training タブを選択してください。
	- 最上段のImage Folder 右列の "Browse..."をクリックしてトレーニング画像が存在すること、Segmentation Folder 右列の "Browse..."をクリックして教師セグメンテーション画像が存在することを確認してください。また Checkpoint Folder ("[UNI]/data/_2DNN_model_tensorflow") が存在することを確認してください。
	- ミトコンドリアのセグメンテーションにはResnetが最適であるため（#）、中段 Generator タブにて resnet を選択し、 N res blocks を 16 に設定します。
	- 必要であれば、右列下段の "Save Parameters" をクリックして設定したパラメータを保存してください。"Load Parameters" をクリックすることでパラメータを呼び出すことができます。

3. 最下段の Execute をクリックして、トレーニングを開始します。


- (参考2) さらに詳細なマニュアル設定を行ってtrainingを実行したい場合は、Python スクリプトを作成したのち、コントロールパネル上端のプルダウンメニューよりScript → Run Scriptを選択して実行してください（実装中です。書き方も記述します）。およびTorsten Bullmann博士のGithubサイトを参照してください。
	- <https://github.com/tbullmann/imagetranslation-tensorflow>

- (参考3) 浦久保 個人情報サイト。
	- <https://researchmap.jp/urakubo/>
