% rebase('base.tpl', title='Edit entry')

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
  .resultPara {
    word-break: break-all;
  }
</style>

<div class="container">
  <div class="row">
    <div class="col-lg-9 col-xl-8">
      <div class="container-fluid">
        % if errormsg:
        <p id="error">Error in re.</p>
        % end
        <h2>Edit entry</h2>
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
              <input type="text" class="form-control" id="desc" name="desc" value="{{ description }}">
            </div>
          </div>
          <div class="form-group row">
            <div class="col">
              <button type="button" class="btn btn-danger mr-3" data-toggle="modal" data-target="#deleteModal">Delete</button>
              <a href="/edit/{{ eid }}" class="btn btn-info mr-3">Reset</a>
              <br class="d-inline d-sm-none">
              <button type="submit" class="btn btn-primary mr-3 mt-2 mt-sm-0">Test</button>
              <button type="submit" class="btn btn-primary mr-3 mt-2 mt-sm-0" name="save" value="true">Save</button>
            </div>
          </div>
        </form>
        <p><a href="/entries">Back</a></p>
        % include('result.tpl')
      </div>
    </div>
  </div>
</div>
<div class="modal fade" id="deleteModal" tabindex="-1" role="dialog" aria-labelledby="deleteModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-sm" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="deleteModalLabel">Confirm deletion</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <p>Delete entry from database&quest;</p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-primary" data-dismiss="modal">No</button>
        <a href="/delete/{{ eid }}" class="btn btn-danger">Yes</a>
      </div>
    </div>
  </div>
</div>
% include('script.tpl')
