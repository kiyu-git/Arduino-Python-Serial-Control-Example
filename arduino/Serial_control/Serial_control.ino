void setup() {
  // LED_BUILTINのデジタルピンを出力モードに設定
  pinMode(2, OUTPUT);

  Serial.begin( 9600 );     // シリアル通信を初期化する。通信速度は9600bps

  Serial.println( "Hello Arduino!" );   // 最初に1回だけメッセージを表示する
}
char key;     // 受信データを格納するchar型の変数
void loop() {

  // 受信データがあった時だけ、処理を行う
  if ( Serial.available() ) {       // 受信データがあるか？
    key = Serial.read();            // 1文字だけ読み込む
    Serial.write( key );            // 1文字送信。受信データをそのまま送り返す。

    // keyの文字に応じて、行う処理を切り替える
    switch( key ) {
      // qキーが押された時の処理
      case '0':
        digitalWrite(2, LOW);   // LED点灯(HIGHは電圧を5Vにする)
        break;

      // aキーが押された時の処理
      case '1':
        digitalWrite(2, HIGH);    // LED消灯(LOWは電圧を0Vにする)
        break;

      // 上記以外の場合の処理(何もしない)
      default:   
        break;
    } //switch文の末尾

  } // if文の末尾
} // loop関数の末尾
