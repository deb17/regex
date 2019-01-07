% rebase('base.tpl', title='Admin page')

<style>
  body {
    background-color: #fff;
  }
  .container {
    margin-top: 30px;
  }
  div#status {
      border: 1px solid #999;
      padding: .5em;
      margin: 2em;
      width: 15em;
      -moz-border-radius: 10px;
      border-radius: 10px;
  }
  div#urls {
    position:absolute;
    top: 30px;
    right:1em;
}
</style>

<div id='main' class="container">
  <h2>Administration page</h2>
  <p>Welcome {{current_user.username}}, your role is: {{current_user.role}},
  access time: {{current_user.session_accessed_time}}</p>
  <div class="row">
    <div id='commands' class="col-sm-4">
      <h4>Create new user:</h4>
      <form action="/create_user" method="post">
          <p><label>Username</label> <input type="text" class="form-control" name="username" /></p>
          <p><label>Role</label> <input type="text" class="form-control" name="role" /></p>
          <p><label>Password</label> <input type="password" class="form-control" name="password" /></p>
          <button type="submit" class="btn btn-primary">OK</button>
      </form>
      <br />
      <h4>Delete user:</h4>
      <form action="/delete_user" method="post">
          <p><label>Username</label><input type="text" class="form-control" name="username" /></p>
          <button type="submit" class="btn btn-primary">OK</button>
      </form>
      <br />
      <h4>Create new role:</h4>
      <form action="/create_role" method="post">
          <p><label>Role</label> <input type="text" class="form-control" name="role" /></p>
          <p><label>Level</label> <input type="text" class="form-control" name="level" /></p>
          <button type="submit" class="btn btn-primary">OK</button>
      </form>
      <br />
      <h4>Delete role:</h4>
      <form action="/delete_role" method="post">
          <p><label>Role</label> <input type="text" class="form-control" name="role" /></p>
          <button type="submit" class="btn btn-primary">OK</button>
      </form>
      <div id='status'><p>Ready.</p></div>
    </div>
    <div class="col-sm-1"></div>
    <div id="users" class="col-sm-6">
        <table class="table">
            <tr><th>Username</th><th>Role</th><th>Email</th><th>Description</th></tr>
            %for u in users:
            <tr><td>{{u[0]}}</td><td>{{u[1]}}</td><td>{{u[2]}}</td><td>{{u[3]}}</td></tr>
            %end
        </table>
        <br/>
        <table class="table">
            <tr><th>Role</th><th>Level</th></tr>
            %for r in roles:
            <tr><td>{{r[0]}}</td><td>{{r[1]}}</td></tr>
            %end
        </table>
        <p>(Reload page to refresh)</p>
    </div>
  </div>
  <div id="urls">
    <a href="/home">Home</a>
  </div>
</div>
<script>
  // Prevent form submission, send POST asynchronously and parse returned JSON
  window.addEventListener("load", function () {
    $('form').submit(function(e) {
        $.post($(this).attr('action'), $(this).serialize(), function(j){
          if (j.ok) {
            $("div#status").css("background-color", "#f0fff0");
            $("div#status p").text('Ok.');
          } else {
            $("div#status").css("background-color", "#fff0f0");
            $("div#status p").text(j.msg);
          }
        }, "json");
        return false;
    });
  });
</script>
