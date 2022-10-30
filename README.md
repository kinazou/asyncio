# asyncio
　Pythonの非同期処理の確認(その他)

## Description
* 非同期機能(Asyn.py)  
asyncioを使った非同期処理の実現  
ProducerConsumerデザイン  
基底クラスで抽象化(Taskクラスの派生を作れば簡易利用可能)  
Python v3.6 と v3.9 で実現

* ログ機能(Logger.py)  
コンソール出力とログ出力とその他(統計)出力を住み分け  

* オプション機能(Option.py)

* CSVファイル読み込み機能

## Usage  
　`pyhon3 MainTool.py -qs 5 -ic input.csv -ol output.log -os stat.log`  

* -qs, --maxqueuesize  
最大キューサイズの指定

* -ic, --inputcsv  
入力CSVファイルの指定を想定  

* -ol, --outputlog
出力ログファイルの指定を想定

* -os, --statistics
出力統計ファイルの指定を想定

## Licence
　MIT Licence
