% rebase('base.tpl', title='Entries')

<style type="text/css">
  body {
    background-color: #e6ffe6;
  }
  .container {
    margin-top: 80px;
  }
  th {
    font-size: 1.2em;
  }
  td:first-child {
    width: 70%;
    word-break: break-word;
  }
  td:nth-child(2) {
    width: 30%;
    word-break: break-all;
  }
  #msg-para {
    color: green;
    font-weight: bold;
  }
  #goback {
    margin-right: 7px;
  }
  #flags {
    font-size: 0.8em;
  }
  pre {
    display: inline;
    white-space: pre-wrap;
    word-break: break-all;
    font-family: inherit;
    font-size: 1em;
    color: inherit;
    margin: 0;
  }
  @-moz-document url-prefix() {
    pre {
      display: inline-block;
      position: relative;
      top: 6px;
    }
  }
</style>

<div class="container">
  % if msg:
  <p id="msg-para">{{ msg }}</p>
  % end
  % if total == 0:
  <h3>There are no entries.</h3>
  % else:
  <h2>Your entries ({{ total }} found)</h2>
  <div><span id="goback"><a href="/home">&lt;&lt;</a></span><a href="/insert">Insert new entry</a></div>
  <div><small>Click on any pattern below to edit it.</small></div>
  <div class="row">
    <div class="col-sm-10">
      <table class="table table-striped">
        <thead class="thead-dark">
          <tr>
            <th class="text-center"><b>Entry</b></th>
            <th class="text-center"><b>Matches</b></th>
          </tr>
        </thead>
        <tbody>
          % import html
          % for entry, match in zip(entries, matches):
          <tr>
            <td>
              Pattern:{{! '<br>' if '\n' in entry.pattern else ' ' }}<a href="/edit/{{ entry.id }}"><b><pre>{{ '"' + entry.pattern.replace('\r\n', '\n') + '"' }}</pre></b></a><br>
              % if entry.flags != '-----':
                % fl = entry.flags
                % flags = ''
                % if fl[0] == 'i':
                  % flags += 'IGNORECASE, '
                % end
                % if fl[1] == 's':
                  % flags += 'DOTALL, '
                % end
                % if fl[2] == 'x':
                  % flags += 'VERBOSE, '
                % end
                % if fl[3] == 'a':
                  % flags += 'ASCII, '
                % end
                % if fl[4] == 'm':
                  % flags += 'MULTILINE'
                % end
                % flags = flags.strip(', ')
              Flags: <span id="flags">{{ flags }}</span><br>
              % end
              % data = entry.testdata
              % if data[:5] == '<div>': 
              % data = data[5:]
              % end
              % data = data.replace('<div>', '\n')
              % data = data.replace('</div>', '')
              % if data[-4:] == '<br>':
              % data = data[:-4] + '\n'
              % end
              % data = data.replace('<br>', '')
              % data = data.replace('&nbsp;', ' ')
              % data = html.unescape(data)
              Test string:{{! '<br>' if '\n' in data else ' ' }}<b><pre>{{ '"' + data + '"' }}</pre></b><br>
              % if entry.description:
              Description: {{ entry.description }}<br>
              % end
              Added: {{ entry.date_added.strftime('%b %d, %Y, %I:%M %p UTC') }}
            </td>
            <td>
              Group: {{! match[0] }}<br>
              Subgroups: {{! match[1] }}<br>
              Group Dict: {{! match[2] }} 
            </td>
          </tr>
          % end
        </tbody>
      </table>
    </div>
  </div>
  % end
  <p>Go back <a href="/home">home</a></p>
</div>
