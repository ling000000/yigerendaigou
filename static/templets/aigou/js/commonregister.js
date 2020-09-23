

$(function () {
    var systemError = "对不起，系统赶忙，请稍后再试！";
    var emailNullError = "*请输入您的电子邮箱地址.";
    var emailFormatError = "*您的电子邮箱地址错误.";
    var emailExistingError = "*邮箱已经被占用，请重新输入";
    var emailLengthError = "*电子邮箱地址不能多于50个字符，请重新输入.";
    var userNameNullError = "*请输入您的用户名.";
    var userNameFormateError = "*用户名不能以空格，下划线，破折号开始或结束.";
    var userNameExistingError = "*此用户名已被使用，请重新输入！";
    var userNameLengthError = "*用户名应少于40个字符.";
    var userNameOnlyError = "*用户名只能用字母、数字、下划线组成";
    var passwordNullError = "*请输入密码!";
    var passwordLengthError = "*密码必须大于6个字符小于30个字符，请重新输入.";
    var rePasswordNullError = "*请输入密码!";
    var rePasswordNotMatchError = "*两次输入的密码不一样.";
    var codeNullError = "*请输入验证码!";
    var codeError = "*验证码错误.";
    var checking = "检测中..";
    var countryNullError = "*请选择国家.";
    var userNameIncorrect = "*用户名错误，请重新输入.";
    var passwordIncorrect = "*密码错误，请重新输入";
    CommonRegister.Init("cn", systemError, emailNullError, emailFormatError, emailExistingError, emailLengthError, userNameNullError, userNameFormateError, userNameExistingError, userNameLengthError, userNameOnlyError, passwordNullError, passwordLengthError, rePasswordNullError, rePasswordNotMatchError, codeNullError, codeError, checking, userNameIncorrect, passwordIncorrect);
});


