#!/bin/bash

# 作業ディレクトリ取得
setup_dir=$(cd $(dirname $0);pwd)

# カレントディレクトリ変更
cd $setup_dir

# リポジトリ更新
sudo apt-get update

# openjtalkとmecabをインストール
# （openjtaklインストール先: /usr/share/hts-voice/）
# （mecabインストール先: /var/lib/mecab/dic/open-jtalk/naist-jdic/）
sudo apt-get install -y open-jtalk open-jtalk-mecab-naist-jdic hts-voice-nitech-jp-atr503-m001

# 女性音声ファイルダウンロード
wget --no-check-certificate https://sourceforge.net/projects/mmdagent/files/MMDAgent_Example/MMDAgent_Example-1.7/MMDAgent_Example-1.7.zip
# 解凍
unzip MMDAgent_Example-1.7.zip
# 音声ファイルをopnejtalkのインストールディレクトリにコピー
sudo cp -R ./MMDAgent_Example-1.7/Voice/mei /usr/share/hts-voice/

# 後処理（ダウンロードファイル・解凍データ削除）
rm MMDAgent_Example-1.7.zip
rm -r MMDAgent_Example-1.7


