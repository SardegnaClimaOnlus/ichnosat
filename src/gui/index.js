$(function () {
    // init layout
    var main_layout = $('#main_layout').w2layout({
        name: 'main_layout',
        panels: [
            { type: 'top', size: 45, style: 'border: 0px; border-bottom: 1px solid silver; background-color: #fff; color: #555;', overflow: 'hidden'},
            { type: 'left', size: 240, resizable: true, style: 'border-right: 1px solid silver;' },
            { type: 'main', style: 'background-color: white;' }
        ]
    });
    w2ui['main_layout'].content('top', '<div style="padding: 12px 20px; font-size: 18px;">Ichnosat - Control Panel </div>');

    w2ui['main_layout'].content('left', $().w2sidebar({
        name: 'demo-sidebar',
        img: null,
        nodes: [
            { id: 'modules', text: 'Modules', icon: '',  group1: true,
                nodes: [
                    { id: 'modules-1', text: 'Downloader', icon: '' },
                    { id: 'modules-2', text: 'Processing Pipe', icon: '' }
                ]
            },
            { id: 'products', text: 'Products', icon: '',  group1: true,
                nodes: [
                    { id: 'products-1', text: 'Pending', icon: '' },
                    { id: 'products-2', text: 'Downloading', icon: '' },
                    { id: 'products-3', text: 'Downloaded', icon: '' },
                    { id: 'products-4', text: 'Processing', icon: '' },
                    { id: 'products-5', text: 'Processed', icon: '' },
                ]
            }
        ],
        onClick: function (event) {
            var cmd = event.target;
            if (parseInt(cmd.substr(cmd.length-1)) != cmd.substr(cmd.length-1)) return;
            var tmp = w2ui['demo-sidebar'].get(cmd);
            document.title = tmp.parent.text + ': ' + tmp.text + ' | ichnosat';
            for (var widget in w2ui) {
                var nm = w2ui[widget].name;
                if (['main_layout', 'demo-sidebar'].indexOf(nm) == -1) $().w2destroy(nm);
            }
            if (tmp.parent && tmp.parent.id != '') {
                var pid = w2ui['demo-sidebar'].get(cmd).parent.id;
                document.location.hash = '!'+ pid + '/' + cmd;
            }
            $.get('examples/'+ cmd +'.html', function (data) {
                var tmp = data.split('<!--CODE-->');
                if (tmp.length == 1) {
                    alert('ERROR: cannot parse example.');
                    console.log('ERROR: cannot parse example.', data);
                    return;
                }
                var w2ui_js  = 'http://rawgit.com/vitmalina/w2ui/master/dist/w2ui.min.js';
                var w2ui_css = 'http://rawgit.com/vitmalina/w2ui/master/dist/w2ui.min.css';
                var html     = tmp[1] ? $.trim(tmp[1]) : '';
                var js       = tmp[2] ? $.trim(tmp[2]) : '';
                var css      = tmp[3] ? $.trim(tmp[3]) : '';
                var json     = tmp[4] ? $.trim(tmp[4]) : '';
                js   = js.replace(/^<script[^>]*>/, '').replace(/<\/script>$/, '');
                js   = $.trim(js);
                css  = css.replace(/^<style[^>]*>/, '').replace(/<\/style>$/, '');
                css  = $.trim(css);
                json = json.replace(/^<script[^>]*>/, '').replace(/<\/script>$/, '');
                json = $.trim(json);
                w2ui['main_layout'].content('main', tmp[0]);
                $('#example_view').html(
                        ''+ html +
                        '<script type="text/javascript">' + js + '</script>' +
                        '<style>' + css + '</style>');
                var code = '<!DOCTYPE html>\n'+
                           '<html>\n'+
                           '<head>\n'+
                           '    <title>W2UI Demo: '+ cmd +'</title>\n'+
                           '    <script src="http://ajax.googleapis.com/ajax/libs/jquery/2.1.0/jquery.min.js"></script>\n'+
                           '    <script type="text/javascript" src="'+ w2ui_js +'"></script>\n'+
                           '    <link rel="stylesheet" type="text/css" href="'+ w2ui_css +'" />\n'+
                           '</head>\n'+
                           '<body>\n\n'+
                           html + '\n\n'+
                           (js != '' ? '<script type="text/javascript">\n' + js + '\n</script>\n\n' : '') +
                           (css != '' ? '<style>\n' + css + '</style>\n\n' : '') +
                           '</body>\n'+
                           '</html>';
                $('#example_code').html('<a href="javascript:" onclick="$(this).next().show(); initCode(); $(this).hide();" class="btn-source">Show Source Code</a>'+
                    '<div id="sourcecode" style="display: none;">'+
                    '<h2>Complete Code '+
                    '<span style="font-weight: normal; padding-left: 10px;">- &nbsp;&nbsp;Copy & paste into your editor or <a href="javascript:" class="jsfiddle">fiddle with code online</a></span> </h2>'+
                    '<textarea class="preview" id="code">'+
                        code.replace(/<textarea/gi, '&lt;textarea').replace(/<\/textarea>/gi, '&lt;/textarea&gt;') +
                    '</textarea>'+
                    (json != '' ?
                        '<h2>JSON file</h2>'+
                        '<textarea class="json" id="json">'+ json +'</textarea>'
                        :
                        '')+
                    '</div>'+
                    '<div style="display: none">'+
                    '<form id="fiddleForm" target="_blank" action="http://jsfiddle.net/api/post/jquery/2.1/" method="post">'+
                    '    <textarea name="title">W2UI Demo: '+ cmd +'</textarea>'+
                    '    <textarea name="resources">'+ w2ui_js +','+ w2ui_css +'</textarea>'+
                    '    <textarea name="html">'+ html.replace(/<textarea/gi, '&lt;textarea').replace(/<\/textarea>/gi, '&lt;/textarea&gt;') +'</textarea>'+
                    '    <textarea name="js">'+ js +'</textarea>'+
                    '    <textarea name="css">'+ css +'</textarea>'+
                    '    <textarea name="wrap">l</textarea>'+
                    '</form>'+
                    '</div>');
            });
        }
    }));

    // check hash
    setTimeout(function () {
        var tmp = String(document.location.hash).split('/');
        switch (tmp[0]) {
            default:
            case '#!dashboard':
                w2ui['demo-sidebar'].expand('dashboard');
                w2ui['demo-sidebar'].click(tmp[1] || 'dashboard-1');
                break;
            case '#!modules':
                w2ui['demo-sidebar'].expand('modules');
                w2ui['demo-sidebar'].click(tmp[1] || 'modules-1');
                break;
            case '#!products':
                w2ui['demo-sidebar'].expand('products');
                w2ui['demo-sidebar'].click(tmp[1] || 'products-1');
                break;
        }
    }, 100);
});

function initCode() {
    var text = $('#example_code .preview');
    if (text.length > 0) {
        var cm = CodeMirror(
            function(elt) { text[0].parentNode.replaceChild(elt, text[0]); },
            {
                value        : $.trim(text.val()),
                mode        : "text/html",
                readOnly    : true,
                gutter        : true,
                lineNumbers    : true
            }
        );
        cm.setSize(null, cm.doc.height + 15);
    }
    var text = $('#example_code .json');
    if (text.length > 0) {
        var cm = CodeMirror(
            function(elt) { text[0].parentNode.replaceChild(elt, text[0]); },
            {
                    value        : $.trim(text.val()),
                mode        : "javascript",
                readOnly    : true,
                gutter        : true,
                lineNumbers    : true
            }
        );
        cm.setSize(null, cm.doc.height + 15);
    }
    $('#example_code .jsfiddle').on('click', function () {
        $('#fiddleForm').submit();
    });
}
