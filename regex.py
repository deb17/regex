import re
import html

def run_re(pattern, flags, testdata, modify='Y'):

    origdata = testdata
    print('origdata', repr(origdata))
    testdata = re.sub(r'<span(.*?)>', '', testdata)
    testdata = testdata.replace('</span>', '')
    if testdata.startswith('<div>'):
        testdata = testdata[5:]
    testdata = testdata.replace('<br>', '') # Firefox introduces <br>
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

    print('mod_data', repr(mod_data))
    return result, mod_data

def check_re(pattern, flags):

    calc_val = get_flags_value(flags)
    try:
        regex = re.compile(pattern, calc_val)
    except Exception:
        return False

    return True

def clean_data(data):

    data = re.sub(r'<span(.*?)>', '', data)
    data = data.replace('</span>', '')

    return data

def get_flags_value(flags):

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

    output = output.replace('<div></div>', '<div><br></div>')
    output = output.replace('<div><span class="hilite"></span></div>',
                            '<div><span class="hilite"><br></span></div>')
    if output.startswith('<div>'):
        output = '<div><br></div>' + output

    return output

def modify_input(modified, data, cnt):

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

    if not data: return data

    data = html.escape(data)
    data = data.replace(' ', '&nbsp;')

    return data
