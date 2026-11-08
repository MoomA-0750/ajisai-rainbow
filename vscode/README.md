# Ajisai Rainbow for VS Code

雨上がりの紫陽花と海、空にかかる虹を描いたドット絵から色を取った配色テーマ。暗い版と明るい版がある。

A color theme taken from a pixel-art scene of hydrangeas after the rain, the sea, and a rainbow — dark and light variants.

| テーマ | 背景 | 文字 |
|---|---|---|
| Ajisai Rainbow | `#0e2a35`（地面の深い青緑） | `#c3f9f0`（雲のミント） |
| Ajisai Rainbow Light | `#c9f7ed`（昼の空と雲） | `#12404f`（紺） |

- 予約語は紫の紫陽花、文字列は葉の緑、関数は青い紫陽花、型は空の色。
- 括弧の色分けは、絵の虹の3本（藤色・ミント・空色）。
- 統合ターミナルの16色は、同じリポジトリの Ghostty のテーマと同じ。
- 絵に赤と黄がないので、誤りはピンク、数と定数はクリーム色にした。

色の出典: 1041uuu さんのドット絵（<https://www.tumblr.com/1041uuu/122075241013>）。このテーマは色を参考にしただけで、絵そのものは含まない。

## 使い方

拡張機能のビューで「Ajisai Rainbow」を探して入れ、コマンドパレットの「Preferences: Color Theme」で選ぶ。Windows・macOS・Linux のデスクトップ版のほか、ブラウザ版（vscode.dev・github.dev）でも使える。

OS の明暗に合わせて切り替えるには、設定に次を書く。

```json
"window.autoDetectColorScheme": true,
"workbench.preferredDarkColorTheme": "Ajisai Rainbow",
"workbench.preferredLightColorTheme": "Ajisai Rainbow Light"
```

ソースと、Ghostty・Starship・lsd 用の同じ配色: <https://github.com/MoomA-0750/ajisai-rainbow>
