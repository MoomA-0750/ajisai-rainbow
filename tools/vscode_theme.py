#!/usr/bin/env python3
"""Ghostty のテーマの色から VS Code の配色テーマ（暗い版・明るい版）を作る。

    python3 tools/vscode_theme.py

ghostty/ajisai-rainbow と ghostty/ajisai-rainbow-light を読み、
vscode/themes/ に JSON を書き出す。色を直すときは Ghostty のほうを直してから実行する。
"""
import json
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def read_ghostty(name):
    text = open(os.path.join(ROOT, "ghostty", name), encoding="utf-8").read()
    colors = dict(re.findall(r"^([a-z-]+) = (#[0-9a-fA-F]{6})", text, re.M))
    colors.update({int(i): c for i, c in re.findall(r"^palette = (\d+)=(#[0-9a-fA-F]{6})", text, re.M)})
    return colors


def mix(a, b, t):
    """a と b を t（0〜1、b の割合）で混ぜる"""
    pa = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    pb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(pa, pb))


def alpha(color, a):
    return f"{color}{round(a * 255):02x}"


def build(name, label, kind):
    g = read_ghostty(name)
    p = g  # 0〜15 の番号で引ける
    bg, fg = g["background"], g["foreground"]
    dark = kind == "dark"

    if dark:
        # 地面の深い青緑を基準に、外側ほど暗くする
        side = mix(bg, "#000000", 0.25)
        outer = mix(bg, "#000000", 0.45)
        raised = p[0]                 # 一段明るい面（行の強調・入力欄）
        border = mix(bg, p[8], 0.35)
        accent = g["cursor-color"]    # 空色
        accent_text = bg
        dim = p[8]                    # 控えめな文字
        comment = p[8]
        prop = p[14]                  # プロパティ: 虹の空色
        punct = mix(mix(fg, bg, 0.45), "#808080", 0.35)  # 記号: 色味を抜いて目立たせない
        number = "#f2b8a2"            # 数と定数: 絵にない暖色（Omarchy のテーマの orange と同じ）
    else:
        # 昼の空と雲を基準に、外側ほど少し濃くする
        side = mix(bg, p[6], 0.08)
        outer = mix(bg, p[6], 0.16)
        raised = mix(bg, "#ffffff", 0.45)
        border = mix(bg, p[8], 0.30)
        accent = p[6]                 # 濃い青緑（明るい背景で読める濃さ）
        accent_text = "#ffffff"
        dim = p[8]
        comment = mix(p[8], bg, 0.15)
        prop = "#0f7f8c"              # プロパティ: 空の青緑
        punct = mix(mix(fg, bg, 0.3), "#606060", 0.55)
        number = "#a8552f"

    # エディターの背景: 暗い版は Ghostty と同じ。明るい版は、よく使われる明るいテーマ（背景の彩度 0〜4）に
    # 寄せて薄いミントにする（真っ白にすると周りとの落差が大きいので、Solarized Light ほどの彩度を残す）
    ed = bg if dark else mix(bg, "#ffffff", 0.4)
    # 入力欄（検索・チャットなど）: 明るい版は周りのミントとエディターの間の色にして、白く浮かないようにする
    field = raised if dark else mix(ed, mix(bg, p[6], 0.08), 0.45)
    sel = g["selection-background"]
    red, green, yellow, blue, magenta, cyan = (p[i] for i in (1, 2, 3, 4, 5, 6))
    b_red, b_green, b_yellow, b_blue, b_magenta, b_cyan = (p[i] for i in (9, 10, 11, 12, 13, 14))
    # 括弧の色分け: 絵の虹の3本（藤色・ミント・空色）。紫が目立たないよう藤色は灰色寄りにする
    rainbow = ("#bec3e8", "#8de7d0", "#6cd5f4") if dark else ("#6c6aa0", "#2a8a6c", "#2a82b4")

    colors = {
        # 全体
        "foreground": fg,
        "descriptionForeground": dim,
        "disabledForeground": alpha(dim, 0.7),
        "errorForeground": red,
        "focusBorder": alpha(accent, 0.8),
        "contrastBorder": "#00000000",
        "selection.background": alpha(sel, 0.9),
        "icon.foreground": fg,
        "widget.shadow": alpha("#000000", 0.35 if dark else 0.12),
        "sash.hoverBorder": accent,
        "textLink.foreground": blue if not dark else b_blue,
        "textLink.activeForeground": accent,
        "textPreformat.foreground": cyan if not dark else b_cyan,
        "textBlockQuote.background": side,
        "textBlockQuote.border": accent,
        "textCodeBlock.background": side,
        "textSeparator.foreground": border,
        "progressBar.background": accent,

        # 窓の枠とタイトル
        "titleBar.activeBackground": outer,
        "titleBar.activeForeground": fg,
        "titleBar.inactiveBackground": outer,
        "titleBar.inactiveForeground": dim,
        "titleBar.border": border,
        "menu.background": side,
        "menu.foreground": fg,
        "menu.selectionBackground": sel,
        "menu.selectionForeground": g["selection-foreground"],
        "menu.separatorBackground": border,
        "menu.border": border,
        "commandCenter.background": side,
        "commandCenter.border": border,
        "commandCenter.activeBackground": raised,

        # アクティビティバー（左端）
        "activityBar.background": outer,
        "activityBar.foreground": accent,
        "activityBar.inactiveForeground": dim,
        "activityBar.border": border,
        "activityBar.activeBorder": accent,
        "activityBarBadge.background": accent,
        "activityBarBadge.foreground": accent_text,

        # サイドバー
        "sideBar.background": side,
        "sideBar.foreground": fg,
        "sideBar.border": border,
        "sideBarTitle.foreground": fg,
        "sideBarSectionHeader.background": side,
        "sideBarSectionHeader.foreground": fg,
        "sideBarSectionHeader.border": border,

        # 一覧と木
        "list.activeSelectionBackground": sel,
        "list.activeSelectionForeground": g["selection-foreground"],
        "list.inactiveSelectionBackground": alpha(sel, 0.6),
        "list.inactiveSelectionForeground": fg,
        "list.hoverBackground": alpha(raised, 0.7),
        "list.hoverForeground": fg,
        "list.focusOutline": alpha(accent, 0.6),
        "list.highlightForeground": accent,
        "list.errorForeground": red,
        "list.warningForeground": yellow,
        "tree.indentGuidesStroke": border,

        # タブ
        "editorGroupHeader.tabsBackground": side,
        "editorGroupHeader.tabsBorder": border,
        "editorGroup.border": border,
        "tab.activeBackground": ed,
        "tab.activeForeground": fg,
        "tab.activeBorderTop": accent,
        "tab.inactiveBackground": side,
        "tab.inactiveForeground": dim,
        "tab.border": border,
        "tab.hoverBackground": ed,
        "tab.unfocusedActiveBorderTop": alpha(accent, 0.4),
        "breadcrumb.foreground": dim,
        "breadcrumb.focusForeground": fg,
        "breadcrumb.activeSelectionForeground": accent,

        # エディター
        "editor.background": ed,
        "editor.foreground": fg,
        "editorCursor.foreground": g["cursor-color"],
        "editorLineNumber.foreground": alpha(dim, 0.8),
        "editorLineNumber.activeForeground": fg,
        "editor.lineHighlightBackground": alpha(raised, 0.6) if dark else mix(ed, p[6], 0.06),
        "editor.lineHighlightBorder": "#00000000",
        "editor.selectionBackground": alpha(sel, 0.85),
        "editor.inactiveSelectionBackground": alpha(sel, 0.45),
        "editor.selectionHighlightBackground": alpha(sel, 0.4),
        "editor.wordHighlightBackground": alpha(sel, 0.4),
        "editor.wordHighlightStrongBackground": alpha(sel, 0.6),
        "editor.findMatchBackground": alpha(yellow, 0.45),
        "editor.findMatchHighlightBackground": alpha(yellow, 0.22),
        "editor.findRangeHighlightBackground": alpha(sel, 0.3),
        "editor.rangeHighlightBackground": alpha(sel, 0.25),
        "editorBracketMatch.background": alpha(accent, 0.18),
        "editorBracketMatch.border": alpha(accent, 0.6),
        "editorIndentGuide.background1": alpha(border, 0.7),
        "editorIndentGuide.activeBackground1": dim,
        "editorWhitespace.foreground": alpha(dim, 0.4),
        "editorRuler.foreground": border,
        "editorLink.activeForeground": accent,
        "editorCodeLens.foreground": dim,
        "editorInlayHint.foreground": dim,
        "editorInlayHint.background": alpha(raised, 0.6),
        "editorGutter.background": ed,
        "editorGutter.addedBackground": green,
        "editorGutter.modifiedBackground": blue,
        "editorGutter.deletedBackground": red,
        "editorError.foreground": red,
        "editorWarning.foreground": yellow,
        "editorInfo.foreground": blue,
        "editorHint.foreground": cyan,
        "editorOverviewRuler.border": "#00000000",
        "editorOverviewRuler.errorForeground": red,
        "editorOverviewRuler.warningForeground": yellow,
        "editorOverviewRuler.addedForeground": green,
        "editorOverviewRuler.modifiedForeground": blue,
        "editorOverviewRuler.deletedForeground": red,
        "editorOverviewRuler.findMatchForeground": yellow,

        # 括弧の色分け: 絵の虹（藤色・ミント・空色）と紫陽花の青
        "editorBracketHighlight.foreground1": rainbow[0],
        "editorBracketHighlight.foreground2": rainbow[1],
        "editorBracketHighlight.foreground3": rainbow[2],
        "editorBracketHighlight.foreground4": cyan,
        "editorBracketHighlight.foreground5": rainbow[0],
        "editorBracketHighlight.foreground6": rainbow[1],
        "editorBracketHighlight.unexpectedBracket.foreground": red,

        # 小窓（候補・ホバー・検索）
        "editorWidget.background": side,
        "editorWidget.foreground": fg,
        "editorWidget.border": border,
        "editorSuggestWidget.background": side,
        "editorSuggestWidget.border": border,
        "editorSuggestWidget.selectedBackground": sel,
        "editorSuggestWidget.highlightForeground": accent,
        "editorHoverWidget.background": side,
        "editorHoverWidget.border": border,
        "quickInput.background": side,
        "quickInput.foreground": fg,
        "quickInputList.focusBackground": sel,
        "pickerGroup.foreground": accent,
        "pickerGroup.border": border,
        "peekView.border": accent,
        "peekViewEditor.background": side,
        "peekViewResult.background": outer,
        "peekViewTitle.background": outer,

        # 入力欄・ボタン・ドロップダウン
        "input.background": field,
        "input.foreground": fg,
        "input.border": border,
        "input.placeholderForeground": alpha(dim, 0.9),
        "inputOption.activeBorder": accent,
        "inputOption.activeBackground": alpha(accent, 0.2),
        "inputValidation.errorBorder": red,
        "inputValidation.errorBackground": side,
        "inputValidation.warningBorder": yellow,
        "inputValidation.warningBackground": side,
        "inputValidation.infoBorder": blue,
        "inputValidation.infoBackground": side,
        # チャット（Copilot など）の入力欄と吹き出し
        "agentsChatInput.background": field,
        "agentsChatInput.foreground": fg,
        "agentsChatInput.border": border,
        "agentsChatInput.focusBorder": accent,
        "agentsChatInput.placeholderForeground": alpha(dim, 0.9),
        "chat.requestBubbleBackground": alpha(accent, 0.14),
        "chat.requestBubbleHoverBackground": alpha(accent, 0.2),
        "inlineChat.background": side,
        "inlineChat.border": border,
        "dropdown.background": field,
        "dropdown.foreground": fg,
        "dropdown.border": border,
        "button.background": accent,
        "button.foreground": accent_text,
        "button.hoverBackground": mix(accent, "#ffffff" if dark else "#000000", 0.15),
        "button.secondaryBackground": raised,
        "button.secondaryForeground": fg,
        "checkbox.background": field,
        "checkbox.border": border,
        "badge.background": accent,
        "badge.foreground": accent_text,
        "scrollbarSlider.background": alpha(dim, 0.25),
        "scrollbarSlider.hoverBackground": alpha(dim, 0.4),
        "scrollbarSlider.activeBackground": alpha(accent, 0.5),

        # 下のパネルとステータスバー
        "panel.background": side,
        "panel.border": border,
        "panelTitle.activeForeground": fg,
        "panelTitle.activeBorder": accent,
        "panelTitle.inactiveForeground": dim,
        "statusBar.background": outer,
        "statusBar.foreground": fg,
        "statusBar.border": border,
        "statusBar.noFolderBackground": outer,
        "statusBar.debuggingBackground": magenta,
        "statusBar.debuggingForeground": accent_text if not dark else bg,
        "statusBarItem.remoteBackground": accent,
        "statusBarItem.remoteForeground": accent_text,
        "statusBarItem.hoverBackground": alpha(raised, 0.8),
        "statusBarItem.errorBackground": red,
        "statusBarItem.errorForeground": bg if dark else "#ffffff",
        "statusBarItem.warningBackground": yellow,
        "statusBarItem.warningForeground": bg if dark else "#ffffff",
        "notifications.background": side,
        "notifications.border": border,
        "notificationCenterHeader.background": outer,
        "notificationLink.foreground": accent,

        # git
        "gitDecoration.addedResourceForeground": green,
        "gitDecoration.untrackedResourceForeground": green,
        "gitDecoration.modifiedResourceForeground": blue if not dark else b_blue,
        "gitDecoration.deletedResourceForeground": red,
        "gitDecoration.renamedResourceForeground": cyan,
        "gitDecoration.conflictingResourceForeground": yellow,
        "gitDecoration.ignoredResourceForeground": dim,
        "diffEditor.insertedTextBackground": alpha(green, 0.18),
        "diffEditor.removedTextBackground": alpha(red, 0.18),
        "diffEditor.insertedLineBackground": alpha(green, 0.10),
        "diffEditor.removedLineBackground": alpha(red, 0.10),
        "merge.currentHeaderBackground": alpha(green, 0.4),
        "merge.incomingHeaderBackground": alpha(blue, 0.4),

        # ミニマップ
        "minimap.selectionHighlight": alpha(sel, 0.8),
        "minimap.findMatchHighlight": alpha(yellow, 0.6),
        "minimapGutter.addedBackground": green,
        "minimapGutter.modifiedBackground": blue,
        "minimapGutter.deletedBackground": red,

        # 統合ターミナル: Ghostty と同じ 16 色
        "terminal.background": side,
        "terminal.foreground": fg,
        "terminalCursor.foreground": g["cursor-color"],
        "terminal.selectionBackground": alpha(sel, 0.85),
    }
    names = ["Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White"]
    for i, n in enumerate(names):
        colors[f"terminal.ansi{n}"] = p[i]
        colors[f"terminal.ansiBright{n}"] = p[i + 8]

    # 文法の色は、絵の色の割合に合わせて、コードの中で多く出る役目ほど絵で多い色にする。
    #   絵: 空と雲のミント 58%、海 7%、葉 16%（深緑 10%・中間 4%・鮮やか 3%）、地面の紺 6%、
    #       紫陽花の青 4.5%、紫陽花の紫 1.4%、赤・黄はなし
    #   コード（コメントを除く文字数）: 変数 28%、文字列 22%、関数 12%、予約語 12%、記号 11%、
    #       プロパティ 7%、型 5%、数と定数 2%
    # 変数＝文字の色（暗い版は雲のミント、明るい版は地面の紺）、文字列＝鮮やかな葉、予約語＝深緑、
    # プロパティ＝中間の葉、型＝海、関数＝紫陽花の青。紫陽花の紫は数と定数・正規表現だけの差し色にし、
    # 赤と黄は文法には使わない（誤りと警告の表示だけ）。引数は文字の色の斜体、記号は色味を抜く
    def t(scope, color, style=None):
        s = {"foreground": color}
        if style:
            s["fontStyle"] = style
        return {"scope": scope, "settings": s}

    if dark:
        string = "#9ade7c"    # 鮮やかな葉（地面の上で映えるよう黄緑に寄せる）
        # 予約語と記号は、実際の画面で測った色の差が最も大きくなる色を探して決めた
        keyword = "#60c096"   # 葉の緑（暗い背景で読める明るさ）
        prop = fg             # プロパティは変数と同じ色（明るい版と同じ考え方）
        typ = "#67d3ef"       # 海
        func = "#7aa8ff"      # 青い紫陽花
        number = "#c79bff"    # 紫の紫陽花（差し色）
        regex = "#e3a6ff"     # 淡い紫の紫陽花
        punct = "#939d9d"     # 電柱や犬の灰色
    else:
        # 明るい版は、ミントの背景でも見分けられるよう彩度を上げる（よく使われる明るいテーマの
        # 文字の彩度は平均 47〜70）。文字列の緑は背景のミントと色相を離すため黄緑に寄せる
        string = "#5c7700"    # 鮮やかな葉（予約語の緑と離すため黄緑に寄せる）
        # 予約語・型は、変数の紺・関数の青・文字列の緑から色の差が最も大きくなる色を探して決めた。
        # 明るい背景で読める濃さの青緑は彩度が出せない（色域の限界）ので、緑と青で鮮やかさを出す
        keyword = "#157d42"   # 深緑の葉（色相を緑に寄せて彩度を上げる）
        prop = fg             # プロパティは変数と同じ色（寒色を詰め込みすぎると見分けられないため）
        typ = "#0974a5"       # 海
        func = "#2b55c9"      # 青い紫陽花
        number = "#7a4fe0"    # 紫の紫陽花（差し色）
        regex = "#a23fc0"     # 赤みの紫陽花
        comment = "#668a91"
        punct = "#5a6e72"     # 電柱や犬の灰青緑
    token_colors = [
        t(["comment", "punctuation.definition.comment", "string.comment"], comment, "italic"),
        t(["keyword", "storage.type", "storage.modifier", "keyword.control", "keyword.operator.new",
           "keyword.operator.expression", "keyword.operator.logical.python", "variable.language.this",
           "variable.language.self", "variable.language.super"], keyword),
        t(["keyword.operator", "punctuation", "meta.brace", "punctuation.separator", "punctuation.terminator"], punct),
        t(["string", "string.quoted", "string.template", "markup.inline.raw"], string),
        t(["string.regexp", "constant.character.escape", "constant.other.placeholder"], regex),
        t(["constant.numeric", "constant.language", "constant.language.boolean", "support.constant",
           "variable.other.constant", "variable.other.enummember"], number),
        t(["entity.name.function", "support.function", "meta.function-call entity.name.function",
           "variable.function"], func),
        t(["entity.name.type", "entity.name.class", "entity.name.namespace", "support.type", "support.class",
           "entity.other.inherited-class", "storage.type.primitive", "entity.name.type.interface"], typ),
        t(["variable", "variable.other.readwrite", "meta.definition.variable"], fg),
        t(["variable.parameter", "meta.parameter"], fg, "italic"),
        t(["variable.other.property", "variable.other.object.property", "support.variable.property",
           "meta.object-literal.key", "entity.name.tag.yaml", "support.type.property-name"], prop),
        t(["entity.name.tag", "punctuation.definition.tag"], func),
        t(["entity.other.attribute-name"], prop, "italic"),
        t(["entity.name.decorator", "meta.decorator", "punctuation.decorator", "entity.name.function.decorator"], cyan),
        t(["support.type.property-name.css", "support.type.vendored.property-name.css"], prop),
        t(["keyword.other.unit", "constant.numeric.css"], number),
        t(["entity.other.attribute-name.class.css", "entity.other.attribute-name.id.css"], typ),
        t(["markup.heading", "entity.name.section"], keyword, "bold"),
        t(["markup.bold"], fg, "bold"),
        t(["markup.italic"], fg, "italic"),
        t(["markup.underline.link", "string.other.link"], func, "underline"),
        t(["markup.quote"], dim, "italic"),
        t(["markup.list punctuation.definition.list"], accent),
        t(["markup.inserted"], green),
        t(["markup.deleted"], red),
        t(["markup.changed"], func),
        t(["invalid", "invalid.illegal"], red, "underline"),
        t(["invalid.deprecated"], yellow, "strikethrough"),
    ]

    semantic = {
        "namespace": typ,
        "class": typ,
        "interface": typ,
        "enum": typ,
        "type": typ,
        "typeParameter": {"foreground": typ, "italic": True},
        "function": func,
        "method": func,
        "decorator": cyan,
        "macro": cyan,
        "parameter": {"foreground": fg, "italic": True},
        "property": prop,
        "enumMember": number,
        "variable.readonly": fg,
        "variable.defaultLibrary": typ,
        "keyword": keyword,
        "string": string,
        "number": number,
        "regexp": regex,
        "comment": {"foreground": comment, "italic": True},
    }

    return {
        "$schema": "vscode://schemas/color-theme",
        "name": label,
        "type": kind,
        "semanticHighlighting": True,
        "colors": colors,
        "tokenColors": token_colors,
        "semanticTokenColors": semantic,
    }


def main():
    out = os.path.join(ROOT, "vscode", "themes")
    os.makedirs(out, exist_ok=True)
    for name, label, kind in [
        ("ajisai-rainbow", "Ajisai Rainbow", "dark"),
        ("ajisai-rainbow-light", "Ajisai Rainbow Light", "light"),
    ]:
        path = os.path.join(out, f"{name}-color-theme.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(build(name, label, kind), f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(path)


if __name__ == "__main__":
    main()
