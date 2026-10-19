# Ajisai Rainbow

雨上がりの紫陽花、海、空にかかる虹を描いたドット絵から色を取った、ターミナル用のカラーテーマ。今は Ghostty 版だけがある。

![色見本](docs/preview.png)

| テーマ | 背景 | 文字 | 用途 |
|---|---|---|---|
| `ajisai-rainbow` | `#0e2a35`（地面の深い青緑） | `#c3f9f0`（雲のミント） | 暗い版 |
| `ajisai-rainbow-light` | `#dcf6f1`（昼の空と雲） | `#12404f`（紺） | 明るい版 |

ANSI の色の割り当て: 赤は虹のピンク、緑は紫陽花の葉、黄は灯りのクリーム色、青は青い紫陽花、マゼンタは紫の紫陽花、シアンは空。

## Ghostty で使う

```sh
mkdir -p ~/.config/ghostty/themes
ln -sf "$PWD"/ghostty/ajisai-rainbow* ~/.config/ghostty/themes/
```

`~/.config/ghostty/config.ghostty` に次の1行を足すと、OS の明暗設定に合わせて切り替わる。

```
theme = light:ajisai-rainbow-light,dark:ajisai-rainbow
```

## 色を直したとき

```sh
python3 tools/contrast.py                      # 背景との対比（WCAG のコントラスト比）を表示
python3 tools/preview.py <等幅フォントのパス> docs/preview.png   # 色見本を描き直す（Pillow が要る）
```

暗い版は文字 12.9、明るい版は 9.9 の対比がある。元の絵は他人の作品の可能性があるため、このリポジトリには入れていない。
