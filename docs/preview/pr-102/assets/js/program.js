// Seminar program table: turns a plain Markdown list into the .program layout (styles in assets/css/main.scss).
//
// Write in the post (.md) like this — every item starts with a time range:
//
//   - 13:30–14:30 Speaker
//     Talk title
//     - Abstract text (a nested list makes the row foldable)
//   - 14:30–15:00 Break
//
// - The text after the time becomes the right column; a line break in the source becomes a line break on the page.
// - A nested list becomes the folded content (opened with the ▶ marker).
// - An item without a nested list is shown as a muted row (for breaks etc.).
// Without JavaScript the list stays as an ordinary nested list.
(function () {
  var TIME_RANGE = /^\s*(\d{1,2}:\d{2}\s*[–—\-~〜～]\s*\d{1,2}:\d{2})\s*/;

  function isProgramList(ul) {
    var items = ul.children;
    if (items.length === 0) return false;
    for (var i = 0; i < items.length; i++) {
      if (items[i].tagName !== "LI" || !TIME_RANGE.test(items[i].textContent)) return false;
    }
    return true;
  }

  // move the item's own content (minus nested lists) into `target`, turning source line breaks into <br>
  function isList(node) {
    return node.nodeType === Node.ELEMENT_NODE && (node.tagName === "UL" || node.tagName === "OL");
  }

  function isBlank(node) {
    return node.nodeName === "BR" || (node.nodeType === Node.TEXT_NODE && node.nodeValue.trim() === "");
  }

  function moveHeadContent(li, target) {
    Array.prototype.slice.call(li.childNodes).forEach(function (node) {
      if (isList(node)) return;
      // blank lines between items make kramdown wrap the text in <p>; unwrap it
      if (node.nodeName === "P") {
        if (target.lastChild && !isBlank(target.lastChild)) target.appendChild(document.createElement("br"));
        moveHeadContent(node, target);
        return;
      }
      if (node.nodeType !== Node.TEXT_NODE) {
        target.appendChild(node);
        return;
      }
      node.nodeValue.split("\n").forEach(function (line, i) {
        if (i > 0) target.appendChild(document.createElement("br"));
        if (line !== "") target.appendChild(document.createTextNode(line));
      });
    });
    // trim the whitespace and line breaks around the content (e.g. the one before a nested list)
    while (target.firstChild && isBlank(target.firstChild)) target.removeChild(target.firstChild);
    while (target.lastChild && isBlank(target.lastChild)) target.removeChild(target.lastChild);
  }

  function buildRow(li) {
    var row = document.createElement("span");
    row.className = "program__row";
    var time = document.createElement("span");
    time.className = "program__time";
    var talk = document.createElement("span");

    // split the time range off the first non-blank text (possibly inside a <p>)
    var walker = document.createTreeWalker(li, NodeFilter.SHOW_TEXT);
    var firstText = walker.nextNode();
    while (firstText && firstText.nodeValue.trim() === "") firstText = walker.nextNode();
    var match = firstText && firstText.nodeValue.match(TIME_RANGE);
    if (match) {
      time.textContent = match[1];
      firstText.nodeValue = firstText.nodeValue.slice(match[0].length);
    }
    moveHeadContent(li, talk);

    row.appendChild(time);
    row.appendChild(document.createTextNode(" "));
    row.appendChild(talk);
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
      var row = buildRow(li);
      if (nested.length > 0) {
        var details = document.createElement("details");
        var summary = document.createElement("summary");
        summary.appendChild(row);
        details.appendChild(summary);
        details.appendChild(buildAbstract(nested));
        program.appendChild(details);
      } else {
        row.className += " program__row--break";
        var div = document.createElement("div");
        while (row.firstChild) div.appendChild(row.firstChild);
        div.className = row.className;
        program.appendChild(div);
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
