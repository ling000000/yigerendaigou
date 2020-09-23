$(function () {
    head.GetUserName();
    head.GetCartNum();
    head.CartMover();
    head.ClickSerach();
});
var UserId = "";
var cartNum = 0;
function DeleteGood(goodsId, obj) {
    if (confirm("确定要删除此商品？")) {
        $.ajax({
            url: "/templets/daigou/Tools/DaiGouCar.ashx",
            cache: false,
            dataType: "json",
            data: { "key": goodsId, "action": "delgood" },
            success: function (data) {
                if (data.result == "true") {

                    art.dialog.alert("删除成功!");
                    location.reload();
                }
                else {
                    art.dialog.alert("删除失败!");
                }
            }
        });
    }
}
function SignOut() {
    $.ajax({
        url: "/Tools/jsonregister.ashx?action=signout",
        dataType: "json",
        cache: false,
        data: {},
        success: function (data) {
            if (data.result == "true") {
                window.location.href = 'index.html';
            }
            else {
                art.dialog.alert("对不起，系统繁忙，请过会儿重试！");
            }
        }
    });
}
var head = {
    GetUserName: function () { //获取用户名字
        $.ajax({
            url: "/Tools/jsonregister.ashx?action=getname",
            data: {},
            type: "POST",
            dataType: "json",
            success: function (data) {
                if (data.result == "true") {
                    $("#username").html("<a href=\"/userindexs.html\">" + data.username + "</a>，欢迎来到 99ygo！");
                    $("#regOrSignOut").html("<div ><a href='javascript:void(0)' onclick='SignOut()' >退出</a><div>");

                } else {
                    if (data.username == null || data.username == "") {

                    } else {
                        $("#username").html("Welcome，" + data.username + "&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href='/login.html'>登录</a>");
                        $("#regOrSignOut").html("<a href='register.html'>免费注册</a>");
                    }
                }
            }
        });
    },
    GetCartNum: function () {//获取购物车数量
        $.ajax({
            url: "/templets/daigou/Tools/DaiGouCar.ashx?Action=carnum",
            dataType: "json",
            cache: false,
            success: function (data) {
                if (data.result == "true") {
                    cartNum = data.data;
                    $(".ShoppingNum").html("(" + data.data + ")");
                }
            }
        });
    },
    GetCartList: function () {
        $("#ShopingCart").show();
        $.ajax({
            url: '/templets/daigou/Tools/DaiGouCar.ashx?Action=getgoods',
            dataType: "json",
            cache: false,
            success: function (data) {
                data = eval(data);
                //alert(data);
                if (data.result == "true") {
                    //UserId = data.userId;
                    var htmlvalue = "";
                    if (data.cont == "0") {
                        htmlvalue += "<li style=\"width:100%;text-align:center;line-height:80px;font-size:12px;font-weight:normal;\">购物车是空的.</li>";
                    }
                    for (var i = 0; i < data.list.length; i++) {
                         htmlvalue += "<div class=\"cart_goods_single\">";
                         htmlvalue += "<div class=\"cart_goods_single_pic\"><img src=\"" + data.list[i].picurl + "\" width=\"50\" height=\"50\"></div>";
                         htmlvalue += "<div class=\"cart_goods_single_text\">";
                         htmlvalue += "<span class=\"cart_goods_single_tittle\" title=\""+data.list[i].goodname+"\"><a href=\""+data.list[i].goodurl+"\" target=\"_black\">"+data.list[i].goodname+"</a></span>";
                         htmlvalue += "<span class=\"cart_goods_single_detail\" title=\""+data.list[i].goodSKU+"\">"+data.list[i].goodSKU+"</span>";
                         htmlvalue += "</div>";
                         htmlvalue += "<div class=\"cart_goods_single_price\">";
                         htmlvalue += "<span class=\"cart_goods_single_unitp\">￥<b style=\"color:#f47a20;\">"+data.list[i].goodprice+"</b></span>";
                         htmlvalue += "<span class=\"cart_goods_single_quantity\">"+data.list[i].goodcount+"</span>";
                         htmlvalue += "</div>";


                    }

                    $("#ShopingCart").html(htmlvalue);
                }
                else {
                    //$("#ShopingCart").html("<div style='text-align:center; width:100%;line-height:30px;margin-top:5px'>The shopping cart is empty.</div><b><a href='http://shoppingcart.yoybuy.com/en/shoppingcart.html' style=\"color:#1F8AEA\">View Shopping Cart &gt;&gt;</a></b>");
                }
            }

        });
    },
    CartMover: function () {
        $(".carthover").mouseleave(function () {
            $("#ShopingCart").hide();
            $("#ShopingCart").html("<li style=\"width:100%;text-align:center;line-height:80px;font-size:12px;font-weight:normal;\">购物车是空的.</li>");
        }).mouseover(function () {
            //alert($("#ShopingCart li").length);
            if ($("#ShopingCart li").length == 1) {
                //  alert(222222);
                head.GetCartList();
                head.GetCartNum();
            }
            $("#ShopingCart").show();
        });
    },
    ClickSerach: function () {
        var searchValue = $("#Search").val();
        $("#Search").focus(function () {
            if (searchValue == "搜索...") {
                $(this).val("");
            }
        }).blur(function () {
            if ($(this).val() == "") {
                $(this).val("搜索...");
            }
        });
    }
};
