// Seminar program table: turns a plain Markdown list into the .program layout (styles in assets/css/main.scss).
// How editors write it (in Japanese): README.md "セミナー記事のプログラム表の書き方".
//
//   - **プログラム**：
//     - 13:30–14:30 Speaker
//       Talk title
//       - Abstract (a nested list becomes the folded content)
//     - 14:30–15:00 Break (no nested list: shown as a muted row)
//
// In a definition list the term is the label instead:
//
//   📝 プログラム
//   : - 13:30–14:30 Speaker
//     - 14:30–15:00 Break
//
// A list is converted only when it sits under an item starting with a bold PROGRAM_LABELS label, or in a definition
// whose term is one (an emoji or symbol before the label is allowed: "📝 **プログラム**："), has 2+ items, and every
// item starts with a time ("13:30–14:30", "13:30〜", "17:30", full-width digits allowed). Otherwise it stays an
// ordinary list, which is also what readers without JavaScript see.
(function () {
  var PROGRAM_LABELS = ["プログラム", "Program"];
  var MIN_ITEMS = 2;
  // text before the bold label without any letter or digit (an emoji, a symbol) counts as decoration
  var LETTER_OR_DIGIT = /[\p{L}\p{N}]/u;
  var LEADING_DECORATION = /^[^\p{L}\p{N}]+/u;
  var TIME = "\\d{1,2}:\\d{2}(?!\\d)";
  var DASH = "[–—\\-~〜ー−―‐]";
  // after the time: a range ("–14:30"), an attached dash meaning open-ended ("〜"), or a spaced dash used only as a
  // separator ("17:30 - Closing"); matched against toAscii() text, so full-width forms are already ASCII
  var TIME_PREFIX = new RegExp(
    "^\\s*(" + TIME + ")(?:\\s*" + DASH + "\\s*(" + TIME + ")|(" + DASH + ")(?!\\s*\\d)|\\s+" + DASH + "(?=\\s))?"
  );
  var DISPLAY_DASH = "–";
  // inline wrappers that may be left empty once the time is cut out of them ("**13:30–14:30** Speaker")
  var INLINE_WRAPPERS = ["STRONG", "B", "EM", "I", "SPAN", "CODE"];

  // full-width digits, colon, hyphen, tilde and space to ASCII; one character to one character, so match lengths
  // on the converted text are valid on the original
  function toAscii(text) {
    return text.replace(/[\uFF10-\uFF19\uFF1A\uFF0D\uFF5E\u3000]/g, function (ch) {
      if (ch === "\u3000") return " ";
      return String.fromCharCode(ch.charCodeAt(0) - 0xFEE0);
    });
  }

  function isList(node) {
    return node.nodeType === Node.ELEMENT_NODE && (node.tagName === "UL" || node.tagName === "OL");
  }

  function isBlank(node) {
    return node.nodeName === "BR" || (node.nodeType === Node.TEXT_NODE && node.nodeValue.trim() === "");
  }

  // walks the text nodes of the item itself, skipping nested lists
  function headTextWalker(li) {
    return document.createTreeWalker(li, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        for (var el = node.parentNode; el !== li; el = el.parentNode) if (isList(el)) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
  }

  function headText(li) {
    var walker = headTextWalker(li);
    var text = "";
    var node;
    while ((node = walker.nextNode())) text += node.nodeValue;
    return toAscii(text);
  }

  function parseTime(li) {
    var m = headText(li).match(TIME_PREFIX);
    if (!m) return null;
    var label = m[1];
    if (m[2]) label += DISPLAY_DASH + m[2];
    else if (m[3]) label += DISPLAY_DASH; // "13:30〜" (open-ended)
    return { label: label, length: m[0].length };
  }

  function labelOf(list) {
    var li = list.parentNode;
    if (li && li.tagName === "DD") return termLabelOf(li);
    if (!li || li.tagName !== "LI") return "";
    // the label is the item's first content (after an optional decoration); it may be wrapped in <p> when the list has
    // blank lines
    var first = firstContent(li);
    if (first && first.nodeName === "P") first = firstContent(first);
    // a decoration before the label ("📝 **プログラム**：") is skipped
    if (first && first.nodeType === Node.TEXT_NODE && !LETTER_OR_DIGIT.test(first.nodeValue)) first = nextContent(first);
    if (!first || first.nodeName !== "STRONG") return "";
    return first.textContent.trim().replace(/[:：]$/, "");
  }

  // in a definition list the label is the term of the definition holding the list ("📝 プログラム" + ": - 13:30–...")
  function termLabelOf(dd) {
    var dt = dd.previousElementSibling;
    if (!dt || dt.tagName !== "DT") return "";
    return dt.textContent.trim().replace(LEADING_DECORATION, "").replace(/[:：]$/, "");
  }

  function firstContent(el) {
    return skipBlankText(el.firstChild);
  }

  function nextContent(node) {
    return skipBlankText(node.nextSibling);
  }

  function skipBlankText(node) {
    while (node && node.nodeType === Node.TEXT_NODE && node.nodeValue.trim() === "") node = node.nextSibling;
    return node;
  }

  function isProgramList(ul) {
    if (ul.closest(".program") || PROGRAM_LABELS.indexOf(labelOf(ul)) < 0) return false;
    var items = ul.children;
    if (items.length < MIN_ITEMS) return false;
    for (var i = 0; i < items.length; i++) {
      if (items[i].tagName !== "LI" || !parseTime(items[i])) return false;
    }
    return true;
  }

  // remove the first `count` characters of the item's own text (the time), even if split across inline elements
  function removePrefix(li, count) {
    var walker = headTextWalker(li);
    var cut = [];
    var node;
    while (count > 0 && (node = walker.nextNode())) {
      var take = Math.min(count, node.nodeValue.length);
      node.nodeValue = node.nodeValue.slice(take);
      count -= take;
      cut.push(node);
    }
    // drop inline wrappers that the cut left empty, innermost first
    cut.forEach(function (text) {
      for (var el = text.parentNode; el && el !== li; ) {
        var parent = el.parentNode;
        var empty = el.textContent.trim() === "" && !el.querySelector("img, svg, br, iframe, video");
        if (INLINE_WRAPPERS.indexOf(el.tagName) < 0 || !empty) break;
        parent.removeChild(el);
        el = parent;
      }
    });
  }

  function appendBreak(target) {
    if (target.lastChild && target.lastChild.nodeName !== "BR") target.appendChild(document.createElement("br"));
  }

  // move the item's own content (minus nested lists) into `target`; a source line break becomes <br>
  function moveHeadContent(li, target) {
    Array.prototype.slice.call(li.childNodes).forEach(function (node) {
      if (isList(node)) return;
      if (node.nodeName === "P") {
        // blank lines between items make kramdown wrap the text in <p>; unwrap it
        appendBreak(target);
        moveHeadContent(node, target);
      } else if (node.nodeName === "BR") {
        appendBreak(target); // a "two trailing spaces" break is followed by a newline; keep a single <br>
      } else if (node.nodeType === Node.TEXT_NODE) {
        var lines = node.nodeValue.split("\n");
        lines.forEach(function (line, i) {
          if (i > 0) appendBreak(target);
          // between source lines, a whitespace-only piece is just indentation
          if (line !== "" && !(lines.length > 1 && line.trim() === "")) target.appendChild(document.createTextNode(line));
        });
      } else {
        target.appendChild(node);
      }
    });
    while (target.firstChild && isBlank(target.firstChild)) target.removeChild(target.firstChild);
    while (target.lastChild && isBlank(target.lastChild)) target.removeChild(target.lastChild);
    if (target.firstChild && target.firstChild.nodeType === Node.TEXT_NODE) {
      target.firstChild.nodeValue = target.firstChild.nodeValue.replace(/^\s+/, "");
    }
    if (target.lastChild && target.lastChild.nodeType === Node.TEXT_NODE) {
      target.lastChild.nodeValue = target.lastChild.nodeValue.replace(/\s+$/, "");
    }
  }

  function buildRow(li, rowTag) {
    var time = parseTime(li);
    removePrefix(li, time.length);

    var row = document.createElement(rowTag);
    row.className = "program__row";
    var timeCell = document.createElement("span");
    timeCell.className = "program__time";
    timeCell.textContent = time.label;
    var talkCell = document.createElement("span");
    moveHeadContent(li, talkCell);

    row.appendChild(timeCell);
    row.appendChild(document.createTextNode(" "));
    row.appendChild(talkCell);
    return row;
  }

  function buildAbstract(lists) {
    var box = document.createElement("div");
    box.className = "program__abstract";
    lists.forEach(function (list) {
      // a single-item list reads as plain text; keep longer lists as lists
      if (list.children.length === 1) {
        while (list.children[0].firstChild) box.appendChild(list.children[0].firstChild);
      } else {
        box.appendChild(list);
      }
    });
    return box;
  }

  function convert(ul) {
    var program = document.createElement("div");
    program.className = "program";
    Array.prototype.slice.call(ul.children).forEach(function (li) {
      var nested = Array.prototype.filter.call(li.children, isList);
      if (nested.length > 0) {
        var details = document.createElement("details");
        var summary = document.createElement("summary");
        summary.appendChild(buildRow(li, "span"));
        details.appendChild(summary);
        details.appendChild(buildAbstract(nested));
        program.appendChild(details);
      } else {
        var row = buildRow(li, "div");
        row.className += " program__row--break";
        program.appendChild(row);
      }
    });
    ul.parentNode.replaceChild(program, ul);
  }

  function init() {
    var lists = document.querySelectorAll(".page__content ul, .page__content ol");
    Array.prototype.forEach.call(lists, function (ul) {
      if (isProgramList(ul)) convert(ul);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
