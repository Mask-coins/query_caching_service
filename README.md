# 簡単な使い方
query を入れると response が返ってくるサービスを使う時に，一度発した query はローカルに置いて何度も同じ query を出したくない……という場合に使います．

```
from query_caching_service.access import URLAccess
u = URLAccess()
res = u.run("https://github.com/Mask-coins")
print(res)
```


# データの保存場所
指定が何もなければ、コードの実行場所と同じところに保存されます．
ファイル名は "クラス名".db です．
なので，継承した場合は，別のファイルに保存されます．

ファイルの置き場所を変えたい場合は，set_directoryを呼び出して下さい．

# アクセス方法を独自定義したい
Accsessクラスを継承して，access()メソッドを定義して下さい．


例：
```
class URLAccess(Access):
    def access(self,query, encoding=None):
        with request.urlopen(query) as fp:
            if encoding:
                return fp.read().decode(encoding)
            res = fp.read()
            enc = chardet.detect(res)
            response = res.decode(enc['encoding'])
            return response
```

# query や response が str じゃない
内部的にはqueryやresponseはstr前提にしていますが，継承して以下4つの関数をオーバーライドし、文字列とquery, response の変換を行えば，独自のデータ型も扱えます。
```
    @classmethod
    def query2str(cls, key:Any) -> str:
        return key

    @classmethod
    def str2query(cls, key:str) -> Any:
        return key

    @classmethod
    def response2str(cls, value:Any) -> str:
        return value

    @classmethod
    def str2response(cls, value:str) -> Any:
        return value
```


