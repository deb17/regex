% rebase('base.tpl', title='Home')

<style type="text/css">
  body {
    background-color: #e6ffe6;
  }
  .container {
    margin-top: 80px;
  }
</style>

<div class="container">
  <h2>Hello {{ username }}!</h2>
  <h3>Welcome to the Regex website.</h3>
  <br><br>
  <p>To see a list of your entries, please click <a href="/entries">here</a></p>
  <p>To insert an entry, please click <a href="/insert">here</a></p>
  <p><a href="/logout">Logout</a></p>
  <br>
  <a href="#" data-toggle="modal" data-target="#homeModal">Feedback</a>
</div>

<!-- Modal -->
<div class="modal fade" id="homeModal" tabindex="-1" role="dialog" aria-labelledby="homeModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="homeModalLabel">Feedback</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <p>This web-app was made with the bottle framework by Debashish Palit, a 
        Python enthusiast. If you have any questions/comments, please send them to
        dpalit17@outlook.com .</p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>
