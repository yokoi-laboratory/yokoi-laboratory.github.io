// Seminar program table: turns a plain Markdown list into the .program layout (styles in assets/css/main.scss).
// How editors write it (in Japanese): README.md "セミナー記事のプログラム表の書き方".
//
//   - **プログラム**：
//     - 13:30–14:30 Speaker
//       Talk title
//       - Abstract (a nested list becomes the folded content)
//     - 14:30–15:00 Break (no nested list: shown as a muted row)
//
// A list is converted only when it sits under an item labelled PROGRAM_LABELS, has 2+ items, and every item starts
// with a time ("13:30–14:30", "13:30〜", "17:30", full-width digits allowed). Otherwise it stays an ordinary list,
// which is also what readers without JavaScript see.
(function () {
  var PROGRAM_LABELS = ["プログラム", "Program"];
  var MIN_ITEMS = 2;
  var TIME = "\\d{1,2}:\\d{2}";
  var DASHES = "–—\\-~〜ー－−―‐";
  // matched against NFKC-normalized text, so full-width digits/colons/tildes are already ASCII
  var TIME_PREFIX = new RegExp("^\\s*(" + TIME + ")(?:\\s*[" + DASHES + "]\\s*(" + TIME + ")?)?");
  var DISPLAY_DASH = "–";

  function isList(node) {
    return node.nodeType === Node.ELEMENT_NODE && (node.tagName === "UL" || node.tagName === "OL");
  }

  function isBlank(node) {
    return node.nodeName === "BR" || (node.nodeType === Node.TEXT_NODE && node.nodeValue.trim() === "");
  }

  // text of the item itself, without nested lists
  function headText(li) {
    var text = "";
    Array.prototype.forEach.call(li.childNodes, function (node) {
      if (!isList(node)) text += node.textContent;
    });
    return text.normalize("NFKC");
  }

  function parseTime(li) {
    var m = headText(li).match(TIME_PREFIX);
    if (!m) return null;
    var label = m[1];
    if (m[2]) label += DISPLAY_DASH + m[2];
    else if (/[^\d:\s]\s*$/.test(m[0])) label += DISPLAY_DASH; // "13:30〜" (open-ended)
    return { label: label, length: m[0].length };
  }

  function labelOf(list) {
    var li = list.parentNode;
    if (!li || li.tagName !== "LI") return "";
    var strong = li.querySelector("strong");
    if (!strong) return "";
    var parent = strong.parentNode; // the label may be wrapped in <p> when the list has blank lines
    if (parent !== li && !(parent.nodeName === "P" && parent.parentNode === li)) return "";
    return strong.textContent.replace(/[:：\s]/g, "");
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

  // remove the first `count` characters of the item's own text (the time), even if split across inline elements;
  // NFKC keeps these characters one-to-one, so counts on the normalized text apply to the original
  function removePrefix(li, count) {
    var walker = document.createTreeWalker(li, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        for (var el = node.parentNode; el !== li; el = el.parentNode) if (isList(el)) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var node;
    while (count > 0 && (node = walker.nextNode())) {
      var take = Math.min(count, node.nodeValue.length);
      node.nodeValue = node.nodeValue.slice(take);
      count -= take;
    }
    // drop inline elements left empty (e.g. "**13:30–14:30** Speaker")
    Array.prototype.slice.call(li.children).forEach(function (el) {
      if (!isList(el) && el.textContent.trim() === "" && !el.querySelector("img")) li.removeChild(el);
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
        node.nodeValue.split("\n").forEach(function (line, i) {
          if (i > 0) appendBreak(target);
          if (line !== "") target.appendChild(document.createTextNode(line));
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
    var lists = document.querySelectorAll(".page__content ul");
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
