# 適用事例

### 2次元DNNによるミトコンドリアのセグメンテーション
UNI-EMを用いて行うセグメンテーションの一例として、2次元DNNによるミトコンドリアのセグメンテーションを行います。

1. 下の Example2DNN.zip をダウンロードして展開してください。dataフォルダの中身をUNI-EMフォルダ（[[UNI-EM]]）中のdataフォルダに置いてください。"__2DNN_training_images" にトレーニング画像、"__2DNN_ground_truth" に教師セグメンテーションが入っています（図）。教師セグメンテーションの作成にはVast liteの使用をお勧めします ( https://software.rc.fas.harvard.edu/lichtman/vast/ )。近いうちにDojoで作成可能にする予定です。

2. 続いて、UNI-EMを起動します。コントロールパネル上端のドロップダウンメニューよりSegmentation → 2DNNを選択して、Training, Inferenceの2つのタブを持つダイアログを起動してください。

3. 最上段のImage Folder 右の "Browse..."をクリックしてトレーニング画像が入っていること、Segmentation Folder 右の "Browse..."をクリックして教師セグメンテーションが入っていることを確認します。また Checkpoint Folder ("[[UNI]]") が存在することを確認します。

4. ミトコンドリアのセグメンテーションにはResNetを用いると高い正確さのセグメンテーションを得ることができます。
- (参考1) cuda 9.0, cuDNN v7のインストール方法。
	- <https://qiita.com/spiderx_jp/items/8d863b087507cd4a56b0>
	- <https://qiita.com/kattoyoshi/items/494238793824f25fa489>
	- <https://haitenaipants.hatenablog.com/entry/2018/07/25/002118>

- (参考2) さらに詳細なマニュアル設定を行ってtrainingを実行したい場合は、Python スクリプトを作成したのち、コントロールパネル上端のプルダウンメニューよりScript → Run Scriptを選択して実行してください（実装中です。書き方も記述します）。およびTorsten Bullmann博士のGithubサイトを参照してください。
	- <https://github.com/tbullmann/imagetranslation-tensorflow>

- (参考3) 浦久保 個人情報サイト。
	- <https://researchmap.jp/urakubo/>
