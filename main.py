import pyxel
from  random import randint



class App:
    # 属性の設定
    def __init__(self):
        pyxel.init(160, 120)
 
        pyxel.load("assets/my_resource.pyxres")
 
        # STARTFLAG
        self.START = False
 
        # GAMEOVERフラグ
        self.GAMEOVER = False
 
        # スコア用変数
        self.score = 0
 
        # プレイヤー初期位置
        self.player_x = 10
        self.player_y = 60
        
        # 重力系変数
        self.gravity = 2.5
        self.MAX_GRAVITY = self.gravity
        self.POWER = 0.25
 
        # ハズレの音符の表示の初期位置の変数
        # 以下の乱数発生は右側の画面外にて、初期位置のみを決定している。
        self.bomb = [(i * 60, randint(0, 104)) for i in range(3,15)]
 
 
        #音再生
        # pyxel.playm(0, loop=True)
 

        # run関数の引数にはフレーム更新処理を行うupdate関数と、描画処理を行うdraw関数を指定します
        pyxel.run(self.update, self.draw)

 


    def update(self):
 
        #終了する
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
 
        #スペース押された場合
        if pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_START):
            self.START = True
 
        if self.GAMEOVER and (pyxel.btn(pyxel.KEY_ENTER)) :
        # if self.GAMEOVER and (pyxel.btn(pyxel.KEY_ENTER or pyxel.btn(pyxel.GAMEPAD1_BUTTON_START))) :
            self.reset()
 
        if not self.START or self.GAMEOVER:
            return
 
        #プレイヤーの更新
        self.update_player()
 
        #ハズレ音符の表示
        for i, v in enumerate(self.bomb):
            self.bomb[i] = self.update_bomb(*v)
 
        # スコア
        if not self.GAMEOVER:
            self.score += 10
 
 

    def draw(self):
        if self.GAMEOVER:
 
            MESSAGE =\
                """
                    GAMEOVER
                    PUSH ENTER RESTART
                """
            pyxel.text(51, 40, MESSAGE, 1)
            pyxel.text(50, 40, MESSAGE, 7)
            return
 
        # 背景表示
        # pyxel.bltm(20, 0, 0, 0, 0, 20, 16, 0)
 
        # 動いていない表示している模様
        # offset = (pyxel.frame_count // 16) % 160
        # for i in range(2):
        #     for x, y in self.note:
        #         pyxel.blt(x + i * 160 , y, 0, 0, 56, 2, 8, 12)
 

        # キャラクタ表示
        if not self.GAMEOVER:
            pyxel.blt(self.player_x, self.player_y, 0, 0, 0, 16, 16, 0)
 


        # ハズレの音符の移動の描画
        for x, y in self.bomb:
            pyxel.blt( # pyxel.blt(x, y, img, u, v, w, h, colkey)
                x, y, # x, y: 画像を描画する座標。
                0, # img: 描画する画像のインデックスまたはファイル名。Pyxelでは画像は16x16ピクセルのタイルとして扱われます。
                30, 33, # u, v: 画像の描画元の座標（左上の座標）。
                16, 20, # w, h: 描画する画像の幅と高さ。
                7 # colkey: カラーキー。指定された色を透明として扱います。
            )
 
 
        # 雲の表示(近く)
        # offset = (pyxel.frame_count // 2) % 160
        # for i in range(2):
        #     for x, y in self.note_2:
        #         pyxel.blt(x + i * 160 - offset, y, 0, 32, 56, 22, 8, 12)
 
        # スコア表示
        s = "SCORE {:>4}".format(self.score)
        pyxel.text(5, 4, s, 1)
        pyxel.text(4, 4, s, 7)
 
        if not self.START:
            MESSAGE ="START=SPACE, STOP=Q"
            pyxel.text(30, 50, MESSAGE, 7)
            return
 

    # プレイヤー更新
    def update_player(self):
        # プレイヤーの更新を行うメソッド
        
        # スペースキーが押されている場合、重力を適用する
        if pyxel.btn(pyxel.KEY_SPACE):
            if self.gravity > -self.MAX_GRAVITY:
                self.gravity = self.gravity - self.POWER
        else:
            # スペースキーが押されていない場合、重力を逆向きに適用する
            if self.gravity < self.MAX_GRAVITY:
                self.gravity = self.gravity + self.POWER
        
        # 重力に応じてプレイヤーのY座標を更新する
        self.player_y = self.player_y + self.gravity 
        
        # プレイヤーのY座標が画面上端より上に行かないようにする
        if self.player_y < 0:
            self.player_y = 0
        
        # プレイヤーのY座標が画面下端より下に行かないようにする
        if self.player_y > pyxel.height - 16:
            self.player_y = pyxel.height - 16

 

    # ハズレの音符の移動
    def update_bomb(self, x, y):

        # ゲームオーバーか否かの判定処理
        # ゲームオーバーの条件に合致する場合
        if abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12: #absは絶対値をとる関数
            self.GAMEOVER = True
            pyxel.blt(x, y, 0, 48, 0, 16, 16, 0) #pyxel.bltは指定された座標に画像を描画するための関数
            pyxel.blt(self.player_x, self.player_y, 0, 16, 0, 16, 16, 0)
            
            pyxel.stop() # 音楽を停止するため

        # こいつのおかげで位置移動している
        x -= 2

        # これ何度も同じインスタンスを表示されているみたいだな
        if x < -40:
            x += 240
            y = randint(0, 104) #指定された範囲内の整数をランダムに生成する関数
 
        return (x, y)
    
 
    # ゲームオーバーになった時の再表示
    def reset(self):
        # STARTFLAG
        self.START = True
 
        # GAMEOVERフラグ
        self.GAMEOVER = False
 
        #スコア用変数
        self.score = 0
 
        #プレイヤー初期地位
        self.player_x = 20
        self.player_y = 60
        
        #重力系変数
        self.gravity = 2.5
        self.MAX_GRAVITY = self.gravity
        self.POWER = 0.25
 
        #爆弾の生成用
        self.bomb = [(i * 60, randint(0, 104)) for i in range(3,15)]
 
        # #遠い雲
        # self.note = [(10, 25), (70, 35), (120, 15), (44, 45), (67, 75), (110, 95)]
 
        # #近い雲
        # self.note_2 = [(20, 15), (40, 75), (110, 40)]
 
        #音再生
        pyxel.playm(0, loop=True)
 
App()