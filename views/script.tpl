<script type="text/javascript">
  var ele1 = document.getElementById("vbose");
  var empty = false;

  function setCursor(node, pos) {
    var range = document.createRange();
    range.setStart(node, pos);
    range.setEnd(node, pos);
    var sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
  }

  function processInput(e) {
    ele = document.getElementById("testdiv");
    if (ele.textContent.length == 0) {
      ele.innerHTML = "";
      empty = true;
    }
    if (empty && ele.textContent.length == 1) {
      ele.innerHTML = ele.textContent;
      empty = false;
      var textNode = ele.firstChild;
      setCursor(textNode, 1);
    }
    try {
      if (document.querySelector("#testdiv .hilite")) {
        // unwrap text in nested span tags
        while (window.getSelection().anchorNode.parentNode.outerHTML.endsWith("</span>")) {
          var node = window.getSelection().anchorNode.parentNode;
          var pos = window.getSelection().anchorOffset;
          var parent = node.parentNode;
          var t = node.firstChild;
          parent.insertBefore(t, node);
          parent.removeChild(node);
          setCursor(t, pos);
        }
      }
    }
    catch(err) {}
  }

  document.getElementById("testdiv").addEventListener("input", processInput);

  function copyContent () {
    document.querySelector("#test > textarea").value =  
        document.getElementById("testdiv").innerHTML;
    return true;
  }

  function textElements() {
    if (ele1.checked) {
      var pattHTML = '<textarea class="form-control" name="pattern" spellcheck="false" placeholder="Pattern" maxlength="500" required>{{! pattern }}</textarea>'
      document.getElementById("patt").innerHTML = pattHTML;
    } else {
      document.querySelector("#patt input").value = "{{! pattern }}";
    }
  }
  textElements();

  ele1.onclick = function () {
    if (ele1.checked) {
      var pattValue = document.querySelector("#patt input").value;
      var pattHTML = '<textarea class="form-control" name="pattern" spellcheck="false" placeholder="Pattern" maxlength="500" required>' + pattValue + '</textarea>'
      document.getElementById("patt").innerHTML = pattHTML;
    } else {
      var pattValue = document.querySelector("#patt textarea").value;
      var firstLine = /.*/.exec(pattValue);
      var pattHTML = '<input type="text" class="form-control" name="pattern" placeholder="Pattern" spellcheck="false" maxlength="500" required value="' + firstLine + '">'
      document.getElementById("patt").innerHTML = pattHTML;
    }
  };

</script>
