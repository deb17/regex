% rebase('base.tpl', title='Insert entry')

<style type="text/css">
  body {
    background-color: #e6ffe6;
  }
  .container {
    margin-top: 80px;
  }
  #error {
    color: red;
    font-weight: bold;
  }
  #success {
    color: green;
    font-weight: bold;
  }
  #desc-label {
    line-height: 19px;
  }
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
  #bottomPara {
    margin-bottom: 5px;
  }
</style>

<div class="container">
  <div class="row">
    <div class="col-lg-9 col-xl-8">
      <div class="container-fluid">
        % if errormsg:
        <p id="error">Error in re.</p>
        % end
        % if successmsg:
        <p id="success">Entry was created successfully.</p>
        % end
        <h2>Insert a new entry</h2>
        <br>
        <form method="POST" id="form1" onsubmit="return copyContent()">
          <div class="form-group row">
            <label for="pattern" class="col-sm-2 col-form-label">Pattern:</label>
            <div class="col-sm-6" id="patt">
              <input type="text" class="form-control" name="pattern" spellcheck="false" placeholder="Pattern" maxlength="500" required>
            </div>
            <div class="col-sm-2">
              <button type="button" class="btn btn-info mt-2 mt-sm-0" data-toggle="popover" data-placement="bottom" data-html="true" data-content="">
              Cheatsheet
              </button>
            </div>
          </div>
          <div class="form-group row">
            <div class="col-sm-2"></div>
            % include('flags.tpl', cls='col-sm-6', index=False)
          </div>
          <div class="form-group row">
            <label for="testdata" class="col-sm-2 col-form-label">Test string:</label>
            <div class="col-sm-6" id="test">
              <div name="testdatadiv" id="testdiv" contenteditable="true" spellcheck="false" class="form-control" placeholder="Test data" maxlength="500" required>{{! testdata }}</div>
              <textarea name="testdata"></textarea>
            </div>
          </div>
          <div class="form-group row">
            <label for="desc" class="col-sm-2 col-form-label" id="desc-label">Description:<br><small>Optional</small></label>
            <div class="col-sm-6">
              <input type="text" class="form-control" id="desc" name="desc" value="{{ description if description else '' }}">
            </div>
          </div>
          <div class="form-group row">
            <div class="col-sm-2"></div>
            <div class="col-sm-6">
              <button type="submit" class="btn btn-primary">Insert</button>
            </div>
          </div>
        </form>
        <br>
        <p id="bottomPara"><a href="/entries">See your entries</a></p>
        <p>Go back <a href="/home">home</a></p>
        
      </div>
    </div>
  </div>
</div>
% include('script.tpl')
