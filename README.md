## spring_block_simulator とは
東京工業大学の1年次の選択、宇宙地球科学基礎ラボ（地球物理） という授業のレポート用に作成したプログラムです。

ばねとブロックを交互に繋いだものを片側から引っ張っていって、そのブロックが動いたときに開放するエネルギー（地震）を出力します。

単位はJです。

## 使い方

Windows PCでの使用方法です。Linuxも同じように実行できます。Mac OSについては知りません。

1. お使いのコンピューターのお好きな場所に `sbsim.py` と `sbsim_config.csv` をダウンロードしてください。

2. `sbsim_config.csv` の中身をさせたいシミュレーションに応じて書き換えてください。順番は変えてはいけません。

`how_many_springs` ...ばねの数

`block_mass` ...ブロックの質量[kg]

`block_length` ...ブロックの長さ[m]

`spring_length` ...ばねの長さ[m]

`gravity` ...重力加速度[ms^{-2}]

`spring_const` ...ばね定数[kgs^{-2}]

`static_friction` ...静止摩擦係数

`dynamic_friction` ...動摩擦係数

`quake_howmany` ...地震を起こす回数

`pull_1st_block_range` ...先頭ばね（計算の簡略化のため先頭ばねの先端にブロックをつけている）を動かす単位長さ[m]

`quake_sim_dt` ...おもりが動く様子をシミュレーションする単位時間[s]

3. コマンドプロンプトを開き、先ほどのファイルの場所に `cd` コマンドで移動してください。

4. `python sbsim.py` でpythonのコードを実行します。 `sbsim_energy_output.csv` に地震のエネルギーが出力されます。
