% rebase('base.tpl', title='Regular expressions')

<style type="text/css">
  #testdiv {
    height: auto;
    word-break: break-all;
  }
  #testdiv:empty::before {
    content: attr(placeholder);
    color: gray;
    cursor: text;
  }
  #test textarea {
    display: none;
  }
  span.hilite {
    background-color: yellow;
  }
  .resultPara {
    word-break: break-all;
  }
</style>

<div class="container mt-3">
  <div class="jumbotron mb-3">
    <h1 id="jumbo-h1" class="d-none d-sm-block display-4">Test your Regular Expressions</h1>
    <h2 id="jumbo-h1" class="d-block d-sm-none">Test your Regular Expressions</h2>
    <p class="lead"><a id="jumbo-link" href="https://pyvideo.org/pycon-us-2017/yes-its-time-to-learn-regular-expressions.html" target="_blank">Learn more about them</a></p>
    <p class="lead">Test your Python regular expression against a string below.</p>
    <hr class="my-4">
    <p>Login to save your regex.</p>
    <a class="btn btn-primary btn-lg" href="/login" role="button">Log in</a>
  </div>
</div>

<div class="container mb-2">
  <h3>Quick test</h3>
  <form method="post" id="form1" onsubmit="return copyContent()">
    <div class="form-row">
      <div class="col-sm-4" id="patt">
        <input type="text" class="form-control" name="pattern" spellcheck="false" placeholder="Pattern" maxlength="500" required>
      </div>
      <div class="col-sm-6" id="test">
        <div name="testdatadiv" id="testdiv" contenteditable="true" spellcheck="false" class="mt-2 mt-sm-0 form-control" placeholder="Test data" maxlength="500" required>{{! testdata }}</div>
        <textarea name="testdata"></textarea>
      </div>
      <div class="col-lg-2">
        <button type="button" class="btn btn-info ml-lg-3 mt-2 mt-lg-0" data-toggle="popover" data-placement="top" data-html="true" data-content="">
        Cheatsheet
        </button>
      </div>
    </div>
    <div class="form-row">
      % include('flags.tpl', cls='col-sm-7 mt-2', index=True)
      <div class="col-sm-4 col-md-3 mt-2">
        <input type="submit" class="btn btn-primary float-right" value="Submit">
        <a href="/" class="btn btn-info float-right mr-3">Reset</a>
      </div>
    </div>
  </form>
  % include('result.tpl')
</div>
% include('script.tpl')
