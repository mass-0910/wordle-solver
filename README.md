# Wordle solver

## 使い方

表示されたクエリをWordleに入力してください。  
その後、クエリの結果を以下のような5文字で入力してください。  
- 文字とその位置が正解 → `g`
- 文字が正解、位置は間違い → `y`
- 文字が間違い → `b`  

(例えば、正解がargueでクエリがdreamの場合、結果は`bgyyb`と入力する)

```console
$ python main.py
Wordle solver v0.1
1 query: "other" ? bbbyy
2 query: "resin" ? yybbb
3 query: "dream" ? bgyyb
4 query: "eruca" ? ygyby
5 query: "argue" ? ggggg
success argue 5/6
```

## 事前準備

[Wordle回答リスト](https://github.com/alex1770/wordle/blob/main/wordlist_hidden)を全てコピーし、プロジェクト内に`wordlist.txt`という名前で保存してください。

## 性能テスト
ソルバの性能をテストするためのプログラムです。  
```console
$ python wordletest.py
```