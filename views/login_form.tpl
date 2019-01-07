% rebase('base.tpl', title='Log in')

<style type="text/css">
  body {
    background-color: white;
  }
  label.error {
    margin-bottom: 20px;
  }
</style>

<!-- <script src="https://www.google.com/recaptcha/api.js" async defer></script> -->

<div class="container mt-3">
  <a href='/'>Back</a>
  <div class="row">
    <div class="col-sm-4">
      % if form == 'form1':
      % include('message.tpl')
      % end
      <h2>Login</h2>
      <form action="/login" method="post" id="form1">
        <input type="text" id="uname1" class="form-control mb-2" name="username" placeholder="username" value="{{ uname if form == 'form1' else '' }}" required>
        <input type="password" id="pass1" class="form-control mb-2" name="password" placeholder="password" required>
        <br>
        <div><button type="submit" class="btn btn-primary">Login</button></div>
      </form>
    </div>
    <div class="col-sm-4">
      % if form == 'form2':
      % include('message.tpl')
      % end
      <h2>Signup</h2>
      <form action="/register" method="post" id="form2">
        <input type="text" id="uname2" class="form-control mb-2" name="username" placeholder="username" value="{{ uname if form == 'form2' else '' }}" required>
        <input type="password" id="pass21" class="form-control mb-2" name="password1" placeholder="password" required>
        <input type="password" id="pass22" class="form-control mb-2" name="password2" placeholder="confirm password" required>
        <input type="email" id="email2" class="form-control mb-2" name="email_address" placeholder="email address" value="{{ email if form == 'form2' else '' }}" required>
        <!-- <div class="g-recaptcha" data-sitekey="6LfeHx4UAAAAAAKUx5rO5nfKMtc9-syDTdFLftnm"></div> -->
        <br>
        <div><button type="submit" class="btn btn-primary">Signup</button></div>
      </form>
    </div>
    <div class="col-sm-4">
      % if form == 'form3':
      % include('message.tpl')
      % end
      <h2>Password reset</h2>
      <form action="/reset_password" method="post" id="form3">
        <input type="text" id="uname3" class="form-control mb-2" name="username" placeholder="username" value="{{ uname if form == 'form3' else '' }}" required>
        <input type="text" id="email3" class="form-control mb-2" name="email_address" placeholder="email address" value="{{ email if form == 'form3' else '' }}" required>
        <br>
        <div><button type="submit" class="btn btn-primary">Submit</button></div>
      </form>
    </div>
  </div>
</div>
<!-- <script type="text/javascript">
  var s = "<ul>"
  % messages = app.get_flashed_messages()
  % if messages:
    % for m in messages:
    s +="<li>" + "{{ m[0] }}" + "</li>";
    % end
    s += "</ul>"
    % if messages[0][1] == 1:
    document.getElementById("form1Div").innerHTML = s;
    % else:
    document.getElementById("form2Div").innerHTML = s;
    % end
  % end
</script> -->
