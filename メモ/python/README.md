uvの使い方の参照サイト
https://okumuralab.org/~okumura/python/uv.html


uvを使おう
今は仮想環境は venv 等ではなく uv を使うのが普通になった。

uvのインストール
Homebrewの入ったMac：

brew install uv
更新は brew upgrade

Windows：

winget install --id=astral-sh.uv -e
更新は winget upgrade --all

一般のMac/Linux：

curl -LsSf https://astral.sh/uv/install.sh | sh
更新は uv self update

uvによるPythonのインストール（オプション）
すでにシステムにPythonが入っていればこれは飛ばしてよい。

必要なバージョンを並べる。入るものは公式版と同じバイナリだが、ユーザ権限でインストールされる（sudo は付けない）。

uv python install 3.13 3.14
~/.local/bin をPATHに登録すればこれらが直接使える。コマンド名は python3.13 等。

あるいは uv run --python 3.13 python で ~/.local/bin/python3.13 が起動する。uv run --python 3.13 python --version でバージョン確認。

uv run python だけなら最新のものが起動する。uv python pin 3.13 と打ち込めばカレントディレクトリに .python-version というものができ、そこに 3.13 と書き込まれ、そのディレクトリ以下では uv run python で3.13が起動するようになる。

更新は uv python upgrade 3.13

削除は uv python uninstall 3.13

従来プロジェクトでのuvの利用
cd /path/to/project
# uv python pin 3.13 (必要なら)
uv venv
uv pip install numpy pandas
# あるいは uv pip install -r requirements.txt
uv run python ...
これでパッケージは .venv/lib/python3.13/site-packages 以下にインストールされる。

頭に uv を付けたコマンドを使う限り、環境は自動で見つけてくれるが、uv run を省略したいときは source .venv/bin/activate で環境をアクティベートする。deactivate で元に戻る。

uv pip install --system numpy などとすればシステムのPythonにパッケージをインストールしようとする。Macでpython.orgからインストールしたPythonなら、/Library/Frameworks/Python.framework/ 以下に書き込もうとして失敗する。

パッケージは ~/.cache/uv 以下にキャッシュされ、そこから copy-on-write でクローンされる。もし ~/.cache と作業ディレクトリが別ファイルシステムにあれば、次のような警告を出力するが、無視すればよい：

warning: Failed to clone files; falling back to full copy. This may lead to degraded performance.
         If the cache and target directories are on different filesystems, reflinking may not be supported.
         If this is intentional, set `export UV_LINK_MODE=copy` or use `--link-mode=copy` to suppress this warning.
もし特定のファイルシステムでの作業が多いならば、export UV_CACHE_DIR="/Volumes/SomeDisk/.uv-cache" のようにしてそのファイルシステム上にキャッシュを置くとよい。ついでにツール用ディレクトリも export UV_TOOL_DIR="/Volumes/SomeDisk/.uv-tools" のように同じドライブに設定しておく。

新規プロジェクトでのuvの利用
まずは新しいプロジェクト用のディレクトリを作り、その中に移動する。

mkdir myproj
cd myproj
ここで次のようにしてプロジェクトを初期化する。

uv init
# Pythonのバージョンも指定するなら uv init -p 3.14
# すでにuv initしたならuv python pin 3.14でPythonバージョンが固定される
プロジェクト内には uv.lock というロックファイルができる。これに合わせて仮想環境を同期する。

uv sync
サンプルの main.py を実行してみる。

uv run main.py
# あるいは uv run python main.py
uv run xxx.py は xxx.py をスクリプトとして実行するので、PEP 723 (Inline script metadata) が効く。一方、uv run python xxx.py は、拡張子が .py でなくても使え、python に -m や -c などのオプションを与えることもできる。

必要なパッケージをaddする。ここではグラフを描いてみたいので、matplotlib を入れる。

uv add matplotlib
pyproject.toml、uv.lock が更新されるので、それに合わせて環境を更新する。

uv sync
何かグラフを描いてみよう。例えば

import matplotlib.pyplot as plt

plt.plot([-1, 1])
plt.title("グラフ")
plt.show()
と書き込んだ plot.py を作り、

uv run plot.py
として実験できる。対話的に実行するには ipython か jupyter を入れるか、あるいは最近流行の marimo を使う。marimo はプロジェクトに入れてもよいが、別ツールとして管理するほうがいいかもしれない。それには

uv tool install marimo
# 更新は uv tool upgrade marimo
のようにして別途入れておく。

marimo を使ってグラフを描いてみよう。

uv run --with marimo marimo edit notebook.py
notebook.py というファイルが作られる。ブラウザが開き、Jupyter や Google Colaboratory と似た画面が現れる。セルに先ほどと同じプログラムを書き込み、Shift + Enter すると、グラフが現れるはずである。詳しくは marimo 参照。

ちょっとした計算をどうするか？
uvはプロジェクトを作って運用するのが基本だが、ちょっとした計算はどうするか。uv run --no-project でプロジェクトを作らないという方法もある。あるいは、work や scratch みたいな一般的な名前で普段使いのプロジェクトを一つ作っておいて、依存関係で困らない標準的なパッケージだけを入れておき、その中で上と同じように作業する、という手もある。

奥村 晴彦

Last modified: 2025-12-16 15:59:18 JST