CommonRegister = {
    Msg: {
        SystemError: "",
        EmailNullError: "",
        EmailFormatError: "",
        EmailExistingError: "",
        EmailLengthError: "",
        UserNameNullError: "",
        UserNameFormateError: "",
        UserNameOnlyError: "",
        UserNameLengthError: "",
        UserNameExistingError: "",
        PasswordNullError: "",
        PasswordLengthError: "",
        RePasswordNullError: "",
        RePasswordNotMatchError: "",
        CodeNullError: "",
        CodeError: "",
        Checking: "",
        CountryNullError: "",
        UserNameIncorrect: "",
        PasswordIncorrect: ""
    },
    Language: 'en',
    CaptchaImageSrc: null,
    EmailIsTrue: false,
    UserNameIsTrue: false,
    PasswordIsTrue: false,
    RePasswordIsMatch: false,
    CountryHaveChosen: false,
    CodeIsTrue: false,


    Init: function (language, systemError, emailNullError, emailFormatError, emailExistingError, emailLengthError, userNameNullError, userNameFormateError, userNameExistingError, userNameLengthError, userNameOnlyError, passwordNullError, passwordLengthError, rePasswordNullError, rePasswordNotMatchError, codeNullError, codeError, checking, userNameIncorrect, passwordIncorrect) {
        this.Language = language;
        this.Msg.SystemError = systemError;
        this.Msg.EmailNullError = emailNullError;
        this.Msg.EmailFormatError = emailFormatError;
        this.Msg.EmailExistingError = emailExistingError;
        this.Msg.EmailLengthError = emailLengthError;
        this.Msg.UserNameNullError = userNameNullError;
        this.Msg.UserNameFormateError = userNameFormateError;
        this.Msg.UserNameExistingError = userNameExistingError;
        this.Msg.UserNameLengthError = userNameLengthError;
        this.Msg.UserNameOnlyError = userNameOnlyError;
        this.Msg.PasswordNullError = passwordNullError;
        this.Msg.PasswordLengthError = passwordLengthError;
        this.Msg.RePasswordNullError = rePasswordNullError;
        this.Msg.RePasswordNotMatchError = rePasswordNotMatchError;
        this.Msg.CodeError = codeError;
        this.Msg.CodeNullError = codeNullError;
        this.Msg.Checking = checking;
        //this.Msg.CountryNullError = countryNullError;
        this.Msg.UserNameIncorrect = userNameIncorrect;
        this.Msg.PasswordIncorrect = passwordIncorrect;


        this.InitEvent();
    },
    InitEvent: function () {
        var json = CommonRegister.GetOriginalShowTitle();
        var originValEmail = json.email;
        var originValUserName = json.username;
        var originValCode = json.code;

        $("#email").bind({
            'blur': function () {
                CommonRegister.CheckEmail(originValEmail);
            },
            'focus': function () {
                if ($(this).val() == originValEmail) {
                    $(this).val('');
                }

            }

        });

        $("#username").bind({
            'blur': function () {
                CommonRegister.CheckUserName(originValUserName);
            },
            'focus': function () {
                if ($(this).val() == originValUserName) {
                    $(this).val('');
                }
            }
        });
        $("#textpassword").focus(function () {
            $(this).hide();
            $("#password").show().focus();

        });
        $("#password").bind({
            'blur': function () {
                if ($(this).val() == "") {
                    $("#textpassword").show();
                    $("#password").hide();
                }
                CommonRegister.CheckPassword();


            }

        });
        $("#textrepassword").focus(function () {
            $(this).hide();
            $("#repassword").show().focus();
        });
        $("#repassword").bind({
            'blur': function () {
                if ($(this).val() == "") {
                    $(this).hide();
                    $("#textrepassword").show();
                }
                CommonRegister.CheckRePassword();
            }
        });

        $("#code").bind({
            'blur': function () {
                CommonRegister.CheckCode(originValCode);
            },
            'focus': function () {
                if ($(this).val() == originValCode) {
                    $(this).val('');
                }
            },
            'keydown': function (e) {
                if (e.keyCode == 13) {
                    CommonRegister.DoSubmit();
                }
            }
        });

        $("#captchaimage").click(function () {
            if (CommonRegister.CaptchaImageSrc == null) {
                CommonRegister.CaptchaImageSrc = $(this).attr("src");
            }

            $(this).attr("src", CommonRegister.CaptchaImageSrc + "&" + (new Date()).getTime());
        });

        $("#submit").click(function () {
            CommonRegister.DoSubmit();
        });

        $("#country").find("dt").click(function (e) {
            var obj = $("#country").find("dd");
            if (obj.is(":visible")) {
                obj.hide();
            } else {
                obj.show();

            }
            e.preventDefault();
            return false;
        });

        $("#country").find("a").bind({
            'click': function (event) {
                var countryName = $.trim($(this).html());
                var countryId = $.trim($(this).attr("data-countryId"));
                $("#country").children().eq(0).children().eq(0).html(countryName);
                $("#country").children().eq(0).children().eq(0).attr("data-countryId", countryId);
                $("#country").find("dd").hide();
                CommonRegister.CheckCountry();
                event.stopPropagation();
            }
        });

        $(document).keyup(function (event) {
            var obj = $("#country").find("dd");

            if ($(obj).is(":visible")) {
                var keycode = event.which ? event.which : event.keyCode;
                var contain = $(obj).children();
                if (keycode >= 65 && keycode <= 90) {
                    var inputText = String.fromCharCode(keycode);
                    var i = 1;
                    var x = 1;
                    if (contain.length > 0) {
                        contain.each(function () {
                            if ($(this).html().substring(0, 1) == inputText && i == 1) {
                                $(this).css("background", "none repeat scroll 0 0 #BF0000");
                                //设置被选中内容出现在结果框里
                                var cuntryId = $(this).attr("data-countryid");
                                $("#country").find('span[class="text"]').html($(this).text());
                                $("#country").find('span[class="text"]').attr("data-countryId", cuntryId);
                                i = x;
                                return;
                            } else {
                                $(this).css("background", "");
                            }
                            x++;
                        });
                    }

                    if (i > 0 && i < 245) {
                        var top = 30 * (i - 1);
                        $(obj)[0].scrollTop = top;
                    }

                }
            }
        });

        CommonRegister.DocumentClick();
    },
    DocumentClick: function () {
        $(document).click(function () {
            $("#country").find("dd").hide();
        });
    },
    GetOriginalShowTitle: function () {
        var originValEmail = "";
        var originValUserName = "";
        var originValCountry = "";
        var originValCode = "";


        switch (CommonRegister.Language) {
            case 'en':
                originValEmail = "Your email address";
                originValUserName = "User name";
                originValCountry = "";
                originValCode = "Code";
                break;
            case 'es':
                originValEmail = "Email";
                originValUserName = "Nombre de usuario";
                originValCountry = "";
                originValCode = "Código";
                break;
            case 'ru':
                originValEmail = "Email";
                originValUserName = "Логин";
                originValCountry = "";
                originValCode = "Введите символы";
                break;
            case 'cn':
                originValEmail = "邮箱";
                originValUserName = "用户名";
                originValCountry = "";
                originValCode = "验证码";
                break;
        }

        return { email: originValEmail, username: originValUserName, code: originValCode };
    }
    ,
    CheckEmail: function (originVal) {
        var val = $.trim($("#email").val());
        if (val == "" || val == originVal) {
            $("#email").val(originVal);    //恢复提示样式
            $("#email").parent().find("em").html(CommonRegister.Msg.EmailNullError).show(); //空错误提示
            CommonRegister.EmailIsTrue = false;
        } else {
            //验证邮箱格式和邮箱是否已经被注册
            var emailRegExp = "^([0-9a-zA-Z-_.])+@[0-9a-zA-Z-.]+$";
            if (!val.match(emailRegExp)) {
                $("#email").parent().find("em").html(CommonRegister.Msg.EmailFormatError).show();
                CommonRegister.EmailIsTrue = false;
            } else if (val.length > 50) {
                $("#email").parent().find("em").html(CommonRegister.Msg.EmailLengthError).show();
            } else {
                $("#email").parent().find("em").html(CommonRegister.Msg.Checking).show();
                $.ajax({
                    url: "/Tools/jsonregister.ashx?action=checkemail",
                    data: { email: val },
                    type: "POST",
                    dataType: "json",
                    success: function (data) {
                        if (data.result == "true") {
                            $("#email").parent().find("em").html("").hide();
                            CommonRegister.EmailIsTrue = true;
                        }
                        else if (data.result == "false") {
                            $("#email").parent().find("em").html(CommonRegister.Msg.EmailExistingError).show();
                            CommonRegister.EmailIsTrue = false;
                        }
                    },
                    error: function () {
                        art.dialog.alert(CommonRegister.Msg.SystemError);
                        CommonRegister.EmailIsTrue = false;
                    }
                });
            }
        }
    },

    CheckUserName: function (originVal) {
        var val = $.trim($("#username").val());
        if (val == "" || val == originVal) {
            $("#username").val(originVal);    //恢复提示样式
            $("#username").parent().find("em").html(CommonRegister.Msg.UserNameNullError).show(); //空错误提示
            CommonRegister.UserNameIsTrue = false;
        } else {
            //验证用户名格式和用户名是否已经被注册
            var zhengze = "^[a-zA-Z0-9]((.*)?[a-zA-Z0-9]$)?";
            var zhengze2 = "^[a-zA-Z0-9_]*$";
            var zhengze3 = "^.{0,40}$";
            if (!val.match(zhengze)) {
                $("#username").parent().find("em").html(CommonRegister.Msg.UserNameFormateError).show();
                CommonRegister.UserNameIsTrue = false;
            } else if (!val.match(zhengze2)) {
                $("#username").parent().find("em").html(CommonRegister.Msg.UserNameOnlyError).show();
                CommonRegister.UserNameIsTrue = false;
            } else if (!val.match(zhengze3)) {
                $("#username").parent().find("em").html(CommonRegister.Msg.UserNameLengthError).show();
                CommonRegister.UserNameIsTrue = false;
            } else {
                $("#username").parent().find("em").html(CommonRegister.Msg.Checking).show();
                $.ajax({
                    url: "/Tools/jsonregister.ashx?action=checkeusername",
                    data: { userName: val },
                    type: "POST",
                    dataType: "json",
                    success: function (data) {
                        if (data.result == "false") {
                            $("#username").parent().find("em").html(CommonRegister.Msg.UserNameExistingError).show();
                            CommonRegister.UserNameIsTrue = false;
                        }
                        else if (data.result == "true") {
                            $("#username").parent().find("em").html("").hide();
                            CommonRegister.UserNameIsTrue = true;
                        }
                    },
                    error: function () {
                        art.dialog.alert(CommonRegister.Msg.SystemError);
                        CommonRegister.UserNameIsTrue = false;
                    }
                });
            }
        }
    },

    CheckPassword: function () {
        var val = $("#password").val();
        if (val == "") {
            $("#password").hide();    //恢复提示样式
            $("#textpassword").show();
            $("#password").parent().find("em").html(CommonRegister.Msg.PasswordNullError).show(); //空错误提示
            CommonRegister.PasswordIsTrue = false;
        } else {
            //验证密码格式是否正确
            var zhengze = "^.{6,30}$";
            if (!val.match(zhengze)) {
                $("#password").parent().find("em").html(CommonRegister.Msg.PasswordLengthError).show();
                CommonRegister.PasswordIsTrue = false;
            } else {
                $("#password").parent().find("em").html("").hide();
                CommonRegister.PasswordIsTrue = true;
            }
        }
    },

    CheckRePassword: function () {
        var val = $("#repassword").val();

        if (val == "") {
            $("#repassword").hide();    //恢复提示样式
            $("#textrepassword").show();
            $("#repassword").parent().find("em").html(CommonRegister.Msg.RePasswordNullError).show(); //空错误提示
            CommonRegister.RePasswordIsMatch = false;
        } else {
            //验证密码和确认密码是否一致
            var pass = $("#password").val();

            if (pass != val) {
                $("#repassword").parent().find("em").html(CommonRegister.Msg.RePasswordNotMatchError).show();
                CommonRegister.RePasswordIsMatch = false;
            } else {
                $("#repassword").parent().find("em").html("").hide();
                CommonRegister.RePasswordIsMatch = true;
            }
        }
    },

    CheckCountry: function () {
        //        var val = $.trim($("#country").find("span[class='text']").attr("data-countryId"));
        //        if (val == 0) {
        //            $("#country").parent().find("em").html(CommonRegister.Msg.CountryNullError).show();//空错误提示
        //            CommonRegister.CountryHaveChosen = false;
        //        }else {
        //            $("#country").parent().find("em").eq(1).html("").hide();//空错误提示
        //            CommonRegister.CountryHaveChosen = true;
        //        }
        CommonRegister.CountryHaveChosen = true;
    },

    CheckCode: function (originVal) {
        var code = $("#code").val();
        var key = $("#captcha-guid").val();

        if (code == null || code == "" || code == originVal) {
            $("#code").val(originVal);
            $("#code").parent().find('em').html(CommonRegister.Msg.CodeNullError).show();
            CommonRegister.CodeIsTrue = false;
        } else if (code.length < 4) {
            $("#code").parent().find('em').html(CommonRegister.Msg.CodeError).show();
            CommonRegister.CodeIsTrue = false;
        } else {
            //根据验证码验证返回的不同参数做出不同的动作
            $("#code").parent().find("em").html(CommonRegister.Msg.Checking).show();
            $.ajax({
                url: "/Tools/CheckVerifyCode.ashx",
                data: { key: key, value: code },
                type: "POST",
                dataType: "json",
                success: function (data) {
                    if (data.result == false) {
                        $("#code").parent().find('em').html(CommonRegister.Msg.CodeError).show();
                        CommonRegister.CodeIsTrue = false;
                    } else {
                        $("#code").parent().find('em').html("").hide();
                        CommonRegister.CodeIsTrue = true;
                    }
                }
            });

        }
    },

    DoSubmit: function () {
        //变换提交按钮样式
        $("#submit").css('backgroundColor', '#ccc');
        //暂时禁用提交功能
        $("#submit").unbind();

        var json = CommonRegister.GetOriginalShowTitle();

        if (!CommonRegister.EmailIsTrue) {
            CommonRegister.CheckEmail(json.email);
        }
        if (!CommonRegister.UserNameIsTrue) {
            CommonRegister.CheckUserName(json.username);
        }
        if (!CommonRegister.PasswordIsTrue) {
            CommonRegister.CheckPassword();
        }
        if (!CommonRegister.RePasswordIsMatch) {
            CommonRegister.CheckRePassword();
        }
        if (!CommonRegister.CountryHaveChosen) {
            CommonRegister.CheckCountry();
        }
        if (!CommonRegister.CodeIsTrue) {
            CommonRegister.CheckCode(json.code);
        }
        //alert("CommonRegister.EmailIsTrue:"+CommonRegister.EmailIsTrue+"<br />"+"CommonRegister.UserNameIsTrue:"+CommonRegister.UserNameIsTrue+"<br />"+"CommonRegister.PasswordIsTrue:"+CommonRegister.PasswordIsTrue+"<br />"+"CommonRegister.RePasswordIsMatch:"+CommonRegister.RePasswordIsMatch+"<br />"+"CommonRegister.CountryHaveChosen:"+CommonRegister.CountryHaveChosen+"<br />"+"CommonRegister.CodeIsTrue:"+CommonRegister.CodeIsTrue+"<br />")
        if (CommonRegister.EmailIsTrue && CommonRegister.UserNameIsTrue && CommonRegister.PasswordIsTrue && CommonRegister.RePasswordIsMatch && CommonRegister.CountryHaveChosen && CommonRegister.CodeIsTrue) {
            var email = $.trim($("#email").val());
            var username = $.trim($("#username").val());
            var password = $("#password").val();
            var code = $("#code").val();
            var key = $("#captcha-guid").val();
            var puid = $("#puid").val();
            //var countryId = $.trim($("#country").find("span[class='text']").attr("data-countryId"));


            $.ajax({
                url: "/Tools/jsonregister.ashx?action=reg",
                data: { key: key, code: code, userName: username, password: password, email: email, share: "", registerSource: "Normal", puid: puid },
                type: "POST",
                dataType: "json",
                success: function (data) {
                    var langcode = 1;

                    switch (CommonRegister.Language) {
                        case "cn":
                            langcode = 1;
                            break;
                        case "en":
                            langcode = 2;
                            break;
                        case "es":
                            langcode = 3;
                            break;
                        case "ru":
                            langcode = 4;
                            break;
                        default:
                            langcode = 2;
                    }

                    if (CommonRegister.Language == "en") {

                    }

                    try {
                        ga('send', 'event', 'button', 'click', 'register', 4);
                    } catch (e) {

                    }
                    if (data.result == "true") {

                        art.dialog({
                            id: 'testID',
                            content: '注册完成，请激活邮箱！',
                            lock: true,
                            button: [
                                            {
                                                name: '关闭',
                                                callback: function () {
                                                    window.location = '/index.html';
                                                }
                                            }
                                        ]
                        });


                    }
                    else {
                        if (data.errorcode == 11) {
                            $("#usrname").parent().find('em').html(CommonRegister.Msg.UserNameNullError).show();
                        }
                        if (data.errorcode == 12) {
                            $("#usrname").parent().find('em').html(CommonRegister.Msg.UserNameIncorrect).show();
                        }
                        if (data.errorcode == 13) {
                            $("#usrname").parent().find('em').html(CommonRegister.Msg.UserNameExistingError).show();
                        }
                        if (data.errorcode == 21) {
                            $("#password").parent().find('em').html(CommonRegister.Msg.PasswordNullError).show();
                        }
                        if (data.errorcode == 22) {

                            $("#password").parent().find('em').html(CommonRegister.Msg.PasswordIncorrect).show();
                        }
                        if (data.errorcode == 31) {
                            $("#email").parent().find('em').html(CommonRegister.Msg.EmailNullError).show();
                        }
                        if (data.errorcode == 32) {
                            $("#email").parent().find('em').html(CommonRegister.Msg.EmailFormatError).show();
                        }
                        if (data.errorcode == 33) {
                            $("#email").parent().find('em').html(CommonRegister.Msg.EmailExistingError).show();
                        }
                        if (data.errorcode == 4) {
                            $("#country").parent().find('em').html(CommonRegister.Msg.CountryNullError).show();
                        }
                        if (data.errorcode == 5) {
                            $("#code").parent().find('em').html(CommonRegister.Msg.CodeError).show();
                        }
                        if (data.errorcode == 99) {
                            art.dialog.alert(CommonRegister.Msg.SystemError);
                        }
                        //恢复提交按钮样式
                        $("#submit").css('backgroundColor', '#c62556');
                        //解除禁用提交功能
                        $("#submit").bind("click", CommonRegister.DoSubmit);
                    }
                },
                error: function () {
                    art.dialog.alert(CommonRegister.Msg.SystemError);
                    //恢复提交按钮样式
                    $("#submit").css('backgroundColor', '#BF0000');
                    //解除禁用提交功能
                    $("#submit").bind("click", CommonRegister.DoSubmit);
                }
            });
        }
        else {
            //恢复提交按钮样式
            $("#submit").css('backgroundColor', '#BF0000');
            //解除禁用提交功能
            $("#submit").bind("click", CommonRegister.DoSubmit);
        }
    }
}
