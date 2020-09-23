var isIe=(document.all)?true:false;
//设置select的可见状态
function setSelectState(state) {
    var objl = document.getElementsByTagName('select');
    for (var i = 0; i < objl.length; i++) {
        objl[i].style.visibility = state;
    }
}
function mousePosition(ev) {
    if (ev.pageX || ev.pageY) {
        return { x: ev.pageX, y: ev.pageY };
    }
    return {
        x: ev.clientX + document.body.scrollLeft - document.body.clientLeft, y: ev.clientY + document.body.scrollTop - document.body.clientTop
    };
}
//弹出方法
function showMessageBox(wTitle, content, pos, wWidth) {
    closeWindow();
    var bWidth = parseInt(document.documentElement.scrollWidth);
    var bHeight = parseInt(document.documentElement.scrollHeight);
    if (isIe) {
        setSelectState('hidden');
    }
    var back = document.createElement("div");
    back.id = "back";
    var styleStr = "top:0px;left:0px;position:absolute;z-index:9999;width:" + bWidth + "px;height:" + bHeight + "px;";
    styleStr += (isIe) ? "background:url(/templets/uulink/msg/bg1.png);filter:alpha(opacity=0);" : "background:#666;opacity:0;";
    back.style.cssText = styleStr;
    document.body.appendChild(back);
    showBackground(back, 30);
    var mesW = document.createElement("div");
    mesW.id = "mesWindow";
    mesW.className = "mesWindow";
    mesW.innerHTML = "<h2><span><input type='button' onclick='closeWindow();' title='关闭窗口' class='close' value='关闭' /></span>网站最新公告<em>（来自新领域国际的最新通知）</em></h2><div class='mesWindowContent' id='mesWindowContent'>" + content + "</div><div class='mesWindowBottom'></div>";
    var v_top = (window.screen.height - mesW.clientHeight) / 2;
    v_top += document.documentElement.scrollTop;
    styleStr = "top:" + (v_top - 150) + "px;left:" + (document.body.clientWidth / 2 - mesW.clientWidth / 2) + "px;position:absolute;width:600px;margin-left:-300px;left:50%;z-index:99999;";
    mesW.style.cssText = styleStr;
    document.body.appendChild(mesW);
}

//让背景渐渐变暗
function showBackground(obj, endInt) {
    if (isIe) {
        try {
            obj.filters.alpha.opacity += 5;
            if (obj.filters.alpha.opacity < endInt) {
                setTimeout(function () { showBackground(obj, endInt) }, 0);
            }
        }
        catch (e) {
//            alert(e.Message);
        }
    } else {
        var al = parseFloat(obj.style.opacity); al += 0.05;
        obj.style.opacity = al;
        if (al < (endInt / 100))
        { setTimeout(function () { showBackground(obj, endInt) }, 5); }
    }
}
//关闭窗口
function closeWindow() {
    if (document.getElementById('back') != null) {
        document.getElementById('back').parentNode.removeChild(document.getElementById('back'));
    }
    if (document.getElementById('mesWindow') != null) {
        document.getElementById('mesWindow').parentNode.removeChild(document.getElementById('mesWindow'));
    }
    if (isIe) {
        setSelectState('');
    }
}
//测试弹出
function testMessageBox(ev) {
    var objPos = mousePosition(ev);
    messContent = "<div class='theme-tips'><p>本周日即2013年7月28号的发货通知</p><p class='notice'><font color='red'>由于仓库线路检修，周日（即2013年7月28号）停电一天，仓库无法正常打包出货，只接收包裹，不出货！请各位客户们知悉，因此给客户们带来不便敬请见谅！</font></p><p>联系QQ：<a href='http://wpa.qq.com/msgrd?V=1&amp;Uin=2715738609&amp;Site=QQ咨询&amp;Menu=yes' target='_blank'><img src=' http://wpa.qq.com/pa?p=1:2715738609:4'  border='0' alt='QQ' /> 客服QQ</a> <a href='http://wpa.qq.com/msgrd?V=1&amp;Uin=2401735100&amp;Site=QQ咨询&amp;Menu=yes' target='_blank'><img src=' http://wpa.qq.com/pa?p=1:2401735100:4'  border='0' alt='QQ' /> 销售QQ</a><p style='padding-left:0px'>鸿承达唯一官方网站：<a href='http://www.hcdexp.com/'  target='_blank'>www.hcdexp.com</a></p><div style='clear: both;'></div></div>";
    showMessageBox('', messContent, objPos, 350);
}
testMessageBox(window);
if (window.Event) 
document.captureEvents(Event.MOUSEUP);
function nocontextmenu() {
    event.cancelBubble = true
    event.returnValue = false;
    return false;
}
function norightclick(e) {
    if (window.Event) {
        if (e.which == 2 || e.which == 3)
            return false;
    }
    else
        if (event.button == 2 || event.button == 3) {
            event.cancelBubble = true
            event.returnValue = false;
            return false;
        }
}
document.oncontextmenu = nocontextmenu; // for IE5+ 
document.onmousedown = norightclick; // for all others 
