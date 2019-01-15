'''This module performs operations related to the re module.

Its functions are:

    run_re - Run the requested re and format the input data with
             highlighting.
    check_re - Check if the re is valid (can be compiled).
    clean_data - Remove all span tags from the input test data.
    get_flags_value - Calculate the binary OR of the flags.
    get_modified_data - Format the input test data with highlighting.
    modify_input - Helper function to copy data from input to output.
    format_result - Format result part of the page for proper display.

NOTE - In this webapp, I have decided to handle the highlighting myself
instead of using a third-party jquery plugin which is also an option.
One issue with jquery plugins is that they change the style of the
textarea, so a number of changes are necessary to make it match
bootstrap style.

TO-DO - Change every 2 spaces in testdiv and results part to a space and
        an nbsp . Use `word-break: break-word` and - for firefox -
        `overflow-wrap: break-word` in the css. Replace ' <' with
        '&nbsp;<' to preserve spaces - may not be required in the
        results part.
'''

import re
import html

def run_re(pattern, flags, testdata, modify='Y'):
    '''Run the search method on the compiled re and format the test
    data with highlighting.

    1. Prepare the test data coming from the content editable div for
    searching. Remove div, br and span tags and introduce newlines.
    Replace non-breaking space with space character.

    2. Compile and run the search method. Format the result by escaping
    <, >, &, quote characters and introducing non-breaking spaces.

    3. Run the finditer method on the regex to get all matches and
    format the data with span tags to show highlighting.
    '''

    origdata = testdata
    testdata = re.sub(r'<span(.*?)>', '', testdata)
    testdata = testdata.replace('</span>', '')
    if testdata.startswith('<div>'):
        testdata = testdata[5:]

    # Firefox introduces <br>. <br> is also present with <div> on blank
    # lines.
    testdata = testdata.replace('<br>', '')

    testdata = testdata.replace('<div>', '\n')
    testdata = testdata.replace('</div>', '')
    # testdata = re.sub(r'<div>(.*?)</div>', r'\n\1', testdata)
    testdata = testdata.replace('&nbsp;', ' ')
    testdata = html.unescape(testdata)
    calc_val = get_flags_value(flags)
    try:
        regex = re.compile(pattern, calc_val)
    except Exception:
        result = 'error'
        mod_data = origdata
    else:
        match = regex.search(testdata)
        if match is None:
            result = (None, None, None)
        else:
            group = match.group().replace('\n', '\\n')
            group = format_result(group)
            groups = tuple(format_result(grp) for grp in match.groups())
            groupdict = {k: format_result(v) for k, v
                         in match.groupdict().items()}
            result = (group,
                      groups or None,
                      groupdict or None)

        if modify == 'Y':
            it = regex.finditer(testdata)
            testdata = html.escape(testdata, quote=False)
            mod_data = get_modified_data(testdata, it)
        else:
            mod_data = origdata

    return result, mod_data

def check_re(pattern, flags):
    '''Compile the re to check its validity.'''

    calc_val = get_flags_value(flags)
    try:
        regex = re.compile(pattern, calc_val)
    except Exception:
        return False

    return True

def clean_data(data):
    '''Remove span tags introduced by this module and those inserted
    automatically by the contenteditable div.
    '''

    data = re.sub(r'<span(.*?)>', '', data)
    data = data.replace('</span>', '')

    return data

def get_flags_value(flags):
    '''Calculate bitwise OR of flags. Flags considered are -
    IGNORECASE, DOTALL, VERBOSE, ASCII, MULTILINE.
    LOCALE flag has been ignored because the official HOWTO for
    Regular Expressions discourages its use. Also this flag would affect
    the server and not the client.
    '''

    val = 0

    if flags[0] == 'i':
        val |= re.I
    if flags[1] == 's':
        val |= re.S
    if flags[2] == 'x':
        val |= re.X
    if flags[3] == 'a':
        val |= re.A
    if flags[4] == 'm':
        val |= re.M

    return val

def get_modified_data(data, it):
    '''Format the test data string used in the re search with HTML tags.

    1. Read the input (in data variable) character by character. See
    docstring for modify_input function.

    2. If match object starts starts at a character, introduce a span
    tag with class hilite in the output (the modified variable).

    3. If match object ends at a character, introduce closing span tag.

    4. Take care to close the span tag and start a new span if a newline
    is encountered when a span tag has not yet been closed.

    5. Replace all spaces by non-breaking spaces.

    6. When iterator is exhausted, copy remaining input to output.

    7. Introduce opening and closing div tags where there are newlines.
    '''

    modified = ''
    cnt = 0
    i = 0
    starttag = False
    try:
        mo = next(it)
        while cnt < len(data):
            if i == mo.span()[0]:
                if data[cnt] != '\n':
                    modified += '<span class="hilite">'
                    modified, cnt = modify_input(modified, data, cnt)
                else:
                    modified += '\n'
                    modified += '<span class="hilite">'
                    cnt += 1
                starttag = True
            elif i == mo.span()[1]:
                modified += '</span>'
                starttag = False
                mo = next(it)
                if i == mo.span()[0]:
                    i -= 1
                else:
                    modified, cnt = modify_input(modified, data, cnt)
            elif starttag and data[cnt] == '\n':
                modified += '</span>\n<span class="hilite">'
                cnt += 1
            else:
                modified, cnt = modify_input(modified, data, cnt)
            i += 1
        if starttag: modified += '</span>'
    except StopIteration:
        modified += data[cnt:].replace(' ', '&nbsp;')

    output = ''
    first = True
    for c in modified:
        if c == '\n' and first:
            output += '<div>'
            first = False
        elif c == '\n':
            output += '</div><div>'
        else:
            output += c

    if not first:
        output += '</div>'

    # introduce br tags to effect blank lines.

    output = output.replace('<div></div>', '<div><br></div>')
    output = output.replace('<div><span class="hilite"></span></div>',
                            '<div><span class="hilite"><br></span></div>')
    if output.startswith('<div>'):
        output = '<div><br></div>' + output

    return output

def modify_input(modified, data, cnt):
    '''Copy input character to output, taking care copy escaped
    characters. It is necessary to escape the test data before modifying
    it because once the tags are introduced, the data cannot be escaped.

    Introduce non-breaking spaces.
    '''

    charrefs = ('&lt;', '&gt;', '&amp;')

    if data[cnt:cnt+4] in charrefs:
        modified += data[cnt:cnt+4]
        cnt += 4
    elif data[cnt:cnt+5] in charrefs:
        modified += data[cnt:cnt+5]
        cnt += 5
    else:
        modified += '&nbsp;' if data[cnt] == ' ' else data[cnt]
        cnt += 1

    return modified, cnt

def format_result(data):
    '''Format result (whole match, groups and group dict) for displaying
    on a webpage.
    '''

    if not data: return data  # data may be None

    data = html.escape(data, quote=False)
    data = data.replace(' ', '&nbsp;')

    return data
