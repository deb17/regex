% rebase('base.tpl', title='Test your Regular Expressions')

<style type="text/css">
  body {
    background-color: #fff;
  }
  .container {
    margin-top: 40px;
  }
</style>

<div class="container">
  <h2>Password change</h2>
  % include('message.tpl')
  <p>Please insert your new password:</p>
  <div class="row">
    <div class="col-sm-4">
      <form action="/change_password" method="post">
        <input type="password" class="form-control" name="password" />
        <input type="hidden" name="reset_code" value="{{reset_code}}" />
        <br/>
        <button type="submit" class="btn btn-primary">OK</button>
      </form>
    </div>
  </div>
</div>
