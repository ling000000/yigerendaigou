function clearall() {

    $("#rmtotal").val('');
    $("#rmbtotal").val('');
    $("#sgtotal").val('');
}
function changemoney() {

 var rm=$("#rmtotal").val();
 var rmb=$("#rmbtotal").val();
 var sg = $("#sgtotal").val();

 if (rm == '' && rmb == '' && sg == '') {
     alert('您好！请输入一种货币!');
     return;
 }
 if (rm != '' && rmb!= '' && sg != '') {
     alert('您好，三种货币只能输入其中一种，谢谢！');
 } else if (rmb != '' && sg != '') {
     alert('您好，三种货币只能输入其中一种，谢谢！');
 } else if (rm != '' && sg != '') {
     alert('您好，三种货币只能输入其中一种，谢谢！');
 } else if (rm!= '' && rmb != '') {
     alert('您好，三种货币只能输入其中一种，谢谢！');
 } else {
 $.ajax({
     url: "Tools/getmoneyshow.ashx",
     type: "post",
     data: { "rm": rm, "rmb": rmb, "sg": sg },
     beforeSend: function () { },
     error: function () { },
     success: function (sb) {
         if (sb != '') {
             var arry = sb.split(',');
             $("#rmtotal").val(parseFloat(arry[0]).toFixed(2));
             $("#rmbtotal").val(parseFloat(arry[1]).toFixed(2));
             $("#sgtotal").val(parseFloat(arry[2]).toFixed(2));
         }
     }
 })

 }
}