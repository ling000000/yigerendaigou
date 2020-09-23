

$(function () {

    var lurl = location.href;
    var ltype = "";
    var baseLang = "";
    if (lurl.indexOf('?') > -1) {
        lurl = lurl.substring(0, lurl.indexOf('?'));
    }
    var arry = lurl.replace("http://", "").split('/');
    if (arry.length > 1) {
        ltype = arry[1];
    } else {
        ltype = "en";
    }
    switch (ltype) {
        case "en":
            $("#langSelectedItem").html($("#" + ltype).html());
            $("#" + ltype).addClass("xyzxz");
            var languagecookie = getCookie("yoybuyLang");
            if (languagecookie == null) {
                if (navigator.userLanguage) {
                    baseLang = $.trim(navigator.userLanguage.substring(0, 2)).toLowerCase();
                } else {
                    baseLang = $.trim(navigator.language.substring(0, 2)).toLowerCase();
                }
                if (baseLang.indexOf('-') > -1) {
                    if (baseLang.split('-')[0] == "es") {
                        //zhe zhao + tan kuang
                        var es = window.confirm("Visita la versión en español？");
                        if (es) {
                            jump("es");
                        }
                    } else if (baseLang.split('-')[0] == "ru") {
                        var ru = window.confirm("Перейти на страницу на русском？");

                        if (ru) {
                            jump("ru");
                        }
                    }
                } else {
                    if (baseLang.split('-')[0] == "es") {
                        //zhe zhao + tan kuang
                        var es1 = window.confirm("Visita la versión en español？");
                        if (es1) {
                            jump("es");
                        }
                    } else if (baseLang.split('-')[0] == "ru") {
                        var ru1 = window.confirm("Перейти на страницу на русском？");
                        if (ru1) {
                            jump("ru");
                        }
                    }
                }

            } 
            SetCookie("yoybuyLang", "en");
            break;
        case "es":
            $("#langSelectedItem").html($("#" + ltype).html());
            $("#" + ltype).addClass("xyzxz");
            SetCookie("yoybuyLang", "es");
            break;
        case "ru":
            $("#langSelectedItem").html($("#" + ltype).html());
            $("#" + ltype).addClass("xyzxz");
            SetCookie("yoybuyLang", "ru");
            break;
        case "cn":
            $("#langSelectedItem").html($("#" + ltype).html());
            $("#" + ltype).addClass("xyzxz");
            SetCookie("yoybuyLang", "cn");
            break;

        default: $("#langSelectedItem").html($("#en").html());
            $("#en").addClass("xyzxz");
            SetCookie("yoybuyLang", "en");
            break;
    }
    $("#langSelectedItem").click(function (e) {
        e ? e.stopPropagation() : event.cancelBubble = true;
    });

    $("#langSelectedItem").click(function () {
        delCookie("yoybuyLang");
        if ($("#langSelectItems").css("display") == "none") {
            $("#langSelectItems").show();
        } else {
            $("#langSelectItems").hide();
        }

    });

    $(document).click(function () {
        $("#langSelectItems").hide();
    });

    $("#langSelectItems > span").bind(
            {
                click: function () {
                    var obj = $(this);
                    var id = obj.attr("id");
                    $("#langSelectedItem").html(obj.html());
                    $("#langSelectItems").hide();
                    jump(obj.attr("id"));
                },
                mouseover: function () {
                    $("#langSelectItems > span").removeClass("xyzxz");
                    $(this).addClass("xyzxz");
                },
                mouseout: function () {
                    $(this).removeClass("xyzxz");
                }
            }
        );


});

function SetCookie(name, value)//两个参数，一个是cookie的名子，一个是值
{
    var Days = 30; //此 cookie 将被保存 30 天

    var exp = new Date();    //new Date("December 31, 9998");

    exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000);

    //document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString();

    document.cookie=name + "=" + escape(value) + ((exp == null) ? "" : ";expires=" + exp.toGMTString()) + ";path=/;domain=yoybuy.com";  
}

function getCookie(name)//取cookies函数       
{
    var arr = document.cookie.match(new RegExp("(^| )" + name + "=([^;]*)(;|$)"));

    if (arr != null) return unescape(arr[2]); return null;

}
function delCookie(name) {//为了删除指定名称的cookie，可以将其过期时间设定为一个过去的时间
    var date = new Date();
    date.setTime(date.getTime() - 10000);
    document.cookie = name + "=; expires=" + date.toGMTString();
}

function jump(selection) {
    switch (selection) {
        case "en":
            changeurl("en");
            break;
        case "ru":
            changeurl("ru");
            break;
        case "es":
            changeurl("es");
            break;
        case "cn":
            changeurl("cn");
            break;
        default:
            changeurl("en");
            break;
    }
}
function changeurl(langType) {
    var lurl = location.href;
    var url = "http://";
    var para = "";
    if (lurl.indexOf('?') > -1) {
        para = lurl.substring(lurl.indexOf('?'));
        lurl = lurl.substring(0, lurl.indexOf('?'));
    }
    var arry = lurl.replace("http://", "").split('/');

    if (typeof (langtourl) == "undefined") {
        if (arry[1] == "") {
            url = lurl + langType+"/";
        } else {
            url += arry[0];
            for (var i = 1; i < arry.length; i++) {
                if (i == 1) {
                    arry[i] = langType;
                }
                url += "/" + arry[i];
            }

        }

        location.href = url+para;
    } else {
        location.href = "/" + langType + "/" + langtourl;
    }
}